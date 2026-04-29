#!/usr/bin/env python3
"""
Content integrity validator for ShovelsSale.com.

Purpose:
    Enforce the first layer of the sovereign quality gate by detecting weak,
    unfinished, placeholder, or structurally empty public content before it is
    committed or published.

Scope:
    By default, this script scans public HTML files only. Governance Markdown
    files are intentionally not scanned because they may legitimately mention
    forbidden terms such as "placeholder", "thin SEO pages", or "TODO" as
    policy examples.

Usage:
    python scripts/validate_content.py
    python scripts/validate_content.py --root .
    python scripts/validate_content.py --include-markdown
    python scripts/validate_content.py --json reports/content_validation.json

Exit codes:
    0 = pass
    1 = one or more content integrity failures
"""

from __future__ import annotations

import argparse
import html
import json
import re
import sys
from dataclasses import asdict, dataclass
from html.parser import HTMLParser
from pathlib import Path
from typing import Iterable, List


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
}

EXCLUDED_FILES = {
    "google28b5398e4140f820.html",
    "schema-templates.html",
}

GOVERNANCE_MARKDOWN_FILES = {
    "README.md",
    "CLAUDE.md",
    "DECISION_LOG.md",
    "QUALITY_GATE.md",
    "SEO_POLICY.md",
    "MONETIZATION_POLICY.md",
    "SECURITY_ARCHITECTURE.md",
}

HTML_EXTENSIONS = {".html", ".htm"}
MARKDOWN_EXTENSIONS = {".md", ".markdown"}

MIN_WORDS_DEFAULT = 80
MIN_WORDS_SHORT_PAGE = 20

SHORT_PAGE_NAMES = {
    "404.html",
}


@dataclass(frozen=True)
class Finding:
    severity: str
    file: str
    message: str
    evidence: str = ""


