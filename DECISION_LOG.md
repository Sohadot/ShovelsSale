# Decision Log

## 2026-04-29 — Constitutional Framework Adopted

ShovelsSale.com now includes CLAUDE.md as its local constitutional development framework.

This decision formally connects ShovelsSale.com to the Sovereign Asset System and defines the asset as a governed sovereign digital asset rather than a generic website, blog, ecommerce concept, or short-term affiliate surface.

Rationale:
- protect conceptual integrity
- preserve long-term asset value
- establish governance before monetization
- prepare quality gates
- prevent future downgrade
- align all development with the Sovereign Asset System

Status: Accepted

## 2026-04-29 — Automated Quality Gate Adopted

ShovelsSale.com now includes automated content, link, asset, and SEO validation through local scripts and GitHub Actions.

This decision moves the asset from documented governance to enforceable quality control.

Implemented gates:
- Content Integrity Gate
- Link Integrity Gate
- Asset Integrity Gate
- SEO Integrity Gate
- Sovereign Quality Gate workflow

Rationale:
- prevent broken pages and missing assets
- protect SEO integrity
- prevent placeholder or weak content
- enforce publication discipline
- make quality visible in GitHub Actions
- support long-term sovereign asset value

Status: Accepted

## 2026-04-29 — Sitemap Lastmod Accuracy Adopted

ShovelsSale.com now generates `sitemap.xml` with page-specific `lastmod` values instead of assigning the same current date to every page.

The sitemap generator now prioritizes meaningful modification sources:
- explicit `dateModified` or page metadata when available
- the latest Git commit date for the page
- filesystem modification time as a fallback outside Git

Rationale:
- reduce artificial sitemap churn
- improve SEO integrity
- align sitemap behavior with `SEO_POLICY.md`
- make sitemap dates more credible and auditable
- prevent technical or non-public artifacts from entering sitemap output

Status: Accepted
