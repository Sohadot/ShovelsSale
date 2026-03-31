"""
ShovelsSale.com — Google Tags Synchronization Engine

Purpose:
- Ensure every real HTML page contains the required Google Tag Manager + GA4 blocks
- Avoid duplicate insertion
- Work safely from repository root
- Remain compatible with publish_pipeline.py and GitHub Actions

This script:
- inserts GTM <script> + GA4 before </head> if missing
- inserts GTM <noscript> immediately after <body...> if missing
- skips excluded directories/files
- is idempotent: running it multiple times should not duplicate tags
"""

from __future__ import annotations

import re
from pathlib import Path


# ============================================================
# CONFIG
# ============================================================

ROOT_DIR = Path(".")
SKIP_DIRS = {
    ".git",
    ".github",
    "node_modules",
    "scripts",
    "__pycache__",
    ".venv",
    "venv",
}
SKIP_FILES = {"404.html"}

GTM_ID = "GTM-K83NSPVC"
GA4_ID = "G-VKVL5E97G3"

GTM_HEAD_BLOCK = f"""  <!-- Google Tag Manager -->
  <script>(function(w,d,s,l,i){{w[l]=w[l]||[];w[l].push({{'gtm.start':
  new Date().getTime(),event:'gtm.js'}});var f=d.getElementsByTagName(s)[0],
  j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
  'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
  }})(window,document,'script','dataLayer','{GTM_ID}');</script>
  <!-- End Google Tag Manager -->

  <!-- Google Analytics 4 -->
  <script async src="https://www.googletagmanager.com/gtag/js?id={GA4_ID}"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){{dataLayer.push(arguments);}}
    gtag('js', new Date());
    gtag('config', '{GA4_ID}');
  </script>
  <!-- End Google Analytics 4 -->
"""

GTM_BODY_BLOCK = f"""  <!-- Google Tag Manager (noscript) -->
  <noscript><iframe src="https://www.googletagmanager.com/ns.html?id={GTM_ID}"
  height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
  <!-- End Google Tag Manager (noscript) -->
"""


# ============================================================
# HELPERS
# ============================================================

def should_skip(path: Path) -> bool:
    if path.name in SKIP_FILES:
        return True
    return any(part in SKIP_DIRS for part in path.parts)


def discover_html_files() -> list[Path]:
    files: list[Path] = []
    for path in ROOT_DIR.rglob("*.html"):
        if should_skip(path):
            continue
        files.append(path)
    return sorted(files)


def has_head_tags(content: str) -> bool:
    return GTM_ID in content and GA4_ID in content


def has_body_noscript(content: str) -> bool:
    return "googletagmanager.com/ns.html?id=" + GTM_ID in content


def inject_head_tags(content: str) -> str:
    if has_head_tags(content):
        return content

    if "</head>" not in content:
        return content

    return content.replace("</head>", GTM_HEAD_BLOCK + "\n</head>", 1)


def inject_body_noscript(content: str) -> str:
    if has_body_noscript(content):
        return content

    body_match = re.search(r"<body\b[^>]*>", content, flags=re.IGNORECASE)
    if not body_match:
        return content

    body_tag = body_match.group(0)
    replacement = body_tag + "\n" + GTM_BODY_BLOCK
    return content.replace(body_tag, replacement, 1)


def process_file(path: Path) -> str:
    original = path.read_text(encoding="utf-8", errors="ignore")
    updated = original

    updated = inject_head_tags(updated)
    updated = inject_body_noscript(updated)

    if updated != original:
        path.write_text(updated, encoding="utf-8")
        return "updated"

    return "unchanged"


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("ShovelsSale.com — Google Tags Synchronization Engine")
    print("=" * 60 + "\n")

    html_files = discover_html_files()
    updated_count = 0
    unchanged_count = 0

    for file_path in html_files:
        result = process_file(file_path)
        if result == "updated":
            updated_count += 1
            print(f"[✓] Updated: {file_path.as_posix()}")
        else:
            unchanged_count += 1

    print("\n" + "-" * 60)
    print(f"[✓] HTML files scanned: {len(html_files)}")
    print(f"[✓] Updated: {updated_count}")
    print(f"[✓] Unchanged: {unchanged_count}")
    print("-" * 60 + "\n")
