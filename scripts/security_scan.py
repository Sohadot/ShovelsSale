"""
ShovelsSale.com — Security Scanner
Scans all HTML files for common vulnerabilities and issues.
Runs automatically via GitHub Actions.

NOTE ON REPORT OUTPUT:
The JSON report is written to the OS temp directory, never to the repo root.
This prevents accidental publication to the live site.
All findings are also printed to stdout for CI log visibility.
"""

import os
import sys
import json
import re
import tempfile
from datetime import datetime
from bs4 import BeautifulSoup

# =========================================================
# CONFIG
# =========================================================
SCAN_TIME = datetime.now().isoformat()
SKIP_DIRS = {'.git', 'scripts', 'node_modules', '.github'}

# Dangerous patterns to detect in HTML/JS
DANGEROUS_PATTERNS = [
    (r'eval\s*\(', 'eval() usage detected — potential XSS risk'),
    (r'document\.write\s*\(', 'document.write() — XSS risk'),
    (r'innerHTML\s*=\s*[^;]+', 'innerHTML assignment without sanitization'),
    (r'javascript:\s*["\']', 'javascript: URI — potential XSS'),
    (r'on\w+\s*=\s*["\'][^"\']+["\']', 'Inline event handler with function call'),
    (r'<script[^>]*src\s*=\s*["\']http://', 'HTTP (not HTTPS) script source'),
    (r'password\s*=\s*["\'][^"\']{3,}', 'Hardcoded password detected'),
    (r'api[_-]?key\s*=\s*["\'][^"\']{6,}', 'Hardcoded API key detected'),
    (r'secret\s*=\s*["\'][^"\']{8,}', 'Hardcoded secret detected'),
    (r'token\s*=\s*["\'][A-Za-z0-9+/=]{20,}', 'Hardcoded token detected'),
]

# Required security/meta tags
REQUIRED_META = [
    'description',
    'viewport',
]

# External domains whitelist
ALLOWED_EXTERNAL = {
    'fonts.googleapis.com',
    'fonts.gstatic.com',
    'plausible.io',
    'www.googletagmanager.com',
    'static.cloudflareinsights.com',
    'app.beehiiv.com',
    'assets.mailerlite.com',
}

# =========================================================
# SCANNER
# =========================================================
def scan_html_file(filepath: str) -> dict:
    """Scan a single HTML file for security issues."""
    issues = []
    warnings = []

    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    soup = BeautifulSoup(content, 'lxml')

    # 1. Check required meta tags
    for meta_name in REQUIRED_META:
        tag = soup.find('meta', {'name': meta_name})
        if not tag:
            warnings.append(f'Missing <meta name="{meta_name}">')

    # 2. Check for title
    if not soup.find('title'):
        issues.append('Missing <title> tag')

    # 3. Check canonical
    if not soup.find('link', {'rel': 'canonical'}):
        warnings.append('Missing canonical link')

    # 4. Check external scripts
    for script in soup.find_all('script', src=True):
        src = script.get('src', '')

        if src.startswith('http://'):
            issues.append(f'Insecure HTTP script: {src}')

        if src.startswith('https://') and not any(domain in src for domain in ALLOWED_EXTERNAL):
            warnings.append(f'External script not in whitelist: {src[:80]}')

    # 5. Check iframes
    for iframe in soup.find_all('iframe'):
        src = iframe.get('src', '')

        # Allow trusted GTM noscript iframe
        if 'www.googletagmanager.com/ns.html' in src:
            continue

        if src and not iframe.get('sandbox'):
            warnings.append(f'iframe without sandbox: {src[:60]}')

    # 6. Check forms
    for form in soup.find_all('form'):
        action = form.get('action', '')
        if action.startswith('http://'):
            issues.append(f'Form submits to HTTP (insecure): {action}')

    # 7. Scan for dangerous JS patterns
    scripts = soup.find_all('script')
    for script in scripts:
        if script.string:
            for pattern, description in DANGEROUS_PATTERNS:
                if re.search(pattern, script.string, re.IGNORECASE):
                    warnings.append(f'Pattern detected: {description}')

    # 8. Check for mixed content (http images)
    for img in soup.find_all('img', src=True):
        if img['src'].startswith('http://'):
            issues.append(f'Mixed content image: {img["src"][:60]}')

    # 9. Check for noindex on important pages
    robots_meta = soup.find('meta', {'name': 'robots'})
    filename = os.path.basename(filepath)
    if robots_meta and 'noindex' in robots_meta.get('content', ''):
        if filename != '404.html':
            warnings.append('Page has noindex — intentional?')

    return {
        'file': filepath,
        'issues': issues,
        'warnings': warnings,
        'status': 'FAIL' if issues else ('WARN' if warnings else 'PASS'),
    }


def scan_project() -> dict:
    """Scan entire project for security issues."""
    results = []
    total_issues = 0
    total_warnings = 0

    print(f"\n{'='*60}")
    print(f"ShovelsSale.com Security Scan — {SCAN_TIME}")
    print(f"{'='*60}\n")

    for root, dirs, files in os.walk('.'):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]

        for filename in files:
            if not filename.endswith('.html'):
                continue

            filepath = os.path.join(root, filename)
            result = scan_html_file(filepath)
            results.append(result)

            total_issues += len(result['issues'])
            total_warnings += len(result['warnings'])

            icon = '\u2713' if result['status'] == 'PASS' else ('\u26a0' if result['status'] == 'WARN' else '\u2717')
            print(f"{icon} {filepath}")

            for issue in result['issues']:
                print(f"   \u2717 ISSUE: {issue}")
            for warning in result['warnings']:
                print(f"   \u26a0 WARN: {warning}")

    print(f"\n{'='*60}")
    print("SCAN COMPLETE")
    print(f"Files scanned: {len(results)}")
    print(f"Issues:        {total_issues}")
    print(f"Warnings:      {total_warnings}")
    print(f"Status:        {'\u2713 CLEAN' if total_issues == 0 else '\u2717 ISSUES FOUND'}")
    print(f"{'='*60}\n")

    report = {
        'scan_time': SCAN_TIME,
        'total_files': len(results),
        'total_issues': total_issues,
        'total_warnings': total_warnings,
        'overall_status': 'FAIL' if total_issues > 0 else ('WARN' if total_warnings > 0 else 'PASS'),
        'results': results,
    }

    # Write report to OS temp directory — never to the repo root.
    # This prevents the report from being committed or served publicly.
    report_path = os.path.join(tempfile.gettempdir(), 'security_report.json')
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2)
    print(f"Report saved to temp only: {report_path}")
    print("(Not committed — never written to repo root)")

    if total_issues > 0:
        print(f"\n\u26a0 {total_issues} critical issue(s) found. Review required.")
        sys.exit(1)
    else:
        print("\u2713 No critical issues. Site is secure.")

    return report


if __name__ == '__main__':
    scan_project()
