"""
ShovelsSale.com — Project Setup Script
ينشئ هيكل المجلدات الكامل تلقائياً
شغّله مرة واحدة على جهازك ثم ارفع على GitHub
"""

import os
import shutil

# ============================================================
# غيّر هذا المسار لمكان تريد إنشاء المشروع عندك
# Windows مثال: r"C:\Users\YourName\Desktop\shovelssale"
# Mac مثال:    "/Users/YourName/Desktop/shovelssale"
# ============================================================
PROJECT_ROOT = os.path.join(os.path.expanduser("~"), "Desktop", "shovelssale")

# الهيكل الكامل للمجلدات
FOLDERS = [
    "about",
    "manifesto",
    "guide",
    "blog/pick-and-shovel-wins-2026",
    "blog/top-ai-infrastructure-plays",
    ".well-known",
    "assets",
    "scripts",
    ".github/workflows",
]

def create_structure():
    print(f"\n{'='*55}")
    print(f"  ShovelsSale.com — Project Setup")
    print(f"{'='*55}\n")

    # إنشاء المجلد الرئيسي
    os.makedirs(PROJECT_ROOT, exist_ok=True)
    print(f"✓ Root folder: {PROJECT_ROOT}\n")

    # إنشاء كل المجلدات الفرعية
    for folder in FOLDERS:
        path = os.path.join(PROJECT_ROOT, folder)
        os.makedirs(path, exist_ok=True)
        print(f"  ✓ {folder}/")

    print(f"\n{'='*55}")
    print(f"  ✓ Structure created successfully!")
    print(f"\n  Now place each file in its correct folder:")
    print(f"\n  ROOT (shovelssale/):")
    print(f"    → index.html")
    print(f"    → 404.html")
    print(f"    → robots.txt")
    print(f"    → sitemap.xml")
    print(f"    → feed.xml")
    print(f"    → manifest.json")
    print(f"    → _headers")
    print(f"    → _redirects")
    print(f"    → .htaccess")
    print(f"\n  about/")
    print(f"    → index.html")
    print(f"\n  manifesto/")
    print(f"    → index.html")
    print(f"\n  guide/")
    print(f"    → index.html")
    print(f"\n  blog/")
    print(f"    → index.html")
    print(f"\n  blog/pick-and-shovel-wins-2026/")
    print(f"    → index.html")
    print(f"\n  .well-known/")
    print(f"    → security.txt")
    print(f"\n  assets/")
    print(f"    → schema-templates.html")
    print(f"\n  scripts/")
    print(f"    → automate.py")
    print(f"    → security_scan.py")
    print(f"    → update_sitemap.py")
    print(f"    → generate_rss.py")
    print(f"\n  .github/workflows/")
    print(f"    → weekly-update.yml")
    print(f"\n{'='*55}")
    print(f"  Then open GitHub Desktop → Add folder → Commit → Push")
    print(f"{'='*55}\n")

if __name__ == "__main__":
    create_structure()
