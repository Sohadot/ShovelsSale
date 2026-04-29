#!/usr/bin/env python3
"""
Sovereign quality gate orchestrator for ShovelsSale.com.

Purpose:
    Run the local validation suite as a single publication gate.

    This script turns the governance policies in QUALITY_GATE.md, SEO_POLICY.md,
    and the local constitutional framework into an executable quality checkpoint.

Checks:
    1. Content integrity
    2. Internal link integrity
    3. Local asset reference integrity
    4. SEO and sitemap integrity

Usage:
    python scripts/quality_gate.py
    python scripts/quality_gate.py --root .
    python scripts/quality_gate.py --json-dir reports
    python scripts/quality_gate.py --strict-og

Exit codes:
    0 = all validators passed
    1 = one or more validators failed
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class GateCheck:
    name: str
    script_name: str
    report_name: str
    description: str


CHECKS = [
    GateCheck(
        name="Content Integrity Gate",
        script_name="validate_content.py",
        report_name="content_validation.json",
        description="Detects placeholder, unfinished, or weak public content.",
    ),
    GateCheck(
        name="Link Integrity Gate",
        script_name="validate_links.py",
        report_name="link_validation.json",
        description="Detects broken internal links and missing anchor targets.",
    ),
    GateCheck(
        name="Asset Integrity Gate",
        script_name="validate_assets.py",
        report_name="asset_validation.json",
        description="Detects missing local CSS, JS, image, icon, manifest, and social preview assets.",
    ),
    GateCheck(
        name="SEO Integrity Gate",
        script_name="validate_seo.py",
        report_name="seo_validation.json",
        description="Detects missing metadata, canonical problems, robots issues, and sitemap coverage failures.",
    ),
]


def repository_root_from_this_file() -> Path:
    return Path(__file__).resolve().parents[1]


def print_header(root: Path) -> None:
    print("=" * 78)
    print("ShovelsSale.com Sovereign Quality Gate")
    print("=" * 78)
    print(f"Repository root: {root}")
    print()
    print("This gate validates whether the asset is safe to publish or merge.")
    print("Any failed validator means the change must be fixed before completion.")
    print()


def run_check(
    check: GateCheck,
    root: Path,
    scripts_dir: Path,
    json_dir: Path | None,
    strict_og: bool,
) -> int:
    script_path = scripts_dir / check.script_name

    print("-" * 78)
    print(check.name)
    print("-" * 78)
    print(check.description)

    if not script_path.exists():
        print(f"FAILED: missing validator script: {script_path}")
        print()
        return 1

    command = [
        sys.executable,
        str(script_path),
        "--root",
        str(root),
    ]

    if json_dir is not None:
        json_dir.mkdir(parents=True, exist_ok=True)
        command.extend(["--json", str(json_dir / check.report_name)])

    if check.script_name == "validate_seo.py" and strict_og:
        command.append("--strict-og")

    print(f"Running: {' '.join(command)}")
    print()
    sys.stdout.flush()

    completed = subprocess.run(command, cwd=root)

    print()

    if completed.returncode == 0:
        print(f"PASS: {check.name}")
    else:
        print(f"FAIL: {check.name} returned exit code {completed.returncode}")

    print()

    return completed.returncode


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run the ShovelsSale.com sovereign quality gate.")
    parser.add_argument(
        "--root",
        default=None,
        help="Repository root. Defaults to the parent directory of this script's directory.",
    )
    parser.add_argument(
        "--json-dir",
        default=None,
        help="Optional directory for JSON reports, for example reports/quality-gate.",
    )
    parser.add_argument(
        "--strict-og",
        action="store_true",
        help="Pass --strict-og to validate_seo.py, making missing Open Graph metadata an error.",
    )
    parser.add_argument(
        "--continue-on-failure",
        action="store_true",
        help="Run all checks even if an earlier check fails. This is the default behavior.",
    )
    parser.add_argument(
        "--fail-fast",
        action="store_true",
        help="Stop immediately after the first failed check.",
    )

    args = parser.parse_args(argv)

    root = Path(args.root).resolve() if args.root else repository_root_from_this_file()
    scripts_dir = root / "scripts"
    json_dir = Path(args.json_dir).resolve() if args.json_dir else None

    if not root.exists():
        print(f"Repository root does not exist: {root}", file=sys.stderr)
        return 1

    if not scripts_dir.exists():
        print(f"Scripts directory does not exist: {scripts_dir}", file=sys.stderr)
        return 1

    print_header(root)

    failed_checks: list[str] = []

    for check in CHECKS:
        result = run_check(
            check=check,
            root=root,
            scripts_dir=scripts_dir,
            json_dir=json_dir,
            strict_og=args.strict_og,
        )

        if result != 0:
            failed_checks.append(check.name)

            if args.fail_fast:
                break

    print("=" * 78)
    print("Quality Gate Summary")
    print("=" * 78)

    if not failed_checks:
        print("PASS: All quality gate checks passed.")
        print()
        print("The current repository state satisfies the active local quality gate.")
        return 0

    print(f"FAIL: {len(failed_checks)} quality gate check(s) failed.")
    print()
    for name in failed_checks:
        print(f"- {name}")

    print()
    print("Do not publish, merge, or treat this change as complete until the failures are fixed.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
