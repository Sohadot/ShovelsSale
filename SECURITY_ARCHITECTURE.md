# Security Architecture — ShovelsSale.com

## Purpose

This document records what actually governs production security for ShovelsSale.com.

It exists to prevent false assumptions, speculative fixes, and cosmetic changes
that create an appearance of security without real enforcement.

Every security decision must be grounded in this document.
If this document cannot confirm that a control is active, the control must not
be treated as active.

---

## Document Status

| Phase | Status | Date Confirmed |
|---|---|---|
| Phase 1 — Repository governance & artifact protection | Complete — merged to main | Confirmed |
| Phase 2 — Live security header activation via Cloudflare | Complete — active in production | Confirmed |
| CSP — Content-Security-Policy | Intentionally deferred | See rationale below |

---

## Production Delivery Path — Confirmed

### Confirmed architecture

- The repository is hosted on **GitHub** (`Sohadot/ShovelsSale`, GitHub Pages).
- A `CNAME` file points the custom domain `shovelssale.com` to GitHub Pages.
- **Cloudflare** is the confirmed live edge layer in front of GitHub Pages.
- GitHub/Fastly are present in the backend delivery chain.
- **Cloudflare is the authoritative layer for live HTTP response headers.**

### Confirmed redirect behavior

Verified via live testing:

- `http://shovelssale.com` → `https://shovelssale.com/` ✔
- `https://www.shovelssale.com` → `https://shovelssale.com/` ✔
- Canonical redirect layer is correct and functioning.

---

## Live Security Headers — Confirmed Active

The following headers are confirmed present in the live production response
as enforced by Cloudflare Transform Rules:

| Header | Value | Status |
|---|---|---|
| `Strict-Transport-Security` | `max-age=31536000; includeSubDomains; preload` | ✔ Active |
| `X-Frame-Options` | `DENY` | ✔ Active |
| `X-Content-Type-Options` | `nosniff` | ✔ Active |
| `Referrer-Policy` | `strict-origin-when-cross-origin` | ✔ Active |
| `Permissions-Policy` | `camera=(), microphone=(), geolocation=(), payment=()` | ✔ Active |
| `Content-Security-Policy` | — | ⏸ Intentionally deferred |

**Configuration location:** Cloudflare Dashboard → Rules → Transform Rules → HTTP Response Headers.

---

## Files That Are Non-Authoritative for Live Headers

The following files exist in the repository but **do not govern production response headers**
under the confirmed delivery architecture (GitHub Pages + Cloudflare edge):

| File | Status |
|---|---|
| `_headers.txt` | Non-authoritative — `.txt` extension, not processed by any platform in this stack |
| `_.htaccess.txt` | Non-authoritative — Apache directive, not applicable to GitHub Pages or Cloudflare |
| `_redirects.txt` | Non-authoritative — `.txt` extension, not processed by any platform in this stack |

These files contain correct security intent but produce no runtime enforcement.
They are retained as documentation of intent only.

Do not rename or activate these files without:
1. Confirming a platform change that would process them.
2. Testing the change against the live response.
3. Updating this document.

---

## What Is Enforced — Full Picture

### At the Cloudflare edge layer (live, confirmed)

- HTTPS enforcement
- `http → https` redirect
- `www → non-www` redirect
- DDoS protection
- `Strict-Transport-Security`
- `X-Frame-Options`
- `X-Content-Type-Options`
- `Referrer-Policy`
- `Permissions-Policy`

### At the repository / CI layer (Phase 1, merged to main)

- `.gitignore` prevents `security_report.json` from being committed or deployed.
- `security_scan.py` writes its report to OS temp only — never to the repo root.
- `security_scan.py` exits with code `1` on critical findings — failures are visible in CI.
- `weekly-update.yml` uses job-level permissions (least privilege per job).
- `security-audit` job has `contents: read` only — no write access.
- `sitemap-ping` job has `contents: none`.
- `git add` in `content-update` is scoped to known outputs, not `git add -A`.

---

## Content-Security-Policy — Intentionally Deferred

CSP is the most complex header to deploy correctly for this site.
A premature or incomplete CSP would cause silent breakage of analytics,
fonts, or the scanner tool without any obvious error to the user.

**CSP must not be activated until the following dependencies are fully mapped
and validated against a tested policy:**

| Dependency | Required CSP directive |
|---|---|
| Google Tag Manager (inline script) | `script-src 'nonce-...'` or `'unsafe-inline'` |
| GA4 external script (`googletagmanager.com`) | `script-src https://www.googletagmanager.com` |
| Google Fonts CSS | `style-src https://fonts.googleapis.com` |
| Google Fonts files | `font-src https://fonts.gstatic.com` |
| GTM noscript iframe | `frame-src https://www.googletagmanager.com` |
| Scanner external API (if active) | `connect-src https://api.exchangerate-api.com` |

**CSP deployment process (when ready):**
1. Draft full policy from dependency map above.
2. Deploy as `Content-Security-Policy-Report-Only` first.
3. Monitor for violations without breaking production.
4. Promote to enforcing `Content-Security-Policy` after clean report period.
5. Set via Cloudflare Transform Rules — same layer as all other headers.

---

## Governance Rules

1. **Cloudflare is the production header authority.** Headers must be set there, not in repo files.
2. **No security control may be described as active unless verified via live `curl -I` response.**
3. **This document must be updated before any change to production security configuration.**
4. **Speculative fixes and cosmetic security changes are explicitly rejected.**
5. **CSP must go through Report-Only phase before enforcement.**
