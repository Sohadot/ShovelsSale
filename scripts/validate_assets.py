#!/usr/bin/env python3
"""
Local asset reference validator for ShovelsSale.com.

Detects missing local CSS, JavaScript, image, icon, manifest, preload, poster,
and social preview asset references from public HTML files.
"""

from __future__ import annotations

import argparse
import html
import json
import posixpath
import re
import sys
from dataclasses import asdict, dataclass
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlparse


SITE_DOMAINS = {"shovelssale.com", "www.shovelssale.com"}
HTML_EXTENSIONS = {".html", ".htm"}

EXCLUDED_DIRECTORIES = {
    ".git",
    ".github",
    ".claude",
    "__pycache__",
    "node_modules",
    "reports",
    "dist",
    "build",
    "vendor",
}

EXCLUDED_FILES = {
    "google28b5398e4140f820.html",
}

IGNORED_SCHEMES = {
    "mailto",
    "tel",
    "sms",
    "javascript",
    "data",
    "blob",
}

ASSET_LINK_RELS = {
    "apple-touch-icon",
    "icon",
    "manifest",
    "modulepreload",
    "preload",
    "prefetch",
    "stylesheet",
}

ASSET_META_NAMES = {
    "msapplication-tileimage",
    "twitter:image",
    "twitter:image:src",
}

ASSET_META_PROPERTIES = {
    "og:image",
    "og:image:secure_url",
    "twitter:image",
    "twitter:image:src",
}


@dataclass(frozen=True)
class AssetReference:
    source_file: str
    line: int
    raw_value: str
    normalized_path: str
    context: str


@dataclass(frozen=True)
class Finding:
    severity: str
    file: str
    message: str
    evidence: str = ""


class AssetHTMLParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.references: list[tuple[int, str, str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        tag = tag.lower()
        attributes = {name.lower(): value for name, value in attrs if name and value}
        line, _column = self.getpos()

        if tag == "script" and attributes.get("src"):
            self.references.append((line, attributes["src"], "script src"))

        if tag in {"img", "iframe", "audio", "video", "source", "track", "embed"} and attributes.get("src"):
            self.references.append((line, attributes["src"], f"{tag} src"))

        if tag in {"img", "source"} and attributes.get("srcset"):
            for candidate in parse_srcset(attributes["srcset"]):
                self.references.append((line, candidate, f"{tag} srcset"))

        if tag == "video" and attributes.get("poster"):
            self.references.append((line, attributes["poster"], "video poster"))

        if tag == "object" and attributes.get("data"):
            self.references.append((line, attributes["data"], "object data"))

        if tag == "link" and attributes.get("href"):
            rel_values = set((attributes.get("rel") or "").lower().split())
            if rel_values & ASSET_LINK_RELS:
                self.references.append((line, attributes["href"], "link href"))

        if tag == "meta" and attributes.get("content"):
            meta_name = (attributes.get("name") or "").lower()
            meta_property = (attributes.get("property") or "").lower()
            if meta_name in ASSET_META_NAMES or meta_property in ASSET_META_PROPERTIES:
                self.references.append((line, attributes["content"], "meta content"))


def parse_srcset(value: str) -> list[str]:
    candidates: list[str] = []
    for part in value.split(","):
        candidate = part.strip().split()
        if candidate:
            candidates.append(candidate[0])
    return candidates


def safe_read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8", errors="replace")


def is_excluded(path: Path, root: Path) -> bool:
    relative_parts = path.relative_to(root).parts
    return any(part in EXCLUDED_DIRECTORIES for part in relative_parts) or path.name in EXCLUDED_FILES


def discover_html_files(root: Path) -> list[Path]:
    return sorted(
        path
        for path in root.rglob("*")
        if path.is_file()
        and path.suffix.lower() in HTML_EXTENSIONS
        and not is_excluded(path, root)
    )


def public_url_directory_for_file(path: Path, root: Path) -> str:
    relative = path.relative_to(root).as_posix()

    if relative == "index.html":
        return "/"

    if relative.endswith("/index.html"):
        return "/" + relative[: -len("index.html")]

    parent = posixpath.dirname("/" + relative)
    return parent if parent.endswith("/") else parent + "/"


def is_same_site_absolute_url(parsed) -> bool:
    return parsed.scheme in {"http", "https"} and parsed.netloc.lower() in SITE_DOMAINS


def normalize_local_asset(value: str, source_file: Path, root: Path) -> str | None:
    value = html.unescape(value.strip())
    if not value:
        return None

    parsed = urlparse(value)

    if parsed.scheme.lower() in IGNORED_SCHEMES:
        return None

    if parsed.scheme in {"http", "https"} and not is_same_site_absolute_url(parsed):
        return None

    if parsed.scheme in {"http", "https"}:
        raw_path = parsed.path or ""
    elif value.startswith("//"):
        protocol_relative = urlparse("https:" + value)
        if not is_same_site_absolute_url(protocol_relative):
            return None
        raw_path = protocol_relative.path or ""
    else:
        raw_path = parsed.path

    raw_path = unquote(raw_path)
    if not raw_path:
        return None

    if raw_path.startswith("/"):
        normalized_path = posixpath.normpath(raw_path)
    else:
        base_directory = public_url_directory_for_file(source_file, root)
        normalized_path = posixpath.normpath(posixpath.join(base_directory, raw_path))

    if normalized_path == ".":
        return None

    return normalized_path if normalized_path.startswith("/") else "/" + normalized_path


def resolve_asset_path(normalized_path: str, root: Path) -> Path:
    return root / normalized_path.lstrip("/")


def parse_html(path: Path) -> AssetHTMLParser:
    parser = AssetHTMLParser()
    parser.feed(safe_read(path))
    return parser


def validate_assets(root: Path) -> list[Finding]:
    findings: list[Finding] = []

    for source_path in discover_html_files(root):
        parser = parse_html(source_path)
        source_relative = source_path.relative_to(root).as_posix()

        for line, raw_value, context in parser.references:
            normalized_path = normalize_local_asset(raw_value, source_path, root)
            if normalized_path is None:
                continue

            asset_path = resolve_asset_path(normalized_path, root)
            if asset_path.exists() and asset_path.is_file():
                continue

            findings.append(
                Finding(
                    severity="error",
                    file=source_relative,
                    message=f"Missing local asset reference at line {line}.",
                    evidence=f"{context}: {raw_value} -> {normalized_path}",
                )
            )

    return findings


def print_human_report(findings: list[Finding]) -> None:
    if not findings:
        print("Asset validation passed. No missing local asset references found.")
        return

    print("Asset validation completed with findings.")
    print(f"Errors: {len(findings)}")
    print()

    for finding in findings:
        print(f"[{finding.severity.upper()}] {finding.file}")
        print(f"  {finding.message}")
        if finding.evidence:
            print(f"  Evidence: {finding.evidence}")
        print()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate local asset references for ShovelsSale.com.")
    parser.add_argument("--root", default=None, help="Repository root. Defaults to the parent directory of this script.")
    parser.add_argument("--json", default=None, help="Optional path to write a JSON report.")
    args = parser.parse_args(argv)

    root = Path(args.root).resolve() if args.root else Path(__file__).resolve().parents[1]
    if not root.exists():
        print(f"Repository root does not exist: {root}", file=sys.stderr)
        return 1

    findings = validate_assets(root)

    if args.json:
        report_path = Path(args.json)
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(json.dumps([asdict(f) for f in findings], indent=2), encoding="utf-8")

    print_human_report(findings)
    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
