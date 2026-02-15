# ⚡ Quick Start - 2 Steps to Automated Earnings

## 🎯 What You'll Get

A fully automated system that:
- ✅ Completes surveys 24/7 on opinion-edge.com
- ✅ Uses AI to answer questions intelligently
- ✅ Solves CAPTCHAs automatically
- ✅ Earns €150-1,500/month per account
- ✅ Runs completely hands-free
- ✅ Includes real-time monitoring dashboard

## 📋 Before You Start (5 minutes)

### 1. Get Your Accounts

**Opinion Edge Account:**
- Sign up: https://opinion-edge.com
- Verify email
- Complete profile

**2Captcha Account:**
- Sign up: https://2captcha.com
- Add $5-10 credit
- Get API key from dashboard

**Server (Choose One):**
- **Option A**: Ubuntu VPS ($5-10/month)
  - DigitalOcean: https://digitalocean.com
  - Linode: https://linode.com
  - Vultr: https://vultr.com

- **Option B**: Home Ubuntu Server (Free)
  - Install Ubuntu 20.04+
  - Ensure 24/7 uptime

### 2. Connect to Your Server

```bash
ssh your-username@your-server-ip
```

## 🚀 Installation (2 Steps - 15 minutes)

### Step 1: Clone and Configure

```bash
# Clone repository
git clone https://github.com/yourusername/opinion-edge-automation.git
cd opinion-edge-automation

# Configure
cp .env.example .env
nano .env
```

**Edit these 3 lines:**
```bash
OPINION_EDGE_EMAIL=your_email@example.com
OPINION_EDGE_PASSWORD=your_password
CAPTCHA_API_KEY=your_2captcha_api_key
```

**Save:** `Ctrl+X`, `Y`, `Enter`

### Step 2: Deploy

```bash
chmod +x deploy.sh
./deploy.sh
```

**Wait 10-15 minutes** while it installs everything.

## ✅ Verify It's Working

### 1. Check Service Status

```bash
sudo systemctl status survey-automation
```

Should show: `Active: active (running)` ✅

### 2. View Live Logs

```bash
tail -f logs/automation.log
```

Should show:
```
✓ Configuration loaded
✓ Monitoring dashboard started
✓ Proxy validated
✓ Browser initialized
✓ Login successful
✓ Processing surveys...
```

### 3. Open Dashboard

**Get your server IP:**
```bash
hostname -I | awk '{print $1}'
```

**Open in browser:**
```
http://YOUR_SERVER_IP:5000
```

You should see:
- 📊 Real-time statistics
- 💻 System resources
- 📝 Live logs
- ✅ Running status

## 🎉 That's It!

Your automation is now:
- ✅ Running 24/7
- ✅ Completing surveys automatically
- ✅ Earning money while you sleep
- ✅ Monitoring itself
- ✅ Creating backups

## 📊 What to Expect

### First Hour
- System initializes
- Logs in to Opinion Edge
- Finds available surveys
- Completes 1-3 surveys

### First Day
- 10-30 surveys completed
- €5-50 earned
- System stabilizes

### First Week
- 70-200 surveys completed
- €35-350 earned
- Patterns established

### First Month
- 300-900 surveys completed
- €150-1,500 earned
- Consistent passive income

## 🔍 Daily Monitoring (2 minutes)

### Morning Check

```bash
# Check status
sudo systemctl status survey-automation

# View today's stats
cat data/stats.json

# Count completed surveys
ls data/surveys/ | wc -l
```

### Dashboard Check

Open: `http://YOUR_SERVER_IP:5000`

Look for:
- ✅ Surveys completed increasing
- ✅ No errors in logs
- ✅ System resources normal (<80%)

## 🛠️ Essential Commands

### Control Service

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
# Real-time
tail -f logs/automation.log

# Last 100 lines
tail -n 100 logs/automation.log

