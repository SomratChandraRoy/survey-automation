# 🚨 Secret Leak Fix Instructions

## Immediate Actions Required

GitGuardian detected exposed credentials in your repository. Follow these steps **immediately**:

---

## Step 1: Revoke Exposed Credentials (URGENT - Do First!)

### 1.1 Change Opinion Edge Password
1. Go to https://opinion-edge.com
2. Login with current credentials
3. Change password immediately
4. Enable 2FA if available

### 1.2 Get New Proxy Credentials
1. Contact your proxy provider (geo.floppydata.com)
2. Request new credentials
3. Disable/revoke old credentials
4. Update your records

### 1.3 Generate New 2Captcha API Key
1. Go to https://2captcha.com
2. Login to your account
3. Generate new API key
4. Revoke old API key

---

## Step 2: Update Local Configuration

### 2.1 Update .env File

```bash
cd opinion-edge-automation
nano .env
```

Update with NEW credentials:
```bash
OPINION_EDGE_EMAIL=your_email@example.com
OPINION_EDGE_PASSWORD=your_NEW_password

PROXY_HOST=your_proxy_host.com
PROXY_PORT=10080
PROXY_USERNAME=your_NEW_proxy_username
PROXY_PASSWORD=your_NEW_proxy_password

CAPTCHA_API_KEY=your_NEW_2captcha_api_key
```

Save and exit (Ctrl+X, Y, Enter)

---

## Step 3: Clean Git History

### Option A: Automatic (Recommended)

```bash
chmod +x fix-secret-leak.sh
./fix-secret-leak.sh
```

### Option B: Manual

```bash
# 1. Create backup
git branch backup-before-cleanup

# 2. Remove .env from history
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch .env" \
  --prune-empty --tag-name-filter cat -- --all

# 3. Clean up
rm -rf .git/refs/original/
git reflog expire --expire=now --all
git gc --prune=now --aggressive

# 4. Verify
git ls-files | grep .env
# Should return nothing
```

---

## Step 4: Force Push to GitHub

⚠️ **WARNING:** This will rewrite Git history!

```bash
# Push cleaned history
git push origin --force --all
git push origin --force --tags
```

---

## Step 5: Verify on GitHub

1. Go to your GitHub repository
2. Check that .env is not visible in any commits
3. Verify GitGuardian alert is resolved
4. Check repository settings → Security → Secret scanning

---

## Step 6: Prevent Future Leaks

### 6.1 Install GitGuardian CLI

```bash
pip install ggshield
```

### 6.2 Setup Pre-commit Hook

```bash
ggshield install -m local
```

### 6.3 Scan Before Committing

```bash
# Scan current changes
ggshield secret scan path .

# Scan before commit
git add .
ggshield secret scan pre-commit
```

---

## Step 7: Notify Collaborators (If Any)

If others have cloned your repository:

```
Subject: URGENT - Repository History Rewritten

The repository history has been rewritten to remove exposed credentials.

Action Required:
1. Delete your local clone
2. Re-clone from GitHub
3. Update your .env file with new credentials

Command:
rm -rf opinion-edge-automation
git clone https://github.com/yourusername/opinion-edge-automation.git
```

---

## Verification Checklist

- [ ] Old credentials revoked
- [ ] New credentials generated
- [ ] .env file updated with new credentials
- [ ] Git history cleaned
- [ ] Force pushed to GitHub
- [ ] GitGuardian alert resolved
- [ ] .env not visible in any commits
- [ ] .gitignore includes .env
- [ ] Pre-commit hook installed
- [ ] Collaborators notified (if any)

---

## Testing

After completing all steps:

```bash
# 1. Verify .env is not tracked
git status
# .env should NOT appear

# 2. Verify .env is in .gitignore
cat .gitignore | grep .env
# Should show: .env

# 3. Test the system still works
./deploy.sh
```

---

## Common Issues

### Issue: "Cannot force push"

**Solution:**
```bash
# Disable branch protection temporarily
# Go to GitHub → Settings → Branches → Edit protection rule
# Then force push
git push origin --force --all
```

### Issue: "Collaborators can't pull"

**Solution:**
They need to re-clone:
```bash
rm -rf opinion-edge-automation
git clone https://github.com/yourusername/opinion-edge-automation.git
```

### Issue: "GitGuardian still shows alert"

**Solution:**
1. Wait 5-10 minutes for GitHub to update
2. Verify credentials are truly removed from all commits
3. Contact GitGuardian support if issue persists

---

## Prevention Tips

1. **Always use .env for secrets**
2. **Never commit .env file**
3. **Use .env.example with placeholders**
4. **Install GitGuardian pre-commit hook**
5. **Scan before every commit**
6. **Review changes before pushing**
7. **Enable GitHub secret scanning**
8. **Use strong, unique passwords**
9. **Rotate credentials regularly**
10. **Enable 2FA on all accounts**

---

## Support

If you need help:

1. Check SECURITY.md
2. Review this guide
3. Contact GitGuardian support
4. Create GitHub issue (without posting credentials!)

---

## Timeline

| Action | Timeframe |
|--------|-----------|
| Revoke credentials | **Immediately** |
| Update .env | Within 5 minutes |
| Clean Git history | Within 15 minutes |
| Force push | Within 20 minutes |
| Verify on GitHub | Within 30 minutes |
| Install prevention tools | Within 1 hour |

---

## ⚠️ CRITICAL REMINDERS

1. **Revoke old credentials FIRST** - They're already exposed!
2. **Don't skip Git history cleanup** - Old commits still contain secrets
3. **Force push is required** - Normal push won't remove secrets
4. **Test after cleanup** - Ensure system still works
5. **Install prevention tools** - Prevent future leaks

---

**Status:** 🚨 URGENT - Complete within 1 hour

**Priority:** CRITICAL

**Impact:** High - Exposed credentials can be used by anyone

---

**Need immediate help?** Check SECURITY.md or create a GitHub issue.
