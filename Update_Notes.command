#!/bin/bash

# =============================================
# Auto Update Notes Archive
# Double-click this file to update everything
# =============================================

cd "$(dirname "$0")"   # Go to the folder where this script lives

echo "===================================="
echo "🚀 Updating Redpill Dispensary Notes"
echo "===================================="

# Pull latest changes from GitHub
echo "📥 Pulling latest changes..."
git pull --rebase

# Run the Python script to regenerate index + thumbnails
echo "🔄 Regenerating index.html and thumbnails..."
python3 generate_index.py

# Add all changes and push to GitHub (triggers Cloudflare rebuild)
echo "📤 Pushing updates to GitHub..."
git add .
git commit -m "Auto-update: $(date '+%Y-%m-%d %H:%M')" 2>/dev/null || echo "No changes to commit"
git push

echo ""
echo "✅ Done! Your site has been updated."
echo "🌐 Cloudflare should rebuild automatically in ~30 seconds."
echo ""
read -p "Press Enter to close..."
