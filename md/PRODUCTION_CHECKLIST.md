# Production Deployment Checklist

## ✅ Pre-Deployment Checks

### Environment Setup
- [ ] Python 3.8+ installed
- [ ] All dependencies installed (`pip install -r requirements.txt`)
- [ ] `.env` file created from `.env.example`
- [ ] All environment variables configured
- [ ] Ollama installed and running
- [ ] Chrome/Chromium browser installed

### Configuration Validation
- [ ] Proxy credentials configured (if using proxy)
- [ ] Persona details filled in `.env`
- [ ] CAPTCHA method selected (`audio_free` recommended for free)
- [ ] Flask port available (default: 5000)
- [ ] Log rotation configured
- [ ] Backup settings configured (if enabled)

### Directory Structure
- [ ] `logs/` directory exists
- [ ] `screenshots/` directory exists
- [ ] `data/` directory exists
- [ ] `data/cookies/` directory exists
- [ ] `data/backups/` directory exists
- [ ] `data/surveys/` directory exists

### Security Checks
- [ ] No hardcoded credentials in code
- [ ] `.env` file in `.gitignore`
- [ ] Proxy credentials not exposed
- [ ] API keys secured
- [ ] File permissions set correctly

## 🚀 Deployment Steps

### 1. Clone Repository
```bash
git clone <your-repo-url>
cd <repo-directory>
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Environment
```bash
cp .env.example .env
nano .env  # Edit with your settings
```

### 4. Install Ollama (if not installed)
```bash
curl -fsSL https://ollama.com/install.sh | sh
sudo systemctl start ollama
ollama pull llava  # or your preferred vision model
```

### 5. Run Health Check
```bash
python main.py
# Check for any validation errors
# Press Ctrl+C after validation passes
```

### 6. Start Production
```bash
# Option 1: Direct run
python main.py

# Option 2: Background with nohup
nohup python main.py > automation.log 2>&1 &

# Option 3: Using screen
screen -S survey-automation
python main.py
# Press Ctrl+A then D to detach
```

## 📊 Post-Deployment Monitoring

### Check Dashboard
- [ ] Access dashboard at `http://localhost:5000`
- [ ] Verify stats are updating
- [ ] Check system resource usage
- [ ] Review error reports

### Monitor Logs
```bash
# Real-time log monitoring
tail -f logs/automation.log

# Check for errors
grep "ERROR" logs/automation.log

# Check error tracker
cat data/errors.json
```

### Verify Functionality
- [ ] Browser launches successfully
- [ ] Proxy connection works (if configured)
- [ ] Login successful
- [ ] CAPTCHA solving works
- [ ] Surveys are being processed
- [ ] Screenshots are being captured
- [ ] Cleanup is running (check every 20 minutes)
- [ ] Backups are created (if enabled)

## 🔧 Troubleshooting

### Common Issues

#### 1. Chrome/ChromeDriver Issues
**Error:** "Chrome binary not found"
**Fix:**
```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install chromium-browser

# Or install Chrome
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo dpkg -i google-chrome-stable_current_amd64.deb
```

#### 2. Ollama Connection Failed
**Error:** "Cannot connect to Ollama"
**Fix:**
```bash
# Check if Ollama is running
sudo systemctl status ollama

# Start Ollama
sudo systemctl start ollama

# Pull vision model
ollama pull llava
```

#### 3. Port Already in Use
**Error:** "Address already in use"
**Fix:**
```bash
# Find process using port 5000
sudo lsof -i :5000

# Kill the process
sudo kill -9 <PID>

# Or change port in .env
FLASK_PORT=5001
```

#### 4. Proxy Connection Failed
**Error:** "Proxy connection failed"
**Fix:**
- Verify proxy credentials in `.env`
- Test proxy manually: `curl --proxy http://user:pass@host:port https://api.ipify.org`
- Check proxy service status
- Try without proxy first (comment out proxy settings)

#### 5. CAPTCHA Solving Failed
**Error:** "Audio CAPTCHA solve failed"
**Fix:**
- Ensure `speech_recognition` is installed
- Install audio dependencies:
  ```bash
  sudo apt-get install portaudio19-dev python3-pyaudio
  pip install pyaudio
  ```
- Try different CAPTCHA method in `.env`:
  ```
  CAPTCHA_METHOD=avoid_only  # Rely on stealth only
  ```

