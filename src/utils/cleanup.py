"""Cleanup manager for screenshots and logs"""

import time
import shutil
from pathlib import Path
from datetime import datetime, timedelta
from loguru import logger

class CleanupManager:
    """Manage automatic cleanup of temporary files"""
    
    def __init__(self, settings):
        self.settings = settings
        self.running = True
    
    def start(self):
        """Start cleanup loop"""
        logger.info("Cleanup manager started")
        
        while self.running:
            try:
                # Clean screenshots every 20 minutes
                self.cleanup_screenshots()
                
                # Clean old logs
                self.cleanup_old_logs()
                
                # Wait for next cleanup cycle
                time.sleep(self.settings.screenshot_cleanup_interval)
                
            except Exception as e:
                logger.error(f"Cleanup error: {e}")
                time.sleep(60)
    
    def cleanup_screenshots(self):
        """Delete all screenshots"""
        try:
            screenshot_dir = self.settings.screenshots_dir
            
            if not screenshot_dir.exists():
                return
            
            count = 0
            for file in screenshot_dir.glob('*.png'):
                try:
                    file.unlink()
                    count += 1
                except Exception as e:
                    logger.warning(f"Could not delete {file}: {e}")
            
            if count > 0:
                logger.info(f"Cleaned up {count} screenshots")
                
        except Exception as e:
            logger.error(f"Screenshot cleanup error: {e}")
    
    def cleanup_old_logs(self):
        """Remove old log files beyond retention"""
        try:
            logs_dir = self.settings.logs_dir
            
            if not logs_dir.exists():
                return
            
            # Keep only the specified number of rotated logs
            log_files = sorted(logs_dir.glob('automation.log.*'), 
                             key=lambda x: x.stat().st_mtime,
                             reverse=True)
            
            # Remove files beyond retention count
            for log_file in log_files[self.settings.log_retention_count:]:
                try:
                    log_file.unlink()
                    logger.info(f"Removed old log: {log_file.name}")
                except Exception as e:
                    logger.warning(f"Could not delete {log_file}: {e}")
                    
        except Exception as e:
            logger.error(f"Log cleanup error: {e}")
    
    def stop(self):
        """Stop cleanup manager"""
        self.running = False
