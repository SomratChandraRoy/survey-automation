# Complete Deployment Guide

## Prerequisites

- Ubuntu 20.04+ Server
- Root or sudo access
- Internet connection
- 2GB+ RAM
- 10GB+ free disk space

## Quick Deployment (2 Steps)

### Step 1: Clone and Configure

```bash
# Clone repository
git clone https://github.com/yourusername/opinion-edge-automation.git
cd opinion-edge-automation

# Copy environment template
cp .env.example .env

# Edit configuration
nano .env
```

**Required Configuration:**
- `OPINION_EDGE_EMAIL`: Your Opinion Edge email
- `OPINION_EDGE_PASSWORD`: Your Opinion Edge password
- `CAPTCHA_API_KEY`: Your 2Captcha API key (get from https://2captcha.com)

### Step 2: Deploy

```bash
chmod +x deploy.sh
./deploy.sh
```

The script will automatically:
1. Install system dependencies
2. Install Ollama and pull AI model
3. Create Python virtual environment
4. Install Python packages
5. Create systemd service
6. Start automation

## Manual Installation

If you prefer manual installation:

### 1. Install System Dependencies

```bash
sudo apt-get update
sudo apt-get install -y python3 python3-pip python3-venv wget curl unzip \
    chromium-browser chromium-chromedriver xvfb supervisor
```

### 2. Install Ollama

```bash
curl -fsSL https://ollama.com/install.sh | sh
sudo systemctl enable ollama
sudo systemctl start ollama
ollama pull llama3.2-vision:latest
```

### 3. Setup Python Environment

```bash
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure Environment

```bash
cp .env.example .env
nano .env  # Edit with your credentials
```

### 5. Create Systemd Service

```bash
sudo nano /etc/systemd/system/survey-automation.service
```

Paste:
```ini
[Unit]
Description=Opinion Edge Survey Automation
After=network.target ollama.service

[Service]
Type=simple
User=YOUR_USERNAME
WorkingDirectory=/path/to/opinion-edge-automation
Environment="PATH=/path/to/opinion-edge-automation/venv/bin:/usr/local/bin:/usr/bin:/bin"
ExecStart=/path/to/opinion-edge-automation/venv/bin/python3 /path/to/opinion-edge-automation/main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Replace `YOUR_USERNAME` and paths accordingly.

### 6. Start Service

```bash
sudo systemctl daemon-reload
sudo systemctl enable survey-automation
sudo systemctl start survey-automation
```

## Verification

### Check Service Status

```bash
sudo systemctl status survey-automation
```

### View Logs

```bash
# Real-time logs
tail -f logs/automation.log

# System logs
sudo journalctl -u survey-automation -f
```

### Access Dashboard

Open browser: `http://your-server-ip:5000`

## Management Commands

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

### View Status
```bash
sudo systemctl status survey-automation
```

### View Logs
```bash
# Application logs
tail -f logs/automation.log

# System logs
sudo journalctl -u survey-automation -n 100
```

## Troubleshooting

### Service Won't Start

1. Check logs:
```bash
sudo journalctl -u survey-automation -n 50
```

2. Verify Ollama is running:
```bash
sudo systemctl status ollama
```

3. Test Ollama:
```bash
curl http://localhost:11434/api/tags
```

### Proxy Issues

1. Test proxy manually:
```bash
curl -x http://username:password@geo.floppydata.com:10080 https://api.ipify.org
```

2. Check proxy credentials in `.env`

### CAPTCHA Solving Fails

1. Verify 2Captcha API key:
```bash
curl -X POST "https://2captcha.com/in.php" \
  -d "key=YOUR_API_KEY" \
  -d "method=userrecaptcha" \
  -d "googlekey=test" \
  -d "pageurl=https://example.com"
```

2. Check balance: https://2captcha.com/enterpage

### Browser Issues

1. Install Chrome dependencies:
```bash
sudo apt-get install -y libnss3 libgconf-2-4 libxss1 libasound2
```

2. Test Chrome:
```bash
chromium-browser --version
```

### Memory Issues

1. Check available memory:
```bash
free -h
```

2. Increase swap if needed:
```bash
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

## Performance Optimization

### Reduce Memory Usage

Edit `.env`:
```
ACTION_DELAY_MIN=5
ACTION_DELAY_MAX=10
```

### Increase Survey Processing

Edit `src/automation/browser.py`:
```python
max_surveys = 20  # Increase from 10
```

### Adjust Cleanup Frequency

Edit `.env`:
```
SCREENSHOT_CLEANUP_INTERVAL=600  # 10 minutes instead of 20
```

## Security Best Practices

1. **Never commit `.env` file**
2. **Use strong passwords**
3. **Regularly update dependencies**:
```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

4. **Monitor logs for suspicious activity**
5. **Keep system updated**:
```bash
sudo apt-get update && sudo apt-get upgrade
```

## Backup and Recovery

### Manual Backup

```bash
tar -czf backup_$(date +%Y%m%d).tar.gz data/ logs/ .env
```

### Restore from Backup

```bash
tar -xzf backup_YYYYMMDD.tar.gz
```

### Automated Backups

Backups run automatically every hour (configurable in `.env`).

Location: `data/backups/`

## Monitoring

### Dashboard Access

URL: `http://your-server-ip:5000`

Features:
- Real-time statistics
- System resource monitoring
- Live log streaming
- Survey completion tracking

### Email Alerts (Optional)

To add email alerts, install:
```bash
pip install sendgrid
```

Add to `.env`:
```
SENDGRID_API_KEY=your_key
ALERT_EMAIL=your@email.com
```

## Scaling

### Multiple Instances

Run multiple instances with different ports:

```bash
# Instance 1
FLASK_PORT=5000 python3 main.py &

# Instance 2
FLASK_PORT=5001 python3 main.py &
```

### Load Balancing

Use nginx for load balancing:

```bash
sudo apt-get install nginx
sudo nano /etc/nginx/sites-available/survey-automation
```

## Support

For issues:
1. Check logs: `tail -f logs/automation.log`
2. Review this guide
3. Create GitHub issue with logs

## License

MIT License - See LICENSE file
