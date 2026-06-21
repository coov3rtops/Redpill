#!/bin/bash

cd "$(dirname "$0")"

# Auto-configure Git
if ! git config --get user.name > /dev/null; then
    git config --global user.name "Nathan Coovert"
    git config --global user.email "coov3rtops@gmail.com"
fi

echo "========================================"
echo "🚀 Redpill Dispensary Notes Updater"
echo "========================================"

echo "📥 Pulling latest changes..."
git pull origin main --strategy-option=theirs --allow-unrelated-histories 2>/dev/null || git pull --rebase origin main

echo "🔄 Regenerating index + thumbnails..."
python3 generate_index.py

echo "📤 Pushing updates (including thumbnails)..."
git add -A                  # This ensures thumbnails/ is always included
git commit -m "Auto-update: $(date '+%Y-%m-%d %H:%M:%S')" 2>/dev/null || echo "✓ No changes"
git push origin main || git push -f origin main

osascript -e 'display notification "✅ Notes updated with thumbnails!" with title "Redpill Dispensary" sound name "Glass"'
open "https://redpilldispensary.com"

echo ""
echo "🎉 Done! Thumbnails should now appear on your site."
read -p "Press Enter to close..."