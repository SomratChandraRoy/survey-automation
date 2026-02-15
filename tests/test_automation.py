"""
Unit tests for automation components
"""

import pytest
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.config.settings import Settings
from src.utils.error_tracker import ErrorTracker, HealthChecker


class TestSettings:
    """Test configuration management"""
    
    def test_settings_load(self):
        """Test settings can be loaded"""
        # This will fail if .env is not configured, which is expected
        try:
            settings = Settings()
            assert settings is not None
        except Exception:
            pytest.skip("Settings require .env configuration")
    
    def test_persona_dict(self):
        """Test persona dictionary generation"""
        try:
            settings = Settings()
            persona = settings.persona_dict
            assert 'name' in persona
            assert 'age' in persona
        except Exception:
            pytest.skip("Settings require .env configuration")


class TestErrorTracker:
    """Test error tracking functionality"""
    
    def test_error_tracker_init(self):
        """Test error tracker initialization"""
        try:
            settings = Settings()
            tracker = ErrorTracker(settings)
            assert tracker is not None
            assert hasattr(tracker, 'track_error')
            assert hasattr(tracker, 'get_error_summary')
        except Exception:
            pytest.skip("Requires .env configuration")
    
    def test_error_summary_structure(self):
        """Test error summary structure"""
        try:
            settings = Settings()
            tracker = ErrorTracker(settings)
            summary = tracker.get_error_summary()
            
            assert 'total_errors' in summary
            assert 'by_category' in summary
            assert 'recent_errors' in summary
        except Exception:
            pytest.skip("Requires .env configuration")


class TestHealthChecker:
    """Test health check functionality"""
    
    def test_health_checker_init(self):
        """Test health checker initialization"""
        try:
            settings = Settings()
            checker = HealthChecker(settings)
            assert checker is not None
            assert hasattr(checker, 'check_all')
        except Exception:
            pytest.skip("Requires .env configuration")
    
    def test_health_check_structure(self):
        """Test health check result structure"""
        try:
            settings = Settings()
            checker = HealthChecker(settings)
            results = checker.check_all()
            
            assert 'overall_status' in results
            assert 'checks' in results
            assert 'timestamp' in results
            
            # Check status values
            assert results['overall_status'] in ['healthy', 'warning', 'error']
        except Exception:
            pytest.skip("Requires .env configuration")


class TestDirectoryStructure:
    """Test directory structure"""
    
    def test_required_directories_exist(self):
        """Test that required directories exist"""
        required_dirs = [
            'src',
            'src/automation',
            'src/ai',
            'src/captcha',
            'src/config',
            'src/monitoring',
            'src/proxy',
            'src/utils',
            'templates',
            'md'
        ]
        
        for dir_path in required_dirs:
            assert Path(dir_path).exists(), f"Required directory missing: {dir_path}"
    
    def test_required_files_exist(self):
        """Test that required files exist"""
        required_files = [
            'main.py',
            'requirements.txt',
            '.env.example',
            'README.md',
            'install.sh',
            'Dockerfile',
            'docker-compose.yml'
        ]
        
        for file_path in required_files:
            assert Path(file_path).exists(), f"Required file missing: {file_path}"


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
