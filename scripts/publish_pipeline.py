import subprocess
import sys

def run_step(name, command):
    print(f"\n=== {name} ===\n")
    result = subprocess.run(command)

    if result.returncode != 0:
        print(f"\n❌ Error in {name}")
        sys.exit(1)

    print(f"\n✔ {name} completed")

if __name__ == "__main__":
    print("\n🚀 ShovelsSale Publishing Pipeline\n")

    run_step("Updating Sitemap", ["python", "scripts/update_sitemap.py"])
    run_step("Generating RSS", ["python", "scripts/generate_rss.py"])

    print("\n🔥 Pipeline executed successfully\n")
