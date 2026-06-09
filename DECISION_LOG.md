# Decision Log

## 2026-06-09 — Final Indexing Readiness Pass Completed (Sprint 10)

ShovelsSale.com completed the final sitemap, robots, canonical, and indexing-readiness audit before manual Cloudflare purge and Google/Bing sitemap submission.

Changes:
- Regenerated `sitemap.xml` via `scripts/update_sitemap.py` — 33 URLs confirmed, homepage `lastmod` refreshed.
- Verified `robots.txt` sitemap directive (`https://shovelssale.com/sitemap.xml`); no Disallow rules block public content.
- Canonical spot-check passed for home, Scanner, Dispatch, Blog, Briefing, Dispatch 009–011, and Layer Intelligence articles.
- Metadata and internal-link spot-checks passed; quality gate 0 errors, 12 non-blocking split-hero H1 warnings.
- Created `INDEXING_SUBMISSION_CHECKLIST.md` for manual Cloudflare purge and search-console submission workflow.

Rationale:
- After Sprint 8 (Layer Intelligence), Sprint 7 (Briefing), and Sprint 9 (search-intent metadata), the reference system requires a governed handoff document for selective manual indexing — not automated submission from code.

Governed by:
- SEO_POLICY.md
- QUALITY_GATE.md
- INDEXING_SUBMISSION_CHECKLIST.md

Status: Accepted

## 2026-06-09 — Search Intent Control Pass Completed (Sprint 9)

ShovelsSale.com refined search-intent language, metadata, and internal anchor text across core reference pages without adding new content or tools.

Changes:
- Tightened title tags and meta descriptions on home, Scanner, Dispatch Atlas, Blog, Briefing, Dispatch 004–011, and Layer Intelligence articles.
- Differentiated Dispatch 009 (Manufacturing Sovereignty), 010 (Architecture Licensing), and 011 (Infrastructure Aggregation) metadata.
- Improved internal anchor language from generic labels to descriptive Shovel Economy vocabulary.
- Regenerated `sitemap.xml` via hardened `scripts/update_sitemap.py`.

Rationale:
- After Scanner, Dispatch, Blog Layer Intelligence, Briefing, and Blog-to-Dispatch graph expansion, the site needed a metadata control pass so search identity matches the governed reference-system architecture.
- Multiple-H1 warnings from split hero typography remain non-blocking; no indexing request in this sprint.

Governed by:
- SEO_POLICY.md
- QUALITY_GATE.md

Status: Accepted

## 2026-06-09 — Blog Layer Intelligence Series Published (Sprint 8)

ShovelsSale.com published five governed long-form Blog intelligence articles as the Layer Intelligence Series, strengthening conceptual search anchors for Shovel Economy reading methods.

Articles:
- `/blog/shovel-economy-scorecard/` — evaluative checklist for structural market positions
- `/blog/infrastructure-signals/` — observable signals of infrastructure necessity
- `/blog/hype-cycle-to-dependency-map/` — from market excitement to dependency maps
- `/blog/strategic-digital-assets-are-not-websites/` — systems vs surfaces for strategic digital assets
- `/blog/beneath-the-winner/` — enabling layers beneath visible winners

Changes:
- Updated `/blog/` index with Layer Intelligence Series and Foundation Essays organization.
- Regenerated `sitemap.xml` via hardened `scripts/update_sitemap.py`.

Rationale:
- Blog is the conceptual entry layer; Layer Intelligence essays turn Framework doctrine into repeatable reading methods that connect to Scanner, Dispatch, and Briefing.

Governed by:
- SEO_POLICY.md
- CLAUDE.md
- QUALITY_GATE.md

Status: Accepted

## 2026-06-09 — Dispatch Briefing Signup Layer Added (Sprint 7)

ShovelsSale.com added a restrained Dispatch Briefing audience capture layer using mailto-only signup, with no third-party embeds, tracking changes, or marketing funnel mechanics.

Changes:
- Created `/briefing/` as a crawlable static page explaining scope, audience, exclusions, and request method.
- Added contextual CTA blocks to `/dispatch/`, `/blog/`, and Dispatch 009–011.
- Extended sitemap public-route rules to include `/briefing/`.
- Regenerated `sitemap.xml` via hardened `scripts/update_sitemap.py`.

