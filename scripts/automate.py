"""
ShovelsSale.com - Weekly Automation Script
Generates updated content and sitemap automatically.
Run locally or via GitHub Actions every week.
"""

import json
import os
from datetime import datetime, date

# ============================================================
# CONFIG
# ============================================================
SITE_URL = "https://shovelssale.com"
TODAY = date.today().isoformat()
NOW = datetime.now().strftime("%Y-%m-%d %H:%M")

# ============================================================
# 1. UPDATE SITEMAP
# ============================================================
def update_sitemap(pages: list[dict]) -> str:
    """Generate fresh sitemap.xml with today's dates."""
    urls = ""
    for page in pages:
        urls += f"""  <url>
    <loc>{SITE_URL}{page['path']}</loc>
    <lastmod>{TODAY}</lastmod>
    <changefreq>{page.get('freq', 'weekly')}</changefreq>
    <priority>{page.get('priority', '0.8')}</priority>
  </url>\n"""

    sitemap = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{urls}</urlset>"""

    with open("sitemap.xml", "w") as f:
        f.write(sitemap)

    print(f"[✓] sitemap.xml updated — {TODAY}")
    return sitemap


# ============================================================
# 2. GENERATE BLOG POST TEMPLATE
# ============================================================
def generate_blog_post(title: str, slug: str, content: str, category: str = "Strategy") -> str:
    """Generate a complete HTML blog post page."""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} — ShovelsSale.com</title>
  <meta name="description" content="{title}. Pick-and-shovel strategy for the AI era.">
  <link rel="canonical" href="{SITE_URL}/blog/{slug}/">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;1,300&family=Bebas+Neue&family=DM+Mono:wght@300;400&display=swap" rel="stylesheet">
  <style>
    :root {{
      --gold: #C9A84C; --gold-dim: #7A5F2A;
      --black: #080808; --dark: #0E0E0E; --dark-2: #141414;
      --white: #F5F0E8; --white-dim: #9A9080;
    }}
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{ background: var(--black); color: var(--white); font-family: 'Cormorant Garamond', serif; }}
    nav {{ padding: 1.5rem 3rem; display: flex; justify-content: space-between; border-bottom: 1px solid rgba(201,168,76,0.1); }}
    .nav-logo {{ font-family: 'DM Mono', monospace; font-size: 0.75rem; color: var(--gold); text-decoration: none; letter-spacing: 0.15em; }}
    .back {{ font-family: 'DM Mono', monospace; font-size: 0.65rem; color: var(--white-dim); text-decoration: none; letter-spacing: 0.1em; }}
    .back:hover {{ color: var(--gold); }}
    article {{ max-width: 720px; margin: 0 auto; padding: 5rem 2rem; }}
    .post-meta {{ font-family: 'DM Mono', monospace; font-size: 0.6rem; color: var(--gold); letter-spacing: 0.2em; text-transform: uppercase; margin-bottom: 2rem; }}
    h1 {{ font-family: 'Bebas Neue', sans-serif; font-size: clamp(2.5rem, 7vw, 5rem); line-height: 0.95; margin-bottom: 2.5rem; }}
    .content p {{ font-size: 1.2rem; line-height: 1.85; color: #D0C8B8; margin-bottom: 1.5rem; }}
    .content h2 {{ font-family: 'Bebas Neue', sans-serif; font-size: 2rem; color: var(--gold); margin: 3rem 0 1rem; }}
    .content strong {{ color: var(--white); }}
    footer {{ text-align: center; padding: 3rem; border-top: 1px solid rgba(201,168,76,0.1); }}
    footer a {{ font-family: 'DM Mono', monospace; font-size: 0.65rem; color: var(--gold); text-decoration: none; letter-spacing: 0.15em; }}
  </style>
</head>
<body>
  <nav>
    <a href="/" class="nav-logo">ShovelsSale.com</a>
    <a href="/blog/" class="back">← All Articles</a>
  </nav>
  <article>
    <p class="post-meta">{category} — {TODAY}</p>
    <h1>{title}</h1>
    <div class="content">
      {content}
    </div>
  </article>
  <footer>
    <a href="/">ShovelsSale.com — The Philosophy of Winning Without Gambling.</a>
  </footer>
</body>
</html>"""

    os.makedirs(f"blog/{slug}", exist_ok=True)
    with open(f"blog/{slug}/index.html", "w") as f:
        f.write(html)

    print(f"[✓] Blog post created: blog/{slug}/index.html")
    return html


