import subprocess

print("\n=== ShovelsSale Publishing Pipeline ===\n")

print("1. Updating sitemap...")
subprocess.run(["python", "scripts/update_sitemap.py"])

print("\n2. Generating RSS feeds...")
subprocess.run(["python", "scripts/generate_rss.py"])

print("\n✔ Pipeline completed successfully\n")
