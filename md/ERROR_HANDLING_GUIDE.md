# Error Handling System Guide

## Overview

The survey automation system now includes comprehensive error handling with automatic tracking, categorization, and reporting.

---

## Error Categories

All errors are automatically categorized into 5 main categories:

### 1. **proxy** - Proxy Connection Issues
- Proxy connection failed
- Proxy timeout
- DNS leak detected
- Kill-switch triggered

### 2. **browser** - Browser/Chrome Issues
- Chrome not found
- ChromeDriver issues
- Browser initialization failed
- Page load timeout
- Element not found

### 3. **captcha** - CAPTCHA Solving Issues
- CAPTCHA detection failed
- Audio download failed
- Transcription failed
- Solution injection failed
- 2Captcha API errors

### 4. **survey** - Survey Processing Issues
- Navigation failed
- Question extraction failed
- Answer submission failed
- Invalid survey URL
- Survey timeout

### 5. **ai** - Ollama AI Issues
- Ollama connection failed
- API timeout
- Image encoding failed
- Response parsing failed
- Empty response

---

## Error Tracker Usage

### Initialization

```python
from src.utils.error_tracker import ErrorTracker
from src.config.settings import Settings

settings = Settings()
error_tracker = ErrorTracker(settings)
```

### Logging Errors

```python
# Log an error
error_tracker.log_error(
    category='browser',           # Category: proxy, browser, captcha, survey, ai
    error_type='chrome_not_found', # Specific error type
    message='Chrome binary not found',  # Error message
    details={'path': '/usr/bin/chrome'}  # Optional details
)
```

### Generating Reports

```python
# Generate error report
report = error_tracker.generate_report()

print(f"Total errors: {report['total_errors']}")
print(f"Errors by category: {report['errors_by_category']}")
print(f"Most common errors: {report['most_common_errors']}")
```

### Saving Reports

```python
# Save report to file
error_tracker.save_report()
# Saves to: data/errors.json
```

---

## Health Checker Usage

### Initialization

```python
from src.utils.error_tracker import HealthChecker
from src.config.settings import Settings

settings = Settings()
health_checker = HealthChecker(settings)
```

### Running Health Check

```python
# Run full health check
health_status = health_checker.run_health_check()

print(f"Status: {health_status['status']}")  # healthy, degraded, or unhealthy
print(f"Checks: {health_status['checks']}")
```

### Individual Checks

```python
# Check Python version
python_ok = health_checker.check_python_version()

# Check directories
dirs_ok = health_checker.check_directories()

# Check packages
packages_ok = health_checker.check_packages()

# Check Ollama
ollama_ok = health_checker.check_ollama()

# Check proxy
proxy_ok = health_checker.check_proxy()

# Check Chrome
chrome_ok = health_checker.check_chrome()

# Check disk space
disk_ok = health_checker.check_disk_space()
```

---

## Module Integration

### Browser Automation

```python
from src.automation.browser import BrowserAutomation

# Initialize with error tracker
automation = BrowserAutomation(settings, error_tracker)

# Errors are automatically logged
automation.run()
```

### Survey Handler

```python
from src.automation.survey_handler import SurveyHandler

# Initialize with error tracker
survey_handler = SurveyHandler(
    driver, 
    ai_client, 
    settings, 
    human_behavior, 
    error_tracker
)

# Errors are automatically logged
survey_handler.process_survey(url)
```

### CAPTCHA Solver

```python
from src.captcha.solver import CaptchaSolver

# Initialize with error tracker
captcha_solver = CaptchaSolver(settings, error_tracker)

# Errors are automatically logged
result = captcha_solver.solve_recaptcha_v2(site_key, page_url)
```

### AI Client

```python
from src.ai.ollama_client import OllamaClient

# Initialize with error tracker
ai_client = OllamaClient(settings, error_tracker)

# Errors are automatically logged
result = ai_client.analyze_screenshot(image_path, prompt)
```

---

## Error Message Format

All error messages follow this format:

```
❌ [Error Description]
💡 Fix: [Solution]
   [Detailed steps or commands]
```

### Examples

```
❌ Chrome/Chromium not found
💡 Fix: Install Chrome
   Ubuntu: sudo apt-get install chromium-browser
   Or: wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && sudo dpkg -i google-chrome-stable_current_amd64.deb
```

```
❌ Cannot connect to Ollama at http://localhost:11434
💡 Fix: Start Ollama
   sudo systemctl start ollama
   ollama pull llava
```

```
❌ Port 5000 is already in use!
💡 Fix: Stop the other process or change FLASK_PORT in .env
   Find process: sudo lsof -i :5000
   Kill process: sudo kill -9 <PID>
   Or change port: FLASK_PORT=5001
```

---

## Dashboard Integration

### Error Report Endpoint

```bash
# Get error report via API
curl http://localhost:5000/api/errors

# Response format:
{
  "total_errors": 42,
  "errors_by_category": {
    "browser": 15,
    "captcha": 10,
    "survey": 8,
    "ai": 6,
    "proxy": 3
  },
  "most_common_errors": [
    {
      "category": "browser",
      "type": "element_not_found",
      "count": 8,
      "last_occurrence": "2026-02-10T15:30:45"
    }
  ],
  "recent_errors": [...]
}
```

### Health Status Endpoint