Rationale:
- Readers who follow source-governed Dispatch dossiers need a low-friction way to request low-frequency updates without compromising sovereign reference-system posture.
- Mailto-only preserves static-site discipline: no backend forms, no external signup services, no cookie or tracking expansion.

Governed by:
- CLAUDE.md
- SEO_POLICY.md
- QUALITY_GATE.md

Status: Accepted

## 2026-06-09 — Sitemap Generator Scope Hardened (Sprint 6B)

ShovelsSale.com hardened `scripts/update_sitemap.py` so automated sitemap generation cannot emit local Claude/worktree or other non-public filesystem paths.

Changes:
- Aligned sitemap discovery exclusions with public-route governance: `.claude/`, hidden directories, worktree paths, venv/cache/backup/temp directories, scripts, and assets.
- Added positive public-route allow rules for homepage, core sections, `/dispatch/NNN.html`, and `/blog/[article]/` only.
- Added final URL validation that exits non-zero when prohibited substrings or non-canonical origins appear.
- Regenerated `sitemap.xml` via the hardened script.

Rationale:
- Sprint 6 required manual sitemap lastmod edits because local `.claude/worktrees` copies were discovered by unrestricted `rglob("*.html")` scanning.
- A sovereign static site must not depend on manual sitemap edits when an automated generator exists.

Governed by:
- SEO_POLICY.md
- QUALITY_GATE.md

Status: Accepted

## 2026-06-09 — Blog-to-Dispatch Reference Graph Established (Sprint 6)

ShovelsSale.com connected six blog concept primers to contextually relevant Dispatch intelligence dossiers, strengthened reverse links from Dispatch 009–011 to foundational blog primers, Scanner, and Framework, and added a reference bridge on the blog index.

Changes:
- Added governed "Related Dispatch Cases" sections to six blog primers with 3–6 contextual dossier links and one-sentence explanations per mapping.
- Updated `/blog/index.html` with a "Read the Concepts, Then Study the Cases" bridge linking Dispatch, Scanner, and Framework.
- Strengthened Dispatch 009, 010, and 011 reverse links to blog primers, Scanner, and Framework with dossier-specific rationale.
- Updated `sitemap.xml` lastmod dates for edited blog pages (2026-06-09); full script regeneration skipped locally because `.claude/worktrees` paths would pollute the sitemap.

Rationale:
- Blog articles are the conceptual entry layer; Dispatch dossiers are the source-governed evidence layer; Scanner is the operational bridge; Framework is the doctrine and taxonomy layer.
- Internal links must be contextual and editorial, not mechanical link-farm patterns across every page.

Governed by:
- CLAUDE.md
- SEO_POLICY.md
- QUALITY_GATE.md

Status: Accepted

## 2026-06-09 — Dispatch 011 Source Governance Audit Completed (Sprint 5B)

ShovelsSale.com performed a strict intelligence-quality audit of Dispatch 011 (Broadcom and the Infrastructure Aggregation Layer) as the third full application of the Dispatch Intelligence Standard (v1.0).

This decision records the audit findings and the corrections applied to bring the dossier into full compliance before any further Dispatch or content development.

Audit findings and corrections:

