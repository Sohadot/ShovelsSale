"""
ShovelsSale.com — Auto Sitemap Updater
Discovers all HTML pages and generates fresh sitemap.xml
Runs weekly via GitHub Actions after content update.
"""

import os
from datetime import date

SITE_URL = "https://shovelssale.com"
TODAY = date.today().isoformat()
SKIP_DIRS = {'.git', 'scripts', 'node_modules', '.github'}
SKIP_FILES = {'404.html', 'google-verification.html'}

# Priority map by path depth and type
PRIORITY_MAP = {
    '/': '1.0',
    '/about/': '0.9',
    '/manifesto/': '0.95',
    '/guide/': '0.9',
    '/blog/': '0.85',
}

FREQ_MAP = {
    '/': 'weekly',
    '/manifesto/': 'monthly',
    '/about/': 'monthly',
    '/guide/': 'weekly',
    '/blog/': 'weekly',
}


def discover_pages() -> list[dict]:
    """Walk directory and find all public HTML pages."""
    pages = []

    for root, dirs, files in os.walk('.'):
        dirs[:] = sorted([d for d in dirs if d not in SKIP_DIRS])

        for filename in files:
            if filename not in ['index.html'] or filename in SKIP_FILES:
                continue

            filepath = os.path.join(root, filename)

            # Convert filesystem path to URL path
            url_path = filepath.replace('./', '/').replace('/index.html', '/')
            if url_path == '//':
                url_path = '/'

            # Determine priority and frequency
            priority = PRIORITY_MAP.get(url_path, '0.7')
            freq = FREQ_MAP.get(url_path, 'weekly')

            # Blog posts get lower priority
            if '/blog/' in url_path and url_path != '/blog/':
                priority = '0.7'
                freq = 'monthly'

            pages.append({
                'url': f"{SITE_URL}{url_path}",
                'lastmod': TODAY,
                'changefreq': freq,
                'priority': priority,
            })

    # Sort: home first, then by priority descending
    pages.sort(key=lambda p: (0 if p['url'] == f"{SITE_URL}/" else 1, -float(p['priority'])))

    return pages


def generate_sitemap(pages: list[dict]) -> None:
    """Generate sitemap.xml from discovered pages."""
    urls = ""
    for page in pages:
        urls += f"""  <url>
    <loc>{page['url']}</loc>
    <lastmod>{page['lastmod']}</lastmod>
    <changefreq>{page['changefreq']}</changefreq>
    <priority>{page['priority']}</priority>
  </url>\n"""

    sitemap = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:schemaLocation="http://www.sitemaps.org/schemas/sitemap/0.9
        http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd">
{urls}</urlset>"""

    with open('sitemap.xml', 'w') as f:
        f.write(sitemap)

    print(f"[✓] sitemap.xml updated — {len(pages)} pages — {TODAY}")
    for p in pages:
        print(f"    {p['priority']} | {p['url']}")


if __name__ == '__main__':
    print(f"\n{'='*50}")
    print(f"Sitemap Generator — {TODAY}")
    print(f"{'='*50}\n")

    pages = discover_pages()
    generate_sitemap(pages)

    print(f"\n[✓] Done. Push via GitHub Desktop to update live site.\n")