class VisibleTextParser(HTMLParser):
    """Extract visible text and headings from an HTML document."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self._ignored_stack: List[str] = []
        self._current_heading: str | None = None
        self.text_parts: List[str] = []
        self.headings: List[tuple[str, str]] = []
        self.title_parts: List[str] = []
        self._inside_title = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        tag = tag.lower()

        if tag in {"script", "style", "svg", "noscript", "template"}:
            self._ignored_stack.append(tag)
            return

        if self._ignored_stack:
            return

        if tag == "title":
            self._inside_title = True

        if re.fullmatch(r"h[1-6]", tag):
            self._current_heading = tag

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()

        if self._ignored_stack:
            if self._ignored_stack[-1] == tag:
                self._ignored_stack.pop()
            return

        if tag == "title":
            self._inside_title = False

        if self._current_heading == tag:
            self._current_heading = None

    def handle_data(self, data: str) -> None:
        if self._ignored_stack:
            return

        cleaned = collapse_whitespace(data)
        if not cleaned:
            return

        if self._inside_title:
            self.title_parts.append(cleaned)

        self.text_parts.append(cleaned)

        if self._current_heading:
            self.headings.append((self._current_heading, cleaned))

    @property
    def visible_text(self) -> str:
        return collapse_whitespace(" ".join(self.text_parts))

    @property
    def title(self) -> str:
        return collapse_whitespace(" ".join(self.title_parts))


def collapse_whitespace(value: str) -> str:
    return re.sub(r"\s+", " ", value or "").strip()


def word_count(text: str) -> int:
    return len(re.findall(r"\b[\w'-]+\b", text, flags=re.UNICODE))


def safe_read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8", errors="replace")


def is_excluded(path: Path, root: Path) -> bool:
    relative_parts = path.relative_to(root).parts

    if any(part in EXCLUDED_DIRECTORIES for part in relative_parts):
        return True

    if path.name in EXCLUDED_FILES:
        return True

    return False


def discover_files(root: Path, include_markdown: bool) -> list[Path]:
    extensions = set(HTML_EXTENSIONS)
    if include_markdown:
        extensions.update(MARKDOWN_EXTENSIONS)

    files: list[Path] = []

    for path in root.rglob("*"):
        if not path.is_file():
            continue

        if is_excluded(path, root):
            continue

        if path.suffix.lower() not in extensions:
            continue

        if path.suffix.lower() in MARKDOWN_EXTENSIONS and path.name in GOVERNANCE_MARKDOWN_FILES:
            continue

        files.append(path)

    return sorted(files)


def strip_markdown(text: str) -> str:
    """Remove common Markdown syntax while keeping human-readable content."""
    text = re.sub(r"```.*?```", " ", text, flags=re.DOTALL)
    text = re.sub(r"`([^`]*)`", r"\1", text)
    text = re.sub(r"!\[[^\]]*\]\([^)]+\)", " ", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"^#{1,6}\s*", "", text, flags=re.MULTILINE)
    text = re.sub(r"[*_~>#-]+", " ", text)
    return collapse_whitespace(text)


def extract_content(path: Path) -> tuple[str, str, list[tuple[str, str]]]:
    raw = safe_read(path)

    if path.suffix.lower() in HTML_EXTENSIONS:
        parser = VisibleTextParser()
        parser.feed(raw)
        return parser.visible_text, parser.title, parser.headings

    text = strip_markdown(raw)
    markdown_headings = [
        ("md-heading", collapse_whitespace(match.group(1)))
        for match in re.finditer(r"^#{1,6}\s+(.+)$", raw, flags=re.MULTILINE)
    ]
    return text, "", markdown_headings


PLACEHOLDER_PATTERNS = [
    (re.compile(r"\blorem\s+ipsum\b", re.IGNORECASE), "Lorem ipsum placeholder text"),
    (re.compile(r"\bTODO\b", re.IGNORECASE), "TODO marker"),
    (re.compile(r"\bFIXME\b", re.IGNORECASE), "FIXME marker"),
    (re.compile(r"\bTBD\b", re.IGNORECASE), "TBD marker"),
    (re.compile(r"\bunder\s+construction\b", re.IGNORECASE), "under construction marker"),
    (re.compile(r"\bcoming\s+soon\b", re.IGNORECASE), "coming soon marker"),
    (re.compile(r"\bcopy\s+goes\s+here\b", re.IGNORECASE), "copy goes here marker"),
    (re.compile(r"\binsert\s+(your\s+)?(text|copy|content)\s+here\b", re.IGNORECASE), "insert text here marker"),
    (re.compile(r"\bsample\s+content\b", re.IGNORECASE), "sample content marker"),
    (re.compile(r"\bdummy\s+text\b", re.IGNORECASE), "dummy text marker"),
    (re.compile(r"\bnew\s+page\s+title\b", re.IGNORECASE), "default page title marker"),
]


GENERIC_TITLE_PATTERNS = [
    re.compile(r"^\s*untitled\s*$", re.IGNORECASE),
    re.compile(r"^\s*document\s*$", re.IGNORECASE),
    re.compile(r"^\s*new\s+page\s*$", re.IGNORECASE),
    re.compile(r"^\s*page\s+title\s*$", re.IGNORECASE),
]


def find_evidence(text: str, pattern: re.Pattern[str]) -> str:
    match = pattern.search(text)
    if not match:
        return ""

    start = max(match.start() - 60, 0)
    end = min(match.end() + 60, len(text))
    snippet = text[start:end]
    return collapse_whitespace(snippet)


def validate_file(path: Path, root: Path) -> list[Finding]:
    relative = str(path.relative_to(root)).replace("\\", "/")
    text, title, headings = extract_content(path)

    findings: list[Finding] = []

    visible_word_count = word_count(text)
    minimum_words = MIN_WORDS_SHORT_PAGE if path.name in SHORT_PAGE_NAMES else MIN_WORDS_DEFAULT

    if visible_word_count < minimum_words:
        findings.append(
            Finding(
                severity="error",
                file=relative,
                message=f"Visible content is too thin ({visible_word_count} words; expected at least {minimum_words}).",
            )
        )

    for pattern, label in PLACEHOLDER_PATTERNS:
        if pattern.search(text):
            findings.append(
                Finding(
                    severity="error",
                    file=relative,
                    message=f"Unfinished or placeholder content detected: {label}.",
                    evidence=find_evidence(text, pattern),
                )
            )

    for heading_tag, heading_text in headings:
        if not collapse_whitespace(heading_text):
            findings.append(
                Finding(
                    severity="error",
                    file=relative,
                    message=f"Empty heading detected: {heading_tag}.",
                )
            )

    if path.suffix.lower() in HTML_EXTENSIONS:
        if not title:
            findings.append(
                Finding(
                    severity="error",
                    file=relative,
                    message="Missing <title> element or empty page title.",
                )
            )
        elif any(pattern.match(title) for pattern in GENERIC_TITLE_PATTERNS):
            findings.append(
                Finding(
                    severity="error",
                    file=relative,
                    message="Generic or default page title detected.",
                    evidence=title,
                )
            )

        if "<h1" not in safe_read(path).lower():
            findings.append(
                Finding(
                    severity="warning",
                    file=relative,
                    message="No <h1> heading detected. This may weaken clarity and accessibility.",
                )
            )

    return findings


def print_human_report(findings: list[Finding]) -> None:
    if not findings:
        print("Content validation passed. No content integrity failures found.")
        return

    errors = [finding for finding in findings if finding.severity == "error"]
    warnings = [finding for finding in findings if finding.severity == "warning"]

    print("Content validation completed with findings.")
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
    parser = argparse.ArgumentParser(description="Validate public content integrity for ShovelsSale.com.")
    parser.add_argument(
        "--root",
        default=None,
        help="Repository root. Defaults to the parent directory of this script's directory.",
    )
    parser.add_argument(
        "--include-markdown",
        action="store_true",
        help="Also scan non-governance Markdown files.",
    )
    parser.add_argument(
        "--json",
        default=None,
        help="Optional path to write a JSON report.",
    )

    args = parser.parse_args(argv)

    if args.root:
        root = Path(args.root).resolve()
    else:
        root = Path(__file__).resolve().parents[1]

    if not root.exists():
        print(f"Repository root does not exist: {root}", file=sys.stderr)
        return 1

    files = discover_files(root, include_markdown=args.include_markdown)

    findings: list[Finding] = []
    for path in files:
        findings.extend(validate_file(path, root))

    if args.json:
        report_path = Path(args.json)
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(
            json.dumps([asdict(finding) for finding in findings], indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

    print_human_report(findings)

    has_errors = any(finding.severity == "error" for finding in findings)
    return 1 if has_errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