- Source table: Added required "Date Checked" column (2026-06-09 for all rows) — previously absent, required by DISPATCH_INTELLIGENCE_STANDARD.md Section 2.10.
- Source table: Added required "Why It Matters" column for all rows — previously absent, required by repository practice established in Dispatch 009 and 010 audits.
- Source table: Renamed "Source Type" column to "Source / Reference Label" — aligned with sprint audit requirements and standard terminology.
- Source table rows 5–6: Differentiated CA Technologies and Symantec Form 8-K source labels to distinguish the two acquisition records.
- Source table row 15 (new): Added T3 / Moderate Confidence row for Arista Networks and Cisco Systems merchant silicon claim — this specific OEM dependency claim appeared in the Dependency Map as stated fact without a source table entry.
- Dependency Map: Arista/Cisco merchant silicon claim labeled as "per technology press; analyst interpretation; see Source Table row 15" — unsourced specific vendor claim made auditable.
- Dependency Map: "a large share of enterprise data center deployments globally" softened to "enterprise data center deployments globally" — "large share" is an unquantified market claim not supported by a primary source.
- Dependency Map: MSP VMware embedding claim labeled as "analyst interpretation based on VMware ecosystem structure."
- Replacement Difficulty: All four competitor lists (networking, hypervisor, storage, security) labeled "per technology press and analyst reports" — these lists were stated as fact without source attribution.
- Replacement Difficulty: "often 3–5 years" hardware refresh claim replaced with "multi-year timelines are typical based on industry analyst estimates" — specific figure had no source.
- Section 12 (Scanner Interpretation): Added contested signals paragraph identifying Replaceable (42/100) as the most analytically contested signal and explaining the distinction between individual-product and aggregate portfolio replaceability.
- Section 12: Added classification sensitivity paragraph identifying which gates (Gate 1 ASIC displacement, Gate 2 VMware migration) would shift the Shovel and Gatekeeper scores, and in what direction.
- Section 12: Added explicit note that no Broadcom preset exists in the scanner engine.
- Section 13 (Related Dispatch Cases): Added structural distinction paragraph for Cloudflare (Dispatch 005, web edge routing/security control layer) and GitHub (Dispatch 008, developer system-of-record layer) — sprint audit required confirming Broadcom is distinguished from all seven prior cases, including these two.
- PDF record: Updated "Source Table Entries" from "14 entries" to "15 entries (13 T1, 1 T3 / Watch Signal, 1 T3 / Moderate)" following addition of row 15.
- sitemap.xml: Regenerated; dispatch/011.html confirmed present.

Quality gate status post-audit: All 5 validators pass (exit code 0).

Rationale:
- A Dispatch dossier that claims source governance must actually have source governance — not structural form without governed content.
- The "Date Checked" and "Why It Matters" columns are required by the Dispatch Intelligence Standard and by repository practice established in the Dispatch 009 and 010 audits.
- Specific vendor claims (Arista/Cisco), market size characterizations ("large share"), and quantitative estimates ("3–5 years") require source attribution or analyst interpretation labels per the Intelligence Standard's strict no-unsourced-fact rule.
- The Cloudflare and GitHub structural distinctions are required to ensure the Broadcom classification is clearly positioned within the full Dispatch atlas.
- Contested signal analysis in Section 12 satisfies DISPATCH_INTELLIGENCE_STANDARD.md Section 2.9 requirements that were previously absent.

Governed by:
- DISPATCH_INTELLIGENCE_STANDARD.md
- CLAUDE.md
- QUALITY_GATE.md

Status: Accepted

## 2026-06-09 — Dispatch 011 Broadcom Infrastructure Aggregation Dossier Published (Sprint 5)

ShovelsSale.com published Dispatch 011: Broadcom and the Infrastructure Aggregation Layer, as the third full application of the Dispatch Intelligence Standard (v1.0).

This decision records the publication of the dossier and the structural classification applied.

Classification record:
- Actor: Broadcom Inc.
- Actor Type: Company — Semiconductor Designer and Infrastructure Software Licensor
- Market Wave: Semiconductor / Cloud / Enterprise IT / Networking / AI Infrastructure
- Primary Classification: Hybrid — Shovel (primary) / Gatekeeper (moderate)
- Confidence Level: Moderate Confidence (aggregation thesis requires interpretation of portfolio combination; individual products have alternatives; hyperscaler ASIC displacement is an open Watch Signal)
- Scanner Scores: Miner: 20 · Shovel: 80 · Gatekeeper: 65
- Replacement Difficulty: Moderate-High
- Source Table Entries: 14 (13 T1, 1 T3/Watch Signal)
- Standard Applied: Dispatch Intelligence Standard v1.0

Rationale for Moderate Confidence (not High):
- Broadcom's infrastructure position is an aggregation thesis requiring interpretation of multiple product segments — more analytical judgment than a single-product classification like ARM or TSMC.
- Each individual product category (networking ASICs, enterprise hypervisor, storage, security) has documented competitive alternatives.
- The hyperscaler custom ASIC displacement signal (Section 9, Gate 1) is a known structural uncertainty bearing directly on the semiconductor segment classification.