```bash
# Get health status via API
curl http://localhost:5000/api/health

# Response format:
{
  "status": "healthy",
  "timestamp": "2026-02-10T15:30:45",
  "checks": {
    "python_version": {
      "healthy": true,
      "message": "Python 3.10.0"
    },
    "directories": {
      "healthy": true,
      "message": "All directories exist"
    },
    "ollama": {
      "healthy": true,
      "message": "Ollama is running"
    }
  }
}
```

---

## Error Recovery Strategies

### Automatic Recovery

The system implements automatic recovery for transient errors:

1. **Retry Logic**: Failed operations are retried up to 3 times
2. **Exponential Backoff**: Wait time increases between retries
3. **Graceful Degradation**: System continues with reduced functionality
4. **Consecutive Error Detection**: Stops after 5 consecutive errors

### Manual Recovery

For persistent errors:

1. **Check Error Report**: `cat data/errors.json | python -m json.tool`
2. **Identify Pattern**: Look for most common error types
3. **Fix Root Cause**: Follow error message fix suggestions
4. **Run Health Check**: Verify fix with health checker
5. **Restart System**: `python main.py`

---

## Monitoring Commands

### View Error Report

```bash
# Pretty print error report
cat data/errors.json | python -m json.tool

# Get error summary
python -c "from src.utils.error_tracker import ErrorTracker; from src.config.settings import Settings; et = ErrorTracker(Settings()); import json; print(json.dumps(et.generate_report(), indent=2))"
```

### View Health Status

```bash
# Get health status
python -c "from src.utils.error_tracker import HealthChecker; from src.config.settings import Settings; hc = HealthChecker(Settings()); import json; print(json.dumps(hc.run_health_check(), indent=2))"
```

### Filter Errors by Category

```bash
# Browser errors
grep '"category": "browser"' data/errors.json

# CAPTCHA errors
grep '"category": "captcha"' data/errors.json

# AI errors
grep '"category": "ai"' data/errors.json
```

### Count Errors

```bash
# Total errors
grep '"category"' data/errors.json | wc -l

# Errors by category
grep '"category": "browser"' data/errors.json | wc -l
grep '"category": "captcha"' data/errors.json | wc -l
grep '"category": "survey"' data/errors.json | wc -l
grep '"category": "ai"' data/errors.json | wc -l
grep '"category": "proxy"' data/errors.json | wc -l
```

---

## Best Practices

### 1. Always Pass Error Tracker

```python
# ✅ Good
automation = BrowserAutomation(settings, error_tracker)

# ❌ Bad
automation = BrowserAutomation(settings)  # Errors won't be tracked
```

### 2. Log Errors with Context

```python
# ✅ Good
error_tracker.log_error(
    'browser',
    'element_not_found',
    f'Login button not found on {url}',
    {'url': url, 'selector': '.login-button'}
)

# ❌ Bad
error_tracker.log_error('browser', 'error', 'Something failed')
```

### 3. Check Error Reports Regularly

```bash
# Daily check
cat data/errors.json | python -m json.tool

# Weekly analysis
python -c "from src.utils.error_tracker import ErrorTracker; from src.config.settings import Settings; et = ErrorTracker(Settings()); print(et.generate_report())"
```

### 4. Run Health Checks Before Deployment

```python
from src.utils.error_tracker import HealthChecker
from src.config.settings import Settings

health_checker = HealthChecker(Settings())
status = health_checker.run_health_check()

if status['status'] != 'healthy':
    print("⚠️ System not healthy, fix issues before deployment")
    for check, result in status['checks'].items():
        if not result['healthy']:
            print(f"  - {check}: {result['message']}")
```

### 5. Monitor Error Trends

```python
# Track error rate over time
import json
from datetime import datetime, timedelta

with open('data/errors.json', 'r') as f:
    errors = json.load(f)

# Errors in last hour
one_hour_ago = datetime.now() - timedelta(hours=1)
recent_errors = [
    e for e in errors.get('errors', [])
    if datetime.fromisoformat(e['timestamp']) > one_hour_ago
]

print(f"Errors in last hour: {len(recent_errors)}")
```

---

## Troubleshooting

### Error Tracker Not Working

**Problem:** Errors not being logged

**Solution:**
1. Check error_tracker is passed to modules
2. Verify `data/` directory exists
3. Check file permissions: `ls -la data/`
4. Check disk space: `df -h`

### Health Check Failing

**Problem:** Health check returns 'unhealthy'

**Solution:**
1. Run individual checks to identify issue
2. Check error messages for specific failures
3. Follow fix suggestions in error messages
4. Verify all dependencies installed

### Dashboard Not Showing Errors

**Problem:** `/api/errors` endpoint returns empty

**Solution:**
1. Check `data/errors.json` exists
2. Verify errors are being logged
3. Check dashboard logs for errors
4. Restart dashboard: `python main.py`

---

## Summary

The error handling system provides:

✅ **Automatic error tracking** - All errors logged automatically
✅ **Error categorization** - Errors grouped by type for easy debugging
✅ **Helpful error messages** - Every error includes fix suggestions
✅ **Health monitoring** - System health checks before startup
✅ **Dashboard integration** - Real-time error reports via API
✅ **Error recovery** - Automatic retry and graceful degradation
✅ **Production ready** - Comprehensive error handling for live deployment

---

**Version:** 2.0
**Status:** Production Ready
**Last Updated:** 2026-02-10
