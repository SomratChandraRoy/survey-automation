# Complete Command Reference

## Initial Setup Commands

### 1. Clone Repository
```bash
git clone https://github.com/yourusername/opinion-edge-automation.git
cd opinion-edge-automation
```

### 2. Configure Environment
```bash
cp .env.example .env
nano .env
```

### 3. Deploy (One Command)
```bash
chmod +x deploy.sh && ./deploy.sh
```

## Service Management

### Start Automation
```bash
sudo systemctl start survey-automation
```

### Stop Automation
```bash
sudo systemctl stop survey-automation
```

### Restart Automation
```bash
sudo systemctl restart survey-automation
```

### Check Status
```bash
sudo systemctl status survey-automation
```

### Enable Auto-Start on Boot
```bash
sudo systemctl enable survey-automation
```

### Disable Auto-Start
```bash
sudo systemctl disable survey-automation
```

## Log Management

### View Real-Time Logs
```bash
tail -f logs/automation.log
```

### View Last 100 Lines
```bash
tail -n 100 logs/automation.log
```

### View System Logs
```bash
sudo journalctl -u survey-automation -f
```

### View Last 50 System Log Entries
```bash
sudo journalctl -u survey-automation -n 50
```

### Search Logs for Errors
```bash
grep -i error logs/automation.log
```

### Search Logs for CAPTCHA
```bash
grep -i captcha logs/automation.log
```

## Monitoring

### Access Dashboard
```bash
# Open in browser
http://your-server-ip:5000
```

### Check System Resources
```bash
# CPU usage
top

# Memory usage
free -h

# Disk usage
df -h

# Process info
ps aux | grep python
```

### Monitor Network
```bash
# Active connections
netstat -tulpn | grep python

# Bandwidth usage
iftop
```

## Maintenance

### Update Code from Git
```bash
cd opinion-edge-automation
git pull origin main
sudo systemctl restart survey-automation
```

### Update Python Dependencies
```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
deactivate
sudo systemctl restart survey-automation
```

### Clean Screenshots Manually
```bash
rm -f screenshots/*.png
```

### Clean Old Logs
```bash
find logs/ -name "*.log.*" -mtime +7 -delete
```

### View Backup Files
```bash
ls -lh data/backups/
```

### Create Manual Backup
```bash
tar -czf manual_backup_$(date +%Y%m%d).tar.gz data/ logs/ .env
```

## Troubleshooting Commands

### Check Ollama Status
```bash
sudo systemctl status ollama
```

### Test Ollama
```bash
curl http://localhost:11434/api/tags
```

### Test Ollama Vision Model
```bash
ollama run llama3.2-vision:latest "Hello"
```

### Check Proxy Connection
```bash
# Use your credentials from .env file
curl -x http://YOUR_PROXY_USERNAME:YOUR_PROXY_PASSWORD@YOUR_PROXY_HOST:YOUR_PROXY_PORT https://api.ipify.org
```

### Test 2Captcha API
```bash
curl "https://2captcha.com/res.php?key=YOUR_API_KEY&action=getbalance"
```

### Check Chrome/Chromium
```bash
chromium-browser --version
which chromium-browser
```

### Check Python Environment
```bash
source venv/bin/activate
python --version
pip list
deactivate
```

### View Environment Variables
```bash
cat .env
```

### Check Port Availability
```bash
sudo netstat -tulpn | grep 5000
```

### Kill Stuck Process
```bash
pkill -f main.py
```

### Force Kill
```bash
pkill -9 -f main.py
```

## Performance Optimization

### Increase Swap Space
```bash
sudo fallocate -l 4G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
```

### Clear System Cache
```bash
sudo sync
sudo sh -c 'echo 3 > /proc/sys/vm/drop_caches'
```

### Monitor Disk I/O
```bash
iostat -x 1
```

## Database/Data Management

### View Survey Results
```bash
ls -lh data/surveys/
cat data/surveys/survey_*.json | jq .
```

### View Statistics
```bash
cat data/stats.json | jq .
```

### Export Survey Data
```bash
cat data/surveys/*.json | jq -s . > all_surveys.json
```

### Count Completed Surveys
```bash
grep -c '"success": true' data/surveys/*.json
```

## Security

### Check File Permissions
```bash
ls -la .env
chmod 600 .env
```

### View Active Sessions
```bash
who
w
```

### Check Failed Login Attempts
```bash
sudo grep "Failed password" /var/log/auth.log
```

### Update System Security
```bash
sudo apt-get update
sudo apt-get upgrade
sudo apt-get dist-upgrade
```

## Advanced Operations

### Run in Debug Mode
```bash
source venv/bin/activate
python main.py
```

### Run Single Survey Test
```bash
source venv/bin/activate
python -c "from src.automation.browser import BrowserAutomation; from src.config.settings import Settings; bot = BrowserAutomation(Settings()); bot.run()"
```

### Test AI Client
```bash
source venv/bin/activate
python -c "from src.ai.ollama_client import OllamaClient; from src.config.settings import Settings; client = OllamaClient(Settings()); print(client.host)"
```

### Test Proxy Manager
```bash
source venv/bin/activate
python -c "from src.proxy.manager import ProxyManager; from src.config.settings import Settings; pm = ProxyManager(Settings()); print(pm.validate_proxy())"
```

## Uninstallation

### Stop and Remove Service
```bash
sudo systemctl stop survey-automation
sudo systemctl disable survey-automation
sudo rm /etc/systemd/system/survey-automation.service
sudo systemctl daemon-reload
```

### Remove Files
```bash
cd ..
rm -rf opinion-edge-automation
```

### Remove Ollama (Optional)
```bash
sudo systemctl stop ollama
sudo systemctl disable ollama
sudo rm /usr/local/bin/ollama
sudo rm -rf /usr/share/ollama
```

## Quick Reference

### Two-Step Deployment
```bash
# Step 1: Clone and configure
git clone https://github.com/yourusername/opinion-edge-automation.git
cd opinion-edge-automation
cp .env.example .env
nano .env

# Step 2: Deploy
chmod +x deploy.sh && ./deploy.sh
```

### Daily Operations
```bash
# Check status
sudo systemctl status survey-automation

# View logs
tail -f logs/automation.log

# Access dashboard
# Open: http://your-server-ip:5000
```

### Emergency Stop
```bash
sudo systemctl stop survey-automation
pkill -9 -f main.py
```

### Quick Restart
```bash
sudo systemctl restart survey-automation && tail -f logs/automation.log
```