Rationale for distinct treatment vs. prior dispatches:
- Broadcom is not analogous to ARM (single ISA specification), TSMC (single manufacturing layer), or NVIDIA (dominant GPU compute). It is a distinct aggregation case.
- The Infrastructure Aggregation Pattern is added to the Dispatch atlas as a structural category not previously represented.

Files created or updated:
- dispatch/011.html (created)
- dispatch/index.html (updated: numberOfItems 10→11, Broadcom card, archive item, "Eleven Markets. Eleven Layers.")
- DISPATCH_ROADMAP.md (updated: Dispatch 011 entry, coverage 001-011)
- DECISION_LOG.md (this entry)
- sitemap.xml (regenerated)

Quality gate status: All 5 validators pass (exit code 0).

Governed by:
- DISPATCH_INTELLIGENCE_STANDARD.md
- CLAUDE.md
- QUALITY_GATE.md

Status: Accepted

## 2026-06-09 — Dispatch 010 Source Governance Audit Completed (Sprint 4B)

ShovelsSale.com performed a strict intelligence-quality audit of Dispatch 010 (ARM and the Architecture Licensing Layer) as the second full application of the Dispatch Intelligence Standard (v1.0).

This decision records the audit findings and the corrections applied to bring the dossier into full compliance before any further Dispatch development.

Audit findings and corrections:

- Superlative removed: "the most commercially significant mobile product category in history" (iPhone 2007 paragraph) replaced with "a globally transformative mobile product category" — superlatives used as structural claims without evidence are prohibited by the Intelligence Standard.
- Android/iOS claim softened: "entirely built on ARM architecture" changed to "predominantly built on ARM architecture" — iOS is entirely ARM, but Android has had x86 implementations, making "entirely" technically inaccurate.
- Quantitative claim removed: "millions of lines of firmware and safety-critical code" changed to "substantial quantities of firmware and safety-critical code" — no source supported the specific quantification.
- RISC-V Alternatives row: Western Digital and SiFive named as RISC-V adopters now explicitly labeled as "T3 — technology press reporting; analyst interpretation." China RISC-V adoption claim changed from specific national attribution to "government-motivated policy objectives" with explicit analyst interpretation label.
- Section 9 (Gatekeeper Limit card): China RISC-V claim changed to "policy-motivated interest in domestic semiconductor alternatives — Analyst interpretation" to avoid stating geopolitical motivation as fact.
- Source table row 3: Claim text updated to include "approximately $40 billion (per NVIDIA press release, September 2020)" — the dollar figure appeared in the body text but was absent from the source table claim.
- Source table row 4: Removed "the IPO was among the largest technology listings of 2023" from the Claim column — this editorial characterization is not supported by the Form 20-F and is not a T1-verifiable claim.
- Source table row 13 added: ARM's 1998 simultaneous listing on the London Stock Exchange and NASDAQ (T1, High Confidence) — this historical fact was cited inline in the body text but was absent from the source table.
- PDF section updated: fact table count corrected from 12 to 13 following addition of row 13.
- Qualcomm/Samsung/MediaTek historical claim (Section 4, 1998 block): Added explicit "consistent with ARM Holdings Form 20-F customer disclosures (T1); analyst interpretation for the broader ecosystem consolidation narrative" label.

Quality gate status post-audit: All 5 validators pass (exit code 0).

Rationale:
- A Dispatch dossier that claims source governance must actually have source governance — not structural form without governed content.
- Superlatives, quantitative claims without sources, and editorially framed claims in the source table Claim column all undermine the Dispatch Intelligence Standard.
- Correcting these issues protects the archive's reference integrity and sets the standard for Sprint 5 (Dispatch 011).

Governed by:
- DISPATCH_INTELLIGENCE_STANDARD.md
- CLAUDE.md
- QUALITY_GATE.md

Status: Accepted

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

## 2026-04-29 — Scanner Methodology Upgraded

ShovelsSale.com upgraded the `/scanner/` page from a simple interactive tool into a clearer Shovel Economy classification layer.

This decision strengthens the asset’s applied reference value by clarifying how the scanner interprets infrastructure, speculation, control, durability, and classification confidence.

Implemented changes:
- clarified scanner methodology
- strengthened classification language
- improved institutional explanation of scoring logic
- reinforced the scanner’s relationship to the Shovel Economy framework
- preserved the existing architecture and visual identity
- avoided monetization, backend logic, or false precision

