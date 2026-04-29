#!/usr/bin/env python3
"""
SEO integrity validator for ShovelsSale.com.

Purpose:
    Enforce the SEO integrity layer of the sovereign quality gate by detecting
    missing or invalid SEO metadata across public HTML pages, and by checking
    sitemap coverage against the repository's public indexable pages.

Usage:
    python scripts/validate_seo.py
    python scripts/validate_seo.py --root .
    python scripts/validate_seo.py --json reports/seo_validation.json
    python scripts/validate_seo.py --strict-og

Exit codes:
    0 = pass
    1 = one or more SEO integrity errors
"""

from __future__ import annotations

import argparse
import html
import json
import re
import sys
import xml.etree.ElementTree as ET
from dataclasses import asdict, dataclass
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse


SITE_ORIGIN = "https://shovelssale.com"
SITE_DOMAINS = {"shovelssale.com", "www.shovelssale.com"}
HTML_EXTENSIONS = {".html", ".htm"}

EXCLUDED_DIRECTORIES = {
    ".git",
    ".github",
    ".claude",
    ".well-known",
    "__pycache__",
    "node_modules",
    "reports",
    "dist",
    "build",
    "vendor",
    "assets",
}

EXCLUDED_FILES = {
    "404.html",
    "google28b5398e4140f820.html",
    "schema-templates.html",
}

MIN_TITLE_LENGTH = 20
MAX_TITLE_LENGTH = 75
MIN_DESCRIPTION_LENGTH = 70
MAX_DESCRIPTION_LENGTH = 180


@dataclass(frozen=True)
class Finding:
    severity: str
    file: str
    message: str
    evidence: str = ""


