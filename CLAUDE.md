# ShovelsSale.com — Constitutional Development Framework

## Purpose

This document defines how **ShovelsSale.com** develops as a **sovereign digital asset** 
guided by the principles, governance, and quality standards established in the 
**Sovereign Asset System** (https://github.com/Sohadot/sovereign-asset-system).

This is not a description of what ShovelsSale is.
This is a description of the **constitutional principles** that guide its development.

---

## 1. CONSTITUTIONAL FOUNDATION

### The Sovereign Asset System — Our Doctrine

ShovelsSale.com is built upon the governance framework defined in the 
**Sovereign Asset System** repository, which establishes:

- **Naming discipline:** lowercase, hyphens, no abbreviations
- **Structural discipline:** clear separation between doctrine, skills, templates, governance, and execution
- **Quality discipline:** multi-dimensional assessment framework
- **Governance discipline:** decision gates at each critical lifecycle stage
- **Operational discipline:** audit trails for all decisions

This CLAUDE.md file documents how these constitutional principles apply to ShovelsSale.

---

## 2. ASSET IDENTITY

### Asset Classification
- **Name:** ShovelsSale.com
- **Type:** Sovereign Digital Asset (static web application)
- **Strategic Category:** Infrastructure Asset (per Shovel Framework)
- **Custodian:** Sohadot
- **Repository:** https://github.com/Sohadot/ShovelsSale
- **Distribution:** GitHub Pages + Cloudflare CDN
- **Status:** Active (Production Phase)

### Asset Philosophy

ShovelsSale.com embodies the **Shovel Framework** philosophy:

> Infrastructure assets (the "shovels") that enable economic activity 
> are more valuable than the commodities they produce.

The asset itself demonstrates this principle:
- **What it teaches:** frameworks for identifying undervalued infrastructure assets
- **What it models:** a governed, secure, scalable digital infrastructure
- **How it operates:** deliberately, with documented decisions and security gates

---

## 3. CONSTITUTIONAL ARCHITECTURE — THE FIVE LAYERS

ShovelsSale follows the 5-layer architecture defined in sovereign-asset-system:

```
┌─────────────────────────────────────────────────────────┐
│ Layer 1: DOCTRINE                                       │
│ (Strategic philosophy, principles, frameworks)          │
│ /manifesto/ | /framework/                               │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│ Layer 2: SKILLS                                         │
│ (Operational capabilities, tools, methods)              │
│ /scanner/ | /guide/                                     │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│ Layer 3: TEMPLATES                                      │
│ (Standardized structures for content, processes)        │
│ /blog/ | /dispatch/ | Script templates                  │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│ Layer 4: GOVERNANCE                                     │
│ (Decision gates, quality standards, rules)              │
│ SECURITY_ARCHITECTURE.md | CI/CD gates | Review rules   │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│ Layer 5: EXECUTION                                      │
│ (Live production, operational truth)                    │
│ shovelssale.com | GitHub Pages + Cloudflare             │
└─────────────────────────────────────────────────────────┘
```

### Layer 1: DOCTRINE — Strategic Foundations

**Files:** `/manifesto/index.html`, `/framework/index.html`

**Purpose:** Define the philosophical and strategic underpinning

**Current doctrine:**
- Infrastructure assets precede commodities in strategic value
- Market inefficiencies create opportunities for research and classification
- Domain names are sovereign digital assets with intrinsic value
- Governance and discipline are prerequisites for long-term asset appreciation

**Governance:** 
- Doctrine changes require explicit commit with rationale in git history
- No speculative doctrine changes — all changes must be justified by production evidence
- Doctrine evolution is logged and versioned via git

---

### Layer 2: SKILLS — Operational Capabilities

**Files:** `/scanner/` | `/guide/index.html` | `scripts/*.py`

**Purpose:** Define the operational tools and methods used to build and maintain the asset

**Current skills:**

| Skill | Tool | Purpose |
|-------|------|---------|
| **Content Discovery** | `automate.py` | Discover and index real blog posts into high-quality archive |
| **Security Assessment** | `security_scan.py` | Weekly automated vulnerability scanning (XSS, injection, credentials) |
| **Measurement** | `sync_google_tags.py` | Maintain GTM + GA4 instrumentation (idempotent) |
| **SEO Infrastructure** | `update_sitemap.py` | Generate sitemap.xml from filesystem discovery |
| **Distribution** | `generate_rss.py` | Create RSS feeds for multiple channels (blog, dispatch) |
| **Orchestration** | `publish_pipeline.py` | Sequence all scripts with error propagation & fail-safety |
| **Interactive Analysis** | `/scanner/` | Client-side tool for asset classification |

**Governance:**
- Skills must be idempotent (safe to run multiple times)
- Skills must fail loudly (no silent partial success)
- Skills must be auditable (clear input/output/logic)
- Skills must be version-controlled with clear purpose statements

---

### Layer 3: TEMPLATES — Standardized Structures

**Files:** `/blog/`, `/dispatch/`, `scripts/` standard patterns

**Purpose:** Define repeatable, consistent patterns for content and process

**Current templates:**

| Template | Structure | Governance |
|----------|-----------|-----------|
| **Blog Post** | `/blog/[year]-[topic]/index.html` | Auto-indexed, metadata extracted, published to feed |
| **Dispatch** | `/dispatch/[number]/index.html` | Sequentially numbered (001, 002, ...), asset analysis |
| **Automation Script** | `scripts/[verb]_[noun].py` | Clear responsibility, single purpose, defensive patterns |
| **Security Report** | `security_report.json` (temp only) | Never committed, write to OS temp, exit code indicates severity |

**Naming discipline (per sovereign-asset-system):**
- ✓ Directories: lowercase with hyphens (`no-code-ai-stack-2026`)
- ✓ URLs: lowercase, hyphens, no abbreviations
- ✓ Scripts: `lowercase_with_underscores` (Python convention)
- ✓ Configuration: clear, non-abbreviated variable names

---

### Layer 4: GOVERNANCE — Decision Gates & Quality Standards

**Files:** `SECURITY_ARCHITECTURE.md`, `.github/workflows/`, `.gitignore`, `git` rules

**Purpose:** Enforce quality, security, and consistency through documented gates

#### 4.1 Gate 1: Security Audit Gate (Phase 1 + Phase 2 — ACTIVE)

**What it enforces:**
- No credentials in code ✓ (enforced by `security_scan.py` + `.gitignore`)
- No XSS vectors ✓ (scanned weekly)
- No injection risks ✓ (pattern-based detection)
- HTTPS enforcement ✓ (Cloudflare + HSTS header)
- Secure headers present ✓ (Cloudflare edge layer)
- Least-privilege CI/CD ✓ (per-job permission scoping)

**How it works:**
- `security_audit` job runs with `contents: read` only (read-only)
- `security_scan.py` exits code 1 on critical findings (CI fails, visible in UI)
- Security reports written to OS temp (never committed)
- `.gitignore` explicitly prevents `security_report.json`

**Evidence:**
- SECURITY_ARCHITECTURE.md documents what is verified (live headers via Cloudflare)
- Non-authoritative files (`_headers.txt`, `_.htaccess.txt`, `_redirects.txt`) retained as intent but not enforced
- No speculative security changes without verification

---

#### 4.2 Gate 2: Quality Gate (Phase 0 — PLANNED)

**What it should enforce:**

| Dimension | Target | Current Status |
|-----------|--------|-----------------|
| **Capability** | Core features operational | ✓ Complete |
| **Reliability** | 99.9% uptime, zero manual interventions | ⏸ Implicit |
| **Performance** | Lighthouse > 90, <2s LCP | ⚠️ Not measured |
| **Security** | Weekly audits, 0 critical findings | ✓ Active |
| **Maintainability** | Code clarity, documentation quality | ⚠️ Partial |
| **Scalability** | 700+ assets without degradation | ⏸ Deferred (architecture supports it) |
| **Governance** | All changes auditable, no orphans | ✓ Git history is authoritative |

**How it will work (to be implemented):**
```
Pull Request → 
  [Security Gate] ✓ ACTIVE
  [Quality Gate] ⏸ PLANNED
  [Performance Gate] ⏸ PLANNED
  [Documentation Gate] ⏸ PLANNED
→ Merge → Deploy
```

---

#### 4.3 Gate 3: Publication Gate (Phase 0 — PLANNED)

**Purpose:** Decide when content is ready for public distribution

**Future governance:**
- Explicit decision to publish vs. hold
- Rationale documented in git commit
- Performance implications assessed
- Audience alignment verified

---

#### 4.4 Gate 4: Monetization Gate (Phase 0 — PLANNED)

**Purpose:** Decide when and how the asset generates revenue

**Future governance:**
- Revenue model aligned with doctrine
- No compromise of core values for short-term gains
- Stewardship accountability documented

---

#### 4.5 Gate 5: Archival Gate (Phase 0 — PLANNED)

**Purpose:** Decide when content becomes historical vs. active

**Future governance:**
- Clear archival policy
- No orphaned content
- Historical versions preserved

---

### Layer 5: EXECUTION — Live Production

**Current state:** shovelssale.com (active, production)

**Distribution architecture (verified):**
```
GitHub Repository (source of truth)
    ↓ [CI/CD: publish_pipeline.py]
GitHub Pages (content delivery)
    ↓ [CNAME: shovelssale.com]
Cloudflare Edge (security + performance)
    ↓ [Transform Rules: inject headers]
Client Browser (end user)
```

**What is live:**
- ✓ Static HTML content
- ✓ Security headers (HSTS, X-Frame-Options, X-Content-Type-Options, Referrer-Policy, Permissions-Policy)
- ✓ HTTPS enforcement
- ✓ GTM + GA4 measurement
- ✓ SEO infrastructure (sitemap.xml, robots.txt)
- ✓ RSS feeds (blog + dispatch channels)

**What is deferred:**
- ⏸ Content-Security-Policy (dependency mapping in progress — see SECURITY_ARCHITECTURE.md)
- ⏸ Performance monitoring (Lighthouse CI)
- ⏸ Staging environment
- ⏸ Change review workflow

---

## 4. QUALITY FRAMEWORK — SEVEN DIMENSIONS

ShovelsSale evaluates itself across **seven dimensions of quality**:

### 1. CAPABILITY — Does it work?

**Definition:** Core features are operational and serve their purpose

**Current state:** ✓ **EXCELLENT**
- Content discovery and indexing: working
- Security scanning: working
- Measurement (GTM + GA4): working
- SEO infrastructure: working
- RSS distribution: working

**Assessment:** Asset delivers on core promise — teach and demonstrate sovereign asset thinking

---

### 2. RELIABILITY — Can you trust it?

**Definition:** Predictable, consistent operation with minimal manual intervention

**Current state:** ✓ **GOOD**
- Automation runs weekly on schedule
- Failures visible in CI/CD (code 1 exits)
- No silent partial failures
- Git history is complete audit trail

**What's needed:**
- Staging environment for testing before production
- Change review process (PR before merge)
- Rollback capability documentation

**Target:** Zero unplanned downtime, all changes reversible

---

### 3. PERFORMANCE — How fast is it?

**Definition:** User experience and operational efficiency

**Current state:** ⚠️ **UNKNOWN**
- Static site + CDN guarantees fast delivery
- No performance metrics collected
- No Lighthouse CI baseline

**What's needed:**
- Lighthouse CI in CI/CD pipeline
- Core Web Vitals tracking
- Image optimization audit
- Load time SLOs documented

**Target:** Lighthouse > 90, LCP < 2s, zero CLS

---

### 4. SECURITY — Is it safe?

**Definition:** No unauthorized access, data exposure, or exploitation

**Current state:** ✓ **EXCELLENT**
- Weekly automated scanning for XSS, injection, credentials
- Production headers verified via Cloudflare
- Least-privilege CI/CD permissions
- Artifacts protected from accidental commit
- No dependencies (eliminates supply chain risk)

**In progress:**
- CSP deployment (Report-Only → Enforcing)

**Target:** 0 critical findings, 0 exploitable vectors, all headers active

---

### 5. MAINTAINABILITY — Can you understand and change it?

**Definition:** Code clarity, documentation, and ease of modification

**Current state:** ⚠️ **GOOD**
- Clear separation of concerns (6 focused scripts)
- Good docstrings describing purpose
- Consistent naming conventions
- Clean directory structure

**What's needed:**
- Inline comments for complex logic (regex patterns, date extraction)
- Architecture decision records (ADRs)
- Operational runbooks (how to handle failures, rollbacks)
- Troubleshooting guides

**Target:** Onboard new contributor in < 1 hour

---

### 6. SCALABILITY — Can it grow?

**Definition:** Handle increasing volume and complexity without degradation

**Current state:** ✓ **STRONG**
- Static site scales infinitely via CDN
- Python scripts are O(n) and lightweight
- Git history scales indefinitely
- No database bottlenecks

**What's needed:**
- Asset discovery mechanism (700+ domains need indexing)
- Search/filtering for large content sets
- Archive strategy for old content

**Target:** Support 700+ assets + 10k+ content pieces without slowdown

---

### 7. GOVERNANCE — Is it auditable and intentional?

**Definition:** All decisions documented, rules enforced, accountability clear

**Current state:** ⚠️ **PARTIAL**
- ✓ Security decisions documented in SECURITY_ARCHITECTURE.md
- ✓ Git history shows development trajectory
- ✓ Governance rules explicit (no speculative fixes)
- ⚠️ Quality decisions implicit, not formalized
- ⚠️ No change review process

**What's needed:**
- Decision logs (why was X approved? why was Y rejected?)
- Change control workflow (PR + review before merge)
- Governance gates enforced in CI/CD
- Rationale documented for deferred decisions

**Target:** Audit trail of every decision, clear ownership, no orphaned changes

---

## 5. ASSET LIFECYCLE

ShovelsSale follows a **5-stage lifecycle**:

```
Stage 1: CREATE
  ↓ What is the asset?
  ↓ What problem does it solve?
  ↓ What is the strategic rationale?
  
Stage 2: PUBLISH
  ↓ Is it complete and polished?
  ↓ Does it meet security standards?
  ↓ Is it discoverable and accessible?
  
Stage 3: MAINTAIN
  ↓ Is it current and relevant?
  ↓ Does it meet performance SLOs?
  ↓ Are there known issues?
  
Stage 4: MONETIZE
  ↓ Does it generate value?
  ↓ What is the revenue model?
  ↓ Is revenue aligned with doctrine?
  
Stage 5: ARCHIVE
  ↓ Is it still relevant?
  ↓ Should it be historical?
  ↓ What should we preserve?
```

### Current Status: Stage 2 → Stage 3 (Published, Maintaining)

ShovelsSale.com is actively published and maintained. It is not yet at Stage 4 (Monetize).

---

## 6. DEVELOPMENT PHASES

ShovelsSale develops in **documented phases**:

### Phase 0: FOUNDATION (2026-01 to 2026-03) — ✓ COMPLETE
- Establish core infrastructure
- Implement security scanning
- Document security architecture
- Build automation pipeline
- Create initial content

**Deliverables:**
- ✓ GitHub repository + GitHub Pages hosting
- ✓ Cloudflare integration
- ✓ Weekly automation workflow
- ✓ Security scanning (security_scan.py)
- ✓ Initial manifesto and framework
- ✓ Blog and dispatch structure

---

### Phase 1: SECURITY HARDENING (2026-04) — ✓ COMPLETE
- Repository governance (artifact protection, least-privilege CI)
- Live security header activation via Cloudflare
- Comprehensive security audit
- Documentation of production truth

**Deliverables:**
- ✓ `.gitignore` prevents sensitive files
- ✓ CI/CD permission scoping (per-job, least privilege)
- ✓ Cloudflare security headers active (HSTS, X-Frame-Options, etc.)
- ✓ SECURITY_ARCHITECTURE.md documents verified controls
- ✓ Non-authoritative files retained as documentation intent

---

### Phase 2: QUALITY FORMALIZATION (2026-05 to 2026-06) — IN PROGRESS
- Write CLAUDE.md (this document) ✓ DONE
- Define 7-dimension quality framework ✓ DONE
- Create governance gates in CI/CD (Lighthouse, linting, documentation checks)
- Establish change review process (PR → review → merge)
- Set up staging environment

**Deliverables (planned):**
- Quality gates in CI/CD pipeline
- Lighthouse CI baseline and SLOs
- Style linting (HTML, Python)
- Documentation verification
- Staging environment (staging.shovelssale.com)
- Change review requirements

**Timeline:** Complete by end of Q2 2026

---

### Phase 3: CSP DEPLOYMENT (2026-07 to 2026-08) — PLANNED
- Map all external dependencies
- Draft comprehensive CSP policy
- Deploy as Report-Only first
- Monitor for violations
- Promote to enforcing CSP

**Deliverables (planned):**
- Complete CSP dependency inventory
- CSP Report-Only deployed to Cloudflare
- Violation monitoring active
- CSP enforced via Cloudflare Transform Rules

**Timeline:** Complete by end of Q3 2026

---

### Phase 4: MONETIZATION STRATEGY (2026-09 to 2026-12) — PLANNED
- Define revenue models
- Implement tracking for monetization metrics
- Test revenue channels
- Document results

**Deliverables (planned):**
- Revenue model architecture
- Monetization tracking implemented
- Revenue channel tests completed
- Documentation of results

**Timeline:** Complete by end of Q4 2026

---

### Phase 5: SCALING & ARCHIVE (2027 onwards) — FUTURE
- Scale to 700+ assets
- Implement asset search/discovery
- Archive old content
- Establish long-term stewardship

---

## 7. GOVERNANCE RULES

These rules are **immutable** and enforce the constitutional principles:

### Rule 1: Naming Discipline
- Directories, files, URLs use lowercase with hyphens
- No abbreviations (unless industry standard like GTM, GA4)
- Naming itself is governance — violation is visible

### Rule 2: Doctrine Before Code
- No code change without understanding its constitutional rationale
- Speculative fixes and cosmetic changes are rejected
- Every feature must align with layer 1 (DOCTRINE)

### Rule 3: Verification Before Trust
- No security control is active unless verified via live response
- SECURITY_ARCHITECTURE.md is authoritative for what is real
- Testing is mandatory, assumptions are banned

### Rule 4: Fail Loudly
- Errors must be visible and propagated
- No silent partial successes
- Exit codes matter in CI/CD

### Rule 5: Idempotence Required
- Every automation script must be safe to run multiple times
- No side effects from repeated runs
- Incremental and re-entrant by design

### Rule 6: Audit Trail Sacred
- All decisions logged in git history
- Commits must include rationale (not just "fix bug")
- Reversibility is a feature

### Rule 7: Least Privilege in Automation
- CI/CD jobs declare only required permissions
- No `git add -A` (explicit staging only)
- Read-only jobs have `contents: read` only

### Rule 8: Documentation is Enforcement
- Documentation is not optional decoration
- SECURITY_ARCHITECTURE.md enforces what is active
- CLAUDE.md enforces what is constitutional

---

## 8. STRATEGIC INTENT

### What ShovelsSale is Testing

ShovelsSale.com is a live experiment in:

1. **Sovereign Digital Asset Stewardship** — Can a digital asset be governed with constitutional discipline?
2. **Infrastructure-First Philosophy** — Can governance and infrastructure drive value more than marketing?
3. **Measurable Quality** — Can quality be defined in seven dimensions and enforced automatically?
4. **Long-Term Thinking** — Can we build for 5-10 year horizon instead of 90-day cycles?

### What Success Looks Like

✓ Asset is secure (0 critical vulnerabilities)
✓ Asset is reliable (near-zero unplanned downtime)
✓ Asset is performant (Lighthouse > 90)
✓ Asset is maintainable (new contributor productive in 1 hour)
✓ Asset is scalable (supports 700+ child assets)
✓ Asset is governed (all decisions auditable)
✓ Asset generates measurable value

---

## 9. IMMEDIATE PRIORITIES (Q2 2026)

### Priority 1: Complete Phase 2 (Quality Formalization)
- [ ] Write CLAUDE.md ✓ DONE
- [ ] Create governance gates in CI/CD (Lighthouse, linting, docs checks)
- [ ] Establish change review process (PR → review → merge)
- [ ] Set up staging environment

**Owner:** Sohadot
**Timeline:** Complete by 2026-05-31

### Priority 2: CSP Dependency Mapping (Phase 3 prep)
- [ ] Inventory all external dependencies (GTM, GA4, Fonts, Plausible, etc.)
- [ ] Draft CSP policy
- [ ] Test in Report-Only mode

**Owner:** Sohadot
**Timeline:** Complete by 2026-06-30

### Priority 3: Monetization Strategy (Phase 4 prep)
- [ ] Define revenue models (sponsorship, affiliate, direct sales, etc.)
- [ ] Design monetization tracking
- [ ] Identify revenue channels to test

**Owner:** Sohadot
**Timeline:** Complete by 2026-08-31

---

## 10. APPENDIX: GLOSSARY

**Constitutional Discipline:** Governance guided by explicit principles, enforced through rules and gates, not ad-hoc decisions

**Sovereign Digital Asset:** A digital property governed with intentionality, auditable decisions, and long-term stewardship

**Doctrine:** The strategic philosophy layer (why we do this)

**Skills:** The operational capability layer (how we do this)

**Templates:** Standardized, repeatable structures

**Governance:** Rules, gates, and decision processes

**Execution:** Live production

**Asset Lifecycle:** Create → Publish → Maintain → Monetize → Archive

**Quality Dimension:** One of seven aspects (capability, reliability, performance, security, maintainability, scalability, governance)

**Governance Gate:** A decision point where the asset must meet defined criteria before advancing

**Phase:** A documented development milestone with clear deliverables

---

## 11. DOCUMENT MAINTENANCE

This document is **constitutional** — it defines how ShovelsSale develops.

**Changes to this document require:**
1. Clear rationale (why this principle?)
2. Git commit with explanation
3. Review against the Sovereign Asset System doctrine
4. Verification that changes don't contradict Layer 1 (DOCTRINE)

**Last Updated:** 2026-04-29
**Status:** Phase 2 (Quality Formalization) in progress
**Next Review:** 2026-05-31