Rationale:
- increase applied usefulness
- make the reference system more interactive
- strengthen the asset’s authority beyond static content
- support repeat usage
- reinforce the Doctrine → Framework → Scanner → Dispatch structure
- move ShovelsSale.com closer to a sovereign reference system with practical classification utility

Status: Accepted

## 2026-04-29 — Dispatch Reference Structure Upgraded

ShovelsSale.com upgraded the Dispatch section from a simple archive into a clearer analytical reference layer connected to the Shovel Economy framework and scanner methodology.

This decision strengthens Dispatch as the applied record of the system: where market cases, infrastructure signals, speculation exposure, and control-layer relevance are interpreted through the asset’s core doctrine.

Implemented changes:
- added a clearer reference method to the Dispatch archive
- connected Dispatch to the Framework and Scanner
- added visible classification summaries to existing dispatch entries
- preserved existing dispatch content and canonical structure
- avoided creating new dispatch entries in this phase

Rationale:
- make Dispatch function as an applied classification archive
- reinforce the Doctrine → Framework → Scanner → Dispatch structure
- improve user understanding of how cases are interpreted
- strengthen the asset’s reference authority
- avoid treating Dispatch as ordinary news or generic blog content

Status: Accepted

## 2026-04-29 — Framework Internal Taxonomy Upgraded

ShovelsSale.com upgraded the `/framework/` page into a clearer central taxonomy reference for the Shovel Economy system.

This decision strengthens the relationship between the Framework, Scanner, and Dispatch by making the core layers, classification roles, and analytical signals more explicit.

Implemented changes:
- clarified the internal taxonomy of the three structural layers
- added or refined classification roles including Hybrid
- defined the analytical signals used by the Scanner and Dispatch
- reinforced internal links to `/scanner/` and `/dispatch/`
- preserved the existing page structure and visual identity
- avoided creating new pages or changing URL architecture

Rationale:
- make the Framework the central taxonomy reference
- strengthen consistency across Scanner and Dispatch
- improve user understanding of the classification system
- support applied reference authority
- preserve conceptual discipline while increasing clarity

Status: Accepted

## 2026-04-29 — Homepage Authority Alignment Completed

ShovelsSale.com updated its homepage to reflect the asset’s current reference-system architecture more clearly.

This decision aligns the public entry point with the mature structure now present across the asset: Doctrine, Framework, Scanner, Dispatch, Blog, governance discipline, and quality-gate enforcement.

Implemented changes:
- clarified ShovelsSale.com as a governed Shovel Economy reference system
- reinforced the Doctrine → Framework → Scanner → Dispatch structure
- referenced Miner, Shovel, Gatekeeper, and Hybrid classification roles
- improved internal entry links, including the Blog
- reflected governance and quality-gate discipline without changing the visual identity
- preserved URL architecture and avoided redesign

Rationale:
- make the homepage accurately represent the current maturity of the asset
- strengthen first-impression authority
- reduce mismatch between homepage positioning and internal system depth
- improve navigation into the reference architecture
- preserve the existing design while improving strategic clarity

Status: Accepted

## 2026-04-29 — Manifesto Sovereign Alignment Completed

ShovelsSale.com lightly aligned the `/manifesto/` page with the current reference-system architecture without changing the core doctrine.

This decision updates the Manifesto so it reflects the asset’s mature structure: Framework, Scanner, Dispatch, governance discipline, and quality-controlled development.

Implemented changes:
- updated outdated future-facing wording now that Framework, Scanner, and Dispatch are active
- added lightweight internal references to the existing reference-system layers
- reinforced the governed posture of the asset
- preserved the original doctrine, tone, structure, and visual identity
- avoided redesign, monetization, or conceptual rewriting

Rationale:
- keep the foundational doctrine consistent with the current asset architecture
- prevent mismatch between Manifesto language and live system maturity
- strengthen coherence across Homepage, Manifesto, Framework, Scanner, and Dispatch
- preserve the Manifesto as doctrine rather than marketing copy

Status: Accepted

## 2026-05-04 — Weekly Workflow Clean-Tree Enforcement Fixed

ShovelsSale.com updated the weekly publishing workflow so generated tracked-file changes are staged before rebase and push operations.

