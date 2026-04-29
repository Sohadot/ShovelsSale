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
SKIP_FILES = {'google28b5398e4140f820.html'}

# Dangerous patterns to detect in HTML/JS
DANGEROUS_PATTERNS = [
    (r'eval\s*\(', 'eval() usage detected — potential XSS risk'),
    (r'document\.write\s*\(', 'document.write() — XSS risk'),
    (r'innerHTML\s*=\s*[^;]+', 'innerHTML assignment without sanitization'),
    (r'javascript:\s*["\']', 'javascript: URI — potential XSS'),
    (r'\bon\w+\s*=\s*["\'][^"\']+["\']', 'Inline event handler with function call'),
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
def scan_html_file(filepath):
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
            warnings.append('Missing <meta name="' + meta_name + '">')

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
            issues.append('Insecure HTTP script: ' + src)
        if src.startswith('https://') and not any(domain in src for domain in ALLOWED_EXTERNAL):
            warnings.append('External script not in whitelist: ' + src[:80])

    # 5. Check iframes
    for iframe in soup.find_all('iframe'):
        src = iframe.get('src', '')
        if 'www.googletagmanager.com/ns.html' in src:
            continue
        if src and not iframe.get('sandbox'):
            warnings.append('iframe without sandbox: ' + src[:60])

    # 6. Check forms
    for form in soup.find_all('form'):
        action = form.get('action', '')
        if action.startswith('http://'):
            issues.append('Form submits to HTTP (insecure): ' + action)

    # 7. Scan for dangerous JS patterns
    for script in soup.find_all('script'):
        if script.string:
            for pattern, description in DANGEROUS_PATTERNS:
                if re.search(pattern, script.string, re.IGNORECASE):
                    warnings.append('Pattern detected: ' + description)

    # 8. Check for mixed content (http images)
    for img in soup.find_all('img', src=True):
        if img['src'].startswith('http://'):
            issues.append('Mixed content image: ' + img['src'][:60])

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


def scan_project():
    """Scan entire project for security issues."""
    results = []
    total_issues = 0
    total_warnings = 0

    print('')
    print('=' * 60)
    print('ShovelsSale.com Security Scan — ' + SCAN_TIME)
    print('=' * 60)
    print('')

    for root, dirs, files in os.walk('.'):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for filename in files:
            if not filename.endswith('.html'):
                continue
            if filename in SKIP_FILES:
                continue
            filepath = os.path.join(root, filename)
            result = scan_html_file(filepath)
            results.append(result)
            total_issues += len(result['issues'])
            total_warnings += len(result['warnings'])

            if result['status'] == 'PASS':
                icon = 'OK'
            elif result['status'] == 'WARN':
                icon = 'WARN'
            else:
                icon = 'FAIL'
            print('[' + icon + '] ' + filepath)

            for issue in result['issues']:
                print('   [ISSUE] ' + issue)
            for warning in result['warnings']:
                print('   [WARN]  ' + warning)

    print('')
    print('=' * 60)
    print('SCAN COMPLETE')
    print('Files scanned: ' + str(len(results)))
    print('Issues:        ' + str(total_issues))
    print('Warnings:      ' + str(total_warnings))

    # Explicit if/else — avoids backslash-in-f-string (Python 3.11 incompatible)
    if total_issues == 0:
        print('Status:        CLEAN')
    else:
        print('Status:        ISSUES FOUND')

    print('=' * 60)
    print('')

    report = {
        'scan_time': SCAN_TIME,
        'total_files': len(results),
        'total_issues': total_issues,
        'total_warnings': total_warnings,
        'overall_status': 'FAIL' if total_issues > 0 else ('WARN' if total_warnings > 0 else 'PASS'),
        'results': results,
    }

    # Write report to OS temp directory — never to the repo root.
    report_path = os.path.join(tempfile.gettempdir(), 'security_report.json')
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2)
    print('Report saved to temp only: ' + report_path)
    print('(Not committed — never written to repo root)')
    print('')

    if total_issues > 0:
        print('[!] ' + str(total_issues) + ' critical issue(s) found. Review required.')
        sys.exit(1)
    else:
        print('[OK] No critical issues. Site is secure.')

    return report


if __name__ == '__main__':
    scan_project()
