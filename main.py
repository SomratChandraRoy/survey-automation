#!/usr/bin/env python3
"""
Opinion Edge Survey Automation - Main Entry Point
Production-ready with comprehensive error handling
"""

import os
import sys
import time
import signal
import threading
import traceback
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from loguru import logger

# Global flag for graceful shutdown
shutdown_flag = threading.Event()

def signal_handler(signum, frame):
    """Handle shutdown signals"""
    logger.info("Shutdown signal received. Cleaning up...")
    shutdown_flag.set()

def validate_environment():
    """Validate environment before starting"""
    logger.info("Validating environment...")
    
    errors = []
    warnings = []
    
    # Check Python version
    if sys.version_info < (3, 8):
        errors.append(f"Python 3.8+ required, found {sys.version_info.major}.{sys.version_info.minor}")
    
    # Check required directories
    required_dirs = ['logs', 'screenshots', 'data', 'data/cookies', 'data/backups', 'data/surveys']
    for dir_path in required_dirs:
        path = Path(dir_path)
        if not path.exists():
            logger.warning(f"Creating missing directory: {dir_path}")
            path.mkdir(parents=True, exist_ok=True)
    
    # Check .env file
    if not Path('.env').exists():
        errors.append(".env file not found! Copy .env.example to .env and configure it.")
    
    # Check required packages
    try:
        import selenium
        import undetected_chromedriver
        import flask
        import speech_recognition
    except ImportError as e:
        errors.append(f"Missing required package: {e.name}. Run: pip install -r requirements.txt")
    
    # Check Ollama
    try:
        import requests
        response = requests.get('http://localhost:11434/api/tags', timeout=5)
        if response.status_code != 200:
            warnings.append("Ollama API not responding. Make sure Ollama is running: sudo systemctl start ollama")
    except Exception as e:
        warnings.append(f"Cannot connect to Ollama: {e}. Install: curl -fsSL https://ollama.com/install.sh | sh")
    
    # Print results
    if warnings:
        logger.warning("=" * 60)
        logger.warning("WARNINGS:")
        for warning in warnings:
            logger.warning(f"  ⚠️  {warning}")
        logger.warning("=" * 60)
    
    if errors:
        logger.error("=" * 60)
        logger.error("VALIDATION FAILED:")
        for error in errors:
            logger.error(f"  ❌ {error}")
        logger.error("=" * 60)
        return False
    
    logger.info("✅ Environment validation passed")
    return True