#### 6. Memory Issues
**Error:** "Out of memory"
**Fix:**
- Reduce screenshot retention time
- Enable cleanup more frequently
- Increase system swap space
- Monitor with: `free -h`

## 📈 Performance Optimization

### Resource Management
- [ ] Monitor CPU usage (should be < 50%)
- [ ] Monitor memory usage (should be < 2GB)
- [ ] Monitor disk space (screenshots can grow)
- [ ] Set up log rotation
- [ ] Enable automatic cleanup

### Success Rate Optimization
- [ ] Adjust human behavior timings
- [ ] Fine-tune CAPTCHA solving method
- [ ] Optimize proxy settings
- [ ] Review error logs for patterns
- [ ] Adjust retry logic if needed

## 🛡️ Security Best Practices

### Credentials
- [ ] Never commit `.env` file
- [ ] Use strong passwords
- [ ] Rotate credentials regularly
- [ ] Use separate accounts for testing

### Network Security
- [ ] Use VPN or proxy
- [ ] Enable DNS leak prevention
- [ ] Disable WebRTC
- [ ] Monitor for IP leaks

### Data Protection
- [ ] Encrypt sensitive data
- [ ] Secure backup storage
- [ ] Set proper file permissions
- [ ] Regular security audits

## 📝 Maintenance Tasks

### Daily
- [ ] Check automation logs
- [ ] Review error reports
- [ ] Monitor success rate
- [ ] Verify backups (if enabled)

### Weekly
- [ ] Clean old screenshots manually
- [ ] Review and optimize settings
- [ ] Update dependencies if needed
- [ ] Check for Ollama updates

### Monthly
- [ ] Full system audit
- [ ] Performance review
- [ ] Security review
- [ ] Update documentation

## 🎯 Success Metrics

### Target Metrics
- **Success Rate:** > 90%
- **Detection Rate:** < 1%
- **CAPTCHA Solve Rate:** > 70% (audio method)
- **Uptime:** > 95%
- **Error Rate:** < 5%

### Monitoring
```bash
# Check success rate
grep "completed successfully" logs/automation.log | wc -l

# Check error rate
grep "ERROR" logs/automation.log | wc -l

# View error report
python -c "import json; print(json.dumps(json.load(open('data/errors.json')), indent=2))"
```

## 🆘 Emergency Procedures

### System Crash
1. Check logs: `tail -100 logs/automation.log`
2. Check error tracker: `cat data/errors.json`
3. Restart with health check: `python main.py`
4. If persistent, check system resources: `top`, `free -h`, `df -h`

### High Error Rate
1. Stop automation: `Ctrl+C` or `kill <PID>`
2. Review error categories in dashboard
3. Fix most common errors first
4. Test with single cycle
5. Resume production

### Detection/Ban
1. Stop immediately
2. Change proxy/IP
3. Clear cookies: `rm -rf data/cookies/*`
4. Wait 24-48 hours
5. Review and improve stealth settings
6. Resume with more conservative timings

## 📞 Support

### Error Reporting
When reporting issues, include:
- Error message from logs
- Error tracker report (`data/errors.json`)
- System info (OS, Python version)
- Configuration (without credentials)
- Steps to reproduce

### Useful Commands
```bash
# View error summary
python -c "from src.utils.error_tracker import ErrorTracker; from src.config.settings import Settings; et = ErrorTracker(Settings()); print(et.generate_report())"

# Check health status
python -c "from src.utils.error_tracker import HealthChecker; from src.config.settings import Settings; hc = HealthChecker(Settings()); print(hc.run_health_check())"

# View stats
cat data/stats.json | python -m json.tool
```

## ✅ Production Ready Checklist

Before going live, ensure:
- [x] All error handling implemented
- [x] Error tracker integrated
- [x] Health checks working
- [x] Dashboard accessible
- [x] Logs rotating properly
- [x] Cleanup running
- [x] Backups configured (optional)
- [x] Human-like behavior enabled
- [x] CAPTCHA solving working
- [x] Proxy configured (optional)
- [x] Stealth measures active
- [ ] All tests passed
- [ ] Documentation reviewed
- [ ] Team trained
- [ ] Monitoring set up
- [ ] Emergency procedures documented

---

**Status:** ✅ Production Ready
**Version:** 2.0
**Last Updated:** 2026-02-10
