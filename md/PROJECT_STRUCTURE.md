# Project Structure

## 📁 Directory Layout

```
opinion-edge-automation/
├── 📄 main.py                      # Main entry point
├── 📄 deploy.sh                    # One-command deployment script
├── 📄 run_local.sh                 # Local testing script
├── 📄 stop.sh                      # Stop automation script
├── 📄 requirements.txt             # Python dependencies
├── 📄 .env.example                 # Environment template
├── 📄 .env                         # Your configuration (not in git)
├── 📄 .gitignore                   # Git ignore rules
├── 📄 LICENSE                      # MIT License
│
├── 📚 Documentation/
│   ├── README.md                   # Project overview
│   ├── QUICK_START.md              # 2-step quick start
│   ├── SETUP_GUIDE.md              # Detailed setup guide
│   ├── DEPLOYMENT.md               # Deployment instructions
│   ├── COMMANDS.md                 # All commands reference
│   ├── EARNING_GUIDE.md            # Earning strategies
│   └── PROJECT_STRUCTURE.md        # This file
│
├── 📦 src/                         # Source code
│   ├── __init__.py
│   │
│   ├── 🤖 automation/              # Browser automation
│   │   ├── __init__.py
│   │   ├── browser.py              # Main browser controller
│   │   ├── survey_handler.py      # Survey question handling
│   │   └── stealth.py              # Anti-detection measures
│   │
│   ├── 🧠 ai/                      # AI integration
│   │   ├── __init__.py
│   │   └── ollama_client.py        # Ollama AI client
│   │
│   ├── 🔐 proxy/                   # Proxy management
│   │   ├── __init__.py
│   │   └── manager.py              # Proxy validation & config
│   │
│   ├── 🧩 captcha/                 # CAPTCHA solving
│   │   ├── __init__.py
│   │   └── solver.py               # 2Captcha integration
│   │
│   ├── ⚙️ config/                  # Configuration
│   │   ├── __init__.py
│   │   └── settings.py             # Settings management
│   │
│   ├── 📊 monitoring/              # Monitoring & logging
│   │   ├── __init__.py
│   │   ├── dashboard.py            # Web dashboard
│   │   └── logger.py               # Logging configuration
│   │
│   └── 🛠️ utils/                   # Utilities
│       ├── __init__.py
│       ├── cleanup.py              # File cleanup manager
│       └── backup.py               # Backup manager
│
├── 🎨 templates/                   # Web templates
│   └── dashboard.html              # Dashboard UI
│
├── 📝 logs/                        # Log files
│   ├── automation.log              # Current log
│   └── automation.log.*            # Rotated logs
│
├── 📸 screenshots/                 # Temporary screenshots
│   └── *.png                       # Auto-deleted every 20 min
│
├── 💾 data/                        # Data storage
│   ├── cookies/                    # Session cookies
│   │   └── session.json
│   ├── surveys/                    # Survey results
│   │   └── survey_*.json
│   ├── backups/                    # Automatic backups
│   │   └── backup_*.tar.gz
│   └── stats.json                  # Statistics
│
└── 🔧 .github/                     # GitHub configuration
    └── workflows/
        └── deploy.yml              # CI/CD workflow
```

## 📄 File Descriptions

### Core Files

**main.py**
- Entry point for the application
- Initializes all components
- Manages main automation loop
- Handles graceful shutdown

**deploy.sh**
- One-command deployment script
- Installs all dependencies
- Configures systemd service
- Starts automation

**requirements.txt**
- Python package dependencies
- Pinned versions for stability

**.env.example**
- Template for configuration
- Shows all available settings
- Safe to commit to git

**.env**
- Your actual configuration
- Contains credentials
- Never committed to git

### Source Code Modules

#### automation/

**browser.py**
- Main browser automation controller
- Handles login workflow
- Manages survey navigation
- Coordinates AI and CAPTCHA solving
- Implements human-like behavior

**survey_handler.py**
- Processes individual surveys
- Extracts questions
- Generates answers using AI
- Submits responses
- Tracks completion

**stealth.py**
- Anti-detection measures
- Removes webdriver properties
- Spoofs browser fingerprint
- Disables WebRTC
- Sets geolocation

#### ai/

