# Security Architecture — ShovelsSale.com

## Purpose

This document records what actually governs production security for ShovelsSale.com.

It exists to prevent false assumptions, speculative fixes, and cosmetic changes
that create an appearance of security without real enforcement.

Every security decision must be grounded in this document.
If this document cannot confirm that a control is active, the control must not
be treated as active.

---

## Production Delivery Path (Current Understanding)

### What is confirmed

- The repository is hosted on **GitHub** (`Sohadot/ShovelsSale`).
- A `CNAME` file exists pointing to `shovelssale.com`.
- The site appears to be served via **GitHub Pages** with a custom domain.
- **Cloudflare** is likely operating as the DNS and edge layer in front of GitHub Pages,
  based on typical configuration patterns for this setup.

### What is unverified

- The exact Cloudflare configuration (Page Rules, Security Headers, WAF settings)
  has not been confirmed from within this repository.
- Whether GitHub Pages alone or Cloudflare Workers/Pages is the actual origin
  has not been verified.
- Whether HSTS is being enforced by Cloudflare or is entirely absent from production
  has not been confirmed.
- Whether any `Content-Security-Policy` header is being set at the edge
  has not been confirmed.

**No security header should be assumed active unless it can be verified
through direct HTTP response inspection or confirmed Cloudflare dashboard settings.**

---

## Files That Are Currently Non-Authoritative

The following files exist in the repository but are **not governing production**
under any confirmed delivery path:

| File | Why it is non-authoritative |
|---|---|
| `_headers.txt` | `.txt` extension — not processed by Netlify, Cloudflare Pages, or any known platform |
| `_.htaccess.txt` | Non-standard prefix `_` and `.txt` extension — not read as `.htaccess` by Apache or any platform |
| `_redirects.txt` | `.txt` extension — not processed by Netlify or Cloudflare Pages |

These files contain correct security intent but are currently **documentation only**.
They produce no runtime enforcement.

Do not reference these files as active security controls.
Do not rename or activate them without first confirming the production delivery platform
and testing that the platform will actually process them.

---

## What Is Currently Enforced

### Confirmed at repository level

- `security_scan.py` scans HTML for common vulnerabilities on a weekly schedule.
- `weekly-update.yml` CI permissions follow least-privilege per job (as of this commit).
- `.gitignore` prevents `security_report.json` from being committed or deployed.
- Security scan report is written to OS temp only — never to the repo root.
- Security scan exits with code `1` on critical issues, making failures visible in CI.

### Likely enforced at Cloudflare level (unconfirmed from this repo)

- HTTPS enforcement (SSL/TLS)
- DDoS protection
- Possibly: security headers via Cloudflare Transform Rules

### Not confirmed as enforced anywhere

- `Content-Security-Policy`
- `Strict-Transport-Security` (HSTS)
- `X-Frame-Options`
- `X-Content-Type-Options`
- `Referrer-Policy`
- `Permissions-Policy`

---

## What Must Be Resolved Before Further Security Work

The following architectural questions must be answered before adding, renaming,
or activating any security configuration file:

1. **What is the actual production delivery platform?**
   GitHub Pages only? Cloudflare Pages? A Cloudflare Worker? Some combination?

2. **What security headers is Cloudflare currently setting (if any)?**
   Inspect `curl -I https://shovelssale.com` to see live response headers.

3. **Is HSTS currently active?**
   If Cloudflare is enforcing it, adding it elsewhere may be redundant.
   If it is absent entirely, it needs to be added at the correct layer.

4. **Which file format does the production platform accept for headers?**
   - Netlify: `_headers` (no extension)
   - Cloudflare Pages: `_headers` (no extension)
   - Apache: `.htaccess`
   - GitHub Pages: none — headers must be set at Cloudflare or a CDN layer

5. **Is `sync_google_tags.py` modifying HTML files?**
   If so, the `git add` in `weekly-update.yml` may need to include those paths.

---

## Governance Rule

This document must be updated before any change to the production security
configuration is made.

If a change cannot be traced back to a confirmed delivery path,
it must not be implemented.

Speculative fixes and cosmetic security theater are explicitly rejected.
