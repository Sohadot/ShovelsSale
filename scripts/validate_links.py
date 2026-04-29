#!/usr/bin/env python3
"""
Internal link validator for ShovelsSale.com.

Detects broken same-site links and missing fragment anchors across public HTML
pages. External links and non-navigation schemes are intentionally ignored.
"""

from __future__ import annotations

import argparse
import html
import json
import posixpath
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
    "ftp",
}


@dataclass(frozen=True)
class Finding:
    severity: str
    file: str
    message: str
    evidence: str = ""


class LinkHTMLParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.links: list[tuple[int, str]] = []
        self.anchors: set[str] = set()

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attributes = {name.lower(): value for name, value in attrs if name}

        element_id = attributes.get("id")
        if element_id:
            self.anchors.add(element_id.strip())

        element_name = attributes.get("name")
        if tag.lower() == "a" and element_name:
            self.anchors.add(element_name.strip())

        if tag.lower() != "a":
            return

        href = attributes.get("href")
        if href:
            line, _column = self.getpos()
            self.links.append((line, href.strip()))


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


def parse_html(path: Path) -> LinkHTMLParser:
    parser = LinkHTMLParser()
    parser.feed(safe_read(path))
    return parser


def public_url_directory_for_file(path: Path, root: Path) -> str:
    relative = path.relative_to(root).as_posix()

    if relative == "index.html":
        return "/"

    if relative.endswith("/index.html"):
        return "/" + relative[: -len("index.html")]

    parent = posixpath.dirname("/" + relative)
    return parent if parent.endswith("/") else parent + "/"


def should_ignore_href(href: str) -> bool:
    if not href or href == "#":
        return True

    parsed = urlparse(href)
    return parsed.scheme.lower() in IGNORED_SCHEMES


def is_same_site_absolute_url(parsed) -> bool:
    return parsed.scheme in {"http", "https"} and parsed.netloc.lower() in SITE_DOMAINS


def normalize_internal_href(href: str, source_file: Path, root: Path) -> tuple[str, str] | None:
    href = html.unescape(href.strip())

    if should_ignore_href(href):
        return None

    parsed = urlparse(href)

    if parsed.scheme in {"http", "https"} and not is_same_site_absolute_url(parsed):
        return None

    if parsed.scheme in {"http", "https"}:
        raw_path = parsed.path or "/"
        fragment = parsed.fragment or ""
    elif href.startswith("//"):
        protocol_relative = urlparse("https:" + href)
        if not is_same_site_absolute_url(protocol_relative):
            return None
        raw_path = protocol_relative.path or "/"
        fragment = protocol_relative.fragment or ""
    else:
        raw_path = parsed.path
        fragment = parsed.fragment or ""

    raw_path = unquote(raw_path)

    if not raw_path:
        if source_file.name == "index.html":
            normalized_path = public_url_directory_for_file(source_file, root)
        else:
            normalized_path = "/" + source_file.relative_to(root).as_posix()
        return normalized_path, fragment

    if raw_path.startswith("/"):
        normalized_path = posixpath.normpath(raw_path)
    else:
        base_directory = public_url_directory_for_file(source_file, root)
        normalized_path = posixpath.normpath(posixpath.join(base_directory, raw_path))

    if normalized_path == ".":
        normalized_path = "/"

    if not normalized_path.startswith("/"):
        normalized_path = "/" + normalized_path

    if raw_path.endswith("/") and not normalized_path.endswith("/"):
        normalized_path += "/"

    return normalized_path, fragment


def candidate_paths_for_url_path(url_path: str, root: Path) -> list[Path]:
    if not url_path or url_path == "/":
        return [root / "index.html"]

    clean = url_path.lstrip("/")
    candidates: list[Path] = []

    if clean.endswith("/"):
        candidates.append(root / clean / "index.html")
    else:
        candidates.append(root / clean)
        if Path(clean).suffix.lower() not in HTML_EXTENSIONS and "." not in Path(clean).name:
            candidates.append(root / clean / "index.html")
            candidates.append(root / f"{clean}.html")

    unique: list[Path] = []
    seen: set[Path] = set()
    for candidate in candidates:
        resolved = candidate.resolve()
        if resolved not in seen:
            seen.add(resolved)
            unique.append(candidate)
    return unique


def resolve_url_path(url_path: str, root: Path) -> Path | None:
    for candidate in candidate_paths_for_url_path(url_path, root):
        if candidate.exists() and candidate.is_file():
            return candidate
    return None


def validate_links(root: Path) -> list[Finding]:
    html_files = discover_html_files(root)
    anchor_map = {path.resolve(): parse_html(path).anchors for path in html_files}
    findings: list[Finding] = []

    for source_path in html_files:
        parser = parse_html(source_path)
        source_relative = source_path.relative_to(root).as_posix()

        for line, raw_href in parser.links:
            normalized = normalize_internal_href(raw_href, source_path, root)
            if normalized is None:
                continue

            normalized_path, fragment = normalized
            target_path = resolve_url_path(normalized_path, root)

            if target_path is None:
                findings.append(
                    Finding(
                        severity="error",
                        file=source_relative,
                        message=f"Broken internal link at line {line}.",
                        evidence=f"{raw_href} -> {normalized_path}",
                    )
                )
                continue

            if fragment and target_path.suffix.lower() in HTML_EXTENSIONS:
                anchors = anchor_map.get(target_path.resolve(), set())
                if fragment not in anchors:
                    findings.append(
                        Finding(
                            severity="warning",
                            file=source_relative,
                            message=f"Internal link target exists, but fragment anchor was not found at line {line}.",
                            evidence=f"{raw_href} -> {normalized_path}#{fragment}",
                        )
                    )

    return findings


def print_human_report(findings: list[Finding]) -> None:
    if not findings:
        print("Link validation passed. No broken internal links found.")
        return

    errors = [finding for finding in findings if finding.severity == "error"]
    warnings = [finding for finding in findings if finding.severity == "warning"]
    print("Link validation completed with findings.")
    print(f"Errors: {len(errors)}")
    print(f"Warnings: {len(warnings)}")
    print()

    for finding in findings:
        print(f"[{finding.severity.upper()}] {finding.file}")
        print(f"  {finding.message}")
        if finding.evidence:
            print(f"  Evidence: {finding.evidence}")
        print()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate internal links for ShovelsSale.com.")
    parser.add_argument("--root", default=None, help="Repository root. Defaults to the parent directory of this script.")
    parser.add_argument("--json", default=None, help="Optional path to write a JSON report.")
    args = parser.parse_args(argv)

    root = Path(args.root).resolve() if args.root else Path(__file__).resolve().parents[1]
    if not root.exists():
        print(f"Repository root does not exist: {root}", file=sys.stderr)
        return 1

    findings = validate_links(root)

    if args.json:
        report_path = Path(args.json)
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(json.dumps([asdict(f) for f in findings], indent=2), encoding="utf-8")

    print_human_report(findings)
    return 1 if any(finding.severity == "error" for finding in findings) else 0


if __name__ == "__main__":
    raise SystemExit(main())
