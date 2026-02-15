"""
Comprehensive Error Tracking and Reporting System
Helps identify and fix issues quickly
"""

import json
import traceback
from datetime import datetime
from pathlib import Path
from collections import defaultdict
from loguru import logger

class ErrorTracker:
    """Track and analyze errors for easy debugging"""
    
    def __init__(self, settings):
        self.settings = settings
        self.error_log_file = settings.data_dir / 'error_log.json'
        self.errors = defaultdict(list)
        self.error_counts = defaultdict(int)
        self.load_errors()
    
    def load_errors(self):
        """Load existing error log"""
        try:
            if self.error_log_file.exists():
                with open(self.error_log_file, 'r') as f:
                    data = json.load(f)
                    self.errors = defaultdict(list, data.get('errors', {}))
                    self.error_counts = defaultdict(int, data.get('counts', {}))
        except Exception as e:
            logger.warning(f"Could not load error log: {e}")
    
    def track_error(self, category: str, error: Exception, context: dict = None):
        """
        Track an error with context
        
        Args:
            category: Error category (e.g., 'proxy', 'browser', 'captcha', 'survey')
            error: The exception object
            context: Additional context information
        """
        error_data = {
            'timestamp': datetime.now().isoformat(),
            'category': category,
            'error_type': type(error).__name__,
            'error_message': str(error),
            'traceback': traceback.format_exc(),
            'context': context or {}
        }
        
        # Add to errors list
        self.errors[category].append(error_data)
        self.error_counts[category] += 1
        
        # Keep only last 100 errors per category
        if len(self.errors[category]) > 100:
            self.errors[category] = self.errors[category][-100:]
        
        # Save to file
        self.save_errors()
        
        # Log error
        logger.error(f"[{category}] {type(error).__name__}: {error}")
        if context:
            logger.error(f"Context: {json.dumps(context, indent=2)}")
    
    def save_errors(self):
        """Save error log to file"""
        try:
            data = {
                'errors': dict(self.errors),
                'counts': dict(self.error_counts),
                'last_updated': datetime.now().isoformat()
            }
            
            with open(self.error_log_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            logger.warning(f"Could not save error log: {e}")
    
    def get_error_summary(self) -> dict:
        """Get summary of all errors"""
        summary = {
            'total_errors': sum(self.error_counts.values()),
            'by_category': dict(self.error_counts),
            'recent_errors': []
        }
        
        # Get 10 most recent errors across all categories
        all_errors = []
        for category, errors in self.errors.items():
            for error in errors:
                error['category'] = category
                all_errors.append(error)
        
        # Sort by timestamp
        all_errors.sort(key=lambda x: x['timestamp'], reverse=True)
        summary['recent_errors'] = all_errors[:10]
        
        return summary
    
    def print_error_report(self):
        """Print comprehensive error report"""
        summary = self.get_error_summary()
        
        logger.info("=" * 60)
        logger.info("ERROR REPORT")
        logger.info("=" * 60)
        logger.info(f"Total Errors: {summary['total_errors']}")
        logger.info("")
        logger.info("Errors by Category:")
        for category, count in summary['by_category'].items():
            logger.info(f"  {category}: {count}")
        logger.info("")
        logger.info("Recent Errors (last 10):")
        for i, error in enumerate(summary['recent_errors'], 1):
            logger.info(f"  {i}. [{error['category']}] {error['error_type']}: {error['error_message']}")
            logger.info(f"     Time: {error['timestamp']}")
        logger.info("=" * 60)
    
    def get_common_errors(self, limit: int = 5) -> list:
        """Get most common error types"""
        error_types = defaultdict(int)
        
        for category, errors in self.errors.items():
            for error in errors:
                key = f"{error['error_type']}: {error['error_message'][:50]}"
                error_types[key] += 1
        
        # Sort by frequency
        sorted_errors = sorted(error_types.items(), key=lambda x: x[1], reverse=True)
        return sorted_errors[:limit]
    
    def get_troubleshooting_tips(self) -> list:
        """Get troubleshooting tips based on error patterns"""
        tips = []
        
        # Check for proxy errors
        if self.error_counts.get('proxy', 0) > 5:
            tips.append({
                'issue': 'Frequent proxy errors',
                'tip': 'Check your proxy configuration in .env file',
                'command': 'curl -x http://USER:PASS@HOST:PORT https://api.ipify.org'
            })
        
        # Check for browser errors
        if self.error_counts.get('browser', 0) > 5:
            tips.append({
                'issue': 'Frequent browser errors',
                'tip': 'Chrome/Chromium may not be installed or outdated',
                'command': 'sudo apt-get install chromium-browser'
            })
        
        # Check for CAPTCHA errors
        if self.error_counts.get('captcha', 0) > 10:
            tips.append({
                'issue': 'Frequent CAPTCHA errors',
                'tip': 'Check CAPTCHA method configuration or API key',
                'command': 'Check CAPTCHA_METHOD in .env file'
            })
        
        # Check for survey errors
        if self.error_counts.get('survey', 0) > 10:
            tips.append({
                'issue': 'Frequent survey errors',
                'tip': 'Opinion Edge website may have changed or is down',
                'command': 'Check https://opinion-edge.com manually'
            })
        
        # Check for AI errors
        if self.error_counts.get('ai', 0) > 5:
            tips.append({
                'issue': 'Frequent AI errors',
                'tip': 'Ollama may not be running or model not downloaded',
                'command': 'sudo systemctl start ollama && ollama pull llama3.2-vision:latest'
            })
        
        return tips
    
    def clear_old_errors(self, days: int = 7):
        """Clear errors older than specified days"""
        from datetime import timedelta
        
        cutoff_date = datetime.now() - timedelta(days=days)
        
        for category in list(self.errors.keys()):
            self.errors[category] = [
                error for error in self.errors[category]
                if datetime.fromisoformat(error['timestamp']) > cutoff_date
            ]
            
            # Update counts
            self.error_counts[category] = len(self.errors[category])
        
        self.save_errors()
        logger.info(f"Cleared errors older than {days} days")


class HealthChecker:
    """Check system health and identify issues"""
    
    def __init__(self, settings):
        self.settings = settings
    
    def check_all(self) -> dict:
        """Run all health checks"""
        results = {
            'timestamp': datetime.now().isoformat(),
            'overall_status': 'healthy',
            'checks': {}
        }
        
        # Check environment
        results['checks']['environment'] = self._check_environment()
        
        # Check proxy
        results['checks']['proxy'] = self._check_proxy()
        
        # Check Ollama
        results['checks']['ollama'] = self._check_ollama()
        
        # Check disk space
        results['checks']['disk_space'] = self._check_disk_space()
        
        # Check memory
        results['checks']['memory'] = self._check_memory()
        
        # Determine overall status
        if any(check['status'] == 'error' for check in results['checks'].values()):
            results['overall_status'] = 'error'
        elif any(check['status'] == 'warning' for check in results['checks'].values()):
            results['overall_status'] = 'warning'
        
        return results
    
    def _check_environment(self) -> dict:
        """Check environment configuration"""
        try:
            from pathlib import Path
            
            issues = []
            
            # Check .env file
            if not Path('.env').exists():
                issues.append('.env file not found')
            
            # Check required directories
            required_dirs = ['logs', 'screenshots', 'data']
            for dir_name in required_dirs:
                if not Path(dir_name).exists():
                    issues.append(f'{dir_name} directory not found')
            
            if issues:
                return {
                    'status': 'warning',
                    'message': 'Environment issues found',
                    'issues': issues
                }
            
            return {
                'status': 'ok',
                'message': 'Environment configured correctly'
            }
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Environment check failed: {e}'
            }
    
    def _check_proxy(self) -> dict:
        """Check proxy connectivity"""
        try:
            import requests
            
            proxy_url = self.settings.proxy_url
            proxies = {
                'http': proxy_url,
                'https': proxy_url
            }
            
            response = requests.get(
                'https://api.ipify.org?format=json',
                proxies=proxies,
                timeout=10
            )
            
            if response.status_code == 200:
                ip = response.json().get('ip')
                return {
                    'status': 'ok',
                    'message': f'Proxy working (IP: {ip})'
                }
            else:
                return {
                    'status': 'error',
                    'message': f'Proxy returned status {response.status_code}'
                }
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Proxy check failed: {e}'
            }
    
    def _check_ollama(self) -> dict:
        """Check Ollama service"""
        try:
            import requests
            
            response = requests.get(
                'http://localhost:11434/api/tags',
                timeout=5
            )
            
            if response.status_code == 200:
                return {
                    'status': 'ok',
                    'message': 'Ollama is running'
                }
            else:
                return {
                    'status': 'error',
                    'message': 'Ollama not responding correctly'
                }
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Ollama check failed: {e}',
                'fix': 'sudo systemctl start ollama'
            }
    
    def _check_disk_space(self) -> dict:
        """Check available disk space"""
        try:
            import shutil
            
            total, used, free = shutil.disk_usage('/')
            free_gb = free // (2**30)
            
            if free_gb < 1:
                return {
                    'status': 'error',
                    'message': f'Low disk space: {free_gb}GB free'
                }
            elif free_gb < 5:
                return {
                    'status': 'warning',
                    'message': f'Disk space getting low: {free_gb}GB free'
                }
            else:
                return {
                    'status': 'ok',
                    'message': f'Disk space OK: {free_gb}GB free'
                }
        except Exception as e:
            return {
                'status': 'warning',
                'message': f'Could not check disk space: {e}'
            }
    
    def _check_memory(self) -> dict:
        """Check available memory"""
        try:
            import psutil
            
            memory = psutil.virtual_memory()
            available_gb = memory.available / (2**30)
            
            if available_gb < 0.5:
                return {
                    'status': 'error',
                    'message': f'Low memory: {available_gb:.1f}GB available'
                }
            elif available_gb < 1:
                return {
                    'status': 'warning',
                    'message': f'Memory getting low: {available_gb:.1f}GB available'
                }
            else:
                return {
                    'status': 'ok',
                    'message': f'Memory OK: {available_gb:.1f}GB available'
                }
        except Exception as e:
            return {
                'status': 'warning',
                'message': f'Could not check memory: {e}'
            }
    
    def print_health_report(self):
        """Print health check report"""
        results = self.check_all()
        
        logger.info("=" * 60)
        logger.info("SYSTEM HEALTH CHECK")
        logger.info("=" * 60)
        logger.info(f"Overall Status: {results['overall_status'].upper()}")
        logger.info("")
        
        for check_name, check_result in results['checks'].items():
            status_icon = {
                'ok': '✅',
                'warning': '⚠️',
                'error': '❌'
            }.get(check_result['status'], '❓')
            
            logger.info(f"{status_icon} {check_name}: {check_result['message']}")
            
            if 'fix' in check_result:
                logger.info(f"   Fix: {check_result['fix']}")
        
        logger.info("=" * 60)
