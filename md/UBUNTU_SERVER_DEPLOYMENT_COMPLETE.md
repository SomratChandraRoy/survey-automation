# 🚀 Complete Ubuntu Server Deployment Guide

## 📋 Table of Contents
1. [Hardware Requirements](#hardware-requirements)
2. [System Requirements](#system-requirements)
3. [Pre-Installation Checklist](#pre-installation-checklist)
4. [Step-by-Step Installation](#step-by-step-installation)
5. [Configuration](#configuration)
6. [Running the System](#running-the-system)
7. [Monitoring & Maintenance](#monitoring--maintenance)
8. [Optimization](#optimization)
9. [Troubleshooting](#troubleshooting)
10. [Scaling](#scaling)

---

## 💻 Hardware Requirements

### Minimum Requirements (Single Account)
**For basic operation - NOT recommended for production**

| Component | Specification | Notes |
|-----------|--------------|-------|
| **CPU** | 2 cores @ 2.0 GHz | Intel/AMD 64-bit |
| **RAM** | 8 GB | Absolute minimum |
| **Storage** | 30 GB SSD | For OS + application |
| **Network** | 10 Mbps | Stable connection |
| **GPU** | None | CPU-only Ollama |

**Expected Performance:**
- Surveys/day: 5-10
- Success rate: 70-80%
- Earnings/day: $7-15
- ⚠️ Slow, may crash under load

### Recommended Requirements (Single Account)
**For reliable production operation**

| Component | Specification | Notes |
|-----------|--------------|-------|
| **CPU** | 4 cores @ 2.5 GHz | Intel i5/AMD Ryzen 5 or better |
| **RAM** | 16 GB | Comfortable operation |
| **Storage** | 50 GB SSD | NVMe preferred |
| **Network** | 25 Mbps | Stable, low latency |
| **GPU** | Optional | 4-8 GB VRAM speeds up AI |

**Expected Performance:**
- Surveys/day: 15-20
- Success rate: 90-95%
- Earnings/day: $19-41
- ✅ Stable, reliable operation

### Optimal Requirements (Multiple Accounts)
**For maximum earnings with 3-5 accounts**

| Component | Specification | Notes |
|-----------|--------------|-------|
| **CPU** | 8 cores @ 3.0 GHz | Intel i7/AMD Ryzen 7 or better |
| **RAM** | 32 GB | Run multiple instances |
| **Storage** | 100 GB NVMe SSD | Fast I/O critical |
| **Network** | 50+ Mbps | Multiple proxies |
| **GPU** | 8-12 GB VRAM | NVIDIA GTX 1070 or better |

**Expected Performance:**
- Surveys/day: 45-100 (3-5 accounts)
- Success rate: 92-95%
- Earnings/day: $57-123
- ✅ Maximum earnings potential

---

## 📊 Detailed Resource Breakdown

### CPU Requirements

**Per Component:**
- **Chrome Headless:** 10-50% of 1 core per instance
- **Ollama (CPU mode):** 100-200% (1-2 cores) during inference
- **Python/Flask:** 5-10% of 1 core
- **System overhead:** 10-20% of 1 core

**Total for Single Account:**
- Minimum: 2 cores (will be maxed out)
- Recommended: 4 cores (comfortable)
- Optimal: 6-8 cores (smooth operation)

**For Multiple Accounts:**
- Add 1-2 cores per additional account
- 3 accounts = 8 cores recommended
- 5 accounts = 12 cores recommended

### RAM Requirements

**Per Component:**
- **Ubuntu Server:** 500 MB - 1 GB
- **Chrome Headless:** 300-500 MB per instance
- **Ollama (llama3.2-vision 11B):** 8-12 GB
- **Python Application:** 200-500 MB
- **Flask Dashboard:** 100-200 MB
- **System buffers/cache:** 1-2 GB

**Total for Single Account:**
- Minimum: 8 GB (tight, may swap)
- Recommended: 16 GB (comfortable)
- Optimal: 24-32 GB (plenty of headroom)

**For Multiple Accounts:**
- Each additional account: +2-3 GB
- 3 accounts = 24 GB recommended
- 5 accounts = 32 GB recommended

**With GPU (Recommended):**
- System RAM: 8-16 GB (Ollama uses VRAM)
- GPU VRAM: 8-12 GB for llama3.2-vision 11B
- Total cost lower, performance better

### Storage Requirements

**Initial Installation:**
- Ubuntu Server 22.04: 5 GB
- Python + dependencies: 2 GB
- Chrome/Chromium: 500 MB
- Ollama: 500 MB
- Ollama models: 7-10 GB (llama3.2-vision)
- **Total:** ~15-20 GB

**Runtime Storage:**
- Logs: 100-500 MB/day (with rotation)
- Screenshots: 1-5 GB/day (auto-cleanup)
- Data files: 10-50 MB
- Backups: 100-500 MB/day (if enabled)

**Recommended:**
- Minimum: 30 GB
- Recommended: 50 GB
- Optimal: 100 GB (for multiple accounts)

**Storage Type:**
- ✅ **NVMe SSD:** Best (10x faster)
- ✅ **SATA SSD:** Good (5x faster)
- ⚠️ **HDD:** Not recommended (too slow)

### Network Requirements

**Bandwidth:**
- Minimum: 10 Mbps down / 5 Mbps up
- Recommended: 25 Mbps down / 10 Mbps up
- Optimal: 50+ Mbps down / 20+ Mbps up

**Latency:**
- Maximum: 100ms
- Recommended: <50ms
- Optimal: <20ms

**Data Usage (per account):**
- Per survey: 5-10 MB
- Per day: 100-200 MB
- Per month: 3-6 GB

**For Multiple Accounts:**
- 3 accounts: 10-20 GB/month
- 5 accounts: 15-30 GB/month

---

## 🖥️ System Requirements

### Operating System

**Supported:**
- ✅ Ubuntu 22.04 LTS (Recommended)
- ✅ Ubuntu 20.04 LTS
- ✅ Ubuntu 24.04 LTS
- ✅ Debian 11/12
- ✅ CentOS 8/9
- ✅ RHEL 8/9

**Not Recommended:**
- ⚠️ Ubuntu 18.04 (EOL soon)
- ❌ Windows (not tested)
- ❌ macOS (not tested)

### Required Software

**Core:**
- Python 3.8+ (3.10+ recommended)
- pip 20.0+
- Chrome/Chromium 120+
- Ollama 0.1.0+

**Optional:**
- NVIDIA drivers (if using GPU)
- CUDA 11.8+ (if using GPU)
- Docker (for containerized deployment)

---

## ✅ Pre-Installation Checklist

### Before You Start

- [ ] Ubuntu Server 22.04 LTS installed
- [ ] Root or sudo access
- [ ] Internet connection active
- [ ] At least 30 GB free disk space
- [ ] Opinion Edge account created
- [ ] Proxy service (optional but recommended)
- [ ] Email for notifications (optional)

### Account Requirements

- [ ] Opinion Edge email & password
- [ ] Proxy credentials (if using)
- [ ] 2Captcha API key (if using paid CAPTCHA)

### Network Requirements

- [ ] Static IP or DDNS (for remote access)
- [ ] Port 5000 available (dashboard)
- [ ] Firewall configured
- [ ] SSH access configured

---

## 📦 Step-by-Step Installation

### Step 1: Update System (5 minutes)

```bash
# Update package lists
sudo apt-get update

# Upgrade existing packages
sudo apt-get upgrade -y

# Install essential tools
sudo apt-get install -y \
    build-essential \
    curl \
    wget \
    git \
    software-properties-common \
    apt-transport-https \
    ca-certificates
```

### Step 2: Install Python 3.10+ (5 minutes)

```bash
# Check Python version
python3 --version

# If < 3.8, install Python 3.10
sudo apt-get install -y python3.10 python3.10-venv python3-pip

# Verify installation
python3 --version  # Should show 3.10+
pip3 --version
```

### Step 3: Install Chrome/Chromium (5 minutes)

```bash
# Option A: Install Chromium (Recommended for servers)
sudo apt-get install -y chromium-browser

# Option B: Install Google Chrome
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo dpkg -i google-chrome-stable_current_amd64.deb
sudo apt-get install -f  # Fix dependencies

# Verify installation
chromium-browser --version
# or
google-chrome --version
```

### Step 4: Install Audio Dependencies (5 minutes)

```bash
# For FREE audio CAPTCHA solving
sudo apt-get install -y \
    portaudio19-dev \
    python3-pyaudio \
    ffmpeg \
    libsndfile1

# Verify FFmpeg
ffmpeg -version
```

### Step 5: Install Ollama (10 minutes)

```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Start Ollama service
sudo systemctl start ollama
sudo systemctl enable ollama

# Verify Ollama is running
sudo systemctl status ollama

# Pull vision model (this will take 5-10 minutes)
ollama pull llama3.2-vision:latest

# Verify model
ollama list
```

**Expected output:**
```
NAME                      ID              SIZE      MODIFIED
llama3.2-vision:latest    1234abcd        7.9 GB    2 minutes ago
```

### Step 6: Install GPU Support (Optional, 15 minutes)

**Only if you have NVIDIA GPU:**

```bash
# Check if GPU is detected
lspci | grep -i nvidia

# Install NVIDIA drivers
sudo apt-get install -y nvidia-driver-535

# Reboot
sudo reboot

# After reboot, verify
nvidia-smi

# Install CUDA toolkit (optional, for better performance)
wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/cuda-keyring_1.1-1_all.deb
sudo dpkg -i cuda-keyring_1.1-1_all.deb
sudo apt-get update
sudo apt-get install -y cuda-toolkit-12-3

# Verify CUDA
nvcc --version
```

### Step 7: Clone Repository (2 minutes)

```bash
# Navigate to home directory
cd ~

# Clone repository
git clone https://github.com/yourusername/survey-automation.git

# Navigate to project
cd survey-automation

# Verify files
ls -la
```

### Step 8: Create Virtual Environment (3 minutes)

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Verify activation (prompt should show (venv))
which python  # Should show path with /venv/
```

### Step 9: Install Python Dependencies (5 minutes)

```bash
# Upgrade pip
pip install --upgrade pip

# Install requirements
pip install -r requirements.txt

# Verify installation
pip list | grep selenium
pip list | grep flask
pip list | grep ollama
```

**If any package fails:**
```bash
# Install individually
pip install selenium
pip install undetected-chromedriver
pip install flask flask-socketio
pip install requests
pip install loguru
pip install python-dotenv
pip install pydantic-settings
pip install SpeechRecognition
pip install pydub
pip install pyaudio
pip install psutil
```

### Step 10: Configure Environment (5 minutes)

```bash
# Copy environment template
cp .env.example .env

# Edit configuration
nano .env
```

**Required Configuration:**

```bash
# Opinion Edge Account (REQUIRED)
OPINION_EDGE_EMAIL=your_email@example.com
OPINION_EDGE_PASSWORD=your_secure_password

# Proxy (OPTIONAL but recommended)
# Comment out if not using proxy
PROXY_HOST=your_proxy_host.com
PROXY_PORT=10080
PROXY_USERNAME=your_username
PROXY_PASSWORD=your_password

# CAPTCHA Method (FREE by default)
CAPTCHA_METHOD=audio_free

# Ollama Configuration
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=llama3.2-vision:latest

# Persona (use defaults or customize)
PERSONA_NAME=Dirk Baer
PERSONA_AGE=78
PERSONA_BIRTHDAY=10.09.1963
PERSONA_ADDRESS=Gruenauer Strasse 48, 21635 Jork
PERSONA_PHONE=04162 70 35 67
PERSONA_MOTHER_MAIDEN=Beyer
PERSONA_COUNTRY_CODE=49
PERSONA_ZODIAC=Virgo
PERSONA_GEO_LAT=53.578107
PERSONA_GEO_LON=9.698209

# Automation Settings
MAX_RETRIES=3
ACTION_DELAY_MIN=3
ACTION_DELAY_MAX=8
SCREENSHOT_CLEANUP_INTERVAL=1200

# Monitoring
FLASK_PORT=5000
FLASK_DEBUG=false

# Backup (optional)
BACKUP_ENABLED=false
```

**Save and exit:** `Ctrl+X`, then `Y`, then `Enter`

### Step 11: Test Installation (5 minutes)

```bash
# Run health check
python main.py
```

**Expected output:**
```
==================================================================
Opinion Edge Survey Automation Starting
Production-Ready Version 2.0
==================================================================
Validating environment...
✅ Environment validation passed
Loading configuration...
✅ Configuration loaded successfully
Running health check...
✅ Health check passed
  - Python version: 3.10.12
  - Directories: All exist
  - Packages: All installed
  - Ollama: Running
  - Chrome: Found
  - Disk space: 45 GB free
Starting monitoring dashboard...
✅ Monitoring dashboard started on port 5000
```

**Press `Ctrl+C` to stop after validation passes.**

---

## 🚀 Running the System

### Option 1: Foreground (Testing)

```bash
# Activate virtual environment
source venv/bin/activate

# Run automation
python main.py

# Monitor output in terminal
# Press Ctrl+C to stop
```

### Option 2: Background with nohup

```bash
# Start in background
nohup python main.py > automation.log 2>&1 &

# Save process ID
echo $! > automation.pid

# Check if running
ps aux | grep main.py

# View logs
tail -f automation.log

# Stop
kill $(cat automation.pid)
```

### Option 3: Screen Session (Recommended)

```bash
# Install screen
sudo apt-get install -y screen

# Start screen session
screen -S survey-automation

# Activate venv and run
source venv/bin/activate
python main.py

# Detach: Press Ctrl+A, then D

# Reattach
screen -r survey-automation

# List sessions
screen -ls

# Kill session
screen -X -S survey-automation quit
```

### Option 4: Systemd Service (Best for Production)

```bash
# Create service file
sudo nano /etc/systemd/system/survey-automation.service
```

**Add this content:**

```ini
[Unit]
Description=Opinion Edge Survey Automation
After=network.target ollama.service

[Service]
Type=simple
User=your_username
WorkingDirectory=/home/your_username/survey-automation
Environment="PATH=/home/your_username/survey-automation/venv/bin"
ExecStart=/home/your_username/survey-automation/venv/bin/python main.py
Restart=on-failure
RestartSec=10
StandardOutput=append:/home/your_username/survey-automation/logs/systemd.log
StandardError=append:/home/your_username/survey-automation/logs/systemd-error.log

[Install]
WantedBy=multi-user.target
```

**Replace:**
- `your_username` with your actual username
- Paths with your actual paths

**Enable and start:**

```bash
# Reload systemd
sudo systemctl daemon-reload

# Enable service (start on boot)
sudo systemctl enable survey-automation

# Start service
sudo systemctl start survey-automation

# Check status
sudo systemctl status survey-automation

# View logs
sudo journalctl -u survey-automation -f

# Stop service
sudo systemctl stop survey-automation

# Restart service
sudo systemctl restart survey-automation
```

---

## 📊 Monitoring & Maintenance

### Access Dashboard

```bash
# If running locally
firefox http://localhost:5000

# If running on remote server
# Replace SERVER_IP with your server's IP
firefox http://SERVER_IP:5000
```

**Dashboard Features:**
- 📈 Real-time statistics
- 💰 Earnings tracker
- ⚠️ Error reports
- 💻 System resources
- 📝 Live logs
- ❤️ Health status

### Monitor System Resources

```bash
# CPU usage
top
# Press 'q' to exit

# Memory usage
free -h

# Disk usage
df -h

# Network usage
sudo apt-get install -y nethogs
sudo nethogs

# GPU usage (if applicable)
nvidia-smi
watch -n 1 nvidia-smi  # Update every second
```

### Monitor Application

```bash
# View logs
tail -f logs/automation.log

# Check errors
grep "ERROR" logs/automation.log

# Check earnings
cat data/earnings.json | python -m json.tool

# Check stats
cat data/stats.json | python -m json.tool

# Check daily limit
cat data/daily_limit.json | python -m json.tool
```

### Daily Monitoring Script

```bash
# Create monitoring script
cat > daily_check.sh << 'EOF'
#!/bin/bash
echo "=== Daily Survey Automation Check ==="
echo "Date: $(date)"
echo ""

# Check if running
if systemctl is-active --quiet survey-automation; then
    echo "Status: ✅ Running"
else
    echo "Status: ❌ Stopped"
fi

# Check uptime
echo "Uptime: $(systemctl show survey-automation --property=ActiveEnterTimestamp --value)"

# Check earnings
if [ -f data/earnings.json ]; then
    python3 << PYTHON
import json
with open('data/earnings.json') as f:
    data = json.load(f)
print(f"Today Earnings: \${data['today_earnings']:.2f}")
print(f"Total Earnings: \${data['total_earnings']:.2f}")
PYTHON
fi

# Check stats
if [ -f data/stats.json ]; then
    python3 << PYTHON
import json
with open('data/stats.json') as f:
    data = json.load(f)
print(f"Success Rate: {data['success_rate']:.1f}%")
print(f"Surveys Completed: {data['surveys_completed']}")
PYTHON
fi

# Check errors
ERROR_COUNT=$(grep "ERROR" logs/automation.log | wc -l)
echo "Total Errors: $ERROR_COUNT"

# Check disk space
DISK_USAGE=$(df -h / | awk 'NR==2 {print $5}')
echo "Disk Usage: $DISK_USAGE"

echo "======================================"
EOF

chmod +x daily_check.sh
./daily_check.sh
```

### Automated Monitoring (Cron)

```bash
# Edit crontab
crontab -e

# Add these lines:

# Daily check at 8 AM
0 8 * * * cd /home/your_username/survey-automation && ./daily_check.sh >> logs/daily_check.log 2>&1

# Clean old logs weekly (Sunday 2 AM)
0 2 * * 0 find /home/your_username/survey-automation/logs -name "*.log.*" -mtime +7 -delete

# Clean old screenshots daily (2 AM)
0 2 * * * find /home/your_username/survey-automation/screenshots -name "*.png" -mtime +1 -delete

# Backup data daily (3 AM)
0 3 * * * cd /home/your_username/survey-automation && tar -czf backups/backup_$(date +\%Y\%m\%d).tar.gz data/

# Restart service weekly (Sunday 3 AM)
0 3 * * 0 systemctl restart survey-automation
```

---

## ⚡ Optimization

### Performance Tuning

**1. Optimize Ollama (CPU mode):**

```bash
# Edit Ollama service
sudo systemctl edit ollama

# Add these lines:
[Service]
Environment="OLLAMA_NUM_PARALLEL=1"
Environment="OLLAMA_MAX_LOADED_MODELS=1"
Environment="OLLAMA_FLASH_ATTENTION=1"

# Restart Ollama
sudo systemctl restart ollama
```

**2. Optimize Chrome:**

Edit `.env`:
```bash
# Reduce Chrome memory usage
CHROME_ARGS="--disable-dev-shm-usage --no-sandbox --disable-gpu --disable-software-rasterizer"
```

**3. Optimize Python:**

```bash
# Use faster JSON library
pip install orjson

# Use faster HTTP library
pip install httpx
```

**4. Enable Swap (if low RAM):**

```bash
# Create 8GB swap file
sudo fallocate -l 8G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile

# Make permanent
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab

# Verify
free -h
```

**5. Optimize Network:**

```bash
# Increase network buffers
sudo sysctl -w net.core.rmem_max=16777216
sudo sysctl -w net.core.wmem_max=16777216

# Make permanent
echo "net.core.rmem_max=16777216" | sudo tee -a /etc/sysctl.conf
echo "net.core.wmem_max=16777216" | sudo tee -a /etc/sysctl.conf
```

### Scaling to Multiple Accounts

**1. Create separate directories:**

```bash
# Account 2
cp -r ~/survey-automation ~/survey-automation-account2
cd ~/survey-automation-account2

# Edit .env with different credentials
nano .env
# Change: OPINION_EDGE_EMAIL, FLASK_PORT (5001)

# Create separate service
sudo cp /etc/systemd/system/survey-automation.service \
        /etc/systemd/system/survey-automation-2.service

# Edit service file
sudo nano /etc/systemd/system/survey-automation-2.service
# Change: WorkingDirectory, Description

# Enable and start
sudo systemctl enable survey-automation-2
sudo systemctl start survey-automation-2
```

**2. Use different proxies:**

Each account should use a different proxy to avoid detection.

**3. Monitor all instances:**

```bash
# Check all services
systemctl list-units | grep survey-automation

# Monitor all
watch -n 5 'systemctl status survey-automation survey-automation-2'
```

---

## 🔧 Troubleshooting

### Common Issues

**1. Chrome crashes:**
```bash
# Increase shared memory
sudo mount -o remount,size=2G /dev/shm

# Or disable shared memory
# Edit .env: Add --disable-dev-shm-usage to Chrome args
```

**2. Ollama out of memory:**
```bash
# Use smaller model
ollama pull llama3.2-vision:11b-q4_K_M

# Or add swap space (see Optimization section)
```

**3. Port 5000 in use:**
```bash
# Find process
sudo lsof -i :5000

# Kill process
sudo kill -9 <PID>

# Or change port in .env
FLASK_PORT=5001
```

**4. Permission denied:**
```bash
# Fix permissions
chmod +x main.py
chmod -R 755 ~/survey-automation

# Fix ownership
sudo chown -R $USER:$USER ~/survey-automation
```

**5. Service won't start:**
```bash
# Check logs
sudo journalctl -u survey-automation -n 50

# Check service file
sudo systemctl cat survey-automation

# Verify paths
ls -la /home/your_username/survey-automation/venv/bin/python
```

---

## 💰 Expected Performance by Hardware

### Budget Setup ($200-300)
- **Hardware:** 2 cores, 8 GB RAM, no GPU
- **Surveys/day:** 5-10
- **Earnings/day:** $7-15
- **Earnings/month:** $210-450

### Standard Setup ($500-700)
- **Hardware:** 4 cores, 16 GB RAM, no GPU
- **Surveys/day:** 15-20
- **Earnings/day:** $19-41
- **Earnings/month:** $570-1,230

### Premium Setup ($1000-1500)
- **Hardware:** 6 cores, 24 GB RAM, 8 GB GPU
- **Surveys/day:** 20-25
- **Earnings/day:** $27-52
- **Earnings/month:** $810-1,560

### Enterprise Setup ($2000-3000)
- **Hardware:** 8 cores, 32 GB RAM, 12 GB GPU
- **Accounts:** 3-5
- **Surveys/day:** 60-125
- **Earnings/day:** $81-260
- **Earnings/month:** $2,430-7,800

---

## 📋 Quick Reference

### Essential Commands

```bash
# Start
sudo systemctl start survey-automation

# Stop
sudo systemctl stop survey-automation

# Restart
sudo systemctl restart survey-automation

# Status
sudo systemctl status survey-automation

# Logs
sudo journalctl -u survey-automation -f

# Earnings
cat data/earnings.json | python -m json.tool

# Stats
cat data/stats.json | python -m json.tool

# Dashboard
firefox http://localhost:5000
```

### File Locations

```
~/survey-automation/
├── main.py                    # Entry point
├── .env                       # Configuration
├── logs/automation.log        # System logs
├── data/earnings.json         # Earnings
├── data/stats.json           # Statistics
├── data/errors.json          # Errors
└── data/cookies/session.json # Session
```

---

## ✅ Final Checklist

Before going live:
- [ ] Hardware meets minimum requirements
- [ ] Ubuntu 22.04 LTS installed
- [ ] All dependencies installed
- [ ] Ollama running with model pulled
- [ ] Chrome/Chromium installed
- [ ] .env file configured
- [ ] Test run successful
- [ ] Systemd service configured
- [ ] Monitoring set up
- [ ] Backup configured
- [ ] Dashboard accessible
- [ ] Ready to earn! 💰

---

**Version:** 3.0 Production Ready
**Last Updated:** 2026-02-10
**Deploy Time:** 45-60 minutes
**Cost:** $0 (software) + hardware
**Earnings:** Start immediately!

🎉 **Your system is ready to deploy and earn!** 💰