class SEOHTMLParser(HTMLParser):
    """Extract SEO-relevant metadata from an HTML document."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self._inside_title = False
        self._inside_h1 = False
        self.title_parts: list[str] = []
        self.h1_values: list[str] = []
        self.meta_by_name: dict[str, str] = {}
        self.meta_by_property: dict[str, str] = {}
        self.link_rels: dict[str, list[str]] = {}

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        tag = tag.lower()
        attributes = {name.lower(): value for name, value in attrs if name and value is not None}

        if tag == "title":
            self._inside_title = True
            return

        if tag == "h1":
            self._inside_h1 = True
            return

        if tag == "meta":
            meta_name = (attributes.get("name") or "").strip().lower()
            meta_property = (attributes.get("property") or "").strip().lower()
            content = collapse_whitespace(attributes.get("content") or "")

            if meta_name:
                self.meta_by_name[meta_name] = content

            if meta_property:
                self.meta_by_property[meta_property] = content

        elif tag == "link":
            rel = (attributes.get("rel") or "").strip().lower()
            href = collapse_whitespace(attributes.get("href") or "")

            if rel and href:
                for token in rel.split():
                    self.link_rels.setdefault(token, []).append(href)

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()

        if tag == "title":
            self._inside_title = False

        if tag == "h1":
            self._inside_h1 = False

    def handle_data(self, data: str) -> None:
        cleaned = collapse_whitespace(data)
        if not cleaned:
            return

        if self._inside_title:
            self.title_parts.append(cleaned)

        if self._inside_h1:
            self.h1_values.append(cleaned)

    @property
    def title(self) -> str:
        return collapse_whitespace(" ".join(self.title_parts))

    @property
    def description(self) -> str:
        return self.meta_by_name.get("description", "")

    @property
    def robots(self) -> str:
        return self.meta_by_name.get("robots", "")

    @property
    def canonical_values(self) -> list[str]:
        return self.link_rels.get("canonical", [])


def collapse_whitespace(value: str) -> str:
    return re.sub(r"\s+", " ", value or "").strip()


def safe_read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8", errors="replace")


def is_excluded(path: Path, root: Path) -> bool:
    relative_parts = path.relative_to(root).parts

    if any(part in EXCLUDED_DIRECTORIES for part in relative_parts):
        return True

    return path.name in EXCLUDED_FILES


def discover_html_files(root: Path) -> list[Path]:
    files: list[Path] = []

    for path in root.rglob("*"):
        if not path.is_file():
            continue

        if is_excluded(path, root):
            continue

        if path.suffix.lower() not in HTML_EXTENSIONS:
            continue

        files.append(path)

    return sorted(files)


def parse_html(path: Path) -> SEOHTMLParser:
    parser = SEOHTMLParser()
    parser.feed(safe_read(path))
    return parser


def expected_public_url(path: Path, root: Path) -> str:
    relative = path.relative_to(root).as_posix()

    if relative == "index.html":
        return f"{SITE_ORIGIN}/"

    if relative.endswith("/index.html"):
        route = relative[: -len("index.html")]
        return f"{SITE_ORIGIN}/{route}"

    return f"{SITE_ORIGIN}/{relative}"


def normalize_url(url: str) -> str:
    url = html.unescape(collapse_whitespace(url))
    parsed = urlparse(url)

    scheme = parsed.scheme.lower()
    netloc = parsed.netloc.lower()
    path = parsed.path or "/"

    if path != "/" and path.endswith("/index.html"):
        path = path[: -len("index.html")]

    if path == "":
        path = "/"

    normalized = f"{scheme}://{netloc}{path}"

    if parsed.path.endswith("/") and not normalized.endswith("/"):
        normalized += "/"

    return normalized


def is_valid_site_url(url: str) -> bool:
    parsed = urlparse(url)
    return parsed.scheme == "https" and parsed.netloc.lower() in SITE_DOMAINS


def is_noindex(robots: str) -> bool:
    return "noindex" in robots.lower()


def validate_metadata(path: Path, root: Path, strict_og: bool) -> list[Finding]:
    parser = parse_html(path)
    relative = path.relative_to(root).as_posix()
    findings: list[Finding] = []
    expected_url = expected_public_url(path, root)

    if not parser.title:
        findings.append(Finding("error", relative, "Missing <title> element or empty page title."))
    else:
        if len(parser.title) < MIN_TITLE_LENGTH:
            findings.append(Finding("warning", relative, f"Page title is short ({len(parser.title)} characters).", parser.title))
        if len(parser.title) > MAX_TITLE_LENGTH:
            findings.append(Finding("warning", relative, f"Page title is long ({len(parser.title)} characters).", parser.title))

    if not parser.description:
        findings.append(Finding("error", relative, "Missing meta description."))
    else:
        if len(parser.description) < MIN_DESCRIPTION_LENGTH:
            findings.append(Finding("warning", relative, f"Meta description is short ({len(parser.description)} characters).", parser.description))
        if len(parser.description) > MAX_DESCRIPTION_LENGTH:
            findings.append(Finding("warning", relative, f"Meta description is long ({len(parser.description)} characters).", parser.description))

    canonical_values = parser.canonical_values
    if not canonical_values:
        findings.append(Finding("error", relative, "Missing canonical URL."))
    elif len(canonical_values) > 1:
        findings.append(Finding("error", relative, "Multiple canonical URLs detected.", ", ".join(canonical_values)))
    else:
        canonical = normalize_url(canonical_values[0])
        expected = normalize_url(expected_url)

        if not is_valid_site_url(canonical):
            findings.append(Finding("error", relative, "Canonical URL must use https://shovelssale.com/ or https://www.shovelssale.com/.", canonical_values[0]))

        if canonical != expected:
            findings.append(Finding("error", relative, "Canonical URL does not match the expected public URL.", f"canonical={canonical}; expected={expected}"))

    if not parser.robots:
        findings.append(Finding("warning", relative, "Missing robots meta tag. Add index, follow unless intentionally non-indexable."))
    elif is_noindex(parser.robots):
        findings.append(Finding("error", relative, "Indexable public page contains noindex.", parser.robots))

    if not parser.h1_values:
        findings.append(Finding("warning", relative, "Missing <h1> heading."))
    elif len(parser.h1_values) > 1:
        findings.append(Finding("warning", relative, "Multiple <h1> headings detected.", " | ".join(parser.h1_values[:5])))

    og_keys = ("og:title", "og:description", "og:url")
    for key in og_keys:
        if not parser.meta_by_property.get(key):
            severity = "error" if strict_og else "warning"
            findings.append(Finding(severity, relative, f"Missing {key} metadata."))

    og_url = parser.meta_by_property.get("og:url", "")
    if og_url and normalize_url(og_url) != normalize_url(expected_url):
        severity = "error" if strict_og else "warning"
        findings.append(Finding(severity, relative, "og:url does not match the expected public URL.", f"og:url={og_url}; expected={expected_url}"))

    og_image = parser.meta_by_property.get("og:image", "")
    twitter_image = parser.meta_by_name.get("twitter:image", "")

    if not og_image:
        severity = "error" if strict_og else "warning"
        findings.append(Finding(severity, relative, "Missing og:image metadata."))
    elif not is_valid_site_url(og_image) and not og_image.startswith("/"):
        findings.append(Finding("warning", relative, "og:image should preferably be a stable absolute ShovelsSale.com URL.", og_image))

    if not twitter_image:
        findings.append(Finding("warning", relative, "Missing twitter:image metadata."))

    return findings


def parse_sitemap(root: Path) -> tuple[set[str], list[Finding]]:
    sitemap_path = root / "sitemap.xml"

    if not sitemap_path.exists():
        return set(), [Finding("error", "sitemap.xml", "sitemap.xml is missing.")]

    try:
        tree = ET.parse(sitemap_path)
    except ET.ParseError as exc:
        return set(), [Finding("error", "sitemap.xml", "sitemap.xml is not valid XML.", str(exc))]

    root_node = tree.getroot()
    namespace_match = re.match(r"\{(.+)\}", root_node.tag)
    namespace = namespace_match.group(1) if namespace_match else ""
    loc_selector = f".//{{{namespace}}}loc" if namespace else ".//loc"

    urls: set[str] = set()
    findings: list[Finding] = []

    for loc in root_node.findall(loc_selector):
        if loc.text:
            normalized = normalize_url(loc.text)
            urls.add(normalized)

            if not is_valid_site_url(normalized):
                findings.append(Finding("error", "sitemap.xml", "Sitemap contains a URL outside the approved ShovelsSale.com HTTPS origin.", loc.text))

    if not urls:
        findings.append(Finding("error", "sitemap.xml", "sitemap.xml contains no <loc> URLs."))

    return urls, findings


def url_to_candidate_file(url: str, root: Path) -> Path | None:
    parsed = urlparse(url)
    path = parsed.path or "/"

    if path == "/":
        candidate = root / "index.html"
    elif path.endswith("/"):
        candidate = root / path.lstrip("/") / "index.html"
    elif path.endswith(".html"):
        candidate = root / path.lstrip("/")
    else:
        candidate = root / path.lstrip("/") / "index.html"

    if candidate.exists() and candidate.is_file() and not is_excluded(candidate, root):
        return candidate

    return None


def validate_sitemap_coverage(root: Path, html_files: list[Path]) -> list[Finding]:
    sitemap_urls, findings = parse_sitemap(root)

    if not sitemap_urls:
        return findings

    expected_urls = {normalize_url(expected_public_url(path, root)) for path in html_files}

    for expected_url in sorted(expected_urls):
        if expected_url not in sitemap_urls:
            findings.append(Finding("error", "sitemap.xml", "Indexable public page is missing from sitemap.xml.", expected_url))

    for sitemap_url in sorted(sitemap_urls):
        if not is_valid_site_url(sitemap_url):
            continue

        if url_to_candidate_file(sitemap_url, root) is None:
            findings.append(Finding("error", "sitemap.xml", "Sitemap URL does not resolve to an existing public HTML page in the repository.", sitemap_url))

    return findings


def validate_seo(root: Path, strict_og: bool) -> list[Finding]:
    html_files = discover_html_files(root)

    findings: list[Finding] = []

    for path in html_files:
        findings.extend(validate_metadata(path, root, strict_og=strict_og))

    findings.extend(validate_sitemap_coverage(root, html_files))
    return findings


def print_human_report(findings: list[Finding]) -> None:
    if not findings:
        print("SEO validation passed. No SEO integrity failures found.")
        return

    errors = [finding for finding in findings if finding.severity == "error"]
    warnings = [finding for finding in findings if finding.severity == "warning"]

    print("SEO validation completed with findings.")
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
    parser = argparse.ArgumentParser(description="Validate SEO integrity for ShovelsSale.com.")
    parser.add_argument("--root", default=None, help="Repository root. Defaults to the parent directory of this script's directory.")
    parser.add_argument("--json", default=None, help="Optional path to write a JSON report.")
    parser.add_argument("--strict-og", action="store_true", help="Treat missing Open Graph metadata as errors instead of warnings.")

    args = parser.parse_args(argv)

    root = Path(args.root).resolve() if args.root else Path(__file__).resolve().parents[1]

    if not root.exists():
        print(f"Repository root does not exist: {root}", file=sys.stderr)
        return 1

    findings = validate_seo(root, strict_og=args.strict_og)

    if args.json:
        report_path = Path(args.json)
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(json.dumps([asdict(finding) for finding in findings], indent=2, ensure_ascii=False), encoding="utf-8")

    print_human_report(findings)

    has_errors = any(finding.severity == "error" for finding in findings)
    return 1 if has_errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
