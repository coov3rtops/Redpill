#!/bin/bash

cd "$(dirname "$0")"

# ===================== CONFIG =====================
CLOUDFLARE_ZONE_ID="YOUR_ZONE_ID_HERE"
CLOUDFLARE_API_TOKEN="YOUR_API_TOKEN_HERE"
# ================================================

# Auto-configure Git
if ! git config --get user.name > /dev/null; then
    git config --global user.name "Nathan Coovert"
    git config --global user.email "coov3rtops@gmail.com"
fi

echo "========================================"
echo "🚀 Redpill Dispensary Notes Updater"
echo "========================================"

# Pull
echo "📥 Pulling latest changes..."
git pull origin main --strategy-option=theirs --allow-unrelated-histories 2>/dev/null || git pull --rebase origin main

# Regenerate
echo "🔄 Regenerating index.html + thumbnails..."
python3 generate_index.py

# Commit & Push
echo "📤 Pushing to GitHub..."
git add -A
if ! git diff --cached --quiet; then
    git commit -m "Auto-update: $(date '+%Y-%m-%d %H:%M:%S')"
fi
git push origin main || git push -f origin main

# Automatic Cloudflare Cache Purge
echo "🧹 Purging Cloudflare cache..."
curl -s -X POST "https://api.cloudflare.com/client/v4/zones/${CLOUDFLARE_ZONE_ID}/purge_cache" \
     -H "Authorization: Bearer ${CLOUDFLARE_API_TOKEN}" \
     -H "Content-Type: application/json" \
     --data '{"purge_everything":true}' > /dev/null && \
echo "✅ Cloudflare cache purged successfully!" || \
echo "⚠️  Cache purge failed (check Zone ID & Token)"

# Success
echo ""
echo "🎉 Update completed successfully!"
osascript -e 'display notification "Notes archive updated + cache purged!" with title "Redpill Dispensary" sound name "Glass"'

open "https://redpilldispensary.com"

echo "You can close this window."
read -p "Press Enter to exit..."