"""
ShovelsSale.com — Content Automation Engine

Purpose:
- Discover real blog posts from the repository
- Extract structured metadata from existing HTML files
- Rebuild blog/index.html as a high-quality archive page
- Support the publishing pipeline without duplicating sitemap/RSS responsibilities

This script DOES NOT:
- generate fake posts
- update sitemap.xml
- generate RSS feeds

Those responsibilities belong to:
- scripts/update_sitemap.py
- scripts/generate_rss.py
"""

from __future__ import annotations

import os
import re
import html
from pathlib import Path
from datetime import datetime, UTC
from typing import Optional, Dict, List
from bs4 import BeautifulSoup


# ============================================================
# CONFIG
# ============================================================

SITE_URL = "https://shovelssale.com"
ROOT_DIR = Path(".")
BLOG_DIR = ROOT_DIR / "blog"
BLOG_INDEX_PATH = BLOG_DIR / "index.html"

SKIP_DIRS = {
    ".git",
    ".github",
    "node_modules",
    "scripts",
    "assets",
    ".well-known",
}

BLOG_ARCHIVE_TITLE = "The <span>Shovels</span><br>Chronicles."
BLOG_ARCHIVE_SUBTITLE = (
    "A structured archive of market infrastructure, shovel economy strategy, "
    "and system-level analysis from ShovelsSale.com."
)


# ============================================================
# HELPERS
# ============================================================

def safe_read_text(path: Path) -> str:
    """Read file safely as UTF-8."""
    return path.read_text(encoding="utf-8", errors="ignore")


def extract_title(soup: BeautifulSoup) -> str:
    """Extract the most suitable title from the page."""
    og_title = soup.find("meta", attrs={"property": "og:title"})
    if og_title and og_title.get("content"):
        return og_title["content"].strip()

    if soup.title and soup.title.string:
        return soup.title.string.strip().split("—")[0].strip()

    h1 = soup.find("h1")
    if h1:
        return h1.get_text(" ", strip=True)

    return "Untitled Post"


def extract_description(soup: BeautifulSoup) -> str:
    """Extract page description."""
    meta_desc = soup.find("meta", attrs={"name": "description"})
    if meta_desc and meta_desc.get("content"):
        return meta_desc["content"].strip()

    og_desc = soup.find("meta", attrs={"property": "og:description"})
    if og_desc and og_desc.get("content"):
        return og_desc["content"].strip()

    first_p = soup.find("p")
    if first_p:
        return first_p.get_text(" ", strip=True)[:220]

    return "ShovelsSale.com publication."


def extract_canonical_slug(soup: BeautifulSoup, fallback_slug: str) -> str:
    """Extract slug from canonical URL if present."""
    canonical = soup.find("link", attrs={"rel": "canonical"})
    if canonical and canonical.get("href"):
        href = canonical["href"].strip()
        match = re.search(r"/blog/([^/]+)/?$", href)
        if match:
            return match.group(1)
    return fallback_slug


def extract_date_from_jsonld(soup: BeautifulSoup) -> Optional[str]:
    """Extract ISO date from JSON-LD blocks if present."""
    scripts = soup.find_all("script", attrs={"type": "application/ld+json"})
    for script in scripts:
        content = script.string or script.get_text(strip=True)
        if not content:
            continue

        match = re.search(r'"datePublished"\s*:\s*"([^"]+)"', content)
        if match:
            return match.group(1)[:10]

        match = re.search(r'"dateModified"\s*:\s*"([^"]+)"', content)
        if match:
            return match.group(1)[:10]

    return None


def extract_date_from_meta(soup: BeautifulSoup) -> Optional[str]:
    """Extract date from meta tags if present."""
    candidates = [
        ("property", "article:published_time"),
        ("property", "article:modified_time"),
        ("name", "date"),
        ("name", "publish_date"),
    ]

    for attr_name, attr_value in candidates:
        meta = soup.find("meta", attrs={attr_name: attr_value})
        if meta and meta.get("content"):
            return meta["content"].strip()[:10]

    return None


def normalize_date(raw_date: Optional[str], file_path: Path) -> str:
    """
    Normalize date to YYYY-MM-DD.
    If missing, fallback to file modification date.
    """
    if raw_date:
        try:
            return datetime.fromisoformat(raw_date.replace("Z", "")).date().isoformat()
        except ValueError:
            pass

    return datetime.fromtimestamp(file_path.stat().st_mtime, UTC).date().isoformat()


