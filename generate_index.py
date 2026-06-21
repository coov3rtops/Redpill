#!/usr/bin/env python3
import os
import sys
from datetime import datetime
from pathlib import Path
from bs4 import BeautifulSoup
from PIL import Image
import io

# ================== CONFIGURATION ==================
FOLDER_PATH = "."   
THUMBNAIL_SIZE = (80, 80)
THUMBNAILS_FOLDER = "thumbnails"
# ===================================================

def create_thumbnail_dir(root):
    thumb_dir = root / THUMBNAILS_FOLDER
    thumb_dir.mkdir(exist_ok=True)
    return thumb_dir

def extract_first_image_base64(html_file):
    try:
        with open(html_file, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f, 'html.parser')
        img = soup.find('img')
        if img and img.get('src', '').startswith('data:image'):
            header, base64_data = img['src'].split(',', 1)
            return base64.b64decode(base64_data)
    except:
        pass
    return None

def save_thumbnail(image_bytes, thumb_path):
    try:
        image = Image.open(io.BytesIO(image_bytes))
        image.thumbnail(THUMBNAIL_SIZE, Image.Resampling.LANCZOS)
        image.save(thumb_path, format="PNG", optimize=True)
        return True
    except:
        return False

def main():
    root = Path(FOLDER_PATH).resolve()
    thumb_dir = create_thumbnail_dir(root)
    notes = []
    
    print(f"🔍 Scanning and generating thumbnails...")

    for html_file in sorted(root.rglob("*.html")):
        if html_file.name.lower() in ["index.html", "generate_index.py"]:
            continue

        rel_path = html_file.relative_to(root)
        title = html_file.stem

        img_bytes = extract_first_image_base64(html_file)
        thumb_rel = None
        if img_bytes:
            thumb_filename = f"{html_file.stem}.png"
            thumb_path = thumb_dir / thumb_filename
            if save_thumbnail(img_bytes, thumb_path):
                thumb_rel = f"{THUMBNAILS_FOLDER}/{thumb_filename}"

        mod_time = datetime.fromtimestamp(html_file.stat().st_mtime)
        date_str = mod_time.strftime("%b %d")

        notes.append({
            "title": title,
            "file": str(rel_path),
            "thumb": thumb_rel,
            "date": date_str
        })

    notes.sort(key=lambda x: x["title"].lower())

    print(f"✅ Building improved dark mode version...")

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>My Notes Archive</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=SF+Pro+Display:wght@400;500&display=swap');
        
        :root {{
            --bg: #f6f6f8;
            --sidebar-bg: #ffffff;
            --text: #1d1d1f;
            --text-secondary: #6e6e73;
            --border: #d2d2d7;
            --hover: #f2f2f7;
            --preview-bg: #ffffff;
        }}
        
        [data-theme="dark"] {{
            --bg: #1c1c1e;
            --sidebar-bg: #2c2c2e;
            --text: #f5f5f7;
            --text-secondary: #a1a1a6;
            --border: #3a3a3c;
            --hover: #3a3a3c;
            --preview-bg: #2c2c2e;
        }}

        body {{ 
            margin:0; 
            font-family:'SF Pro Display', -apple-system, sans-serif; 
            background:var(--bg); 
            color:var(--text); 
            display:flex; 
            height:100vh; 
            overflow:hidden; 
        }}
        
        .sidebar {{ 
            width:380px; 
            background:var(--sidebar-bg); 
            border-right:1px solid var(--border); 
            overflow-y:auto; 
            padding:12px 0; 
            box-shadow:2px 0 8px rgba(0,0,0,0.1); 
        }}
        .header {{ 
            padding:0 20px 8px; 
            font-size:13px; 
            font-weight:500; 
            color:var(--text-secondary); 
            text-transform:uppercase; 
            letter-spacing:0.5px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        .theme-toggle {{
            background: none;
            border: none;
            font-size: 20px;
            cursor: pointer;
            padding: 4px 8px;
            border-radius: 6px;
            color: var(--text-secondary);
        }}
        .theme-toggle:hover {{ background: var(--hover); }}

        ul {{ list-style:none; margin:0; padding:0; }}
        li {{ padding:8px 20px; display:flex; align-items:center; gap:12px; cursor:pointer; transition:background 0.2s; }}
        li:hover {{ background:var(--hover); }}
        li a {{ 
            text-decoration:none; 
            color:var(--text); 
            flex:1; 
            display:flex; 
            align-items:center; 
            gap:12px; 
            font-size:15px; 
        }}
        .thumb {{ width:52px; height:52px; object-fit:cover; border-radius:8px; background:#f0f0f0; flex-shrink:0; }}
        .no-thumb {{ width:52px; height:52px; display:flex; align-items:center; justify-content:center; font-size:28px; background:#f0f0f0; border-radius:8px; flex-shrink:0; }}
        .title {{ overflow:hidden; text-overflow:ellipsis; white-space:nowrap; flex:1; }}
        .date {{ font-size:12px; color:var(--text-secondary); white-space:nowrap; }}

        .preview-pane {{ 
            flex:1; 
            background:var(--preview-bg); 
            overflow:auto; 
            padding:40px; 
            color: var(--text);
        }}
        .preview-pane iframe {{ 
            width:100%; 
            height:100%; 
            border:none; 
        }}
    </style>
</head>
<body>
    <div class="sidebar">
        <div class="header">
            All Notes • {len(notes)} total
            <button class="theme-toggle" id="theme-toggle" title="Toggle Dark Mode">🌙</button>
        </div>
        <ul id="notes-list">
"""

    for note in notes:
        thumb_html = f'<img class="thumb" src="{note["thumb"]}" alt="">' if note['thumb'] else '<div class="no-thumb">📄</div>'
        html_content += f"""            <li>
                <a href="{note['file']}" class="note-link" data-file="{note['file']}">
                    {thumb_html}
                    <span class="title">{note['title']}</span>
                    <span class="date">{note['date']}</span>
                </a>
            </li>
"""

    html_content += """        </ul>
    </div>

    <div class="preview-pane" id="preview">
        <iframe id="note-frame" src=""></iframe>
    </div>

    <script>
        const toggle = document.getElementById('theme-toggle');
        const body = document.body;
        const frame = document.getElementById('note-frame');

        // Load saved theme
        if (localStorage.getItem('theme') === 'dark') {
            body.setAttribute('data-theme', 'dark');
            toggle.textContent = '☀️';
        }

        toggle.addEventListener('click', () => {
            if (body.getAttribute('data-theme') === 'dark') {
                body.removeAttribute('data-theme');
                toggle.textContent = '🌙';
                localStorage.setItem('theme', 'light');
            } else {
                body.setAttribute('data-theme', 'dark');
                toggle.textContent = '☀️';
                localStorage.setItem('theme', 'dark');
            }
        });

        // Note loading
        document.querySelectorAll('.note-link').forEach(link => {
            link.addEventListener('click', function(e) {
                e.preventDefault();
                const file = this.getAttribute('data-file');
                frame.src = file;
            });
        });

        // Load first note
        const firstLink = document.querySelector('.note-link');
        if (firstLink) frame.src = firstLink.getAttribute('data-file');
    </script>
</body>
</html>"""

    with open(root / "index.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    
    print(f"🎉 Improved dark mode with white text applied!")

if __name__ == "__main__":
    main()