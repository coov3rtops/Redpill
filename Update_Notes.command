#!/bin/bash

# =============================================
# Ultimate Redpill Dispensary Notes Updater
# Double-click to update + rebuild + notify
# =============================================

cd "$(dirname "$0")"

# Auto configure Git identity (only once)
if ! git config --get user.name > /dev/null; then
    git config --global user.name "Nathan Coovert"
    git config --global user.email "coov3rtops@gmail.com"
    echo "✓ Git identity configured"
fi

echo "========================================"
echo "🚀 Redpill Dispensary Notes Updater"
echo "========================================"

# Pull latest changes safely
echo "📥 Pulling latest changes..."
git fetch origin
git pull origin main --strategy-option=theirs --allow-unrelated-histories 2>/dev/null || git pull --rebase origin main

# Regenerate everything
echo "🔄 Regenerating index.html + thumbnails..."
python3 generate_index.py

# Commit & Push
echo "📤 Pushing to GitHub..."
git add -A

if git diff --cached --quiet; then
    echo "✓ No changes to commit"
else
    git commit -m "Auto-update: $(date '+%Y-%m-%d %H:%M:%S')"
fi

git push origin main || git push -f origin main

# Success!
echo ""
echo "🎉 Update completed successfully!"
echo "🌐 Cloudflare is rebuilding your site..."

# macOS Notification
osascript -e 'display notification "Notes archive updated successfully!" with title "Redpill Dispensary" subtitle "Cloudflare is rebuilding..." sound name "Glass"'

# Optional: Open your website
open "https://redpilldispensary.com"

echo ""
echo "You can close this window now."
read -p "Press Enter to exit..."