def infer_category(soup: BeautifulSoup, slug: str) -> str:
    """
    Infer category from page markup or slug.
    Keeps categories editorially broad and premium.
    """
    category_sources = []

    meta_section = soup.find("meta", attrs={"name": "article:section"})
    if meta_section and meta_section.get("content"):
        category_sources.append(meta_section["content"].strip())

    post_meta = soup.find(class_=re.compile(r"post-meta|article-meta|meta", re.I))
    if post_meta:
        text = post_meta.get_text(" ", strip=True)
        if text:
            category_sources.append(text)

    joined = " ".join(category_sources).lower() + " " + slug.lower()

    if any(word in joined for word in ["dispatch", "scanner", "classification"]):
        return "Classification"
    if any(word in joined for word in ["infrastructure", "compute", "stack"]):
        return "Infrastructure"
    if any(word in joined for word in ["strategy", "shovel", "market"]):
        return "Strategy"
    if any(word in joined for word in ["guide", "method", "framework"]):
        return "Method"

    return "Analysis"


def extract_excerpt(description: str) -> str:
    """Create a clean archive excerpt."""
    description = re.sub(r"\s+", " ", description).strip()
    if len(description) <= 180:
        return description
    return description[:177].rstrip() + "..."


def discover_blog_posts() -> List[Dict[str, str]]:
    """
    Discover real blog posts from blog/*/index.html.
    Excludes blog/index.html itself.
    """
    posts: List[Dict[str, str]] = []

    if not BLOG_DIR.exists():
        return posts

    for child in BLOG_DIR.iterdir():
        if not child.is_dir():
            continue
        if child.name in SKIP_DIRS:
            continue

        post_file = child / "index.html"
        if not post_file.exists():
            continue

        raw_html = safe_read_text(post_file)
        soup = BeautifulSoup(raw_html, "lxml")

        title = extract_title(soup)
        description = extract_description(soup)
        slug = extract_canonical_slug(soup, child.name)

        raw_date = extract_date_from_jsonld(soup) or extract_date_from_meta(soup)
        date_value = normalize_date(raw_date, post_file)

        category = infer_category(soup, slug)
        excerpt = extract_excerpt(description)

        posts.append({
            "title": title,
            "slug": slug,
            "date": date_value,
            "category": category,
            "excerpt": excerpt,
            "url": f"{SITE_URL}/blog/{slug}/",
        })

    posts.sort(key=lambda x: x["date"], reverse=True)
    return posts


# ============================================================
# BLOG ARCHIVE HTML
# ============================================================