def main():
    """Main entry point with comprehensive error handling"""
    
    # Setup logger first
    from src.monitoring.logger import setup_logger
    global logger
    logger = setup_logger()
    
    logger.info("=" * 60)
    logger.info("Opinion Edge Survey Automation Starting")
    logger.info("Production-Ready Version 2.0")
    logger.info("=" * 60)
    
    try:
        # Validate environment
        if not validate_environment():
            logger.error("Environment validation failed. Please fix errors and try again.")
            sys.exit(1)
        
        # Load settings
        logger.info("Loading configuration...")
        try:
            from src.config.settings import Settings
            settings = Settings()
            logger.info("✅ Configuration loaded successfully")
        except Exception as e:
            logger.error(f"❌ Failed to load configuration: {e}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            logger.error("Check your .env file and ensure all required variables are set.")
            sys.exit(1)
        
        # Initialize error tracker
        logger.info("Initializing error tracker...")
        try:
            from src.utils.error_tracker import ErrorTracker, HealthChecker
            error_tracker = ErrorTracker(settings)
            health_checker = HealthChecker(settings)
            logger.info("✅ Error tracker initialized")
        except Exception as e:
            logger.error(f"❌ Failed to initialize error tracker: {e}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            logger.warning("Continuing without error tracker...")
            error_tracker = None
            health_checker = None
        
        # Run health check
        if health_checker:
            logger.info("Running health check...")
            try:
                health_status = health_checker.check_all()
                if health_status['overall_status'] == 'healthy':
                    logger.info("✅ Health check passed")
                elif health_status['overall_status'] == 'warning':
                    logger.warning("⚠️ Health check: System has warnings")
                    for check, result in health_status['checks'].items():
                        if result['status'] != 'ok':
                            logger.warning(f"  - {check}: {result.get('message', 'Failed')}")
                else:
                    logger.error("❌ Health check failed")
                    for check, result in health_status['checks'].items():
                        if result['status'] == 'error':
                            logger.error(f"  - {check}: {result.get('message', 'Failed')}")
            except Exception as e:
                logger.error(f"❌ Health check failed: {e}")
                logger.error(f"Traceback: {traceback.format_exc()}")
        
        # Register signal handlers
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
        
        # Start monitoring dashboard in background
        logger.info("Starting monitoring dashboard...")
        try:
            from src.monitoring.dashboard import MonitoringDashboard
            dashboard = MonitoringDashboard(settings)
            dashboard_thread = threading.Thread(target=dashboard.run, daemon=True)
            dashboard_thread.start()
            logger.info(f"✅ Monitoring dashboard started on port {settings.flask_port}")
            logger.info(f"   Access at: http://localhost:{settings.flask_port}")
        except Exception as e:
            logger.error(f"❌ Failed to start dashboard: {e}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            logger.warning("Continuing without dashboard...")
        
        # Start cleanup manager
        logger.info("Starting cleanup manager...")
        try:
            from src.utils.cleanup import CleanupManager
            cleanup_manager = CleanupManager(settings)
            cleanup_thread = threading.Thread(target=cleanup_manager.start, daemon=True)
            cleanup_thread.start()
            logger.info("✅ Cleanup manager started")
        except Exception as e:
            logger.error(f"❌ Failed to start cleanup manager: {e}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            logger.warning("Continuing without cleanup manager...")
        
        # Start backup manager if enabled
        if settings.backup_enabled:
            logger.info("Starting backup manager...")
            try:
                from src.utils.backup import BackupManager
                backup_manager = BackupManager(settings)
                backup_thread = threading.Thread(target=backup_manager.start, daemon=True)
                backup_thread.start()
                logger.info("✅ Backup manager started")
            except Exception as e:
                logger.error(f"❌ Failed to start backup manager: {e}")
                logger.error(f"Traceback: {traceback.format_exc()}")
                logger.warning("Continuing without backup manager...")
        
        # Initialize browser automation
        automation = None
        
        try:
            logger.info("Initializing browser automation...")
            from src.automation.browser import BrowserAutomation
            automation = BrowserAutomation(settings, error_tracker)
            logger.info("✅ Browser automation initialized")
            
            # Main automation loop
            cycle_count = 0
            error_count = 0
            max_consecutive_errors = 5
            
            while not shutdown_flag.is_set():
                cycle_count += 1
                logger.info("=" * 60)
                logger.info(f"Starting automation cycle #{cycle_count}")
                logger.info("=" * 60)
                
                try:
                    success = automation.run()
                    
                    if success:
                        error_count = 0  # Reset error counter on success
                        logger.info(f"✅ Cycle #{cycle_count} completed successfully")
                    else:
                        error_count += 1
                        logger.warning(f"⚠️ Cycle #{cycle_count} completed with issues (error count: {error_count})")
                    
                    # Check if too many consecutive errors
                    if error_count >= max_consecutive_errors:
                        logger.error(f"❌ Too many consecutive errors ({error_count}). Stopping automation.")
                        logger.error("Please check logs and fix issues before restarting.")
                        break
                    
                    # Wait before next cycle
                    if not shutdown_flag.is_set():
                        wait_time = 60 if success else 120  # Wait longer after errors
                        logger.info(f"Waiting {wait_time} seconds before next cycle...")
                        shutdown_flag.wait(wait_time)
                        
                except KeyboardInterrupt:
                    logger.info("Keyboard interrupt received")
                    break
                    
                except Exception as e:
                    error_count += 1
                    logger.error(f"❌ Error in automation cycle #{cycle_count}: {e}")
                    logger.error(f"Traceback: {traceback.format_exc()}")
                    
                    if error_count >= max_consecutive_errors:
                        logger.error(f"❌ Too many consecutive errors ({error_count}). Stopping automation.")
                        break
                    
                    if not shutdown_flag.is_set():
                        logger.info("Waiting 120 seconds before retry...")
                        shutdown_flag.wait(120)
        
        except Exception as e:
            logger.error(f"❌ Fatal error in browser automation: {e}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            sys.exit(1)
        
        finally:
            # Cleanup
            logger.info("=" * 60)
            logger.info("Shutting down...")
            logger.info("=" * 60)
            
            # Generate error report if error tracker exists
            if error_tracker:
                try:
                    logger.info("Generating error report...")
                    summary = error_tracker.get_error_summary()
                    logger.info(f"📊 Error Report:")
                    logger.info(f"   Total errors: {summary['total_errors']}")
                    logger.info(f"   Errors by category:")
                    for category, count in summary['by_category'].items():
                        logger.info(f"     - {category}: {count}")
                    
                    if summary['total_errors'] > 0:
                        logger.info(f"   Most common errors:")
                        common_errors = error_tracker.get_common_errors(5)
                        for error_type, count in common_errors:
                            logger.info(f"     - {error_type}: {count} times")
                except Exception as e:
                    logger.error(f"Failed to generate error report: {e}")
            
            if automation:
                try:
                    automation.cleanup()
                    logger.info("✅ Browser automation cleaned up")
                except Exception as e:
                    logger.error(f"Error during cleanup: {e}")
            
            logger.info("Shutdown complete")
            logger.info("=" * 60)
    
    except Exception as e:
        logger.error(f"❌ Unexpected fatal error: {e}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        sys.exit(1)

if __name__ == "__main__":
    main()
