"""
ShovelsSale.com — Sitemap Generation Engine

Purpose:
- Discover all public HTML pages in the repository
- Convert filesystem paths into clean canonical URLs
- Generate a production-grade sitemap.xml
- Remain compatible with Windows, GitHub Actions, and static-site deployment
"""

from __future__ import annotations

from pathlib import Path
from datetime import date

SITE_URL = "https://shovelssale.com"
TODAY = date.today().isoformat()
ROOT_DIR = Path(".")

SKIP_DIRS = {
    ".git",
    ".github",
    "scripts",
    "node_modules",
    "__pycache__",
    ".well-known",
}

SKIP_FILES = {
    "404.html",
    "google-verification.html",
    "google28b5398e414f820.html",
    "schema-templates.html",
}

PRIORITY_MAP = {
    "/": "1.0",
    "/about/": "0.9",
    "/manifesto/": "0.95",
    "/guide/": "0.9",
    "/framework/": "0.9",
    "/scanner/": "0.9",
    "/dispatch/": "0.95",
    "/blog/": "0.85",
}

FREQ_MAP = {
    "/": "weekly",
    "/about/": "monthly",
    "/manifesto/": "monthly",
    "/guide/": "weekly",
    "/framework/": "weekly",
    "/scanner/": "weekly",
    "/dispatch/": "weekly",
    "/blog/": "weekly",
}


def should_skip(path: Path) -> bool:
    """Return True if the path should be excluded from sitemap discovery."""
    
    # Skip specific files
    if path.name in SKIP_FILES:
        return True

    # 🔒 Skip ALL Google verification files (dynamic-safe)
    if path.name.startswith("google") and path.name.endswith(".html"):
        return True

    # Skip system directories
    if any(part in SKIP_DIRS for part in path.parts):
        return True

    # Skip assets completely (critical for SEO cleanliness)
    if "assets" in path.parts:
        return True

    return False

def path_to_url_path(path: Path) -> str:
    """
    Convert a filesystem path into a clean URL path.

    Examples:
    - index.html -> /
    - about/index.html -> /about/
    - dispatch/index.html -> /dispatch/
    - blog/post-slug/index.html -> /blog/post-slug/
    - dispatch/001.html -> /dispatch/001.html
    """
    relative = path.relative_to(ROOT_DIR).as_posix()

    if relative == "index.html":
        return "/"

    if relative.endswith("/index.html"):
        return "/" + relative[:-10].strip("/") + "/"

    return "/" + relative.lstrip("/")


def discover_pages() -> list[dict]:
    """Discover all public HTML pages and assign sitemap metadata."""
    pages: list[dict] = []

    for path in sorted(ROOT_DIR.rglob("*.html")):
        if should_skip(path):
            continue

        url_path = path_to_url_path(path)

        priority = PRIORITY_MAP.get(url_path, "0.7")
        freq = FREQ_MAP.get(url_path, "weekly")

        # Blog article pages
        if url_path.startswith("/blog/") and url_path != "/blog/":
            priority = "0.7"
            freq = "monthly"

        # Dispatch issue pages
        if url_path.startswith("/dispatch/") and url_path != "/dispatch/":
            priority = "0.8"
            freq = "monthly"

        pages.append({
            "url": f"{SITE_URL.rstrip('/')}{url_path}",
            "lastmod": TODAY,
            "changefreq": freq,
            "priority": priority,
            "url_path": url_path,
        })

    # Sort:
    # 1. homepage first
    # 2. dispatch issues newest first
    # 3. then higher priority
    # 4. then URL path alphabetically
    def sort_key(p):
        if p["url_path"] == "/":
            return (0, 0, "")

        if p["url_path"].startswith("/dispatch/") and p["url_path"].endswith(".html"):
            try:
                num = int(p["url_path"].split("/")[-1].replace(".html", ""))
                return (1, -num, "")
            except ValueError:
                pass

        return (1, -float(p["priority"]), p["url_path"])

    pages.sort(key=sort_key)

    return pages


def generate_sitemap(pages: list[dict]) -> None:
    """Generate sitemap.xml from discovered pages."""
    url_blocks = []

    for page in pages:
        url_blocks.append(f"""  <url>
    <loc>{page['url']}</loc>
    <lastmod>{page['lastmod']}</lastmod>
    <changefreq>{page['changefreq']}</changefreq>
    <priority>{page['priority']}</priority>
  </url>""")

    sitemap = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:schemaLocation="http://www.sitemaps.org/schemas/sitemap/0.9
        http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd">
{chr(10).join(url_blocks)}
</urlset>
"""

    Path("sitemap.xml").write_text(sitemap, encoding="utf-8")

    print(f"[✓] sitemap.xml updated — {len(pages)} pages — {TODAY}")
    for page in pages:
        print(f"    {page['priority']} | {page['url']}")


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print(f"Sitemap Generator — {TODAY}")
    print("=" * 60 + "\n")

    pages = discover_pages()
    generate_sitemap(pages)

    print("\n[✓] Sitemap generation complete.\n")
