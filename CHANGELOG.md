# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [3.1.0] - 2026-03-05

### Added
- 📖 `stepsforstarttoearn.md` — Complete DigitalOcean Ubuntu setup guide with all commands
- 💰 Earnings API endpoint (`/api/earnings`) on the monitoring dashboard
- 💰 Earnings card in dashboard UI (today/week/month/total/average)
- 📊 Success rate percentage displayed in dashboard statistics
- 🔐 HTTP Basic Auth for the dashboard (`DASHBOARD_USERNAME` / `DASHBOARD_PASSWORD`)
- 🔑 `FLASK_SECRET_KEY` env var with stable derived fallback (no more hardcoded secret)
- 🌐 `OPINION_EDGE_BASE_URL` setting (defaults to `https://panel.opinion-edge.com`)
- 🎨 Color-coded log entries in dashboard (green=success, red=error, yellow=warning)

### Fixed
- 🐛 **Critical**: Added missing `log_error(category, error_type, msg)` method to `ErrorTracker` — was called in 35+ places throughout the codebase but didn't exist, causing `AttributeError` crashes at runtime
- 🔧 Proxy configuration is now fully optional — no longer required, bot runs fine without proxy
- 📅 Fixed earnings period tracking — daily/weekly/monthly now use accurate ISO calendar keys instead of additive counters that never reset
- 🔄 Fixed `use_reloader=False` in dashboard to prevent double-initialization issues
- 📦 Removed `PyAudio` from required dependencies (build fails without system libs; it's optional)
- 🏗️ Moved inline imports to module top level (`json`, `os`, `datetime`, `hmac`, `hashlib`)
- 📅 Fixed ISO week number using `isocalendar()` instead of `%W` (year-boundary bug)
- 🔒 `ReadWritePaths` in systemd service now includes `.env` file

### Changed
- 🔀 `ProxyManager.validate_proxy()` now skips validation and returns `True` when no proxy configured
- 🔀 `BrowserAutomation` survey URLs now use `settings.opinion_edge_base_url` instead of hardcoded URLs
- 🔀 Cookie loading now uses configurable base URL
- ⚡ Systemd service updated with `StartLimitInterval`, `StartLimitBurst`, separate `error.log`
- 📝 `README.md` updated — `yourusername` replaced with `SomratChandraRoy`, new guide linked

## [3.0.0] - 2026-02-15

### Added
- 🚀 One-command installation script (`install.sh`)
- 🐳 Docker and Docker Compose support
- 🔧 GitHub Actions CI/CD pipeline
- 📊 Prometheus metrics endpoint
- 📈 Grafana dashboard integration
- 🌐 Nginx reverse proxy configuration
- 🧪 Automated testing framework
- 🔐 Security scanning (Trivy, TruffleHog)
- 📦 Multi-stage Docker builds
- ⚙️ Systemd service with security hardening
- 🔍 Comprehensive health checks
- 📝 Enhanced logging and monitoring
- 🛡️ Rate limiting and DDoS protection
- 🔄 Automatic recovery mechanisms
- 📚 Comprehensive documentation (50KB+)

### Changed
- ♻️ Refactored dashboard with Prometheus metrics
- 🎨 Improved code organization and modularity
- 📊 Enhanced error tracking and reporting
- ⚡ Optimized performance and resource usage
- 🔒 Strengthened security measures

### Fixed
- 🐛 Fixed health check method mismatch
- 🐛 Fixed error report method missing
- 🐛 Fixed health status key inconsistency
- 🐛 Resolved all diagnostic warnings

## [2.0.0] - 2026-02-10

### Added
- 💰 Earnings tracking system
- 📊 Performance metrics
- 🔄 Session persistence (90% faster logins)
- ⏱️ Rate limiting (2-3 min between surveys)
- 📅 Daily limit enforcement (max 20/day)
- 🍪 Cookie age validation (7 days)
- 📈 Success rate tracking
- ⚠️ Comprehensive error handling
- 🔍 Error tracking by category
- 🏥 Health check system

### Changed
- 🎯 Improved human behavior simulation
- 🤖 Enhanced AI decision making
- 🔐 Better proxy management
- 📝 Improved logging

## [1.0.0] - 2026-02-05

### Added
- 🤖 Initial release
- 🎭 Basic automation
- 🧩 CAPTCHA solving
- 📊 Dashboard
- 🔒 Proxy support
- 🤖 AI integration

---

[3.0.0]: https://github.com/yourusername/survey-automation/compare/v2.0.0...v3.0.0
[2.0.0]: https://github.com/yourusername/survey-automation/compare/v1.0.0...v2.0.0
[1.0.0]: https://github.com/yourusername/survey-automation/releases/tag/v1.0.0
