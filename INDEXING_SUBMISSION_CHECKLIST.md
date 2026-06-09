# Indexing Submission Checklist — ShovelsSale.com

## Purpose

Manual operations checklist for Cloudflare cache purge and Google/Bing sitemap submission after Sprint 10 indexing-readiness verification.

This document is governance-only. It does not trigger indexing from code or external APIs.

**Prepared:** 2026-06-09 (Sprint 10)  
**HEAD at preparation:** `a4b912d` — Refine search intent and metadata across reference system

---

## Pre-submission verification (completed in repository)

| Check | Status |
|-------|--------|
| `sitemap.xml` contains exactly 33 URLs | ✓ |
| All `<loc>` URLs use `https://shovelssale.com/` | ✓ |
| `robots.txt` includes canonical sitemap directive | ✓ |
| No `.claude`, `worktree`, or `www.shovelssale.com` in sitemap | ✓ |
| Quality gate: 0 errors | ✓ |
| SEO warnings: 12 (non-blocking split-hero `<h1>` pattern) | ✓ |
| No new public pages in Sprint 10 | ✓ |
| No third-party scripts or tracking added | ✓ |

**Final sitemap URL:** `https://shovelssale.com/sitemap.xml`

---

## Step 1 — Cloudflare cache purge

Purge these URLs individually (or purge by prefix if your Cloudflare plan supports selective purge):

| URL | Role |
|-----|------|
| `https://shovelssale.com/` | Homepage |
| `https://shovelssale.com/sitemap.xml` | Sitemap |
| `https://shovelssale.com/robots.txt` | Robots |
| `https://shovelssale.com/scanner/` | Scanner Engine |
| `https://shovelssale.com/dispatch/` | Dispatch Atlas index |
| `https://shovelssale.com/blog/` | Blog index |
| `https://shovelssale.com/briefing/` | Dispatch Briefing |

**Blog Layer Intelligence Series (five articles):**

| URL |
|-----|
| `https://shovelssale.com/blog/shovel-economy-scorecard/` |
| `https://shovelssale.com/blog/infrastructure-signals/` |
| `https://shovelssale.com/blog/hype-cycle-to-dependency-map/` |
| `https://shovelssale.com/blog/strategic-digital-assets-are-not-websites/` |
| `https://shovelssale.com/blog/beneath-the-winner/` |

**Dispatch dossiers (priority):**

| URL |
|-----|
| `https://shovelssale.com/dispatch/009.html` |
| `https://shovelssale.com/dispatch/010.html` |
| `https://shovelssale.com/dispatch/011.html` |

After purge, confirm live responses return current content (spot-check homepage title and sitemap URL count).

---

## Step 2 — Google Search Console

Property: `https://shovelssale.com/`

1. **Sitemaps** — Submit or resubmit: `https://shovelssale.com/sitemap.xml`
2. **URL Inspection** — Run live test for each priority URL below before requesting indexing.
3. **Request indexing** — Only for priority URLs after live test passes.

### Priority indexing URLs

| URL | Rationale |
|-----|-----------|
| `https://shovelssale.com/` | Core reference entry |
| `https://shovelssale.com/scanner/` | Scanner Engine |
| `https://shovelssale.com/dispatch/` | Dispatch Intelligence Atlas |
| `https://shovelssale.com/blog/` | Blog index |
| `https://shovelssale.com/briefing/` | Dispatch Briefing |
| `https://shovelssale.com/dispatch/009.html` | TSMC — Manufacturing Sovereignty Layer |
| `https://shovelssale.com/dispatch/010.html` | ARM — Architecture Licensing Layer |
| `https://shovelssale.com/dispatch/011.html` | Broadcom — Infrastructure Aggregation Layer |
| `https://shovelssale.com/blog/shovel-economy-scorecard/` | Layer Intelligence |
| `https://shovelssale.com/blog/infrastructure-signals/` | Layer Intelligence |
| `https://shovelssale.com/blog/hype-cycle-to-dependency-map/` | Layer Intelligence |
| `https://shovelssale.com/blog/strategic-digital-assets-are-not-websites/` | Layer Intelligence |
| `https://shovelssale.com/blog/beneath-the-winner/` | Layer Intelligence |

**Do not submit:** low-value, duplicate, or thin URLs. Dispatch 001–008 and foundation blog essays are covered by sitemap discovery; request indexing only if inspection shows crawl or indexing problems.

---

## Step 3 — Bing Webmaster Tools

Property: `https://shovelssale.com/`

1. **Sitemaps** — Submit or resubmit: `https://shovelssale.com/sitemap.xml`
2. **URL Submission** — Use for the same priority URLs listed above, if the tool is available in your Bing property.
3. Confirm sitemap reports 33 discovered URLs after crawl.

---

## Step 4 — Monitor (do not over-resubmit)

- Wait at least 7–14 days after initial submission before repeated resubmit requests.
- Monitor Search Console and Bing coverage for errors, canonical mismatches, or soft 404s.
- Re-run `python scripts/quality_gate.py` locally before any content change that precedes another submission wave.
- Do not request indexing for URLs that have not changed since the last successful crawl.

---

## Governance notes

- Indexing is a manual steward action, not an automated repository operation.
- `robots.txt` allows public content; sitemap directive is present at line 88.
- All public pages retain `index, follow`; no `noindex` was added in Sprint 10.
- Canonical URLs use bare `https://shovelssale.com/` (no `www`).

**Governed by:** SEO_POLICY.md, QUALITY_GATE.md, DECISION_LOG.md