def render_blog_index(posts: List[Dict[str, str]]) -> str:
    """Render the blog archive page."""
    cards = []

    for post in posts:
        title = html.escape(post["title"])
        category = html.escape(post["category"])
        excerpt = html.escape(post["excerpt"])
        date_value = html.escape(post["date"])
        slug = html.escape(post["slug"])

        cards.append(f"""
      <a href="/blog/{slug}/" class="post-card">
        <span class="post-category">{category}</span>
        <h2>{title}</h2>
        <p>{excerpt}</p>
        <span class="post-date">{date_value}</span>
      </a>""")

    cards_html = "\n".join(cards) if cards else """
      <div class="empty-state">
        <h2>No published articles yet.</h2>
        <p>The archive will appear here as real posts are added to the system.</p>
      </div>"""

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">

  <title>Blog | ShovelsSale.com</title>
  <meta name="description" content="A structured archive of market infrastructure, shovel economy strategy, and system-level analysis from ShovelsSale.com.">
  <meta name="robots" content="index, follow">
  <link rel="canonical" href="{SITE_URL}/blog/">
  <link rel="alternate" type="application/rss+xml" title="ShovelsSale Blog" href="/blog/feed.xml">

  <meta property="og:title" content="Blog | ShovelsSale.com">
  <meta property="og:description" content="A structured archive of market infrastructure, shovel economy strategy, and system-level analysis from ShovelsSale.com.">
  <meta property="og:type" content="website">
  <meta property="og:url" content="{SITE_URL}/blog/">
  <meta property="og:site_name" content="ShovelsSale.com">

  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="Blog | ShovelsSale.com">
  <meta name="twitter:description" content="A structured archive of market infrastructure, shovel economy strategy, and system-level analysis from ShovelsSale.com.">

  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "CollectionPage",
    "name": "ShovelsSale Blog",
    "url": "{SITE_URL}/blog/",
    "description": "A structured archive of market infrastructure, shovel economy strategy, and system-level analysis from ShovelsSale.com.",
    "publisher": {{
      "@type": "Organization",
      "name": "ShovelsSale.com",
      "url": "{SITE_URL}/"
    }}
  }}
  </script>

  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,600&family=Bebas+Neue&family=DM+Mono:wght@300;400&display=swap" rel="stylesheet">

  <style>
    :root {{
      --gold: #C9A84C;
      --gold-dim: #7A5F2A;
      --black: #080808;
      --dark-2: #141414;
      --white: #F5F0E8;
      --white-dim: #9A9080;
      --line: rgba(201,168,76,0.12);
    }}

    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    html {{ scroll-behavior: smooth; }}

    body {{
      background: var(--black);
      color: var(--white);
      font-family: 'Cormorant Garamond', serif;
      overflow-x: hidden;
    }}

    nav {{
      padding: 1.5rem 3rem;
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-bottom: 1px solid var(--line);
      background: rgba(8,8,8,0.95);
      backdrop-filter: blur(10px);
      position: sticky;
      top: 0;
      z-index: 50;
    }}

    .nav-logo {{
      font-family: 'DM Mono', monospace;
      font-size: 0.75rem;
      color: var(--gold);
      text-decoration: none;
      letter-spacing: 0.15em;
      text-transform: uppercase;
    }}

    .back {{
      font-family: 'DM Mono', monospace;
      font-size: 0.65rem;
      color: var(--white-dim);
      text-decoration: none;
      letter-spacing: 0.1em;
      text-transform: uppercase;
    }}

    .back:hover {{ color: var(--gold); }}

    .blog-header {{
      padding: 5rem 3rem 3rem;
      max-width: 960px;
      margin: 0 auto;
    }}

    .blog-title {{
      font-family: 'Bebas Neue', sans-serif;
      font-size: clamp(3rem, 8vw, 6rem);
      line-height: 0.9;
      margin-bottom: 1rem;
      letter-spacing: 0.02em;
    }}

    .blog-title span {{ color: var(--gold); }}

    .blog-sub {{
      font-style: italic;
      color: var(--white-dim);
      font-size: 1.12rem;
      line-height: 1.8;
      max-width: 760px;
    }}

    .posts-grid {{
      max-width: 960px;
      margin: 0 auto;
      padding: 2rem 3rem 6rem;
      display: grid;
      gap: 2px;
    }}

    .post-card {{
      background: var(--dark-2);
      padding: 2.5rem;
      text-decoration: none;
      display: block;
      transition: background 0.3s ease, border-left-color 0.3s ease;
      border-left: 3px solid transparent;
    }}

    .post-card:hover {{
      background: #1A1A1A;
      border-left-color: var(--gold);
    }}

    .post-category {{
      font-family: 'DM Mono', monospace;
      font-size: 0.6rem;
      color: var(--gold);
      letter-spacing: 0.2em;
      text-transform: uppercase;
    }}

    .post-card h2 {{
      font-family: 'Cormorant Garamond', serif;
      font-size: 1.55rem;
      font-weight: 600;
      color: var(--white);
      margin: 0.55rem 0;
      line-height: 1.2;
    }}

    .post-card p {{
      font-size: 1rem;
      color: var(--white-dim);
      line-height: 1.7;
      margin-bottom: 1rem;
      max-width: 760px;
    }}

    .post-date {{
      font-family: 'DM Mono', monospace;
      font-size: 0.6rem;
      color: var(--white-dim);
      opacity: 0.55;
      letter-spacing: 0.1em;
      text-transform: uppercase;
    }}

    .empty-state {{
      background: var(--dark-2);
      padding: 2.5rem;
      border-left: 3px solid var(--gold-dim);
    }}

    .empty-state h2 {{
      font-size: 1.5rem;
      margin-bottom: 0.6rem;
    }}

    .empty-state p {{
      color: var(--white-dim);
      line-height: 1.7;
    }}

    footer {{
      text-align: center;
      padding: 3rem;
      border-top: 1px solid var(--line);
    }}

    footer a {{
      font-family: 'DM Mono', monospace;
      font-size: 0.65rem;
      color: var(--gold);
      text-decoration: none;
      letter-spacing: 0.15em;
      text-transform: uppercase;
    }}

    @media (max-width: 768px) {{
      nav {{
        padding: 1.2rem 1.25rem;
      }}

      .blog-header {{
        padding: 3.5rem 1.25rem 2rem;
      }}

      .posts-grid {{
        padding: 1rem 1.25rem 4rem;
      }}

      .post-card,
      .empty-state {{
        padding: 1.5rem;
      }}
    }}
  </style>
</head>
<body>
  <nav>
    <a href="/" class="nav-logo">ShovelsSale.com</a>
    <a href="/" class="back">← Home</a>
  </nav>

  <div class="blog-header">
    <h1 class="blog-title">{BLOG_ARCHIVE_TITLE}</h1>
    <p class="blog-sub">{BLOG_ARCHIVE_SUBTITLE}</p>
  </div>

  <div class="posts-grid">
    {cards_html}
  </div>

  <footer>
    <a href="/">ShovelsSale.com — The Philosophy of Winning Without Gambling.</a>
  </footer>
</body>
</html>"""


# ============================================================
# WRITERS
# ============================================================

def rebuild_blog_index() -> None:
    """Rebuild blog archive from real published posts."""
    posts = discover_blog_posts()
    BLOG_DIR.mkdir(exist_ok=True)

    html_output = render_blog_index(posts)
    BLOG_INDEX_PATH.write_text(html_output, encoding="utf-8")

    print(f"[✓] blog/index.html rebuilt — {len(posts)} post(s) discovered")


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("ShovelsSale.com — Content Automation Engine")
    print("=" * 60 + "\n")

    rebuild_blog_index()

    print("\n[✓] Automation complete.\n")