**ollama_client.py**
- Ollama AI integration
- Vision-based screenshot analysis
- Question answering
- CAPTCHA detection
- Persona-based responses

#### proxy/

**manager.py**
- Proxy configuration
- Connection validation
- Kill-switch implementation
- DNS leak prevention
- Speed testing

#### captcha/

**solver.py**
- 2Captcha integration
- reCAPTCHA v2/v3 solving
- hCaptcha support
- Image CAPTCHA solving
- Solution injection

#### config/

**settings.py**
- Pydantic-based configuration
- Environment variable loading
- Type validation
- Default values
- Path management

#### monitoring/

**dashboard.py**
- Flask web server
- Real-time statistics
- System resource monitoring
- Log streaming
- REST API endpoints

**logger.py**
- Loguru configuration
- Log rotation
- Console and file output
- Colored formatting

#### utils/

**cleanup.py**
- Screenshot cleanup (every 20 min)
- Old log removal
- Disk space management

**backup.py**
- Hourly automatic backups
- Cloud upload support (S3/GDrive)
- Retention management
- Compression

### Templates

**dashboard.html**
- Responsive web dashboard
- Real-time updates
- Statistics display
- System monitoring
- Log viewer

### Data Directories

**logs/**
- Application logs
- Rotated automatically
- Max 10MB per file
- Keep last 5 files

**screenshots/**
- Temporary AI analysis images
- Auto-deleted every 20 minutes
- Not backed up

**data/cookies/**
- Session cookies
- Reused for faster login
- Backed up hourly

**data/surveys/**
- Completed survey records
- JSON format
- Backed up hourly
- Used for statistics

**data/backups/**
- Automatic backups
- Created every hour
- Compressed tar.gz
- 30-day retention

## 🔄 Data Flow

```
1. main.py starts
   ↓
2. Load settings from .env
   ↓
3. Start monitoring dashboard (Flask)
   ↓
4. Start cleanup manager (background)
   ↓
5. Start backup manager (background)
   ↓
6. Initialize browser automation
   ↓
7. Validate proxy (kill-switch)
   ↓
8. Launch browser with stealth
   ↓
9. Login to Opinion Edge
   ├─→ Take screenshot
   ├─→ AI analyzes page
   ├─→ Detect CAPTCHA
   ├─→ Solve if present
   └─→ Enter credentials
   ↓
10. Navigate to surveys
    ↓
11. Find survey links
    ↓
12. For each survey:
    ├─→ Click survey link
    ├─→ For each question:
    │   ├─→ Take screenshot
    │   ├─→ Extract question text
    │   ├─→ Check knowledge base
    │   ├─→ Or ask AI for answer
    │   ├─→ Submit answer
    │   └─→ Handle CAPTCHA if needed
    ├─→ Check completion
    └─→ Save result
    ↓
13. Return to survey list
    ↓
14. Repeat from step 11
```

## 🔌 Component Interactions

```
┌─────────────┐
│   main.py   │
└──────┬──────┘
       │
       ├─→ ┌──────────────────┐
       │   │ MonitoringDashboard│
       │   └──────────────────┘
       │
       ├─→ ┌──────────────────┐
       │   │ CleanupManager   │
       │   └──────────────────┘
       │
       ├─→ ┌──────────────────┐
       │   │ BackupManager    │
       │   └──────────────────┘
       │
       └─→ ┌──────────────────┐
           │BrowserAutomation │
           └────────┬─────────┘
                    │
                    ├─→ ┌──────────────┐
                    │   │ProxyManager  │
                    │   └──────────────┘
                    │
                    ├─→ ┌──────────────┐
                    │   │OllamaClient  │
                    │   └──────────────┘
                    │
                    ├─→ ┌──────────────┐
                    │   │CaptchaSolver │
                    │   └──────────────┘
                    │
                    ├─→ ┌──────────────┐
                    │   │StealthBrowser│
                    │   └──────────────┘
                    │
                    └─→ ┌──────────────┐
                        │SurveyHandler │
                        └──────────────┘
```

## 🚀 Execution Flow

### Startup Sequence

1. **Load Configuration** (1 second)
   - Read .env file
   - Validate settings
   - Create directories

2. **Start Background Services** (2 seconds)
   - Launch Flask dashboard
   - Start cleanup manager
   - Start backup manager

3. **Initialize Browser** (10 seconds)
   - Validate proxy
   - Launch Chrome
   - Apply stealth
   - Load cookies

4. **Login** (30-60 seconds)
   - Navigate to site
   - AI finds login button
   - Solve CAPTCHA if present
   - Enter credentials
   - Save session

5. **Main Loop** (Continuous)
   - Find surveys
   - Process surveys
   - Handle errors
   - Retry on failure
   - Sleep between cycles

### Survey Processing

1. **Find Surveys** (5 seconds)
   - Navigate to survey page
   - Extract survey links
   - Prioritize by value

2. **Process Survey** (2-5 minutes)
   - Click survey link
   - Wait for load
   - Loop through questions
   - Submit answers
   - Check completion

3. **Handle Question** (10-30 seconds)
   - Take screenshot
   - Extract text
   - Check knowledge base
   - Or ask AI
   - Submit answer

4. **Save Result** (1 second)
   - Record completion
   - Update statistics
   - Log details

## 📊 Monitoring Points

### Application Metrics

- Surveys completed
- Surveys failed
- CAPTCHAs solved
- Average time per survey
- Success rate
- Uptime

### System Metrics

- CPU usage
- Memory usage
- Disk usage
- Network bandwidth
- Process count

### Business Metrics

- Estimated earnings
- Surveys per hour
- Surveys per day
- Monthly projection
- ROI calculation

## 🔧 Configuration Options

### Environment Variables

See `.env.example` for all options:

**Required:**
- OPINION_EDGE_EMAIL
- OPINION_EDGE_PASSWORD
- CAPTCHA_API_KEY

**Optional:**
- Proxy settings
- Persona details
- Timing parameters
- Backup configuration
- Monitoring settings

### Runtime Configuration

Modify behavior by editing:
- `src/automation/browser.py` - Survey limits
- `src/automation/survey_handler.py` - Answer logic
- `src/config/settings.py` - Default values

## 🛠️ Maintenance Tasks

### Daily
- Check dashboard
- Review logs
- Verify surveys completing

### Weekly
- Check 2Captcha balance
- Review error patterns
- Update if needed

### Monthly
- Calculate earnings
- Optimize settings
- Plan scaling

## 📈 Scaling Architecture

### Single Account
```
Server → Browser → Opinion Edge
```

### Multiple Accounts
```
Server → Browser 1 → Opinion Edge (Account 1)
      → Browser 2 → Opinion Edge (Account 2)
      → Browser 3 → Opinion Edge (Account 3)
```

### Distributed
```
Server 1 → Browsers → Opinion Edge (Accounts 1-5)
Server 2 → Browsers → Opinion Edge (Accounts 6-10)
Server 3 → Browsers → Opinion Edge (Accounts 11-15)
```

## 🔐 Security Layers

1. **Environment Variables** - Credentials in .env
2. **Proxy** - Hide real IP
3. **Stealth** - Avoid detection
4. **Rate Limiting** - Human-like speed
5. **Session Management** - Cookie reuse
6. **Error Handling** - Graceful failures

## 📝 Logging Levels

- **DEBUG** - Detailed execution info
- **INFO** - Normal operations
- **WARNING** - Potential issues
- **ERROR** - Failures requiring attention
- **CRITICAL** - System failures

## 🎯 Success Indicators

✅ Service running
✅ No errors in logs
✅ Surveys completing
✅ Dashboard accessible
✅ Backups creating
✅ Resources normal

## 🚨 Failure Indicators

❌ Service stopped
❌ Repeated errors
❌ No surveys completing
❌ High resource usage
❌ Proxy failures
❌ CAPTCHA failures

## 📚 Further Reading

- **README.md** - Project overview
- **QUICK_START.md** - Fast setup
- **SETUP_GUIDE.md** - Detailed setup
- **COMMANDS.md** - Command reference
- **EARNING_GUIDE.md** - Earning strategies
- **DEPLOYMENT.md** - Deployment details

---

**This structure is designed for:**
- Easy understanding
- Simple maintenance
- Reliable operation
- Scalable growth
- Secure execution
