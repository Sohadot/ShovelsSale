# Quality Gate — ShovelsSale.com

## Purpose

This document defines the quality gate for ShovelsSale.com.

ShovelsSale.com is not a generic static website, blog, affiliate surface, or ecommerce concept. It is a sovereign digital asset governed by the Sovereign Asset System and developed as a reference system around the Shovel Economy.

The purpose of this quality gate is to prevent degradation, broken publishing, weak content, shallow SEO expansion, and conceptual drift.

Quality is not decoration. Quality is part of the asset itself.

---

## 1. Governing Principle

No page, script, tool, dispatch, blog post, design change, monetization layer, or structural update should be accepted unless it strengthens or preserves:

1. Conceptual integrity
2. Structural coherence
3. Reference authority
4. Security discipline
5. SEO legitimacy
6. Performance quality
7. Long-term asset value

Any change that weakens these dimensions must be rejected, deferred, or redesigned.

---

## 2. Required Quality Dimensions

ShovelsSale.com is evaluated across seven quality dimensions.

### 2.1 Capability

The asset must work as intended.

Required standards:

- Core pages must load correctly.
- `/manifesto/`, `/framework/`, `/scanner/`, `/dispatch/`, `/guide/`, and `/blog/` must remain accessible.
- Scripts must perform their stated function.
- Generated outputs must be complete and usable.
- The scanner must remain functional and understandable.

Failure examples:

- Broken navigation
- Empty pages
- Non-functional scanner logic
- Feed generation failure
- Sitemap generation failure

### 2.2 Reliability

The asset must behave predictably.

Required standards:

- Automation scripts must be idempotent.
- CI/CD jobs must fail visibly when errors occur.
- No silent partial success.
- No manual-only process should become critical without documentation.
- All changes must be reversible through git history.

Failure examples:

- Script exits successfully after incomplete output
- Manual publishing without record
- Broken pages committed without detection
- Undocumented operational dependency

### 2.3 Performance

The asset must remain fast, lightweight, and stable.

Required standards:

- Static delivery must remain the default.
- No heavy framework may be introduced without explicit rationale.
- External scripts must be minimized.
- Images must be reasonably optimized.
- Core Web Vitals must be protected.
- Lighthouse performance target: 90+ when Lighthouse CI is implemented.
- LCP target: under 2 seconds where technically reasonable.
- CLS target: near zero.

Failure examples:

- Adding heavy JavaScript for decorative effects
- Loading unnecessary third-party scripts
- Unoptimized hero images
- Layout shifts caused by missing dimensions
- Excessive font loading

### 2.4 Security

The asset must preserve a low-risk static-site posture.

Required standards:

- No secrets, API keys, credentials, or private tokens in the repository.
- No unnecessary external scripts.
- Security scan must remain active.
- Cloudflare security controls must be documented before being considered active.
- CSP must move through Report-Only before enforcement.
- Security reports must not be committed.
- CI/CD permissions must follow least privilege.

Failure examples:

- Committing `.env` files
- Adding third-party widgets without review
- Treating unverified headers as active
- Overbroad workflow permissions
- Adding dynamic forms without security review

### 2.5 Maintainability

The asset must remain understandable and editable.

Required standards:

- Scripts must have clear purpose and readable structure.
- Complex regex, parsing, or file discovery logic must be commented.
- Directory names must remain lowercase and hyphenated.
- Python scripts must use clear function names.
- No unexplained duplicate logic.
- No hidden dependency on local-only files.

Failure examples:

- Adding unclear script logic
- Creating folders with inconsistent naming
- Duplicating metadata in multiple places without reason
- Local machine paths in committed files
- Large undocumented changes

### 2.6 Scalability

The asset must support future growth without structural decay.

Required standards:

- New content types must fit the existing doctrine → framework → tool → archive logic.
- New sections must have a clear purpose.
- No orphan pages.
- Internal linking must be intentional.
- Expansion must preserve reference quality.
- The architecture should remain compatible with portfolio-scale sovereign asset operations.

Failure examples:

- Adding dozens of weak SEO pages
- Creating categories without long-term purpose
- Publishing articles that do not support the Shovel Economy framework
- Adding isolated tools without integration
- Creating content that cannot be maintained

### 2.7 Governance

The asset must remain auditable and intentional.

Required standards:

- Major decisions must be documented in `DECISION_LOG.md`.
- Constitutional or doctrine-level changes require rationale.
- Monetization changes require review against `MONETIZATION_POLICY.md`.
- SEO expansion must comply with `SEO_POLICY.md`.
- Security claims must match verified production reality.
- Commits should explain why the change was made, not only what changed.

Failure examples:

- Vague commits for major changes
- Unrecorded monetization decisions
- Major framework edits without rationale
- Unexplained removal of content
- Adding revenue elements before monetization approval

---

## 3. Non-Negotiable Publication Checks

Before any change is considered publishable, the following checks must pass.

### 3.1 Content Integrity

- No placeholder text
- No lorem ipsum
- No empty headings
- No unfinished sections
- No generic filler
- No duplicated low-value content
- No broken conceptual logic
- No downgraded tone

### 3.2 Link Integrity

- All internal links must resolve.
- Navigation links must be valid.
- Footer links must be valid.
- Canonical URLs must be correct.
- No orphaned internal pages.

### 3.3 Asset Integrity

- All referenced CSS files must exist.
- All referenced JavaScript files must exist.
- All referenced images must exist.
- Open Graph images must exist where referenced.
- Favicon and icon references must be valid.

### 3.4 SEO Integrity

- Every indexable page must have a meaningful `<title>`.
- Every indexable page must have a meaningful meta description.
- Every indexable page must have a canonical URL.
- `robots.txt` must reference the sitemap.
- `sitemap.xml` must include all indexable public pages.
- `lastmod` must reflect meaningful update logic, not artificial churn.
- No weak SEO pages may be generated only to inflate page count.

### 3.5 Security Integrity

- No credentials or secrets.
- No private local files.
- No security reports committed.
- No unnecessary permissions in workflows.
- No new third-party dependency without review.

---

## 4. Conceptual Downgrade Protection

The following changes are prohibited unless explicitly approved through a documented decision:

- Turning ShovelsSale.com into a literal shovel store.
- Repositioning the asset as ordinary ecommerce.
- Repositioning the asset as a generic affiliate blog.
- Weakening the Shovel Economy doctrine.
- Removing the relationship between manifesto, framework, scanner, and dispatch.
- Adding mass SEO pages without reference quality.
- Adding monetization that reduces trust or authority.
- Replacing institutional language with shallow marketing language.

---

## 5. Required Future Automation

The quality gate should eventually be enforced through scripts and CI/CD.

Planned scripts:

- `scripts/validate_content.py`
- `scripts/validate_links.py`
- `scripts/validate_assets.py`
- `scripts/validate_seo.py`
- `scripts/quality_gate.py`

Planned CI/CD checks:

- Security Gate
- Content Integrity Gate
- Link Integrity Gate
- SEO Integrity Gate
- Asset Integrity Gate
- Performance Gate
- Documentation Gate

A change should not be considered complete until the relevant checks pass.

---

## 6. Current Status

Status: Active as governance policy.

Automation status: Planned.

Next implementation step: Add lightweight validation scripts and connect them to GitHub Actions.

---

## 7. Decision Authority

The custodian of ShovelsSale.com may revise this policy only through a documented governance decision.

Policy changes should be recorded in `DECISION_LOG.md`.

---

Last Updated: 2026-04-29

Status: Active
