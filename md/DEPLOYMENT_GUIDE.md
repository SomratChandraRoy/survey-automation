# 🚀 Complete Deployment Guide

## Quick Navigation
- [Prerequisites](#prerequisites)
- [Method 1: One-Command Install](#method-1-one-command-install-recommended)
- [Method 2: Docker Compose](#method-2-docker-compose)
- [Method 3: GitHub Deployment](#method-3-github-deployment)
- [Post-Deployment](#post-deployment)
- [Verification](#verification)

---

## Prerequisites

### System Requirements
- **OS**: Ubuntu 20.04+ or Debian 11+
- **CPU**: 4 cores @ 2.5 GHz (minimum: 2 cores)
- **RAM**: 16 GB (minimum: 8 GB)
- **Storage**: 50 GB SSD (minimum: 30 GB)
- **Network**: Stable internet connection

### Required Accounts
- Opinion Edge account (sign up at https://opinion-edge.com)
- Proxy service (optional but recommended)
- GitHub account (for CI/CD deployment)

---

## Method 1: One-Command Install (Recommended)

### Step 1: Clone Repository
```bash
git clone https://github.com/yourusername/survey-automation.git
cd survey-automation
```

### Step 2: Run Installer
```bash
chmod +x install.sh
./install.sh
```

The installer will:
1. ✅ Check system compatibility
2. ✅ Install all dependencies
3. ✅ Setup Ollama and download AI model
4. ✅ Create Python virtual environment
5. ✅ Configure systemd service
6. ✅ Setup Nginx reverse proxy
7. ✅ Run health checks
8. ✅ Start automation

### Step 3: Configure .env
During installation, you'll be prompted to edit `.env`:

```bash
# Required settings
OPINION_EDGE_EMAIL=your_email@example.com
OPINION_EDGE_PASSWORD=your_password

# Optional but recommended
PROXY_HOST=your_proxy_host.com
PROXY_PORT=10080
PROXY_USERNAME=your_username
PROXY_PASSWORD=your_password
```

### Step 4: Verify Installation
```bash
# Check service status
sudo systemctl status survey-automation

# View logs
tail -f logs/automation.log

# Access dashboard
# Open http://YOUR_SERVER_IP:5000 in browser
```

**Installation Time**: ~10 minutes  
**Difficulty**: Easy  
**Best For**: Production deployment

---

## Method 2: Docker Compose

### Step 1: Clone Repository
```bash
git clone https://github.com/yourusername/survey-automation.git
cd survey-automation
```

### Step 2: Configure Environment
```bash
cp .env.example .env
nano .env
```

Edit required settings:
```bash
OPINION_EDGE_EMAIL=your_email@example.com
OPINION_EDGE_PASSWORD=your_password
```

### Step 3: Start Services
```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f survey-automation

# Check status
docker-compose ps
```

### Step 4: Access Services
- **Dashboard**: http://localhost:5000
- **Grafana**: http://localhost:3000 (admin/admin)
- **Prometheus**: http://localhost:9090

### Management Commands
```bash
# Stop services
docker-compose down

# Restart services
docker-compose restart

# Update and restart
git pull
docker-compose up -d --build

# View logs
docker-compose logs -f

# Scale services
docker-compose up -d --scale survey-automation=3
```

**Installation Time**: ~5 minutes  
**Difficulty**: Medium  
**Best For**: Development, multi-service deployment

---

## Method 3: GitHub Deployment

### Step 1: Fork Repository
1. Go to https://github.com/yourusername/survey-automation
2. Click "Fork" button
3. Clone your fork

### Step 2: Configure Secrets
In your GitHub repository, go to Settings → Secrets and add:

```
DOCKERHUB_USERNAME=your_dockerhub_username
DOCKERHUB_TOKEN=your_dockerhub_token
DEPLOY_HOST=your_server_ip
DEPLOY_USER=your_ssh_username
DEPLOY_KEY=your_ssh_private_key
```

### Step 3: Setup Server
On your deployment server:

```bash
# Create deployment directory
sudo mkdir -p /opt/survey-automation
sudo chown $USER:$USER /opt/survey-automation

# Clone repository
cd /opt/survey-automation
git clone https://github.com/yourusername/survey-automation.git .

# Configure .env
cp .env.example .env
nano .env
```

### Step 4: Deploy
```bash
# Push to main branch
git add .
git commit -m "Deploy to production"
git push origin main
```

GitHub Actions will automatically:
1. ✅ Run tests
2. ✅ Build Docker image
3. ✅ Push to Docker Hub
4. ✅ Deploy to server
5. ✅ Restart service

### Step 5: Monitor Deployment
- Check GitHub Actions tab for deployment status
- View logs: `sudo journalctl -u survey-automation -f`

**Installation Time**: Automated  
**Difficulty**: Medium  
**Best For**: Continuous deployment, team collaboration

---

## Post-Deployment

### 1. Verify System Health
```bash
# Check health endpoint
curl http://localhost:5000/api/health

# Expected response:
{
  "overall_status": "healthy",
  "checks": {
    "environment": {"status": "ok"},
    "proxy": {"status": "ok"},
    "ollama": {"status": "ok"},
    "disk_space": {"status": "ok"},
    "memory": {"status": "ok"}
  }
}
```

### 2. Access Dashboard
Open browser and navigate to:
```
http://YOUR_SERVER_IP:5000
```

You should see:
- Live statistics
- Earnings tracker
- System resources
- Recent logs

### 3. Monitor First Survey
```bash
# Watch logs in real-time
tail -f logs/automation.log

# Look for:
# - "Login successful"
# - "Survey processing..."
# - "Survey completed successfully"
```

### 4. Check Earnings
```bash
# View earnings data
cat data/earnings.json | python -m json.tool

# Expected output:
{
  "total_earnings": 1.50,
  "surveys_completed": 1,
  "today_earnings": 1.50,
  ...
}
```

---

## Verification

### System Checks
```bash
# 1. Service status
sudo systemctl status survey-automation
# Should show: active (running)

# 2. Process check
ps aux | grep main.py
# Should show Python process

# 3. Port check
sudo netstat -tulpn | grep 5000
# Should show Flask listening on port 5000

# 4. Ollama check
ollama list
# Should show llama3.2-vision:latest

# 5. Chrome check
chromium-browser --version
# Should show version 120+
```

### Functional Tests
```bash
# 1. Health check
curl http://localhost:5000/api/health

# 2. Stats check
curl http://localhost:5000/api/stats

# 3. Metrics check
curl http://localhost:5000/api/metrics

# 4. Dashboard check
curl -I http://localhost:5000
# Should return 200 OK
```

### Performance Tests
```bash
# 1. CPU usage
top -bn1 | grep "Cpu(s)"
# Should be <50% on average

# 2. Memory usage
free -h
# Should have >2GB available

# 3. Disk space
df -h
# Should have >10GB free

# 4. Network connectivity
ping -c 4 opinion-edge.com
# Should have <100ms latency
```

---

## Troubleshooting

### Issue: Service won't start
```bash
# Check logs
sudo journalctl -u survey-automation -n 50

# Common fixes:
# 1. Check .env file exists
ls -la .env

# 2. Verify Python path
which python3

# 3. Check permissions
ls -la main.py
chmod +x main.py

# 4. Restart service
sudo systemctl restart survey-automation
```

### Issue: Dashboard not accessible
```bash
# Check if Flask is running
sudo netstat -tulpn | grep 5000

# Check firewall
sudo ufw status
sudo ufw allow 5000/tcp

# Check Nginx (if using)
sudo nginx -t
sudo systemctl restart nginx
```

### Issue: Ollama not working
```bash
# Check Ollama service
sudo systemctl status ollama

# Start Ollama
sudo systemctl start ollama

# Pull model
ollama pull llama3.2-vision:latest

# Test Ollama
curl http://localhost:11434/api/tags
```

### Issue: CAPTCHA solving fails
```bash
# Install audio dependencies
sudo apt-get install -y portaudio19-dev python3-pyaudio ffmpeg libsndfile1

# Reinstall Python packages
source venv/bin/activate
pip install --upgrade pyaudio pydub SpeechRecognition
```

---

## Maintenance

### Daily Tasks
```bash
# Check logs for errors
grep "ERROR" logs/automation.log | tail -20

# Check earnings
cat data/earnings.json | python -m json.tool

# Check system resources
htop
```

### Weekly Tasks
```bash
# Update system
sudo apt-get update && sudo apt-get upgrade

# Clean old logs
find logs/ -name "*.log.*" -mtime +7 -delete

# Clean old screenshots
find screenshots/ -name "*.png" -mtime +1 -delete

# Backup data
tar -czf backup_$(date +%Y%m%d).tar.gz data/
```

### Monthly Tasks
```bash
# Update Python packages
source venv/bin/activate
pip install --upgrade -r requirements.txt

# Review performance
cat data/stats.json | python -m json.tool

# Optimize settings
nano .env
```

---

## Scaling

### Adding More Accounts

1. **Create new directory**:
```bash
cp -r ~/survey-automation ~/survey-automation-account2
cd ~/survey-automation-account2
```

2. **Update configuration**:
```bash
nano .env
# Change: OPINION_EDGE_EMAIL, FLASK_PORT (5001)
```

3. **Create new service**:
```bash
sudo cp /etc/systemd/system/survey-automation.service \
        /etc/systemd/system/survey-automation-2.service

sudo nano /etc/systemd/system/survey-automation-2.service
# Update: WorkingDirectory, Description
```

4. **Start new service**:
```bash
sudo systemctl daemon-reload
sudo systemctl enable survey-automation-2
sudo systemctl start survey-automation-2
```

### Load Balancing

For multiple accounts, use Nginx load balancing:

```nginx
upstream survey_backend {
    server localhost:5000;
    server localhost:5001;
    server localhost:5002;
}

server {
    listen 80;
    location / {
        proxy_pass http://survey_backend;
    }
}
```

---

## Security Checklist

- [ ] .env file not committed to git
- [ ] Strong passwords used
- [ ] Firewall configured
- [ ] SSH key authentication enabled
- [ ] Fail2ban installed
- [ ] Regular backups enabled
- [ ] SSL/TLS configured (for production)
- [ ] Security updates enabled
- [ ] Monitoring alerts configured
- [ ] Access logs reviewed regularly

---

## Support

### Getting Help
1. Check logs: `tail -100 logs/automation.log`
2. Check health: `curl http://localhost:5000/api/health`
3. Read documentation: See `md/` folder
4. Open issue: GitHub Issues
5. Join Discord: Community support

### Useful Commands
```bash
# Service management
sudo systemctl start survey-automation
sudo systemctl stop survey-automation
sudo systemctl restart survey-automation
sudo systemctl status survey-automation

# Logs
tail -f logs/automation.log
sudo journalctl -u survey-automation -f

# Data
cat data/earnings.json | python -m json.tool
cat data/stats.json | python -m json.tool
cat data/error_log.json | python -m json.tool

# Health
curl http://localhost:5000/api/health
curl http://localhost:5000/api/stats
curl http://localhost:5000/api/metrics
```

---

## Success Criteria

Your deployment is successful when:
- ✅ Service is running (`systemctl status survey-automation`)
- ✅ Dashboard is accessible (http://YOUR_IP:5000)
- ✅ Health check passes (`/api/health`)
- ✅ First survey completes successfully
- ✅ Earnings are tracked (`data/earnings.json`)
- ✅ No critical errors in logs
- ✅ System resources are healthy (<50% CPU, <70% RAM)

---

## Next Steps

1. **Monitor for 24 hours** - Ensure stability
2. **Optimize settings** - Adjust delays, rate limits
3. **Add more accounts** - Scale gradually
4. **Setup alerts** - Get notified of issues
5. **Review earnings** - Track performance
6. **Join community** - Share experiences

---

**Congratulations! Your survey automation system is deployed and earning money!** 💰

For detailed guides, see:
- [README.md](README.md) - Complete documentation
- [START_HERE.md](md/START_HERE.md) - Getting started guide
- [TROUBLESHOOTING.md](md/TROUBLESHOOTING.md) - Common issues

**Happy earning!** 🎉
