#!/bin/bash

# Script to fix secret leak in Git history
# WARNING: This will rewrite Git history!

set -e

echo "================================================"
echo "Secret Leak Fix Script"
echo "================================================"
echo ""
echo "⚠️  WARNING: This will rewrite Git history!"
echo "⚠️  Make sure you have a backup before proceeding."
echo ""
read -p "Do you want to continue? (yes/no): " confirm

if [ "$confirm" != "yes" ]; then
    echo "Aborted."
    exit 1
fi

echo ""
echo "Step 1: Creating backup branch..."
git branch backup-before-cleanup || true

echo ""
echo "Step 2: Removing .env from Git history..."
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch .env" \
  --prune-empty --tag-name-filter cat -- --all

echo ""
echo "Step 3: Cleaning up refs..."
rm -rf .git/refs/original/
git reflog expire --expire=now --all
git gc --prune=now --aggressive

echo ""
echo "Step 4: Verifying .env is not tracked..."
if git ls-files | grep -q "^.env$"; then
    echo "❌ ERROR: .env is still tracked!"
    exit 1
else
    echo "✅ .env is not tracked"
fi

echo ""
echo "Step 5: Checking .gitignore..."
if grep -q "^.env$" .gitignore; then
    echo "✅ .env is in .gitignore"
else
    echo "⚠️  Adding .env to .gitignore..."
    echo ".env" >> .gitignore
    git add .gitignore
    git commit -m "Add .env to .gitignore"
fi

echo ""
echo "================================================"
echo "✅ Secret leak fixed locally!"
echo "================================================"
echo ""
echo "Next steps:"
echo ""
echo "1. Revoke the exposed credentials:"
echo "   - Change Opinion Edge password"
echo "   - Get new proxy credentials"
echo "   - Generate new 2Captcha API key"
echo ""
echo "2. Update your .env file with new credentials"
echo ""
echo "3. Force push to GitHub (this will rewrite history):"
echo "   git push origin --force --all"
echo "   git push origin --force --tags"
echo ""
echo "4. Notify collaborators to re-clone the repository"
echo ""
echo "⚠️  IMPORTANT: Force push will affect all collaborators!"
echo ""
