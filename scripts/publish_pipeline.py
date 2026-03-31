"""
ShovelsSale.com — Publishing Pipeline

Purpose:
- Run the site's publishing steps in the correct order
- Keep responsibilities separated across scripts
- Fail safely when one stage breaks
- Serve as the single execution entry point for automation

Pipeline order:
1. automate.py        -> rebuild derived archive pages (e.g. blog index)
2. update_sitemap.py  -> rebuild sitemap from real discovered pages
3. generate_rss.py    -> rebuild channel feeds from real published pages
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


# ============================================================
# CONFIG
# ============================================================

PYTHON_EXECUTABLE = sys.executable

PIPELINE_STEPS = [
    {
        "name": "Content Automation",
        "script": "scripts/automate.py",
        "required": True,
    },
    {
        "name": "Sitemap Update",
        "script": "scripts/update_sitemap.py",
        "required": True,
    },
    {
        "name": "RSS Generation",
        "script": "scripts/generate_rss.py",
        "required": True,
    },
]


# ============================================================
# HELPERS
# ============================================================

def ensure_file_exists(path_str: str) -> None:
    """Ensure required script file exists before execution."""
    path = Path(path_str)
    if not path.exists():
        print(f"[✗] Missing required file: {path}")
        sys.exit(1)


def run_step(step: dict) -> None:
    """Run one pipeline step safely."""
    step_name = step["name"]
    script_path = step["script"]

    print("\n" + "=" * 60)
    print(f"{step_name}")
    print("=" * 60)

    ensure_file_exists(script_path)

    result = subprocess.run(
        [PYTHON_EXECUTABLE, script_path],
        check=False,
    )

    if result.returncode != 0:
        print(f"\n[✗] {step_name} failed with exit code {result.returncode}")
        if step.get("required", True):
            sys.exit(result.returncode)
        print(f"[!] {step_name} is non-critical. Continuing.")
    else:
        print(f"\n[✓] {step_name} completed successfully")


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":
    print("\n" + "#" * 60)
    print("ShovelsSale.com — Publishing Pipeline")
    print("#" * 60)

    for step in PIPELINE_STEPS:
        run_step(step)

    print("\n" + "#" * 60)
    print("[✓] Full publishing pipeline completed successfully")
    print("#" * 60 + "\n")
