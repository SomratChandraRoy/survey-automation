"""Backup manager for data and logs"""

import time
import shutil
import tarfile
from pathlib import Path
from datetime import datetime, timedelta
from loguru import logger

class BackupManager:
    """Manage automatic backups"""
    
    def __init__(self, settings):
        self.settings = settings
        self.running = True
    
    def start(self):
        """Start backup loop"""
        if not self.settings.backup_enabled:
            logger.info("Backup disabled")
            return
        
        logger.info("Backup manager started")
        
        while self.running:
            try:
                # Create backup
                self.create_backup()
                
                # Clean old backups
                self.cleanup_old_backups()
                
                # Wait for next backup cycle
                wait_seconds = self.settings.backup_interval_hours * 3600
                time.sleep(wait_seconds)
                
            except Exception as e:
                logger.error(f"Backup error: {e}")
                time.sleep(300)  # Wait 5 minutes on error
    
    def create_backup(self):
        """Create backup archive"""
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_name = f"backup_{timestamp}.tar.gz"
            backup_path = self.settings.backups_dir / backup_name
            
            logger.info(f"Creating backup: {backup_name}")
            
            with tarfile.open(backup_path, 'w:gz') as tar:
                # Backup survey data
                if self.settings.surveys_dir.exists():
                    tar.add(self.settings.surveys_dir, arcname='surveys')
                
                # Backup logs (current only)
                log_file = self.settings.logs_dir / 'automation.log'
                if log_file.exists():
                    tar.add(log_file, arcname='logs/automation.log')
                
                # Backup stats
                stats_file = self.settings.data_dir / 'stats.json'
                if stats_file.exists():
                    tar.add(stats_file, arcname='stats.json')
                
                # Backup cookies
                cookie_file = self.settings.cookies_dir / 'session.json'
                if cookie_file.exists():
                    tar.add(cookie_file, arcname='cookies/session.json')
            
            logger.info(f"Backup created: {backup_path}")
            
            # Upload to cloud if configured
            if self.settings.backup_type in ['s3', 'gdrive']:
                self.upload_to_cloud(backup_path)
                
        except Exception as e:
            logger.error(f"Backup creation error: {e}")
    
    def upload_to_cloud(self, backup_path: Path):
        """Upload backup to cloud storage"""
        try:
            if self.settings.backup_type == 's3':
                self.upload_to_s3(backup_path)
            elif self.settings.backup_type == 'gdrive':
                self.upload_to_gdrive(backup_path)
        except Exception as e:
            logger.error(f"Cloud upload error: {e}")
    
    def upload_to_s3(self, backup_path: Path):
        """Upload to AWS S3"""
        try:
            import boto3
            
            s3 = boto3.client('s3')
            bucket = self.settings.aws_bucket_name
            
            s3.upload_file(
                str(backup_path),
                bucket,
                f"backups/{backup_path.name}"
            )
            
            logger.info(f"Backup uploaded to S3: {bucket}")
            
        except Exception as e:
            logger.error(f"S3 upload error: {e}")
    
    def upload_to_gdrive(self, backup_path: Path):
        """Upload to Google Drive"""
        logger.warning("Google Drive upload not implemented yet")
        # TODO: Implement Google Drive upload
    
    def cleanup_old_backups(self):
        """Remove backups older than retention period"""
        try:
            retention_date = datetime.now() - timedelta(days=self.settings.backup_retention_days)
            
            count = 0
            for backup_file in self.settings.backups_dir.glob('backup_*.tar.gz'):
                try:
                    file_time = datetime.fromtimestamp(backup_file.stat().st_mtime)
                    
                    if file_time < retention_date:
                        backup_file.unlink()
                        count += 1
                        
                except Exception as e:
                    logger.warning(f"Could not delete {backup_file}: {e}")
            
            if count > 0:
                logger.info(f"Cleaned up {count} old backups")
                
        except Exception as e:
            logger.error(f"Backup cleanup error: {e}")
    
    def stop(self):
        """Stop backup manager"""
        self.running = False
