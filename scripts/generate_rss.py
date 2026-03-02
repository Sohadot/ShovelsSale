"""
ShovelsSale.com — RSS Feed Auto-Generator
Builds feed.xml from blog posts automatically.
Runs weekly via GitHub Actions — enables RSS-to-email via Beehiiv/EmailOctopus.
"""

import os
import json
from datetime import datetime, date
from email.utils import formatdate
import time

SITE_URL = "https://shovelssale.com"
SITE_TITLE = "ShovelsSale.com — The Shovels Chronicles"
SITE_DESC = "Pick-and-shovel strategy for the AI era. Weekly insights for those who sell shovels while the world mines for gold."
FEED_URL = f"{SITE_URL}/feed.xml"
MAX_ITEMS = 20  # Max posts in feed


def date_to_rfc2822(date_str: str) -> str:
    """Convert YYYY-MM-DD to RFC 2822 format for RSS."""
    dt = datetime.strptime(date_str, "%Y-%m-%d")
    return formatdate(time.mktime(dt.timetuple()))


def discover_posts() -> list[dict]:
    """Find all blog posts from blog/ directory."""
    posts = []
    blog_dir = "blog"

    if not os.path.exists(blog_dir):
        return posts

    for slug in os.listdir(blog_dir):
        post_path = os.path.join(blog_dir, slug, "index.html")
        meta_path = os.path.join(blog_dir, slug, "meta.json")

        if not os.path.exists(post_path):
            continue

        # Load metadata if exists
        meta = {}
        if os.path.exists(meta_path):
            with open(meta_path) as f:
                meta = json.load(f)

        posts.append({
            "slug": slug,
            "title": meta.get("title", slug.replace("-", " ").title()),
            "date": meta.get("date", date.today().isoformat()),
            "category": meta.get("category", "Strategy"),
            "excerpt": meta.get("excerpt", ""),
            "url": f"{SITE_URL}/blog/{slug}/",
        })

    # Sort by date descending
    posts.sort(key=lambda p: p["date"], reverse=True)
    return posts[:MAX_ITEMS]


def generate_rss(posts: list[dict]) -> None:
    """Generate feed.xml from posts list."""
    build_date = formatdate(time.time())

    items = ""
    for post in posts:
        pub_date = date_to_rfc2822(post["date"])
        items += f"""
    <item>
      <title>{post['title']}</title>
      <link>{post['url']}</link>
      <guid isPermaLink="true">{post['url']}</guid>
      <pubDate>{pub_date}</pubDate>
      <dc:creator>ShovelsSale.com</dc:creator>
      <category>{post['category']}</category>
      <description>{post['excerpt']}</description>
      <content:encoded><![CDATA[
        <p>{post['excerpt']}</p>
        <p><a href="{post['url']}">Read the full article →</a></p>
      ]]></content:encoded>
    </item>"""

    rss = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0"
  xmlns:atom="http://www.w3.org/2005/Atom"
  xmlns:dc="http://purl.org/dc/elements/1.1/"
  xmlns:content="http://purl.org/rss/1.0/modules/content/">

  <channel>
    <title>{SITE_TITLE}</title>
    <link>{SITE_URL}</link>
    <description>{SITE_DESC}</description>
    <language>en-us</language>
    <lastBuildDate>{build_date}</lastBuildDate>
    <managingEditor>hello@shovelssale.com</managingEditor>
    <ttl>10080</ttl>
    <atom:link href="{FEED_URL}" rel="self" type="application/rss+xml"/>
    {items}
  </channel>
</rss>"""

    with open("feed.xml", "w") as f:
        f.write(rss)

    print(f"[✓] feed.xml updated — {len(posts)} posts — {date.today()}")


if __name__ == "__main__":
    print(f"\n{'='*50}")
    print(f"RSS Feed Generator — {date.today()}")
    print(f"{'='*50}\n")

    posts = discover_posts()
    generate_rss(posts)
    print("[✓] RSS feed ready. Beehiiv/EmailOctopus can now auto-send weekly digest.\n")
