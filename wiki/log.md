# Atlas Wiki — Log

Append-only record of wiki activity. Each entry starts with `## [date] action | subject`.

## [2026-04-19] audited | WDAI tech debt — Phase 1 (Polaris)

Full tech debt audit against `wdai-foundation-platform`, Phase 1 covering architecture, critical paths, security, DevOps. 9 Must Fix / 19 Nice to Fix / 4 Negligible. Audit doc at `projects/wdai-tech-debt.md`. Two root-cause P0 findings: MainProtection ruleset is theater (0 approvals, no CODEOWNERS check) + 8-PR backlog stalled for lack of forcing function. Stripe webhook race condition exists on main (PR #569 fixes). Three Prisma schemas with model overlap — drift risk. No Sentry. Scripts dir (4285 LOC) bypasses lint/TS. CLAUDE.md docs drift after PRs #569/#571 merge. Phase 2 (duplication, file-size, deps, test coverage, docs line-by-line) deferred pending Builder + QA delegation.

## [2026-04-15] reorganized | Wiki sources index extracted from main index

Main index was 145 lines, sources alone ~95 lines. Created `sources/INDEX.md` with domain grouping (Danaher Pricing, LBS/VOC, HR/Copilot, Strategy, Freight/Ops, Microsoft/Snowflake, Quality, WDAI, Personal, Research). Main index now ~55 lines with a single link to sources sub-index. Per Polaris's recommendation (option 3).

## [2026-04-15] ingested | 30 Granola meetings (Mar 1–15 + Apr 15 backlog)

Batch ingestion of 30 meetings. Mar 1–15 covers: Martin 1:1 (compensation $228K, HR AI, McKinsey), HR transformation tollgate 2, freight kaizen prep (Cesar), Anish/Keith VOC sessions (SDLC, Node.js upgrade $88→$7.5K savings, unlimited AI currency), pricing excellence (McKinsey DDS + Contract AI), Beckman margin levers ($50–80M), Felix Rode IDN contract workflow, Ty Usrey LBS VOC, Craig/Alice community of practice, Josh/Andrew Copilot dashboard, PPG training (Karen Bogren), Snowflake demos (Cortex + Horizon), HR enablement (Craig/Chris, 5380 licenses needed), Echo calibration ($112M revenue), WDAI core team sync (Mar 4) + AI Foundations scaling, Geese MBA capital structure assignment, Patrick McKenzie/Frontier Audio client intro. Apr 15: Enterprise AI forward deployment strategy (post-Martin, $5M threshold, "Strike Team" concept). Two WDAI items routed technical.

## [2026-04-15] ingested | 15 Granola meetings (Mar 16–30 backlog)

Batch ingestion of 15 unprocessed meetings from Mar 16–30. Covers: LBS AI pilot planning (Keith/Anish/Ty VOC sessions), Martin 1:1 on token budgets, Sameer Doshi India finance use cases, Cepheid pricing strategy (McKinsey $46–75M), Chris Bouda finance AI prioritization, Microsoft Copilot licensing + IP agent prototype, Cortex Code workshop, Google Analytics with Lorie (WDAI), AI strategy panel (Women Who Rule AI), Patrick McKenzie client intro (Frontier Audio). Two technical items routed to Polaris (IP agent, GA/WDAI).

## [2026-04-15] improved | Polaris sub-agents (Builder, Designer, QA)

Updated all three sub-agent definitions: added "read CLAUDE.md first" as step 1, workspace paths for cross-repo awareness, structured report-back formats. QA got WebFetch in allowed-tools for smoke testing. Builder/Designer report-back now includes files changed, concerns, and blockers in consistent format.

## [2026-04-15] built | Heartbeat skill + gather-context script

Adapted from unclaw (github.com/shahshrey/unclaw). PowerShell script gathers context deterministically (memory staleness, wiki inbox, git status, slack-watcher health, scheduled tasks, disk space, runtime errors). Heartbeat skill reads output and acts only if actionable. Running as `/loop 30m` in active sessions, not Task Scheduler.

## [2026-04-15] shipped | Defrag skill for WDAI (PR #560)

Polaris built `/defrag` skill for wdai-foundation-platform. Scans for duplicated components, inconsistent patterns, dead code, shared logic. Verifies findings before presenting, requires user confirmation before fixing. PR assigned to Helen (helenlkupp). First run found 6 issues (0 dupes, 2 inconsistencies, 2 dead code, 2 shared logic).

## [2026-04-15] built | Slack Socket Mode Watcher (shared agent service)

Polaris built `C:\Workspace\agents\slack-watcher\` — persistent Socket Mode listener replacing the old Discord watcher. Watches #atlas-cos and #polaris-tl, routes to the right agent, spawns Claude sessions. Config-driven: add new agents via config.json entry. Running as `node watcher.mjs`.

## [2026-04-15] pipeline-confirmed | Atlas → Polaris transcript handoff validated

Polaris confirmed end-to-end pipeline working:
- Wiki source read: OK
- Granola transcript pull (via claude.ai MCP): OK
- Slack #polaris-tl read: OK (scopes fixed by Dina)
- Technical review completed for Rebekah/Helen/Madina call

**Atlas:** Pipeline is live. Continue routing `routing: technical` items to #polaris-tl. Polaris will pick them up via wiki inbox check on session start + Slack read. No changes needed on your side.

## [2026-04-15] ingest | Rebekah <> Helen / Madina — Analytics & Technical Roadmap

Post-meeting transcript assessment (first run of new pipeline). WDAI call with Rebekah Leslie-Hurd, Helen Kupp, Madina. Routed as **technical** — covers PostHog analytics cleanup, staging environment, branch protection, CI analytics skill, on-call engineering agent vision. Polaris notified via #polaris-tl.

- `sources/2026-04-15-rebekah-helen-madina-analytics.md`

## [2026-04-14] ingest | 10 Granola transcripts (Mar 31 - Apr 8, 2026)

Batch ingestion of 10 Granola meeting transcripts covering LBS San Diego site visit prep and execution, RegDes regulatory AI demo, McKinsey pricing diagnostic for Leica, and finance Copilot training planning.

**Sources created (10):**
- `sources/2026-04-08-ai-tools-training-interactive.md` — Training workshop feedback, interactive polling tool development
- `sources/2026-04-08-lbs-copilot-training.md` — Day 1 Copilot training: architecture, CLI agents, customization, licensing
- `sources/2026-04-08-ai-code-review-strategy.md` — AI code review strategy, automated testing, Indica partnership, revenue model
- `sources/2026-04-08-budget-cap-backend.md` — $600K infra budget, GPU needs, SAM backend rebuild, GitHub migration desire
- `sources/2026-04-08-robot-arm-recap.md` — Ozan's $450 robot arm demo, Cursor leaderboard metrics, team dynamics
- `sources/2026-04-07-remote-scan-settings.md` — APQ flexibility, Smart Scan architecture, remote manual scan development
- `sources/2026-04-03-regdes-demo.md` — RegDes regulatory AI platform (translation, forms, Clara agentic AI, May v6.0)
- `sources/2026-04-02-chris-bouda-sync.md` — Finance Copilot training plan (~6 sessions, 200-300 users, DC visit proposed)
- `sources/2026-04-02-lbs-fireside-chat-planning.md` — Fireside chat goals, Anish's 3K->30K image story, Rovo gap, API access need
- `sources/2026-03-31-margin-expansion-leica.md` — McKinsey pricing diagnostic: $25-35M Leica opportunity, 3-year ramp

**Pages updated (3):**
- `projects/github-copilot-adoption.md` — Added 9 new source refs, 5 new key people (Ty detail, Ozan, Nikolai, Sean, Melbourne), 7 new findings (Copilot architecture, licensing, Cursor leaderboard, infrastructure, Rovo gap, API access)
- `projects/pricing-ai.md` — Added Leica-specific opportunity section ($25-35M, 27K SKUs, implementation timeline)
- `projects/finance-ai.md` — Added Copilot training plan section (Chris Bouda sync), DC visit proposal

**Reflection:** No contradictions found. The Leica $25-35M figure is a component of the previously documented $51-71M total Danaher pricing opportunity — consistent. LBS infrastructure budget ($600K) and GitHub migration desire are new data points not previously captured. The Cursor leaderboard metrics (Blaze at 71K, LBS at 40K+) provide concrete adoption data complementing the earlier dashboard stats. RegDes is a new entity not previously in the wiki — may warrant its own project page if evaluation continues.

**Remaining unprocessed:** ~17 meetings from Mar 16 - Mar 30 still need ingestion (excluding the two "New note" entries).

## [2026-04-14] ingest | 10 Granola transcripts (Apr 9-14, 2026)

Batch ingestion of 10 recent Granola meeting transcripts covering LBS on-site training week, Helen 1:1, DHA orientation, and finance sync.

**Sources created (10):**
- `sources/2026-04-14-ai-foundations-registration-training.md` — EAI team debrief + WDAI AI Foundations registration flow redesign
- `sources/2026-04-13-madina-helen-1on1.md` — Signal framework review, value scoring (ops-first), product prioritization
- `sources/2026-04-13-dha-program-orientation.md` — OSU DHA course planning with admissions advisor
- `sources/2026-04-10-lbs-ai-tools-pulse.md` — Interactive pulse session with LBS San Diego team
- `sources/2026-04-10-anish-fda-demo.md` — FDA slide scanning automation ($350 in API credits, 40K screenshots)
- `sources/2026-04-10-eai-workshop-debrief.md` — Post-training debrief, training vendor critique
- `sources/2026-04-10-m365-ai-productivity-demo.md` — MCP connectors, M365 Copilot desktop features
- `sources/2026-04-09-bryan-conn-ai-performance.md` — Non-developer power user VOC (Salesforce MCP, ImageScope revival)
- `sources/2026-04-09-finance-ai-use-cases-monthly.md` — Monthly finance use case prioritization with Chris Bouda, Nick Johnson
- `sources/2026-04-09-github-migration-planning.md` — LBS source control state (Perforce/BitBucket/GitLab), migration blockers

**Pages updated (3):**
- `projects/github-copilot-adoption.md` — Added LBS training week section, Bryan Conn + Ty as key people, 8 new source refs
- `projects/dha-admissions.md` — Full course plan, faculty details, program logistics from advisor session
- `projects/finance-ai.md` — Apr 9 monthly sync notes, Snowflake data lake strategy, Nick Johnson role

**Remaining unprocessed:** ~21 meetings from Mar 16 - Apr 8 still need ingestion.

## [2026-04-14] ingest | 10 Granola transcripts (Dec 11-16, 2025)

Batch ingestion of the 10 oldest unprocessed Granola meeting transcripts.

**Sources created (10):**
- `sources/2025-12-11-quality-audit-mpl-intake.md` — QA audit AI project ($300k budget, 51% ROI, 127+ sites)
- `sources/2025-12-11-wdai-community-huddle.md` — Community meet & greet, 20+ members, program overview
- `sources/2025-12-15-jainendra-meet-greet.md` — Data engineer on Krishna's IDC team, Enterprise Search concerns
- `sources/2025-12-15-wdai-2026-planning.md` — Website migration plan, volunteer strategy, instructor certification
- `sources/2025-12-15-david-gering-meet-greet.md` — 30yr AI veteran, training/enablement lead, Innovation Catalyst
- `sources/2025-12-15-finance-use-case-part2.md` — 95% automation-focused, data centralization strategy
- `sources/2025-12-15-finance-martin-siyu-madina.md` — $13M target, 460 finance team, $5M+ ROI bar
- `sources/2025-12-16-ppg-year-end.md` — All-project portfolio review, 2026 priorities, productivity framework
- `sources/2025-12-16-martin-1on1.md` — Copilot metrics (26% WAU, 2883 deployed), role clarity issues
- `sources/2025-12-16-krishna-meet-greet.md` — Enterprise AI reality check, funding pressure ($50M->$200M targets)

**People created (2):**
- `people/david-gering.md` — AI Training & Enablement Lead, Danaher Brain team
- `people/krishna.md` — IDC / Platform Core Team Lead, Danaher

**Projects created (2):**
- `projects/enterprise-search.md` — Unified search, two-track (operational + Copilot vs Glean eval)
- `projects/finance-ai.md` — Finance function AI enablement, $13M target potential

**Pages updated (5):**
- `people/martin-kang.md` — Added 3 earlier source references (Dec 2025)
- `people/helen-kupp.md` — Added 2 earlier source references (Dec 2025)
- `projects/github-copilot-adoption.md` — Added 3 earlier source references with Dec 2025 baseline data
- `organizations/wdai.md` — Added Nichole Sterling to core team
- `index.md` — Added all new pages

**Reflection:** No contradictions found. Dec 2025 data provides earlier baseline for GitHub Copilot (2,883 deployed, 26% WAU) that's consistent with Apr 2026 state (<50% logged in). WDAI platform migration timeline (Jan 2026) aligns with existing wiki. Krishna's funding pressure context ($50M->$200M targets) adds important backdrop to the $40M productivity target in later sources.

## [2026-04-14] lint | Full wiki audit and cleanup

**Fixes applied (11):**
- Added 8 orphan source pages to index.md (voice profile, DHA statement, career targets, resume v7, karpathy feedback, openclaw research, Helen prep, Dina self page)
- Fixed broken wikilink in `decisions/2026-04-13-value-scoring-ops-first.md` — pointed to nonexistent `sources/2026-04-13-madina-helen-1on1`, replaced with note + prep page link
- Fixed contradiction in `organizations/wdai.md` — merged duplicate "Dina's Role" sections, updated frontmatter from stale "AI Enablement Lead" to current "VP/CPO"
- Updated stale date in `projects/dha-admissions.md` — advising session marked as attended (was yesterday)
- Updated stale date in `projects/elizabeth-mckenzie-redesign.md` — overdue count updated
- Added `org: personal` to 6 project pages missing required field (nala-paw, media-theater, madina-portfolio, tax-app, career-ops, raunch)
- Added Key Sources section to `people/brigitte-lyons.md` and `people/lauren-irving.md`
- Added board presentation source link to `people/martin-kang.md`
- Added overdue Brigitte meeting note to `people/brigitte-lyons.md`
- Deleted 2 empty root-level files (`2026-04-12.md`, `2026-04-13.md`) that violated wiki structure

**Flagged for Dina (5):**
- Missing source page: Apr 13 Helen 1:1 Granola transcript needs ingestion (referenced by both decision pages)
- Schema gaps: `people/jr-gregory.md` missing `org` field, `people/dina-gbotoe.md` uses non-standard `type: self` — left as-is since these are special cases
- Schema gaps: Several source pages use non-standard `source_type` values (`feedback`, `preferences`, `meeting-prep`) — SCHEMA.md may need updating to include these types
- Elizabeth McKenzie lead: 23+ days overdue — needs decision to follow up or close
- Brigitte meeting: still overdue from Mar 30 action items — needs scheduling

## [2026-04-13] create | Decision — CPO Mission & Vision
- Mission: "WDAI doesn't just teach AI — we run on it."
- Vision: graduation ecosystem, ops people as primary customer
- Updated index.md

## [2026-04-13] create | Decision — Value Scoring Ops First
- Created first decision page: `decisions/2026-04-13-value-scoring-ops-first.md`
- Helen flipped the priority: ops impact > member impact for 2026. Portal is "good enough" for members.
- Additional refinements: audience & impact reframing, graduation model, access level classifier, cut test, Gumloop descoping, roadmap visibility, core team VOC
- Updated index.md with Decisions section

## [2026-04-13] create | WDAI Product Spectrum Registry wiki page
- Created project page: `projects/wdai-product-spectrum-registry.md`
- Documents the Google Sheet structure, origin (Mar 30 Helen 1:1), access details
- Cross-linked with signal detector and Mar 30 source page

## [2026-04-13] create | Helen 1:1 prep agenda
- Created meeting prep: `sources/2026-04-helen-1on1-prep.md`
- 5-section agenda: registry walkthrough, top 5 decisions, bus factor cleanup, signal detector pitch, action item checkpoint
- Pulled from Mar 30 transcript, registry sheet, and signal detector spec

## [2026-04-13] create | WDAI Product Signal Detector spec
- Created project page: `projects/wdai-product-signal-detector.md`
- Spec for Slack watcher that detects product/tool build signals across WDAI channels
- Classifies by relevance (personal vs. WDAI) and maturity (ideation → deployed)
- Feeds into the Product Spectrum Registry sheet
- Ready for dev agent handoff after Madina + Helen review open questions
- Updated index.md with signal detector + registry entries

## [2026-04-12] classify | Meeting type classification for 8 Granola transcripts

Added `meeting_type` frontmatter to all 8 source pages per schema's classify-before-extract workflow:
- **1:1** (4): `2026-01-26-performance-review-martin`, `2026-02-10-martin-1on1-dlc-conference`, `2026-03-30-madina-helen-1on1`, `2026-04-02-martin-1on1`
- **strategy** (3): `2026-03-02-danaher-board-ai-presentation`, `2026-03-10-pricing-ai-strategy`, `2026-04-06-github-copilot-adoption`
- **team-sync** (1): `2026-04-01-wdai-core-team-sync`

No content rewrites needed — existing summaries already covered type-specific details well. No cross-page contradictions found.

## [2026-04-12] research | Chief of Staff Role Definition & Atlas Recommendations

Comprehensive research on the CoS role across corporate, government, and AI-agent contexts. Synthesized into two source files:
- `sources/cos-role-research.md` — Role responsibilities, operating cadences, frameworks (McChrystal, RAPID), CoS vs EA distinction, traits from job postings, AI CoS landscape 2025-2026, gap analysis vs Atlas
- `sources/cos-atlas-recommendations.md` — 10 specific capability recommendations for Atlas with implementation details, mapped to existing scheduled tasks, wiki, and Discord briefs. Priority-ordered by effort vs impact.

## [2026-04-12] update | DHA Admissions — Accepted

Dina confirmed acceptance into OSU's DHA program. Updated `organizations/osu.md` and `projects/dha-admissions.md` status to "accepted." She's now building her course schedule.

## [2026-04-12] ingest | 8 Granola meeting transcripts

Batch ingestion of 8 high-priority meeting transcripts from Granola (Jan-Apr 2026).

**Sources created (8):**
- `sources/2026-01-26-performance-review-martin.md` — Performance review walkthrough (3/5 meets expectations)
- `sources/2026-02-10-martin-1on1-dlc-conference.md` — DLC conference debrief, decision to deprioritize finance function
- `sources/2026-03-02-danaher-board-ai-presentation.md` — Board presentation on AI productivity (software + legal)
- `sources/2026-03-10-pricing-ai-strategy.md` — McKinsey pricing AI architecture for Beckman/Cepheid
- `sources/2026-03-30-madina-helen-1on1.md` — WDAI role scope decision (holistic/CPO approach)
- `sources/2026-04-01-wdai-core-team-sync.md` — Data dashboard, Q2 priorities, decision norms
- `sources/2026-04-02-martin-1on1.md` — Pod model org restructuring pitch, Beckman $10M win
- `sources/2026-04-06-github-copilot-adoption.md` — Adoption metrics review, field visit planning

**Projects created (2):**
- `projects/github-copilot-adoption.md` — 3,000 developers, $40M+ target, <50% logged in
- `projects/pricing-ai.md` — McKinsey-led, $51-71M opportunity, Q2 implementation target

**People created (1):**
- `people/sandhya-simhan.md` — WDAI Core Team, marketing & content

**Pages updated (4):**
- `people/martin-kang.md` — Full name (Martin Kang), relationship context, current priorities, key sources
- `people/helen-kupp.md` — Added data dashboard note, key sources
- `organizations/danaher.md` — Manager name updated to Martin Kang
- `organizations/wdai.md` — Added updated role definition, linked Sandhya

**Index updated** with all new pages.

## [2026-04-12] init | Wiki created
Atlas setup session. Created initial structure with people, organizations, projects, decisions, and sources directories. Seeded index with known entities from calendar, email, and resume data.

## [2026-04-19] debug | Watcher self-loop fix + inter-agent rubric
**Atlas:** Debugged Slack watcher spawning 9 replies per "hey" in #atlas-cos. Root cause: per-agent token split broke `event.user === botUserId` self-filter (listening bot is Polaris's ID, reply bot is Atlas's ID — different users). Consulted Polaris, he confirmed and approved one-line fix at the bot_message handler. Branch `fix/watcher-self-loop` commit 8e795fc pushed. Polaris's own WIP (token split, Windows claude.cmd + stdin-piping spawn fix, resilience) left unstaged for him to split into 3 commits on top.

**Atlas:** Also formalized inter-agent Slack discipline in `infrastructure.md` — 4 triggers each way, what stays in wiki vs Slack, what escalates to Dina. Heartbeat skill now reads #polaris-tl hourly using `.claude/runtime/polaris-last-seen.ts` as the watermark so Polaris replies don't get missed.
