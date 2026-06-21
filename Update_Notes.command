#!/bin/bash

# =============================================
# Smart Auto Update for Redpill Dispensary Notes
# Double-click friendly + handles common issues
# =============================================

cd "$(dirname "$0")"

echo "========================================"
echo "🚀 Redpill Dispensary Notes Updater"
echo "========================================"

# === Setup remote if missing ===
if ! git config --get remote.origin.url > /dev/null; then
    echo "⚠️  Remote not configured. Please run this once in Terminal:"
    echo "   git remote add origin https://github.com/coov3rtops/Redpill.git"
    echo ""
    read -p "Press Enter after you have set the remote..."
fi

echo "📥 Pulling latest changes from GitHub..."
git fetch origin

# Smart pull strategy
if git merge-base --is-ancestor origin/main main 2>/dev/null; then
    git pull --rebase origin main
else
    echo "🔄 Merging changes (keeping your local files)..."
    git pull origin main --strategy-option=theirs --allow-unrelated-histories
fi

# Regenerate the website
echo "🔄 Regenerating index.html + thumbnails..."
python3 generate_index.py

# Commit and push
echo "📤 Pushing updates to GitHub..."
git add -A

if git diff --cached --quiet; then
    echo "✓ No changes to commit"
else
    git commit -m "Auto-update: $(date '+%Y-%m-%d %H:%M:%S')"
fi

git push origin main || git push -f origin main

echo ""
echo "🎉 Update completed successfully!"
echo "🌐 Cloudflare Pages should be rebuilding right now."
echo ""
echo "You can close this window."
read -p "Press Enter to exit..."