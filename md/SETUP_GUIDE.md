# Complete Setup Guide - Step by Step

## 🎯 Goal
Deploy a fully automated survey completion system on your Ubuntu server in just 2 steps.

## 📋 Prerequisites Checklist

Before starting, ensure you have:

- [ ] Ubuntu 20.04+ server (VPS or dedicated)
- [ ] Root or sudo access
- [ ] At least 2GB RAM
- [ ] At least 10GB free disk space
- [ ] Internet connection
- [ ] Opinion Edge account
- [ ] 2Captcha account (sign up at https://2captcha.com)
- [ ] GitHub account (for code hosting)

## 🚀 Quick Start (2 Steps)

### Step 1: Clone and Configure (5 minutes)

```bash
# Clone the repository
git clone https://github.com/yourusername/opinion-edge-automation.git
cd opinion-edge-automation

# Copy environment template
cp .env.example .env

# Edit configuration file
nano .env
```

**Required Configuration in `.env`:**

```bash
# Your Opinion Edge login credentials
OPINION_EDGE_EMAIL=your_email@example.com
OPINION_EDGE_PASSWORD=your_password_here

# Your 2Captcha API key (get from https://2captcha.com/enterpage)
CAPTCHA_API_KEY=your_2captcha_api_key_here

# Proxy is pre-configured, but you can change if needed
PROXY_HOST=your_proxy_host.com
PROXY_PORT=10080
PROXY_USERNAME=your_proxy_username
PROXY_PASSWORD=your_proxy_password
```

**Save and exit**: Press `Ctrl+X`, then `Y`, then `Enter`

### Step 2: Deploy (10-15 minutes)

```bash
# Make deployment script executable
chmod +x deploy.sh

# Run deployment
./deploy.sh
```

**That's it!** The script will automatically:
1. ✅ Update system packages
2. ✅ Install Python and dependencies
3. ✅ Install and configure Ollama AI
4. ✅ Download AI vision model
5. ✅ Create virtual environment
6. ✅ Install Python packages
7. ✅ Create systemd service
8. ✅ Start automation

## 🎉 Verification

### Check if Service is Running

```bash
sudo systemctl status survey-automation
```

You should see: `Active: active (running)`

### View Live Logs

```bash
tail -f logs/automation.log
```

You should see:
```
Opinion Edge Survey Automation Starting
Configuration loaded successfully
Monitoring dashboard started on port 5000
Browser automation initialized
```

### Access Dashboard

Open your web browser and go to:
```
http://your-server-ip:5000
```

Replace `your-server-ip` with your actual server IP address.

**To find your server IP:**
```bash
hostname -I | awk '{print $1}'
```

## 📊 What Happens Next?

The automation will:

1. **Validate Proxy** (30 seconds)
   - Check proxy connectivity
   - Verify no IP leaks
   - Test speed

2. **Initialize Browser** (1 minute)
   - Launch Chrome with stealth mode
   - Apply anti-detection measures
   - Configure proxy

3. **Login to Opinion Edge** (1-2 minutes)
   - Navigate to website
   - Use AI to find login button
   - Solve any CAPTCHAs
   - Enter credentials
   - Save session cookies

4. **Navigate to Surveys** (30 seconds)
   - Go to survey page
   - Wait for full page load

5. **Process Surveys** (Continuous)
   - Find available surveys
   - Click survey links
   - Answer questions using AI
   - Handle CAPTCHAs automatically
   - Submit responses
   - Move to next survey

## 🔍 Monitoring

### Real-Time Dashboard

Access: `http://your-server-ip:5000`

Shows:
- 📊 Surveys completed
- ❌ Surveys failed
- 🧩 CAPTCHAs solved
- 💻 CPU/Memory/Disk usage
- 📝 Live logs

### Command Line Monitoring

```bash
# View logs in real-time
tail -f logs/automation.log

# Check service status
sudo systemctl status survey-automation

# View system logs
sudo journalctl -u survey-automation -f
```

## 🛠️ Common Commands

### Start/Stop/Restart

```bash
# Start
sudo systemctl start survey-automation

# Stop
sudo systemctl stop survey-automation

# Restart
sudo systemctl restart survey-automation

# Status
sudo systemctl status survey-automation
```

### View Logs

```bash
# Real-time logs
tail -f logs/automation.log

# Last 100 lines
tail -n 100 logs/automation.log

# Search for errors
grep -i error logs/automation.log
```

### Check Statistics

```bash
# View stats file
cat data/stats.json

# Count completed surveys
ls data/surveys/ | wc -l

# View survey results
cat data/surveys/survey_*.json | head -20
```

## 🔧 Troubleshooting

### Issue: Service Won't Start

**Check logs:**
```bash
sudo journalctl -u survey-automation -n 50
```

**Common causes:**
1. Missing `.env` file
2. Invalid credentials
3. Ollama not running

**Solution:**
```bash
# Check Ollama
sudo systemctl status ollama
sudo systemctl start ollama

# Verify .env exists
ls -la .env

# Restart service
sudo systemctl restart survey-automation
```

### Issue: Proxy Connection Failed

**Test proxy manually:**
```bash
# Use your credentials from .env file
curl -x http://YOUR_PROXY_USERNAME:YOUR_PROXY_PASSWORD@YOUR_PROXY_HOST:YOUR_PROXY_PORT https://api.ipify.org
```

**Should return an IP address.**

**If fails:**
1. Check proxy credentials in `.env`
2. Verify internet connection
3. Try different proxy

### Issue: CAPTCHA Solving Fails

**Check 2Captcha balance:**
```bash
curl "https://2captcha.com/res.php?key=YOUR_API_KEY&action=getbalance"
```

**Should return your balance.**

**If fails:**
1. Verify API key in `.env`
2. Top up balance at https://2captcha.com
3. Check 2Captcha service status

### Issue: Browser Won't Launch

**Install Chrome dependencies:**
```bash
sudo apt-get install -y libnss3 libgconf-2-4 libxss1 libasound2 libxtst6 libgtk-3-0
```

**Verify Chrome:**
```bash
chromium-browser --version
```

### Issue: Out of Memory

**Check memory:**
```bash
free -h
```

**Add swap space:**
```bash
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
```

## 📈 Optimization Tips

### 1. Increase Survey Processing

Edit `src/automation/browser.py`:
```python
max_surveys = 20  # Change from 10 to 20
```

Restart:
```bash
sudo systemctl restart survey-automation
```

### 2. Adjust Delays

Edit `.env`:
```bash
ACTION_DELAY_MIN=2  # Faster (default: 3)
ACTION_DELAY_MAX=5  # Faster (default: 8)
```

### 3. More Frequent Cleanup

Edit `.env`:
```bash
SCREENSHOT_CLEANUP_INTERVAL=600  # 10 minutes (default: 1200)
```

### 4. Enable Auto-Restart on Boot

```bash
sudo systemctl enable survey-automation
```

## 🔐 Security Best Practices

1. **Protect `.env` file:**
```bash
chmod 600 .env
```

2. **Never commit `.env` to Git:**
```bash
# Already in .gitignore
git status  # Should not show .env
```

3. **Use strong passwords**

4. **Keep system updated:**
```bash
sudo apt-get update && sudo apt-get upgrade
```

5. **Monitor logs for suspicious activity**

## 📦 Backup and Recovery

### Automatic Backups

Backups run every hour automatically.

Location: `data/backups/`

### Manual Backup

```bash
tar -czf backup_$(date +%Y%m%d).tar.gz data/ logs/ .env
```

### Restore from Backup

```bash
tar -xzf backup_YYYYMMDD.tar.gz
sudo systemctl restart survey-automation
```

## 🌐 GitHub Setup

### 1. Create Repository

Go to GitHub and create a new repository: `opinion-edge-automation`

### 2. Push Code

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/yourusername/opinion-edge-automation.git
git push -u origin main
```

### 3. Keep `.env` Private

The `.gitignore` file already excludes `.env`, so your credentials won't be uploaded.

## 🎓 Next Steps

1. **Monitor for 24 hours** - Ensure everything runs smoothly
2. **Check earnings** - View completed surveys in dashboard
3. **Optimize settings** - Adjust delays and limits
4. **Scale up** - Consider multiple accounts (see EARNING_GUIDE.md)
5. **Set up alerts** - Get notified of issues

## 📚 Additional Resources

- **Full Commands**: See `COMMANDS.md`
- **Earning Strategies**: See `EARNING_GUIDE.md`
- **Deployment Details**: See `DEPLOYMENT.md`
- **Troubleshooting**: See logs and GitHub issues

## 💡 Tips for Success

1. **Start small** - Run one account first
2. **Monitor daily** - Check logs and dashboard
3. **Keep balance** - Maintain 2Captcha credits
4. **Be patient** - Earnings grow over time
5. **Stay updated** - Pull latest code regularly

## 🆘 Getting Help

If you encounter issues:

1. **Check logs first:**
```bash
tail -f logs/automation.log
```

2. **Review this guide**

3. **Search GitHub issues**

4. **Create new issue** with:
   - Error message
   - Log excerpt
   - System info
   - Steps to reproduce

## ✅ Success Checklist

After setup, verify:

- [ ] Service is running: `sudo systemctl status survey-automation`
- [ ] Dashboard accessible: `http://your-server-ip:5000`
- [ ] Logs show activity: `tail -f logs/automation.log`
- [ ] No errors in logs
- [ ] Proxy validated successfully
- [ ] Browser initialized
- [ ] Login successful
- [ ] Surveys being processed

## 🎊 Congratulations!

Your automated survey system is now running! 

The system will:
- ✅ Run 24/7 automatically
- ✅ Complete surveys with AI
- ✅ Solve CAPTCHAs automatically
- ✅ Handle errors and retry
- ✅ Clean up files automatically
- ✅ Create backups hourly
- ✅ Provide real-time monitoring

**Sit back and watch the earnings grow!** 💰

---

**Questions?** Check the documentation or create a GitHub issue.

**Happy automating!** 🤖
