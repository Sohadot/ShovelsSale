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

## 2026-04-29 — Core Social Metadata Standardized

ShovelsSale.com now includes standardized Open Graph and Twitter/X metadata across core public authority pages.

This decision improves how the asset appears when shared across social platforms, messaging apps, and professional networks.

Implemented changes:
- added a local social preview asset
- standardized `og:image` and `twitter:image` on core pages
- added missing metadata to core authority pages
- reduced SEO warnings without introducing new errors
- preserved the scope by avoiding article-level edits in this phase

Rationale:
- strengthen social preview integrity
- improve trust during link sharing
- support SEO presentation quality
- reinforce the asset’s institutional identity
- reduce metadata inconsistency across core pages

Status: Accepted

## 2026-04-29 — Article and Dispatch SEO Metadata Improved

ShovelsSale.com now includes improved robots, Open Graph, and Twitter/X metadata across article and dispatch pages.

This decision completes the second phase of SEO warning reduction by extending social and indexing metadata beyond the core authority pages into long-form and analytical archive content.

Implemented changes:
- standardized metadata for two blog articles
- standardized metadata for two dispatch files
- reused the existing local social preview asset
- reduced SEO warnings without introducing new errors
- preserved scope by avoiding unrelated page or content edits

Rationale:
- improve article-level SEO integrity
- strengthen dispatch archive presentation
- improve link-sharing trust for analytical content
- reduce metadata inconsistency
- preserve controlled, phase-based SEO improvement

Status: Accepted

## 2026-04-29 — Remaining SEO Metadata Warnings Reduced

ShovelsSale.com completed the third phase of SEO warning reduction by addressing low-risk metadata issues while preserving layout and conceptual identity.

Implemented changes:
- shortened long meta descriptions without changing strategic positioning
- fixed missing social metadata on the About page
- refined title and description metadata for Dispatch 002
- reduced SEO warnings from 18 to 9 without introducing errors
- preserved remaining h1 warnings where fixing them would risk layout or identity changes

Rationale:
- improve SEO metadata discipline
- reduce low-risk warning noise
- preserve visual and conceptual integrity
- avoid cosmetic changes that weaken the asset
- keep the quality gate passing

Status: Accepted
