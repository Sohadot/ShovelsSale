import os
from datetime import datetime
import xml.etree.ElementTree as ET

SITE_URL = "https://shovelssale.com"
TODAY = datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")

SKIP_DIRS = {'.git', 'scripts', 'node_modules', '.github'}
SKIP_FILES = {'404.html'}

# ==============================
# CONTENT CLASSIFICATION SYSTEM
# ==============================
CONTENT_RULES = {
    '/dispatch/': {
        'type': 'dispatch',
        'priority_index': '0.9',
        'priority_page': '0.8',
        'freq_index': 'weekly',
        'freq_page': 'monthly'
    },
    '/blog/': {
        'type': 'blog',
        'priority_index': '0.8',
        'priority_page': '0.7',
        'freq_index': 'weekly',
        'freq_page': 'monthly'
    },
    '/guide/': {
        'type': 'guide',
        'priority_index': '0.9',
        'priority_page': '0.8',
        'freq_index': 'weekly',
        'freq_page': 'monthly'
    },
    '/framework/': {
        'type': 'core',
        'priority_index': '0.95',
        'priority_page': '0.9',
        'freq_index': 'monthly',
        'freq_page': 'monthly'
    },
    '/manifesto/': {
        'type': 'core',
        'priority_index': '0.95',
        'priority_page': '0.9',
        'freq_index': 'monthly',
        'freq_page': 'monthly'
    }
}

def classify(url_path):
    for base, config in CONTENT_RULES.items():
        if url_path.startswith(base):
            if url_path == base:
                return config, config['priority_index'], config['freq_index']
            return config, config['priority_page'], config['freq_page']
    return None, '0.7', 'weekly'

# ==============================
# DISCOVER PAGES
# ==============================
def discover_pages():
    pages = []

    for root, dirs, files in os.walk("."):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]

        for file in files:
            if not file.endswith(".html") or file in SKIP_FILES:
                continue

            path = os.path.join(root, file)

            url_path = path.replace("\\", "/").replace("./", "/")
            url_path = url_path.replace("index.html", "")

            if url_path == "":
                url_path = "/"

            config, priority, freq = classify(url_path)

            pages.append({
                "url": f"{SITE_URL}{url_path}",
                "path": url_path,
                "priority": priority,
                "freq": freq,
                "type": config['type'] if config else 'general'
            })

    return pages

# ==============================
# GENERATE SITEMAP
# ==============================
def generate_sitemap(pages):
    urlset = ET.Element("urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")

    for p in pages:
        url = ET.SubElement(urlset, "url")
        ET.SubElement(url, "loc").text = p["url"]
        ET.SubElement(url, "lastmod").text = datetime.utcnow().date().isoformat()
        ET.SubElement(url, "changefreq").text = p["freq"]
        ET.SubElement(url, "priority").text = p["priority"]

    tree = ET.ElementTree(urlset)
    tree.write("sitemap.xml", encoding="utf-8", xml_declaration=True)

# ==============================
# GENERATE RSS (MULTI CHANNEL)
# ==============================
def generate_rss(pages):
    grouped = {}

    for p in pages:
        t = p["type"]
        if t not in grouped:
            grouped[t] = []
        grouped[t].append(p)

    for content_type, items in grouped.items():

        rss = ET.Element("rss", version="2.0")
        channel = ET.SubElement(rss, "channel")

        ET.SubElement(channel, "title").text = f"ShovelsSale {content_type.capitalize()}"
        ET.SubElement(channel, "link").text = f"{SITE_URL}/{content_type}/"
        ET.SubElement(channel, "description").text = f"{content_type} feed"
        ET.SubElement(channel, "lastBuildDate").text = TODAY

        for item in items[:20]:  # limit
            entry = ET.SubElement(channel, "item")
            ET.SubElement(entry, "title").text = item["url"].split("/")[-1]
            ET.SubElement(entry, "link").text = item["url"]
            ET.SubElement(entry, "guid").text = item["url"]
            ET.SubElement(entry, "pubDate").text = TODAY

        filename = f"{content_type}_feed.xml"
        ET.ElementTree(rss).write(filename, encoding="utf-8", xml_declaration=True)

# ==============================
# MAIN
# ==============================
if __name__ == "__main__":
    print("\n=== Publishing Engine ===\n")

    pages = discover_pages()
    print(f"Discovered: {len(pages)} pages")

    generate_sitemap(pages)
    print("✔ sitemap.xml updated")

    generate_rss(pages)
    print("✔ RSS feeds generated")

    print("\n✔ System fully updated\n")