# ============================================================
# 3. UPDATE BLOG INDEX
# ============================================================
def update_blog_index(posts: list[dict]) -> None:
    """Generate blog listing page."""

    cards = ""
    for post in posts:
        cards += f"""
      <a href="/blog/{post['slug']}/" class="post-card">
        <span class="post-category">{post.get('category', 'Strategy')}</span>
        <h2>{post['title']}</h2>
        <p>{post.get('excerpt', '')}</p>
        <span class="post-date">{post.get('date', TODAY)}</span>
      </a>"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Blog — ShovelsSale.com</title>
  <meta name="description" content="Pick-and-shovel strategy articles for the AI era. Updated weekly.">
  <link rel="canonical" href="{SITE_URL}/blog/">
  <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,600&family=Bebas+Neue&family=DM+Mono:wght@300;400&display=swap" rel="stylesheet">
  <style>
    :root {{ --gold: #C9A84C; --black: #080808; --dark-2: #141414; --white: #F5F0E8; --white-dim: #9A9080; --gold-dim: #7A5F2A; }}
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{ background: var(--black); color: var(--white); font-family: 'Cormorant Garamond', serif; }}
    nav {{ padding: 1.5rem 3rem; display: flex; justify-content: space-between; border-bottom: 1px solid rgba(201,168,76,0.1); }}
    .nav-logo {{ font-family: 'DM Mono', monospace; font-size: 0.75rem; color: var(--gold); text-decoration: none; letter-spacing: 0.15em; }}
    .back {{ font-family: 'DM Mono', monospace; font-size: 0.65rem; color: var(--white-dim); text-decoration: none; }}
    .back:hover {{ color: var(--gold); }}
    .blog-header {{ padding: 5rem 3rem 3rem; max-width: 900px; margin: 0 auto; }}
    .blog-title {{ font-family: 'Bebas Neue', sans-serif; font-size: clamp(3rem, 8vw, 6rem); line-height: 0.9; margin-bottom: 1rem; }}
    .blog-title span {{ color: var(--gold); }}
    .blog-sub {{ font-style: italic; color: var(--white-dim); font-size: 1.1rem; }}
    .posts-grid {{ max-width: 900px; margin: 0 auto; padding: 2rem 3rem 6rem; display: grid; gap: 2px; }}
    .post-card {{ background: var(--dark-2); padding: 2.5rem; text-decoration: none; display: block; transition: background 0.3s; border-left: 3px solid transparent; }}
    .post-card:hover {{ background: #1A1A1A; border-left-color: var(--gold); }}
    .post-category {{ font-family: 'DM Mono', monospace; font-size: 0.6rem; color: var(--gold); letter-spacing: 0.2em; text-transform: uppercase; }}
    .post-card h2 {{ font-family: 'Cormorant Garamond', serif; font-size: 1.5rem; font-weight: 600; color: var(--white); margin: 0.5rem 0; }}
    .post-card p {{ font-size: 1rem; color: var(--white-dim); line-height: 1.6; margin-bottom: 1rem; }}
    .post-date {{ font-family: 'DM Mono', monospace; font-size: 0.6rem; color: var(--white-dim); opacity: 0.4; }}
    footer {{ text-align: center; padding: 3rem; border-top: 1px solid rgba(201,168,76,0.1); }}
    footer a {{ font-family: 'DM Mono', monospace; font-size: 0.65rem; color: var(--gold); text-decoration: none; }}
  </style>
</head>
<body>
  <nav>
    <a href="/" class="nav-logo">ShovelsSale.com</a>
    <a href="/" class="back">← Home</a>
  </nav>
  <div class="blog-header">
    <h1 class="blog-title">The <span>Shovels</span><br>Chronicles.</h1>
    <p class="blog-sub">Pick-and-shovel strategy for the AI era. Updated weekly.</p>
  </div>
  <div class="posts-grid">
    {cards}
  </div>
  <footer>
    <a href="/">ShovelsSale.com — The Philosophy of Winning Without Gambling.</a>
  </footer>
</body>
</html>"""

    os.makedirs("blog", exist_ok=True)
    with open("blog/index.html", "w") as f:
        f.write(html)
    print(f"[✓] Blog index updated with {len(posts)} posts")


# ============================================================
# 4. MAIN — RUN WEEKLY
# ============================================================
if __name__ == "__main__":
    print(f"\n{'='*50}")
    print(f"ShovelsSale.com Automation — {NOW}")
    print(f"{'='*50}\n")

    # UPDATE SITEMAP
    pages = [
        {"path": "/", "freq": "weekly", "priority": "1.0"},
        {"path": "/blog/", "freq": "weekly", "priority": "0.9"},
        {"path": "/manifesto/", "freq": "monthly", "priority": "0.8"},
        {"path": "/guide/", "freq": "weekly", "priority": "0.9"},
    ]
    update_sitemap(pages)

    # SAMPLE BLOG POST (add new posts here weekly)
    posts = [
        {
            "title": "Why Pick-and-Shovel Wins in 2026",
            "slug": "pick-and-shovel-wins-2026",
            "category": "Strategy",
            "date": "2026-02-22",
            "excerpt": "Every gold rush has two kinds of players. Here's why the shovel sellers always win.",
        },
        {
            "title": "Top 10 AI Infrastructure Plays Right Now",
            "slug": "top-ai-infrastructure-plays",
            "category": "Investing",
            "date": "2026-02-22",
            "excerpt": "The undervalued picks and shovels of the AI boom that most people are ignoring.",
        },
    ]

    # Generate first post as example
    generate_blog_post(
        title=posts[0]["title"],
        slug=posts[0]["slug"],
        category=posts[0]["category"],
        content="""
        <p>In 1849, thousands of men left their homes, their families, their entire lives — chasing gold in California.</p>
        <p>Most of them came back with nothing. Sunburned. Broken. Empty-handed.</p>
        <p>But one man saw something different. <strong>Levi Strauss</strong> looked at thousands of desperate miners and asked a single question:</p>
        <p><em>"What do they all need?"</em></p>
        <h2>The Pattern Repeats</h2>
        <p>Today, the gold rush is AI. Billions are pouring into startups racing to build the next ChatGPT. Everyone wants to be the miner.</p>
        <p>But the pick-and-shovel strategy says: don't bet on which model wins. Build the infrastructure every model needs.</p>
        <p>NVIDIA didn't bet on which AI startup would succeed. They sold GPUs to all of them. Today they are a $3 trillion company.</p>
        <h2>The Shovels of 2026</h2>
        <p>The shovels of the AI era are not made of wood and steel. They are GPU clusters, data center cooling systems, open-source pipelines, and premium digital real estate.</p>
        <p>The miners need all of these. And they need them now.</p>
        <p><strong>That is the philosophy of ShovelsSale.com.</strong> Not to join the rush. To own the tools the rush depends on.</p>
        """
    )

    update_blog_index(posts)

    print(f"\n[✓] All done. Commit and push via GitHub Desktop.\n")
