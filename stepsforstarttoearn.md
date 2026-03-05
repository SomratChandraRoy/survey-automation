# 💰 Steps to Start Earning — Complete DigitalOcean Ubuntu Setup Guide

**Full step-by-step guide to deploy the Opinion Edge Survey Automation on a DigitalOcean Ubuntu droplet and start earning passive income.**

---

## 📋 Table of Contents

1. [What You Need Before Starting](#1-what-you-need-before-starting)
2. [Create Your DigitalOcean Droplet](#2-create-your-digitalocean-droplet)
3. [Connect to Your Server via SSH](#3-connect-to-your-server-via-ssh)
4. [Initial Server Setup](#4-initial-server-setup)
5. [Install System Dependencies](#5-install-system-dependencies)
6. [Install Ollama AI Engine](#6-install-ollama-ai-engine)
7. [Clone the Project](#7-clone-the-project)
8. [Set Up Python Environment](#8-set-up-python-environment)
9. [Configure Your Settings](#9-configure-your-settings)
10. [Set Up Firewall and Security](#10-set-up-firewall-and-security)
11. [Install and Start the Automation Service](#11-install-and-start-the-automation-service)
12. [Access Your Dashboard](#12-access-your-dashboard)
13. [Verify Everything is Working](#13-verify-everything-is-working)
14. [Daily Monitoring (2 minutes/day)](#14-daily-monitoring-2-minutesday)
15. [Troubleshooting Common Issues](#15-troubleshooting-common-issues)
16. [Essential Commands Reference](#16-essential-commands-reference)
17. [Maximise Earnings](#17-maximise-earnings)
18. [Maintenance and Updates](#18-maintenance-and-updates)

---

## 1. What You Need Before Starting

### Accounts Required

| Account | Where to Sign Up | Cost | Notes |
|---------|-----------------|------|-------|
| **Opinion Edge** | https://panel.opinion-edge.com | Free | Your survey account — complete your profile 100% |
| **DigitalOcean** | https://digitalocean.com | $6–24/month | Use referral link for $200 free credit |

### Optional (for better results)

| Service | Website | Cost | Purpose |
|---------|---------|------|---------|
| Residential Proxy | https://brightdata.com or https://oxylabs.io | $10–30/mo | Hides automation, reduces bans |
| 2Captcha | https://2captcha.com | ~$3/1000 CAPTCHAs | Paid CAPTCHA solving backup |

### Minimum Server Specs

| Resource | Minimum | Recommended |
|----------|---------|-------------|
| **CPU** | 2 vCPU | 4 vCPU |
| **RAM** | 8 GB | 16 GB |
| **Disk** | 50 GB SSD | 100 GB NVMe SSD |
| **OS** | Ubuntu 22.04 LTS | Ubuntu 22.04 LTS |

> **💡 Tip**: Start with a 4 vCPU / 8 GB RAM droplet (~$24/month on DigitalOcean). It easily handles Ollama + Chrome.

---

## 2. Create Your DigitalOcean Droplet

### Step-by-Step Droplet Creation

1. **Log into DigitalOcean**: https://cloud.digitalocean.com

2. **Click "Create" → "Droplets"**

3. **Choose Region**: Pick the region closest to you (or US/EU for better survey availability)

4. **Choose Image**: 
   ```
   Ubuntu 22.04 (LTS) x64
   ```

5. **Choose Plan**: 
   - Click **"Basic"** tab
   - Select **"Regular"** CPU
   - Pick **8 GB RAM / 4 vCPU / 160 GB disk** (~$48/mo)  
   - Or minimum **4 GB RAM / 2 vCPU** (~$24/mo) to start

6. **Authentication**: Choose **SSH Key** (recommended) or **Password**

   To create an SSH key on your local machine:
   ```bash
   ssh-keygen -t ed25519 -C "your_email@example.com"
   cat ~/.ssh/id_ed25519.pub
   ```
   Paste the output into DigitalOcean's SSH key field.

7. **Hostname**: Give it a name like `survey-automation`

8. **Click "Create Droplet"** — wait ~60 seconds

9. **Copy your Droplet IP address** (shown on the dashboard)

---

## 3. Connect to Your Server via SSH

### From Linux / macOS / Windows (WSL)

```bash
# Replace YOUR_SERVER_IP with your actual droplet IP
ssh root@YOUR_SERVER_IP

# If using a non-root user:
ssh your-username@YOUR_SERVER_IP
```

### From Windows (PuTTY)

1. Open PuTTY
2. Enter your server IP in "Host Name"
3. Port: 22
4. Click Open → accept fingerprint → log in

### First Login

```bash
# You'll see the Ubuntu welcome message
# Verify you're connected:
whoami   # should show: root (or your username)
hostname # should show your droplet name
```

---

## 4. Initial Server Setup

### Create a Non-Root User (Recommended for Security)

```bash
# Create a new user (replace 'survey' with your preferred username)
adduser survey

# Give sudo privileges
usermod -aG sudo survey

# Copy SSH keys to new user (if using SSH key auth)
rsync --archive --chown=survey:survey ~/.ssh /home/survey

# Switch to new user
su - survey

# Verify sudo works
sudo echo "sudo works!"
```

### Update the System

```bash
# Update package lists
sudo apt-get update

# Upgrade all packages
sudo apt-get upgrade -y

# Install important utilities
sudo apt-get install -y curl wget git htop nano unzip bc
```

### Set Timezone (Important for scheduling)

```bash
# Set to your timezone (examples below)
sudo timedatectl set-timezone Europe/Berlin    # Germany
sudo timedatectl set-timezone Europe/London    # UK
sudo timedatectl set-timezone America/New_York # US East
sudo timedatectl set-timezone Asia/Kolkata     # India

# Verify
timedatectl
```

---

## 5. Install System Dependencies

### Install All Required Packages

```bash
# Update first
sudo apt-get update

# Install core dependencies
sudo apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    python3-dev \
    build-essential \
    wget \
    curl \
    git \
    unzip \
    htop \
    tmux \
    supervisor \
    nginx

# Install Chrome/Chromium browser
sudo apt-get install -y \
    chromium-browser \
    chromium-chromedriver

# Verify Chrome installation
chromium-browser --version
# Expected output: Chromium 12x.x.x.x

# Install audio/media libraries (for CAPTCHA solving)
sudo apt-get install -y \
    ffmpeg \
    libsndfile1 \
    portaudio19-dev

# Install virtual display (for headless Chrome)
sudo apt-get install -y xvfb

echo "✅ System dependencies installed"
```

### Verify Chrome Works

```bash
# Test headless Chrome
chromium-browser --headless --no-sandbox --dump-dom https://example.com 2>/dev/null | head -5
# Should output some HTML — if it does, Chrome works!
```

---

## 6. Install Ollama AI Engine

The AI engine (Ollama) reads survey questions and generates intelligent answers.

### Install Ollama

```bash
# One-command install
curl -fsSL https://ollama.com/install.sh | sh

# Verify installation
ollama --version
```

### Start Ollama Service

```bash
# Enable and start Ollama
sudo systemctl enable ollama
sudo systemctl start ollama

# Wait a moment for it to start
sleep 5

# Verify it's running
sudo systemctl status ollama | grep Active
# Expected: Active: active (running)
```

### Download the AI Vision Model

> ⚠️ **This will download ~8 GB** — takes 10–30 minutes depending on your connection speed.

```bash
# Pull the vision model (required for reading surveys)
ollama pull llama3.2-vision:latest

# You'll see a progress bar — wait for it to complete
# Expected output:
# pulling manifest
# pulling ...  100% ████████████████████ 8.4 GB
# success

# Verify model is available
ollama list
# Should show: llama3.2-vision:latest
```

### Test Ollama Works

```bash
# Quick test
ollama run llama3.2-vision "Say hello" 2>/dev/null | head -3
# Should output a greeting message
```

---

## 7. Clone the Project

```bash
# Go to your home directory
cd ~

# Clone the repository
git clone https://github.com/SomratChandraRoy/survey-automation.git

# Enter the project directory
cd survey-automation

# Verify files are there
ls -la
# Should show: main.py, src/, templates/, install.sh, .env.example, etc.
```

---

## 8. Set Up Python Environment

```bash
# Make sure you're in the project directory
cd ~/survey-automation

# Create Python virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate

# Your prompt should now show (venv) at the start

# Upgrade pip
pip install --upgrade pip

# Install all Python dependencies
pip install -r requirements.txt

# Verify key packages are installed
python3 -c "import selenium, flask, loguru; print('✅ All packages installed')"
```

---

## 9. Configure Your Settings

### Copy the Example Configuration

```bash
# Make sure you're in the project directory
cd ~/survey-automation

# Copy example config
cp .env.example .env

# Open the config file for editing
nano .env
```

### Edit the Configuration File

Inside `nano`, update these values:

```bash
# =============================================
# REQUIRED — MUST FILL IN
# =============================================

# Your Opinion Edge account
OPINION_EDGE_EMAIL=your_actual_email@example.com
OPINION_EDGE_PASSWORD=your_actual_password

# Opinion Edge panel URL
OPINION_EDGE_BASE_URL=https://panel.opinion-edge.com

# =============================================
# PROXY (Optional but recommended)
# =============================================
# Leave blank if you don't have a proxy
PROXY_HOST=
PROXY_PORT=
PROXY_USERNAME=
PROXY_PASSWORD=

# =============================================
# CAPTCHA SOLVING METHOD
# =============================================
# Use "audio_free" for FREE solving (no API key needed)
CAPTCHA_METHOD=audio_free

# Or use 2Captcha (paid, better success rate):
# CAPTCHA_API_KEY=your_2captcha_key_here
# CAPTCHA_METHOD=2captcha

# =============================================
# DASHBOARD SECURITY (Highly Recommended)
# =============================================
# Generate a random secret key:
# python3 -c "import secrets; print(secrets.token_hex(32))"
FLASK_SECRET_KEY=paste_your_generated_key_here

# Protect the dashboard with a password
DASHBOARD_USERNAME=admin
DASHBOARD_PASSWORD=choose_a_strong_password_here

# Dashboard port (keep 5000 unless it conflicts)
FLASK_PORT=5000

# =============================================
# PERSONA PROFILE
# =============================================
# Pre-configured German persona — change if needed
PERSONA_NAME=Dirk Baer
PERSONA_AGE=78
PERSONA_BIRTHDAY=10.09.1963
```

**Save and exit**: Press `Ctrl+X`, then `Y`, then `Enter`

### Generate a Secure Secret Key

```bash
# Generate and copy a strong secret key
python3 -c "import secrets; print(secrets.token_hex(32))"
```

Edit `.env` again and paste this value as `FLASK_SECRET_KEY`.

### Verify Configuration is Valid

```bash
# Test settings load correctly
source venv/bin/activate
python3 -c "
import sys; sys.path.insert(0, '.')
from src.config.settings import Settings
s = Settings()
print(f'✅ Email: {s.opinion_edge_email}')
print(f'✅ Base URL: {s.opinion_edge_base_url}')
print(f'✅ Proxy enabled: {s.proxy_enabled}')
print(f'✅ Flask port: {s.flask_port}')
"
```

Expected output:
```
✅ Email: your_email@example.com
✅ Base URL: https://panel.opinion-edge.com
✅ Proxy enabled: False
✅ Flask port: 5000
```

---

## 10. Set Up Firewall and Security

```bash
# Allow SSH (IMPORTANT — do this first or you'll lock yourself out!)
sudo ufw allow 22/tcp

# Allow the dashboard port
sudo ufw allow 5000/tcp

# Allow HTTP/HTTPS (if using Nginx)
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# Enable firewall
sudo ufw --force enable

# Verify rules
sudo ufw status
```

Expected output:
```
Status: active

To                         Action      From
--                         ------      ----
22/tcp                     ALLOW       Anywhere
5000/tcp                   ALLOW       Anywhere
80/tcp                     ALLOW       Anywhere
443/tcp                    ALLOW       Anywhere
```

---

## 11. Install and Start the Automation Service

### Option A: One-Command Install (Recommended)

```bash
cd ~/survey-automation

# Make scripts executable
chmod +x install.sh deploy.sh main.py

# Run the installer (takes ~15 minutes)
./install.sh
```

The installer will:
- Install all system dependencies
- Set up the Python virtual environment
- Create the systemd service
- Configure Nginx reverse proxy
- Start the automation

**OR use the quick deploy script:**

```bash
./deploy.sh
```

### Option B: Manual Service Setup

```bash
cd ~/survey-automation

# Make sure venv is activated
source venv/bin/activate

# Create required directories
mkdir -p logs screenshots data/cookies data/backups data/surveys

# Create systemd service
sudo tee /etc/systemd/system/survey-automation.service > /dev/null << SYSTEMD_EOF
[Unit]
Description=Opinion Edge Survey Automation
After=network.target ollama.service
Wants=ollama.service

[Service]
Type=simple
User=$USER
WorkingDirectory=$(pwd)
Environment="PATH=$(pwd)/venv/bin:/usr/local/bin:/usr/bin:/bin"
ExecStart=$(pwd)/venv/bin/python3 $(pwd)/main.py
Restart=always
RestartSec=10
StartLimitInterval=200
StartLimitBurst=5
StandardOutput=append:$(pwd)/logs/automation.log
StandardError=append:$(pwd)/logs/error.log

# Security hardening
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=strict
ProtectHome=read-only
ReadWritePaths=$(pwd)/logs $(pwd)/screenshots $(pwd)/data $(pwd)/.env

[Install]
WantedBy=multi-user.target
SYSTEMD_EOF

# Reload systemd and enable the service
sudo systemctl daemon-reload
sudo systemctl enable survey-automation
sudo systemctl start survey-automation

# Wait for startup
sleep 5

# Check if it started
sudo systemctl status survey-automation
```

### Verify the Service is Running

```bash
# Check service status
sudo systemctl status survey-automation

# Expected output:
# ● survey-automation.service - Opinion Edge Survey Automation
#    Active: active (running) since ...
#    ...

# Watch live logs (wait 30 seconds to see activity)
tail -f ~/survey-automation/logs/automation.log
```

You should see:
```
✅ Environment validation passed
✅ Configuration loaded successfully
✅ Error tracker initialized
✅ Monitoring dashboard started on port 5000
✅ Cleanup manager started
✅ Backup manager started
✅ Browser automation initialized
Step 1/5: Validating proxy...
Step 2/5: Initializing browser...
Step 3/5: Logging in...
```

Press `Ctrl+C` to stop watching logs.

---

## 12. Access Your Dashboard

### Get Your Server IP

```bash
hostname -I | awk '{print $1}'
# Example output: 159.89.45.123
```

### Open the Dashboard

Open your web browser and go to:
```
http://YOUR_SERVER_IP:5000
```

For example:
```
http://159.89.45.123:5000
```

If you set `DASHBOARD_USERNAME` and `DASHBOARD_PASSWORD`, enter them when prompted.

### What You'll See

The dashboard shows:
- **📊 Statistics**: Surveys completed, failed, success rate, CAPTCHAs solved
- **💰 Earnings Tracker**: Today / This Week / This Month / Total earnings
- **💻 System Resources**: CPU, Memory, and Disk usage with progress bars
- **📝 Recent Logs**: Live log entries with color coding (green=success, red=error)

### Dashboard API Endpoints

| Endpoint | Description |
|----------|-------------|
| `http://IP:5000/` | Main dashboard |
| `http://IP:5000/api/stats` | JSON stats |
| `http://IP:5000/api/earnings` | JSON earnings |
| `http://IP:5000/api/system` | JSON system info |
| `http://IP:5000/api/health` | JSON health status |
| `http://IP:5000/api/metrics` | Prometheus metrics |

---

## 13. Verify Everything is Working

Run through this checklist after setup:

### ✅ Checklist

```bash
# 1. Check Ollama is running
sudo systemctl is-active ollama && echo "✅ Ollama running" || echo "❌ Ollama not running"

# 2. Check automation service is running
sudo systemctl is-active survey-automation && echo "✅ Automation running" || echo "❌ Automation not running"

# 3. Check dashboard is accessible
curl -s -o /dev/null -w "%{http_code}" http://localhost:5000/ && echo " ✅ Dashboard up"

# 4. Check logs directory has entries
[ -f ~/survey-automation/logs/automation.log ] && echo "✅ Logs exist" || echo "❌ No logs"

# 5. Check Chrome works
chromium-browser --headless --no-sandbox --dump-dom https://example.com 2>/dev/null | grep -q "html" && echo "✅ Chrome working" || echo "❌ Chrome issue"

# 6. Check settings load correctly
cd ~/survey-automation && source venv/bin/activate && python3 -c "
from src.config.settings import Settings
s = Settings()
print('✅ Settings:', s.opinion_edge_email, '| Port:', s.flask_port)
"
```

### Check the Last 50 Log Lines

```bash
tail -50 ~/survey-automation/logs/automation.log
```

Look for these positive signs:
- `✅ Configuration loaded successfully`
- `✅ Monitoring dashboard started`
- `✅ Browser initialized successfully`
- `✅ Login successful`
- `✅ Survey completed`
- `💰 Estimated earnings: +$1.50`

### Check Health Status via API

```bash
curl -s http://localhost:5000/api/health | python3 -m json.tool
```

Expected:
```json
{
    "overall_status": "healthy",
    "checks": {
        "environment": {"status": "ok"},
        "ollama": {"status": "ok"},
        "disk_space": {"status": "ok"},
        "memory": {"status": "ok"}
    }
}
```

---

## 14. Daily Monitoring (2 minutes/day)

### Morning Check (30 seconds)

```bash
# Quick status check
sudo systemctl status survey-automation --no-pager | head -5

# Count surveys completed today
ls ~/survey-automation/data/surveys/ 2>/dev/null | wc -l

# Check earnings
cat ~/survey-automation/data/earnings.json 2>/dev/null | python3 -m json.tool | grep -E "today|total|week"
```

### View Today's Stats

```bash
# Full stats
cat ~/survey-automation/data/stats.json | python3 -m json.tool
```

### Check Earnings via Dashboard API

```bash
curl -s http://localhost:5000/api/earnings | python3 -m json.tool
```

### Watch Live Activity

```bash
# Real-time log watching (press Ctrl+C to stop)
tail -f ~/survey-automation/logs/automation.log

# Only show important lines
tail -f ~/survey-automation/logs/automation.log | grep -E "✅|❌|💰|Survey|Login|ERROR"
```

---

## 15. Troubleshooting Common Issues

### ❌ Service Won't Start

```bash
# Check detailed error logs
sudo journalctl -u survey-automation -n 100 --no-pager

# Check Python environment
cd ~/survey-automation && source venv/bin/activate
python3 -c "from src.config.settings import Settings; Settings()"

# Common fix: check .env file exists and has valid values
cat .env | grep -v "^#" | grep -v "^$"
```

### ❌ Login Fails

```bash
# Check your credentials in .env
grep -E "OPINION_EDGE_EMAIL|OPINION_EDGE_PASSWORD" ~/survey-automation/.env

# Manually test login in browser:
# Go to: https://panel.opinion-edge.com
# Try logging in with your credentials

# Check if website is accessible
curl -s -o /dev/null -w "%{http_code}" https://panel.opinion-edge.com
# Expected: 200 or 301/302
```

### ❌ Browser/Chrome Issues

```bash
# Reinstall Chrome
sudo apt-get install --reinstall chromium-browser chromium-chromedriver

# Verify Chrome version
chromium-browser --version

# Test headless Chrome
chromium-browser --headless --no-sandbox --disable-gpu \
  --dump-dom https://panel.opinion-edge.com 2>&1 | head -20
```

### ❌ Ollama Not Working

```bash
# Restart Ollama
sudo systemctl restart ollama
sleep 10

# Check status
sudo systemctl status ollama

# Re-pull model if needed
ollama pull llama3.2-vision:latest

# Test Ollama
curl http://localhost:11434/api/tags
# Should return JSON with model list
```

### ❌ Port 5000 Already in Use

```bash
# Find what's using the port
sudo ss -tlnp | grep :5000

# Kill the process (replace PID with actual number)
sudo kill -9 PID

# Or change the dashboard port in .env
nano ~/survey-automation/.env
# Change FLASK_PORT=5001
sudo systemctl restart survey-automation
```

### ❌ Out of Memory

```bash
# Check memory usage
free -h

# Add 2 GB swap space
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab

# Verify swap is active
free -h | grep Swap
```

### ❌ No Surveys Available

This is normal! Surveys have limited availability. Check:

```bash
# Check what time it is on your server (surveys peak during business hours)
date

# Check logs for survey availability messages
grep -i "no surveys\|surveys available\|survey" ~/survey-automation/logs/automation.log | tail -20

# The system will automatically retry every 60 seconds
```

### ❌ High CPU Usage

```bash
# Check what's using CPU
htop

# Reduce Chrome CPU usage in .env
nano ~/survey-automation/.env
# Add: ACTION_DELAY_MIN=5
# Add: ACTION_DELAY_MAX=12
sudo systemctl restart survey-automation
```

### ❌ Dashboard Not Accessible from Browser

```bash
# Check firewall allows port 5000
sudo ufw status | grep 5000

# If not allowed:
sudo ufw allow 5000/tcp

# Check Flask is bound to 0.0.0.0 (not just localhost)
grep -i "flask_port\|flask" ~/survey-automation/logs/automation.log | head -5
# Should show: Starting dashboard on http://0.0.0.0:5000

# Try accessing locally first
curl -s http://localhost:5000/ | head -5
```

---

## 16. Essential Commands Reference

### Service Management

```bash
# Start the automation
sudo systemctl start survey-automation

# Stop the automation
sudo systemctl stop survey-automation

# Restart the automation
sudo systemctl restart survey-automation

# Check status
sudo systemctl status survey-automation

# View all recent logs from systemd
sudo journalctl -u survey-automation -f

# Enable auto-start on reboot (already done by install.sh)
sudo systemctl enable survey-automation
```

### Log Commands

```bash
# Watch live logs (most useful!)
tail -f ~/survey-automation/logs/automation.log

# Last 100 lines
tail -100 ~/survey-automation/logs/automation.log

# Last 100 lines of error log
tail -100 ~/survey-automation/logs/error.log

# Search for errors
grep "ERROR\|❌" ~/survey-automation/logs/automation.log | tail -20

# Search for earnings
grep "💰\|earnings" ~/survey-automation/logs/automation.log | tail -20

# Count completed surveys in log
grep "Survey completed" ~/survey-automation/logs/automation.log | wc -l
```

### Data and Earnings

```bash
# View current stats
cat ~/survey-automation/data/stats.json | python3 -m json.tool

# View earnings breakdown
cat ~/survey-automation/data/earnings.json | python3 -m json.tool

# Count survey files
ls ~/survey-automation/data/surveys/ | wc -l

# Calculate estimate from files
COUNT=$(ls ~/survey-automation/data/surveys/ 2>/dev/null | wc -l)
echo "Surveys: $COUNT | Estimated: \$$(echo "scale=2; $COUNT * 1.50" | bc)"
```

### System Health

```bash
# Check memory
free -h

# Check disk space
df -h ~/survey-automation

# Check CPU and memory in real time
htop

# Check what ports are open
sudo ss -tlnp

# System uptime
uptime

# Check if services are running
for svc in ollama survey-automation nginx; do
    sudo systemctl is-active $svc &>/dev/null && echo "✅ $svc running" || echo "⚠️  $svc not running"
done
```

### Update the Project

```bash
cd ~/survey-automation

# Stop the service
sudo systemctl stop survey-automation

# Pull latest changes
git pull origin main

# Reactivate venv and update packages
source venv/bin/activate
pip install -r requirements.txt --upgrade

# Restart the service
sudo systemctl start survey-automation

# Check it came back up
sudo systemctl status survey-automation
```

### Backup and Restore

```bash
# Manual backup (automatic backups run hourly)
cd ~/survey-automation
tar -czf ~/manual-backup-$(date +%Y%m%d).tar.gz data/ logs/

# List available backups
ls ~/survey-automation/data/backups/

# Restore from a backup
tar -xzf ~/survey-automation/data/backups/backup_YYYYMMDD_HHMMSS.tar.gz -C ~/survey-automation/
```

---

## 17. Maximise Earnings

### 1. Complete Your Opinion Edge Profile

Log into https://panel.opinion-edge.com and complete 100% of your profile:
- Demographics (age, gender, location, education)
- Employment and income information
- Interests and hobbies
- Shopping and consumer habits
- Technology usage patterns

**More profile data = more targeted surveys = more earnings!**

### 2. Use a Residential Proxy (Optional but Recommended)

A residential proxy makes your account look more legitimate and reduces CAPTCHA frequency.

```bash
nano ~/survey-automation/.env
```

Add your proxy details:
```
PROXY_HOST=your-proxy-host.com
PROXY_PORT=12345
PROXY_USERNAME=your-proxy-user
PROXY_PASSWORD=your-proxy-pass
```

```bash
sudo systemctl restart survey-automation
```

Good proxy providers:
- **Brightdata**: https://brightdata.com (most reliable)
- **Oxylabs**: https://oxylabs.io
- **Smartproxy**: https://smartproxy.com (~$75/month for residential)

### 3. Adjust Speed Settings

Edit `.env` to fine-tune behavior:
```bash
# Faster (higher detection risk, more surveys/day)
ACTION_DELAY_MIN=2
ACTION_DELAY_MAX=5

# Safer (lower detection risk, more stable)
ACTION_DELAY_MIN=3
ACTION_DELAY_MAX=8

# Very safe (recommended for long-term use)
ACTION_DELAY_MIN=4
ACTION_DELAY_MAX=10
```

### 4. Monitor Peak Survey Hours

Surveys are most available during these times:
- **Peak times**: Weekdays 9 AM – 12 PM and 6 PM – 9 PM (Germany/EU time)
- **Good times**: Weekdays 6 AM – 9 AM and 3 PM – 6 PM
- **Slow times**: Weekends and late nights

The bot runs 24/7 and will catch all available surveys automatically.

### 5. Check and Withdraw Earnings Regularly

Log into your Opinion Edge account to check your points balance and withdraw:
- **PayPal**: Minimum €10, 1–3 days processing
- **Amazon gift cards**: Minimum €5, instant
- **Bank transfer**: Minimum €25, 5–7 days

### 6. Run Multiple Accounts (Advanced)

> ⚠️ Check Opinion Edge Terms of Service before running multiple accounts.

```bash
# Create a second instance
mkdir ~/survey-automation-account2
cp -r ~/survey-automation/* ~/survey-automation-account2/
cd ~/survey-automation-account2

# Configure with different account credentials
cp .env.example .env
nano .env
# Set: OPINION_EDGE_EMAIL=account2@example.com
# Set: OPINION_EDGE_PASSWORD=different_password
# Set: FLASK_PORT=5001  ← Must be different!
# Set: DASHBOARD_USERNAME=admin2

# Create second service
sudo tee /etc/systemd/system/survey-automation-2.service > /dev/null << EOF2
[Unit]
Description=Opinion Edge Survey Automation Account 2
After=network.target ollama.service

[Service]
Type=simple
User=$USER
WorkingDirectory=$(pwd)
Environment="PATH=$(pwd)/venv/bin:/usr/local/bin:/usr/bin:/bin"
ExecStart=$(pwd)/venv/bin/python3 $(pwd)/main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF2

sudo systemctl daemon-reload
sudo systemctl enable survey-automation-2
sudo systemctl start survey-automation-2
```

Access second dashboard at: `http://YOUR_IP:5001`

---

## 18. Maintenance and Updates

### Keep the System Healthy

```bash
# Weekly system update (run every Sunday)
sudo apt-get update && sudo apt-get upgrade -y

# Clear old screenshots (automated, but manual override if disk is full)
find ~/survey-automation/screenshots/ -mtime +1 -delete

# Check disk usage
df -h ~/survey-automation/

# Remove old backups older than 30 days (automated, but manual if needed)
find ~/survey-automation/data/backups/ -mtime +30 -delete
```

### Monitor Disk Space

```bash
# Check overall disk
df -h /

# Check project size
du -sh ~/survey-automation/
du -sh ~/survey-automation/screenshots/
du -sh ~/survey-automation/logs/
du -sh ~/survey-automation/data/
```

### Reboot Checklist

After a server reboot, everything starts automatically. But verify:

```bash
# After reboot, wait 2 minutes then check:
sudo systemctl status ollama
sudo systemctl status survey-automation
curl -s http://localhost:5000/api/health
```

### Keep Ollama Updated

```bash
# Check Ollama version
ollama --version

# Update Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Restart after update
sudo systemctl restart ollama
```

---

## 🎉 Quick Start Checklist

Use this checklist to make sure everything is set up correctly:

```
□ DigitalOcean droplet created (Ubuntu 22.04, 8GB+ RAM)
□ SSH access working
□ System updated (apt-get update && upgrade)
□ Timezone set correctly
□ All system packages installed
□ Chromium browser installed and working
□ Ollama installed and running
□ AI model downloaded (llama3.2-vision)
□ Project cloned from GitHub
□ Python venv created and packages installed
□ .env file configured with Opinion Edge credentials
□ Strong FLASK_SECRET_KEY generated and set
□ Dashboard password set (DASHBOARD_USERNAME/PASSWORD)
□ Firewall configured (port 22, 5000 open)
□ Automation service installed (systemd)
□ Service running (systemctl status shows "active")
□ Dashboard accessible at http://YOUR_IP:5000
□ Logs showing login/survey activity
□ Opinion Edge profile 100% complete
```

---

## 💰 Expected Earnings Timeline

| Timeframe | Surveys | Estimated Earnings |
|-----------|---------|-------------------|
| **Day 1** | 2–8 | $3–$12 |
| **Week 1** | 15–50 | $22–$75 |
| **Month 1** | 100–300 | $150–$450 |
| **Month 3** | 300–900 | $450–$1,350 |
| **Month 6** | 700–2,000 | $1,050–$3,000 |

> **Note**: Earnings vary based on survey availability, account quality, and time zone. These are estimates based on $1.50/survey average.

---

## 🆘 Need Help?

1. **Check logs first**: `tail -100 ~/survey-automation/logs/automation.log`
2. **Check health**: `curl -s http://localhost:5000/api/health | python3 -m json.tool`
3. **Restart service**: `sudo systemctl restart survey-automation`
4. **Read more guides**: See the `md/` folder in the project
5. **Open an issue**: https://github.com/SomratChandraRoy/survey-automation/issues

---

*Happy earning! 💰🤖*