This decision resolves workflow failures caused by publishing automation leaving tracked HTML files modified but unstaged after generation and tag synchronization.

Implemented changes:
- reordered the publishing pipeline so blog generation runs before Google tag synchronization
- staged tracked generated changes with `git add -u`
- added explicit clean-tree checks using `git status --porcelain`
- replaced ambiguous rebase failures with clear diagnostic output
- preserved strict workflow behavior instead of masking errors with stash-based recovery
- confirmed the Weekly Update + Security Scan workflow passes successfully

Rationale:
- keep weekly automation compatible with sovereign quality enforcement
- prevent generated tracked files from breaking rebase operations
- make workflow failures auditable
- preserve clean-tree discipline before publication
- avoid weakening validation or hiding generated changes

Status: Accepted

## 2026-05-04 — Dispatch Methodology Documented

ShovelsSale.com now includes `DISPATCH_METHODOLOGY.md` as the governing methodology for the Dispatch archive.

This decision formalizes Dispatch as an analytical record layer rather than a generic content feed, news section, opinion blog, or affiliate surface.

Implemented changes:
- defined the purpose and limits of Dispatch entries
- established the required Dispatch structure
- clarified metadata and classification standards
- aligned Dispatch with the Framework and Scanner methodology
- defined quality standards, rejection criteria, and publication workflow
- documented how Dispatch may support future monetization without weakening trust
- preserved institutional tone and reference-grade discipline

Rationale:
- prevent Dispatch from becoming generic content
- strengthen the applied archive layer of the Shovel Economy system
- make future entries structurally consistent
- support long-term authority, reports, newsletter development, and selective monetization
- reinforce the Doctrine → Framework → Scanner → Dispatch architecture

Status: Accepted

## 2026-05-06 — First Dispatch Atlas Sequence Completed

ShovelsSale.com completed the first sovereign Dispatch atlas sequence covering compute infrastructure, industrial bottleneck machinery, naming infrastructure, enterprise memory, web control, payment rails, commerce operating systems, and developer system-of-record infrastructure.

Implemented changes:
- deployed Dispatch 003 on strategic domain names
- deployed Dispatch 004 on Oracle and enterprise system-of-record infrastructure
- deployed Dispatch 005 on Cloudflare and the modern web control layer
- deployed Dispatch 006 on Stripe and payment rails
- deployed Dispatch 007 on Shopify and commerce operating systems
- deployed Dispatch 008 on GitHub and the developer system-of-record layer
- updated the Dispatch archive index with structured data for all eight entries
- created DISPATCH_ROADMAP.md establishing the sovereign archive sequence
- created assets/css/dispatch.css for consistent Dispatch presentation
- regenerated sitemap.xml to include all Dispatch pages
- preserved quality-gate enforcement throughout

Rationale:
- transform Dispatch from a content archive into a sovereign analytical atlas
- demonstrate the Shovel Economy across multiple market layers
- make the framework useful through applied cases
- increase the long-term reference value of the asset
- support future reports, methodology pages, and premium research products

Status: Accepted

## 2026-05-06 — Blog Foundation Presentation Upgraded

ShovelsSale.com upgraded the visual presentation of its Blog foundation essays into a coherent sovereign reference reading layer.

This decision completes the Blog presentation phase by ensuring that the individual blog articles visually align with the institutional dark/gold ShovelsSale identity instead of rendering as default browser pages.

Implemented changes:
- added a shared blog article presentation layer
- applied the sovereign dark/gold article layout across all current blog essays
- preserved article content, metadata, URLs, and internal links
- maintained the distinction between Blog primers, Framework taxonomy, Scanner classification, and Dispatch Atlas records
- kept the Blog as an educational entry layer rather than a generic publishing section
- preserved quality gate discipline

Rationale:
- make the Blog visually consistent with the wider ShovelsSale system
- strengthen reader trust and perceived institutional quality
- ensure foundational essays function as serious primers into the Shovel Economy
- support the progression from Blog to Framework, Scanner, and Dispatch Atlas
- prevent article pages from weakening the sovereign-grade presentation of the asset

Status: Accepted

DEC-2026-06-09 — McAfee False Positive and Canonical Redirect Hygiene Resolved

