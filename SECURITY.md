# 🔒 Security Guide

## ⚠️ IMPORTANT: Secret Management

**NEVER commit sensitive credentials to Git!**

This project uses environment variables to keep your credentials secure.

## 🔐 Securing Your Credentials

### 1. Use .env File (Already Configured)

All sensitive data should be in `.env` file:

```bash
# Opinion Edge Credentials
OPINION_EDGE_EMAIL=your_email@example.com
OPINION_EDGE_PASSWORD=your_password

# Proxy Credentials (Get from your proxy provider)
PROXY_HOST=your_proxy_host.com
PROXY_PORT=10080
PROXY_USERNAME=your_proxy_username
PROXY_PASSWORD=your_proxy_password

# 2Captcha API Key
CAPTCHA_API_KEY=your_2captcha_api_key
```

### 2. .env File is Protected

The `.gitignore` file already excludes `.env`:

```
.env
venv/
*.pyc
__pycache__/
```

### 3. Never Hardcode Credentials

❌ **WRONG:**
```python
proxy_url = "http://username:password@proxy.com:10080"
```

✅ **CORRECT:**
```python
from src.config.settings import Settings
settings = Settings()
proxy_url = settings.proxy_url  # Loaded from .env
```

## 🚨 If You Accidentally Exposed Secrets

### Immediate Actions:

1. **Revoke the exposed credentials immediately**
   - Change your Opinion Edge password
   - Get new proxy credentials from your provider
   - Generate new 2Captcha API key

2. **Remove from Git history**
   ```bash
   # Install BFG Repo-Cleaner
   brew install bfg  # macOS
   # or download from: https://rtyley.github.io/bfg-repo-cleaner/
   
   # Remove secrets from history
   bfg --replace-text passwords.txt
   
   # Force push (WARNING: This rewrites history)
   git push --force
   ```

3. **Update your .env file with new credentials**

4. **Verify .gitignore is working**
   ```bash
   git status
   # .env should NOT appear in the list
   ```

## 🔍 Checking for Exposed Secrets

### Before Committing:

```bash
# Check what will be committed
git status

# Verify .env is not tracked
git ls-files | grep .env
# Should return nothing

# Check for hardcoded credentials
grep -r "password" --include="*.py" --include="*.sh" src/
```

### Using GitGuardian (Recommended):

1. Install GitGuardian CLI:
   ```bash
   pip install ggshield
   ```

2. Scan before commit:
   ```bash
   ggshield secret scan path .
   ```

3. Setup pre-commit hook:
   ```bash
   ggshield install -m local
   ```

## 📋 Security Checklist

- [ ] `.env` file exists and contains all credentials
- [ ] `.env` is in `.gitignore`
- [ ] No hardcoded credentials in source code
- [ ] `.env.example` contains only placeholders
- [ ] Documentation uses placeholders, not real credentials
- [ ] Git history doesn't contain secrets
- [ ] GitGuardian or similar tool is configured

## 🛡️ Best Practices

### 1. Use Strong Passwords
- Minimum 16 characters
- Mix of uppercase, lowercase, numbers, symbols
- Use a password manager

### 2. Rotate Credentials Regularly
- Change passwords every 90 days
- Rotate API keys every 6 months
- Update proxy credentials if compromised

### 3. Limit Access
- Don't share your `.env` file
- Use separate credentials for each account
- Don't commit `.env` to version control

### 4. Monitor for Breaches
- Enable GitGuardian alerts
- Check haveibeenpwned.com
- Monitor your accounts for suspicious activity

### 5. Use Environment-Specific Credentials
- Development: Use test credentials
- Production: Use production credentials
- Never mix them

## 🔧 Proxy Security

### Getting Secure Proxy Credentials

1. **Use Reputable Providers:**
   - Bright Data (formerly Luminati)
   - Smartproxy
   - Oxylabs
   - IPRoyal

2. **Proxy Types:**
   - Residential proxies (best for surveys)
   - Datacenter proxies (cheaper, higher risk)
   - Mobile proxies (most expensive, lowest risk)

3. **Security Features:**
   - IP whitelisting
   - Username/password authentication
   - Session management
   - Automatic rotation

### Proxy Configuration Example

```bash
# In .env file
PROXY_HOST=proxy.provider.com
PROXY_PORT=10080
PROXY_USERNAME=user_abc123
PROXY_PASSWORD=pass_xyz789
```

## 🚨 What to Do If Credentials Are Leaked

### 1. Immediate Response (Within 1 hour)

```bash
# 1. Revoke all exposed credentials
# - Change Opinion Edge password
# - Get new proxy credentials
# - Generate new 2Captcha API key

# 2. Update .env file
nano .env  # Add new credentials

# 3. Remove from Git history
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch .env" \
  --prune-empty --tag-name-filter cat -- --all

# 4. Force push
git push origin --force --all
git push origin --force --tags

# 5. Notify your proxy provider
# Contact support about potential compromise
```

### 2. Long-term Actions (Within 24 hours)

- [ ] Review all commits for other secrets
- [ ] Enable 2FA on all accounts
- [ ] Set up GitGuardian monitoring
- [ ] Update documentation
- [ ] Notify team members (if applicable)
- [ ] Monitor accounts for suspicious activity

## 📞 Support

If you need help securing your credentials:

1. Check this guide
2. Review `.env.example` for proper format
3. Ensure `.gitignore` includes `.env`
4. Use GitGuardian for scanning
5. Create a GitHub issue (without posting credentials!)

## ⚖️ Legal Notice

- Never share your credentials
- Don't use stolen or shared accounts
- Respect proxy provider terms of service
- Follow Opinion Edge terms of service
- Use credentials only for authorized purposes

---

**Remember: Security is not optional. Protect your credentials!** 🔒

**Last Updated:** 2024
**Status:** Active