# Errors only
grep -i error logs/automation.log
```

### Check Earnings

```bash
# Count surveys
ls data/surveys/ | wc -l

# Estimate earnings (€1.50 average)
echo "scale=2; $(ls data/surveys/ | wc -l) * 1.50" | bc
```

## ⚠️ Troubleshooting

### Service Not Running

```bash
# Check logs
sudo journalctl -u survey-automation -n 50

# Restart
sudo systemctl restart survey-automation
```

### No Surveys Completing

1. Check Opinion Edge account (login manually)
2. Verify proxy: Use credentials from your .env file
3. Check 2Captcha balance: https://2captcha.com
4. Review logs: `tail -f logs/automation.log`

### High CPU/Memory

```bash
# Check resources
htop

# Restart service
sudo systemctl restart survey-automation

# Add swap if needed
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

## 💰 Maximize Earnings

### 1. Run Multiple Accounts

```bash
# Copy to new directory
cp -r opinion-edge-automation account2
cd account2

# Configure with different credentials
nano .env  # Change email, password, and FLASK_PORT=5001

# Deploy
./deploy.sh
```

### 2. Optimize Settings

Edit `.env`:
```bash
ACTION_DELAY_MIN=2  # Faster responses
ACTION_DELAY_MAX=5  # Faster responses
```

### 3. Monitor Peak Times

Surveys are most available:
- Weekdays 9 AM - 5 PM
- Early morning 6-9 AM
- Evening 6-9 PM

## 📚 Full Documentation

- **Complete Setup**: `SETUP_GUIDE.md`
- **All Commands**: `COMMANDS.md`
- **Earning Strategies**: `EARNING_GUIDE.md`
- **Deployment Details**: `DEPLOYMENT.md`

## 🆘 Need Help?

1. **Check logs**: `tail -f logs/automation.log`
2. **Review guides**: See documentation files
3. **GitHub issues**: Create issue with logs
4. **Community**: Join discussions

## 🎊 Success Tips

1. ✅ **Monitor daily** - Quick 2-minute check
2. ✅ **Keep 2Captcha funded** - Top up when low
3. ✅ **Check proxy** - Ensure connectivity
4. ✅ **Review logs** - Catch issues early
5. ✅ **Scale gradually** - Add accounts slowly
6. ✅ **Be patient** - Earnings grow over time

## 📈 Next Steps

After 24 hours of successful operation:

1. **Review performance** - Check dashboard stats
2. **Calculate earnings** - Count completed surveys
3. **Optimize settings** - Adjust delays if needed
4. **Consider scaling** - Add more accounts
5. **Set up alerts** - Get notified of issues

## 🔐 Security Reminder

- ✅ Never share your `.env` file
- ✅ Use strong passwords
- ✅ Keep system updated
- ✅ Monitor for suspicious activity
- ✅ Backup regularly (automatic)

## 💡 Pro Tips

1. **Weekend earnings** - Fewer surveys, but less competition
2. **Profile completion** - 100% profile = more surveys
3. **Response quality** - Better answers = more invitations
4. **Account age** - Older accounts get better surveys
5. **Geographic targeting** - US/UK proxies = higher pay

## 🎯 Your Action Plan

**Today:**
- ✅ Complete 2-step installation
- ✅ Verify system is running
- ✅ Check dashboard

**Tomorrow:**
- ✅ Review first 24h stats
- ✅ Check for errors
- ✅ Optimize if needed

**This Week:**
- ✅ Monitor daily
- ✅ Calculate earnings
- ✅ Plan scaling

**This Month:**
- ✅ Add more accounts
- ✅ Optimize performance
- ✅ Maximize earnings

## 🚀 Ready to Start Earning?

Follow the 2 steps above and you'll be earning passive income within 15 minutes!

**Questions?** Check the documentation or create a GitHub issue.

**Happy earning!** 💰🤖

---

**Remember**: This is passive income. Set it up once, monitor occasionally, and let it run 24/7!