Date: 2026-06-09
Status: Closed
Area: Trust, Security, Canonical Routing, External Reputation

Decision:
ShovelsSale.com corrected its canonical redirect behavior and resolved the McAfee false-positive warning that previously marked "http://www.shovelssale.com/" as suspicious / potentially unwanted content.

Context:
McAfee had shown a warning for the "http://www" version of the domain. Investigation showed that the site required cleaner canonical routing from "http://www.shovelssale.com/" and "https://www.shovelssale.com/" toward the official non-www HTTPS root.

Action Taken:
A Cloudflare Redirect Rule was deployed to redirect "www.shovelssale.com" traffic to the canonical root:

"https://shovelssale.com/"

The rule preserves paths and supports cleaner canonical routing across the site.

Result:
The McAfee warning no longer appears, and the site now opens normally. This restores a critical trust layer for visitors, search engines, social sharing, and future strategic buyer review.

Strategic Rationale:
A sovereign-grade digital asset cannot carry unresolved browser/security reputation warnings. Resolving this issue strengthens trust posture, canonical discipline, public accessibility, and acquisition-readiness.

Affected Layers:

- Cloudflare canonical routing
- External reputation hygiene
- Search trust posture
- Social sharing confidence
- Strategic asset credibility

Reversal Conditions:
This decision should only be revisited if McAfee, another browser/security provider, or search console tools report a renewed trust or routing problem.

## 2026-06-09 — Dispatch 010 ARM Architecture Licensing Dossier Published (Sprint 4)

ShovelsSale.com published Dispatch 010 as the second full application of the Dispatch Intelligence Standard (v1.0), covering ARM Holdings and the Architecture Licensing Layer.

This decision extends the Dispatch atlas from nine to ten entries and introduces the Architecture Licensing Layer as a distinct structural category: the processor ISA and IP infrastructure that enables chip design without chip manufacturing.

Implemented changes:
- created Dispatch 010 as a source-governed intelligence dossier (dispatch/010.html)
- applied Dispatch Intelligence Standard v1.0 with 12 source-governed fact table rows
- classified ARM as Hybrid — Shovel (primary) / Gatekeeper (moderate) — High Confidence
- Scanner scores: Miner 16, Shovel 88, Gatekeeper 73
- documented the ARM/TSMC Gatekeeper distinction: ARM moderate (73) vs. TSMC strong (86) due to RISC-V as a credible open alternative
- included five analyst use cases, historical/current/future analysis, and dependency map
- updated dispatch/index.html with the ARM entry (numberOfItems 9→10, new archive item, layer map card)
- updated DISPATCH_ROADMAP.md with Dispatch 010 entry and sequencing logic
- regenerated sitemap.xml to include dispatch/010.html
- all five quality gate validators pass

Rationale:
- ARM's architecture licensing model is structurally distinct from every prior dispatch entry
- the specification layer sits above manufacturing (TSMC) and below compute applications (NVIDIA), completing a three-layer vertical in the atlas
- the RISC-V comparison makes ARM the first entry where the Gatekeeper ceiling is explicitly bounded by an open-source alternative
- publishing under the Intelligence Standard ensures source governance discipline is maintained across the second dossier

Governed by:
- DISPATCH_INTELLIGENCE_STANDARD.md
- CLAUDE.md
- QUALITY_GATE.md

Status: Accepted

## 2026-06-09 — Dispatch 009 Source Governance Audit Completed (Sprint 3C)

ShovelsSale.com performed a strict intelligence-quality audit of Dispatch 009 (TSMC Manufacturing Sovereignty Layer) as the first full application of the Dispatch Intelligence Standard (v1.0).

This decision records the audit findings and the corrections applied to bring the dossier into full compliance with DISPATCH_INTELLIGENCE_STANDARD.md before any further Dispatch development.

Audit findings and corrections:

