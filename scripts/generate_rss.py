"""
ShovelsSale.com — Multi-Channel RSS Engine

Purpose:
- Discover real published HTML content
- Generate channel-specific RSS feeds
- Support blog and dispatch as separate distribution layers
- Remain compatible with the publishing pipeline

This script DOES NOT:
- generate content
- update sitemap.xml
- modify archive pages

Those responsibilities belong to:
- scripts/automate.py
- scripts/update_sitemap.py
"""

from __future__ import annotations

import re
import html
from pathlib import Path
from datetime import datetime, timezone
from typing import Optional, Dict, List
from bs4 import BeautifulSoup


# ============================================================
# CONFIG
# ============================================================

SITE_URL = "https://shovelssale.com"
ROOT_DIR = Path(".")

CHANNELS = {
    "blog": {
        "dir": ROOT_DIR / "blog",
        "feed_path": ROOT_DIR / "blog" / "feed.xml",
        "title": "ShovelsSale Blog",
        "link": f"{SITE_URL}/blog/",
        "description": (
            "A structured archive of market infrastructure, shovel economy strategy, "
            "and system-level analysis from ShovelsSale.com."
        ),
    },
    "dispatch": {
        "dir": ROOT_DIR / "dispatch",
        "feed_path": ROOT_DIR / "dispatch" / "feed.xml",
        "title": "ShovelsSale Dispatch",
        "link": f"{SITE_URL}/dispatch/",
        "description": (
            "The analytical publication layer of ShovelsSale.com — structured releases "
            "on classification, infrastructure, dependency, and control."
        ),
    },
}

MAX_ITEMS_PER_FEED = 25


# ============================================================
# HELPERS
# ============================================================

def safe_read_text(path: Path) -> str:
    """Read file safely as UTF-8."""
    return path.read_text(encoding="utf-8", errors="ignore")


def xml_escape(value: str) -> str:
    """Escape XML-sensitive characters."""
    return html.escape(value, quote=True)


def discover_channel_pages(channel_dir: Path) -> List[Path]:
    """
    Discover real content pages for a channel.
    Excludes the channel index itself and feed.xml.
    Supports:
    - /blog/<slug>/index.html
    - /dispatch/001.html
    - /dispatch/002.html
    """
    pages: List[Path] = []

    if not channel_dir.exists():
        return pages

    for child in sorted(channel_dir.iterdir()):
        # Case 1: nested directory pages (e.g. blog/post-slug/index.html)
        if child.is_dir():
            index_file = child / "index.html"
            if index_file.exists():
                pages.append(index_file)

        # Case 2: flat html files (e.g. dispatch/001.html)
        elif child.is_file():
            if child.name == "index.html":
                continue
            if child.name == "feed.xml":
                continue
            if child.suffix.lower() == ".html":
                pages.append(child)

    return pages


def extract_title(soup: BeautifulSoup) -> str:
    """Extract the best title available."""
    og_title = soup.find("meta", attrs={"property": "og:title"})
    if og_title and og_title.get("content"):
        return og_title["content"].strip()

    if soup.title and soup.title.string:
        raw = soup.title.string.strip()
        return raw

    h1 = soup.find("h1")
    if h1:
        return h1.get_text(" ", strip=True)

    return "Untitled Entry"


def extract_description(soup: BeautifulSoup) -> str:
    """Extract description or summary."""
    meta_desc = soup.find("meta", attrs={"name": "description"})
    if meta_desc and meta_desc.get("content"):
        return meta_desc["content"].strip()

    og_desc = soup.find("meta", attrs={"property": "og:description"})
    if og_desc and og_desc.get("content"):
        return og_desc["content"].strip()

    first_p = soup.find("p")
    if first_p:
        return first_p.get_text(" ", strip=True)[:260]

    return "ShovelsSale.com publication."


def extract_canonical_url(soup: BeautifulSoup) -> Optional[str]:
    """Extract canonical URL."""
    canonical = soup.find("link", attrs={"rel": "canonical"})
    if canonical and canonical.get("href"):
        return canonical["href"].strip()
    return None


def extract_date_from_jsonld(soup: BeautifulSoup) -> Optional[str]:
    """Extract datePublished or dateModified from JSON-LD."""
    scripts = soup.find_all("script", attrs={"type": "application/ld+json"})
    for script in scripts:
        content = script.string or script.get_text(strip=True)
        if not content:
            continue

        match = re.search(r'"datePublished"\s*:\s*"([^"]+)"', content)
        if match:
            return match.group(1).strip()

        match = re.search(r'"dateModified"\s*:\s*"([^"]+)"', content)
        if match:
            return match.group(1).strip()

    return None


