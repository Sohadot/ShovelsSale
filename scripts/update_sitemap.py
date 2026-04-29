"""
ShovelsSale.com — Sitemap Generation Engine

Purpose:
- Discover all public HTML pages in the repository
- Convert filesystem paths into clean canonical URLs
- Generate a production-grade sitemap.xml
- Remain compatible with Windows, GitHub Actions, and static-site deployment
"""

from __future__ import annotations

import json
import re
import subprocess
from html.parser import HTMLParser
from pathlib import Path
from datetime import date

SITE_URL = "https://shovelssale.com"
RUN_DATE = date.today().isoformat()
ROOT_DIR = Path(".")

SKIP_DIRS = {
    ".git",
    ".github",
    "scripts",
    "node_modules",
    "__pycache__",
    ".well-known",
    "assets",
    "reports",
    "dist",
    "build",
    "vendor",
}

SKIP_FILES = {
    "404.html",
    "google-verification.html",
    "google28b5398e4140f820.html",
    "schema-templates.html",
}

DATE_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}")
METADATA_DATE_KEYS = {
    "dateModified",
    "modified",
    "uploadDate",
}
META_DATE_NAMES = {
    "date",
    "date.modified",
    "modified",
    "lastmod",
}
META_DATE_PROPERTIES = {
    "article:modified_time",
    "og:updated_time",
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


class SitemapMetadataParser(HTMLParser):
    """Extract explicit page update dates from HTML metadata."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self._json_ld_depth = 0
        self._json_ld_parts: list[str] = []
        self.json_ld_blocks: list[str] = []
        self.meta_dates: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        tag = tag.lower()
        attributes = {name.lower(): value for name, value in attrs if name and value is not None}

        if tag == "script" and attributes.get("type", "").lower() == "application/ld+json":
            self._json_ld_depth += 1
            self._json_ld_parts = []
            return

        if tag != "meta":
            return

        content = attributes.get("content", "").strip()
        if not content:
            return

        meta_name = attributes.get("name", "").strip().lower()
        meta_property = attributes.get("property", "").strip().lower()

        if meta_name in META_DATE_NAMES or meta_property in META_DATE_PROPERTIES:
            self.meta_dates.append(content)

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() == "script" and self._json_ld_depth:
            self._json_ld_depth -= 1
            block = "".join(self._json_ld_parts).strip()
            if block:
                self.json_ld_blocks.append(block)
            self._json_ld_parts = []

    def handle_data(self, data: str) -> None:
        if self._json_ld_depth:
            self._json_ld_parts.append(data)


def normalize_date(value: str | None) -> str | None:
    """Return YYYY-MM-DD when value begins with an ISO-like date."""
    if not value:
        return None

    match = DATE_PATTERN.match(str(value).strip())
    if not match:
        return None

    return match.group(0)


def iter_json_nodes(value):
    """Yield all dictionaries inside JSON-LD objects, lists, and @graph values."""
    if isinstance(value, dict):
        yield value
        graph = value.get("@graph")
        if isinstance(graph, list):
            for item in graph:
                yield from iter_json_nodes(item)
    elif isinstance(value, list):
        for item in value:
            yield from iter_json_nodes(item)


def metadata_lastmod(path: Path) -> str | None:
    """Return explicit page metadata date when present."""
    parser = SitemapMetadataParser()
    parser.feed(path.read_text(encoding="utf-8", errors="ignore"))

    for value in parser.meta_dates:
        parsed = normalize_date(value)
        if parsed:
            return parsed

    for block in parser.json_ld_blocks:
        try:
            data = json.loads(block)
        except json.JSONDecodeError:
            continue

        for node in iter_json_nodes(data):
            for key in METADATA_DATE_KEYS:
                parsed = normalize_date(node.get(key))
                if parsed:
                    return parsed

    return None


def git_lastmod(path: Path) -> str | None:
    """Return the last committed date for a file, avoiding checkout-time churn."""
    try:
        completed = subprocess.run(
            ["git", "log", "-1", "--format=%cs", "--", str(path)],
            cwd=ROOT_DIR,
            check=False,
            capture_output=True,
            text=True,
        )
    except OSError:
        return None

    if completed.returncode != 0:
        return None

    return normalize_date(completed.stdout.strip())


def filesystem_lastmod(path: Path) -> str:
    """Fallback for non-Git environments."""
    return date.fromtimestamp(path.stat().st_mtime).isoformat()


def page_lastmod(path: Path) -> str:
    """Return the best available meaningful lastmod date for a public page."""
    return metadata_lastmod(path) or git_lastmod(path) or filesystem_lastmod(path)


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
            "lastmod": page_lastmod(path),
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

    print(f"[OK] sitemap.xml updated - {len(pages)} pages - generated {RUN_DATE}")
    for page in pages:
        print(f"    {page['priority']} | {page['lastmod']} | {page['url']}")


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print(f"Sitemap Generator - {RUN_DATE}")
    print("=" * 60 + "\n")

    pages = discover_pages()
    generate_sitemap(pages)

    print("\n[OK] Sitemap generation complete.\n")