- Factual error corrected: Arizona fab announcement year changed from "2022" to "2020" — the original announcement was May 2020; the CHIPS Act preliminary memorandum was April 2024.
- Hero subtitle softened: removed "entire modern technology economy" superlative, replaced with scoped structural language referencing leading-edge chip production specifically.
- Executive Brief softened: "most of the world's fabless chip designers" changed to "many of the world's leading fabless chip designers" — the broader claim was unsourced.
- Control-Layer section: added explicit "Analyst interpretation — Moderate Confidence" qualifier to "only TSMC has proven high-volume manufacturing" — this claim is directionally well-supported but stated too absolutely given Samsung Foundry exists as a partial alternative.
- Use Case 03 HTML corrected: number element was placed after content with a CSS order hack; restructured to match the consistent pattern used by use cases 01/02/04/05.
- "Millions of gallons" water claim removed: replaced with "enormous volumes" — the specific quantity had no source.
- Upstream dependency list annotated: added an explicit note that the supplier list represents analyst interpretation based on semiconductor industry supply chain structure, not verified primary disclosures.
- Japan fab (JASM) second fab claim: added explicit Watch Signal label — the second fab has been reported in T3 press but not confirmed in primary sources.
- DoD dependency claim corrected: changed from implying a direct TSMC-DoD relationship to accurately describing an indirect supply chain dependency through customers; labeled as Analyst interpretation.
- Source table column 6 renamed from "Claim Type" to "Why It Matters" and all 12 rows updated with meaningful structural relevance descriptions.
- Source table row 9 tier badge corrected: GlobalFoundries 2018 announcement is a T1 (official company press release), not T3.
- Source table row 10 tier badge corrected: TSMC press releases are T1 (primary/authoritative), not T2.
- Two new source table rows added: SMIC export controls (T1 — US DoC BIS Entity List and EUV export rules) and Apple's foundry transition from Samsung to TSMC (T3 — technology press).
- SMIC export control claim upgraded: added explicit source reference to US Bureau of Industry and Security (BIS) — T1, High Confidence.
- Apple-Samsung-TSMC migration claim: added source reference (T3) and dating (2014–2016); previously used in the text without a source table entry.
- PDF section updated: fact table count corrected from 10 to 12 following addition of 2 new rows.

Quality gate status post-audit: All 5 validators pass (exit code 0).

Rationale:
- A Dispatch dossier that claims source governance must actually have source governance — not structural form without governed content.
- Factual errors, unsourced superlatives, and claims used without source table entries all undermine the Dispatch Intelligence Standard.
- Correcting these issues before issuing Dispatch 010 protects the archive's reference integrity.
- The audit demonstrates that the Intelligence Standard works as a governance instrument, not merely a template.

Governed by:
- DISPATCH_INTELLIGENCE_STANDARD.md
- CLAUDE.md
- QUALITY_GATE.md

Status: Accepted

DEC-2026-06-09 — Scanner Custom Actor Preset-Carryover Bug Closed

Date: 2026-06-09
Status: Closed
Area: Scanner Engine, Runtime State, Trust Logic, UX Integrity

Decision:
ShovelsSale.com repaired the Scanner Engine’s custom actor logic so manually typed actors can no longer inherit stale preset signal values.

Context:
Live mobile testing showed that when a user typed a custom actor such as “Space x,” the Scanner could display “Custom Signal Analysis” while still reusing prior preset values such as high infrastructure density and control-layer strength. This created a trust issue because the interface appeared to generate actor-specific analysis while actually carrying forward previous preset signals.

Root Cause:
The preset-clearing condition depended on a state comparison that failed when "activePreset" was already null. In that case, typing a second custom actor did not trigger a reset because the old and new active-preset states both evaluated as null.

Action Taken:
A dedicated custom-mode path was introduced. Manual actor input now resets all ten signals to neutral 50/100, clears preset state, and marks the analysis as custom. The classify path independently recomputes the custom-neutral state, so stale event state cannot allow preset values to pass through.

Result:
Untouched custom actors now produce Unclear / Early Signal with Low Confidence until the user adjusts structural signals manually or selects a preset. Manually typing a preset name no longer silently loads preset values. Preset behavior remains explicit and user-controlled.

Strategic Rationale:
The Scanner must operate as a transparent classification instrument, not as a false automated company-research engine. This change protects trust by clearly separating preset-based structural starting profiles from manual custom analysis.

Validation:
Quality gate passed with all active checks. The page preserves one H1, SEO metadata, canonical posture, internal links, and static client-side operation.

Reversal Conditions:
This behavior should only be changed if ShovelsSale later introduces a governed, source-backed company intelligence layer capable of loading verified actor profiles intentionally.