def extract_date_from_meta(soup: BeautifulSoup) -> Optional[str]:
    """Extract common article date meta fields."""
    candidates = [
        ("property", "article:published_time"),
        ("property", "article:modified_time"),
        ("name", "date"),
        ("name", "publish_date"),
    ]

    for attr_name, attr_value in candidates:
        meta = soup.find("meta", attrs={attr_name: attr_value})
        if meta and meta.get("content"):
            return meta["content"].strip()

    return None


def normalize_datetime(raw_date: Optional[str], file_path: Path) -> datetime:
    """
    Normalize to UTC datetime.
    If date missing or invalid, fallback to file mtime.
    """
    if raw_date:
        candidate = raw_date.strip().replace("Z", "+00:00")
        try:
            dt = datetime.fromisoformat(candidate)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            return dt.astimezone(timezone.utc)
        except ValueError:
            pass

        # Try YYYY-MM-DD fallback
        try:
            dt = datetime.strptime(raw_date[:10], "%Y-%m-%d")
            return dt.replace(tzinfo=timezone.utc)
        except ValueError:
            pass

    return datetime.fromtimestamp(file_path.stat().st_mtime, tz=timezone.utc)


def to_rfc2822(dt: datetime) -> str:
    """Convert datetime to RSS-compliant RFC 2822 string."""
    return dt.strftime("%a, %d %b %Y %H:%M:%S GMT")


def clean_title_for_rss(title: str) -> str:
    """
    Clean long SEO title separators while preserving meaning.
    RSS titles should be readable, not bloated.
    """
    return re.sub(r"\s+\|\s+ShovelsSale\.com$", "", title).strip()


def extract_item_data(file_path: Path) -> Dict[str, str]:
    """Extract all metadata needed for RSS item generation."""
    raw_html = safe_read_text(file_path)
    soup = BeautifulSoup(raw_html, "lxml")

    title = clean_title_for_rss(extract_title(soup))
    description = extract_description(soup)
    canonical = extract_canonical_url(soup)

    raw_date = extract_date_from_jsonld(soup) or extract_date_from_meta(soup)
    dt = normalize_datetime(raw_date, file_path)

    if canonical:
        url = canonical
    else:
        relative = str(file_path).replace("\\", "/").replace("./", "")
        if relative.endswith("/index.html"):
            relative = relative[:-10]
        url = f"{SITE_URL}/{relative}".replace("//", "/")
        url = url.replace("https:/", "https://")

    return {
        "title": title,
        "description": description,
        "url": url,
        "pub_date": to_rfc2822(dt),
        "sort_date": dt.isoformat(),
    }


# ============================================================
# RSS BUILDERS
# ============================================================

def build_rss_xml(channel_key: str, items: List[Dict[str, str]]) -> str:
    """Build RSS XML for a specific channel."""
    config = CHANNELS[channel_key]

    last_build_date = items[0]["pub_date"] if items else to_rfc2822(datetime.now(timezone.utc))

    item_blocks = []
    for item in items[:MAX_ITEMS_PER_FEED]:
        item_blocks.append(f"""    <item>
      <title>{xml_escape(item["title"])}</title>
      <link>{xml_escape(item["url"])}</link>
      <guid>{xml_escape(item["url"])}</guid>
      <pubDate>{xml_escape(item["pub_date"])}</pubDate>
      <description>{xml_escape(item["description"])}</description>
    </item>""")

    items_xml = "\n".join(item_blocks)

    return f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
  <channel>
    <title>{xml_escape(config["title"])}</title>
    <link>{xml_escape(config["link"])}</link>
    <description>{xml_escape(config["description"])}</description>
    <language>en</language>
    <lastBuildDate>{xml_escape(last_build_date)}</lastBuildDate>
{items_xml}
  </channel>
</rss>
"""


def generate_channel_feed(channel_key: str) -> None:
    """Generate RSS feed for a specific channel."""
    config = CHANNELS[channel_key]
    pages = discover_channel_pages(config["dir"])

    items = [extract_item_data(page) for page in pages]
    items.sort(key=lambda x: x["sort_date"], reverse=True)

    config["dir"].mkdir(exist_ok=True)
    rss_xml = build_rss_xml(channel_key, items)
    config["feed_path"].write_text(rss_xml, encoding="utf-8")

    print(
        f"[✓] {channel_key}/feed.xml generated — "
        f"{len(items[:MAX_ITEMS_PER_FEED])} item(s)"
    )


def generate_all_feeds() -> None:
    """Generate all channel feeds."""
    for channel_key in CHANNELS:
        generate_channel_feed(channel_key)


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("ShovelsSale.com — Multi-Channel RSS Engine")
    print("=" * 60 + "\n")

    generate_all_feeds()

    print("\n[✓] RSS generation complete.\n")
