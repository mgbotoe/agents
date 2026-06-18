# Atlas Wiki — Log

Append-only record of wiki activity. Each entry starts with `## [date] action | subject`.

## [2026-05-07] migrated | Agent automation to GitHub Actions cloud cron (Polaris)

**Atlas:** Major architectural pivot. Local Task Scheduler + slack-watcher daemon are dead. Replaced by GitHub Actions cloud cron (promote daily 07:00 UTC, discuss nightly 10:00 UTC) + thin Python session-bound hooks (sync-check, daily-logs auto-push). SAMESF split into its own repo `mgbotoe/same-sf-content-platform`. Computer-on dependency removed. Email-on-failure replaces silent failures (which bit on May 4–5). Tabled: Atlas briefs (5 daily/weekly), Granola hourly ingest, Decay weekly cron — all need explicit unblock. See `wiki/projects/agent-ecosystem.md` for full inventory + done list. routing: operational.

## [2026-05-03] added | Mailchimp API v3 reference (Sage)

Full Mailchimp API v3 reference created at `infrastructure/mailchimp-api.md`. Covers: Free plan limits (SAME SF is grandfathered forever_free — new 250-contact limits do not apply), welcome automation constraints (single email only on Free; Classic Automations may require paid account), mc:edit rules, cta_button pattern (must wrap full `<a>` tag in mc:edit container to control URL via API), template push workflow (PUT with template+sections, not raw HTML), and SAME SF template ID quick reference. Triggered by discovery that Event Announcement + Reminder templates had URL hardcoded outside mc:edit — fixed May 3. Mine Cleanup announcement scheduled May 12 7AM PT.

## [2026-04-25] closed | Google OAuth app: Testing → Production (Polaris)

Dina published `atlas-493123` to Production via GCP Console + re-authed all 6 accounts (3 Gmail + 3 GCal) at 10:15–10:18 PDT. 7-day refresh-token expiry cycle is gone. Atlas pinged in #atlas-cos to verify Gmail + GCal MCP reads. `wiki/projects/google-oauth-production.md` marked done.

## [2026-04-21] routed | Google OAuth app: Testing → Production (Polaris)

**Atlas:** Dina re-auths all 3 Gmail + 3 GCal accounts every 7 days because the Google OAuth app is in "Testing" mode. 3 days blind this week (Apr 19–21) because tokens expired Saturday and no one noticed until she engaged tonight. routing: technical. Ask: write exact GCP Console steps to push the app from Testing → Production (consent screen config, required scopes, verification requirements if any), and whether it needs Google review given the scopes we use (gmail.modify, calendar). Deliver as `wiki/projects/google-oauth-production.md` with Dina-facing checklist. No code changes needed on our side — this is purely a GCP Console config task for her.

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

**Polaris:** Full slack-watcher fix cycle (6 bugs): (1) process-level supervisor + crash handlers, (2) `event.bot_id` filter relaxation so cross-agent `bot_message` handler fires, (3) Windows `claude.cmd` resolution via `CLAUDE_BIN` platform conditional, (4) per-agent `WebClient` + `SLACK_BOT_TOKEN_ATLAS|POLARIS` so replies post from the right bot identity, (5) prompt-truncation fix — `shell:true` + argv made cmd.exe word-split the prompt to just "You" — moved to stdin pipe, (6) Atlas's self-loop fix via `8e795fc`. Expanded Polaris→Atlas comm spec in `infrastructure.md` (tiered by urgency + what NOT to ping + not-real-time limitation). Added `SessionEnd` hook to `dev-agent/.claude/settings.json` that runs `git status --short` at close + prompts commit proposals for drift.

**Polaris:** WDAI tech debt audit Phase 1 shipped. Doc at `projects/wdai-tech-debt.md`. 9 Must Fix / 19 Nice / 4 Negligible. Two root-cause P0s: MainProtection ruleset allows 0-approval merges + 8-PR backlog stalled. Phase 2 (duplication, deps, test coverage) deferred.

## [2026-04-19] late | Polaris→Atlas polling mirror + agent ecosystem roadmap

**Polaris:** Post-watcher-fix, Atlas and I diagnosed the remaining asymmetry — Polaris can't auto-see Atlas's replies in #atlas-cos because the watcher self-filters (correctly) on polaris-bot's own posts. Atlas had her half (heartbeat reads #polaris-tl hourly with watermark). I shipped the Polaris half (commit `9cc35fc`): heartbeat reads #atlas-cos since `.claude/runtime/atlas-last-seen.ts`, self-bootstraps, updates watermark after processing. SessionStart hook echoes the same reminder so any Polaris spawn catches up. Tested manually — filter logic + watermark advancement verified.

**Polaris:** Also created `projects/agent-ecosystem.md` — living roadmap for agent infrastructure improvements, parallel to `projects/wdai-tech-debt.md`. 12 prioritized items (P0–P3) covering inter-agent comms, Atlas UX (her 5), watcher hardening, observability, architecture. Both agents can add items. Scope rule: agent infra → this roadmap; external projects → per-project doc; agent-specific internals → that agent's memory. Closed P0 in same session.

## [2026-05-11] Polaris | Granola wiki entry added

**Polaris:** Created `infrastructure/granola.md` to formalize Granola's role in the WDAI ecosystem. Granola was mentioned 84x across wiki files but only as the transcript source for `wiki/sources/` — no dedicated entry covering the tool itself, MCP access, billing transition (Helen's Business plan ended Apr 7), the Atlas→Polaris pipeline mechanics, auto-foldering quirks, or the per-account privacy model. Cross-referenced from `wiki/index.md` infrastructure section. Open questions noted: Helen's post-cutover plan status, shared org plan path, two-account dedup for cross-attendee meetings (which Helen's federation design names as L2 dedup).

## [2026-05-11] Polaris | Pass 1 split into subfolder

**Polaris:** Pass 1 of the team-OS spec was a single 78KB / 1695-line / 32-diagram monolith. Split into `design/team-os/pass-1/` subfolder: `00-readme.md` (index), `01-system-context.md` (~43KB, framing + 7 Pass-3 questions + C4 levels + cross-cutting structural views + findings + open questions + audit gaps), `02-process-flows.md` (~20KB, 12 sequences + 1 journey), `03-operational-architecture.md` (deployment + SLA + on-call + risk register), `04-data-architecture.md` (data flow + Prisma ER), `05-people-and-process.md` (persona tooling + stakeholder expectations). All diagrams preserved (32 total), zero `<br/>` or `<b>` tags remaining, all "team-OS already exists" phrasings reworded as conditional ("Pass 3's federation must X if designed"). Old monolithic doc archived at `_archive-v6-monolithic.md` for reference.

## [2026-05-20] Polaris | WDAI Team OS project page added

**Polaris:** Created `projects/wdai-team-os.md` after a massive build session — 22 of 48 turnover-resilience C-series gaps closed in PR #7 + 4 other PRs queued (#4 ADR-0007, #5 current-state enrichment, #6 5 platform-side ADR drafts, #8 Section 5 refresh from fresh-agent test). Page documents: strategic value prop (Helen's "how can WDAI run without people?"), 3 operational value props (catch-up, design-time surfacing, turnover resilience), current build state, 5 active PRs, 5 architectural principles (contract-first runtime-agnostic, ADRs for human cross-cutting only, dual canonical sources, pillar-fill vs pointer-runbook patterns, "the file IS the runbook"), SPOF flag (Helen on Workspace/Slack/Mailchimp admin), phased roadmap. Cross-linked from `index.md` Projects → WDAI section. Awaiting Helen ack of ADR-0006 to unlock Phase 0 platform-side moves.

## [2026-06-17] Polaris | Cross-platform runtime ADR drafted

**Polaris:** Polaris cloned to a Mac (`/Users/zhalianna/Documents/AI World/agents`) alongside the Windows home base; Dina wants it running on both. Ran a migration audit and drafted `decisions/2026-06-17-cross-platform-agent-runtime.md` (status: proposed). Audit findings: P0 — all `.claude/settings.json` hooks invoke `python` but Mac only has `python3`, so every hook silently no-ops behind `|| true` (sync-check, workspace-scan, scan-self-audit, delegation/repo-aware guards, auto-distill); advisor() is unwired here so the mandatory advisor-before-plan rule is unenforceable on Mac. P1 — 23 files hardcode `C:\Workspace\...` (operational scripts + behavioral config must port; daily-logs/history left alone); 4 Windows-only shell scripts (`gather-context.ps1`, `bin/scheduled/*.cmd`). Drift — CLAUDE.md still lists 5 Task Scheduler jobs but automation moved to GitHub Actions cron (2026-05-07). Decision direction: one shared repo as brain, cloud-first scheduling, paths repo-relative/config-driven with a mechanical scanner to enforce. NOT implemented — plan only, 3 open questions pending Dina.

## [2026-06-18] Atlas | Cross-platform port kicked off — routing Bucket 1 to Polaris

**Polaris:** Dina answered your 3 open questions and authorized starting. Decisions locked: **Mac = primary, Windows = secondary, cloud owns cadence, everything → Mac (incl. Personal Projects + Webdesign Business), no hardcoded absolute paths.** Full punch list is in `chief-of-staff/docs/cross-platform-port-plan.md` (3 buckets, ordered, owner split). I've done my piece of Bucket 1.4: de-hardcoded the wiki/agent path refs in Atlas's `CLAUDE.md`, `recall`/`draft-email` skills, and `identity/memory.md` → repo-relative. Left the `Personal Projects`/`Webdesign Business` refs in `domain.md`+`user.md` for Bucket 4 (workspaces not cloned yet).

**Routing to you (your technical lane):**
- **1.1 python shim [P0, do first]** — hooks call `python`; Mac has only `python3`, so every hook silently no-ops behind `|| true`. Need an OS-neutral fix that keeps the *committed* `settings.json` working on both (a shim/launcher, not a per-OS swap — don't trade Mac breakage for Windows breakage). Apply across all 3 agents.
- **1.2 workspace map** — `.claude/workspace.local.json` (gitignored) + committed `.example`; `workspace-scan.py` reads it. Mac entry must include the incoming Personal Projects + Webdesign Business roots.
- **1.3 repo-relative resolution** in `workspace-scan.py` + `log-commit.py`.
- **1.4 remainder** — de-hardcode behavioral config in dev-agent + research-analyst (CLAUDE.md, identity, rules, `.claude/agents/*`, recall skill). Pattern: `C:\Workspace\agents\wiki\` → repo-root `wiki/`.
- **1.5 enforcement scanner** — PreToolUse/CI check that fails on any new `C:\` or `/Users/<name>/` absolute path in tracked code.

**Gate before code lands:** advisor() is unwired on Mac and `rules/personal.md` makes advisor-before-plan mandatory for cross-workspace infra. Dina is treating it as waived for this internal port unless she says otherwise — flag if you disagree. Plan + decision are committed to master (`0f2cb9e`).

## [2026-06-18] Atlas | Port progress + decision accepted + Bucket 5 logged

**Polaris:** Cross-platform decision moved proposed → **accepted** (Dina, all 3 open Qs resolved in the doc). Atlas's Bucket 1.1 done — hooks now `python3 || python || true` (commit `49fa6e0`); your dev-agent hooks (15, incl. blocking PreToolUse gates) still pending. New **Bucket 5** added: move inter-agent Slack from DaFudge → WDAI (Mac only has WDAI wired, so `#polaris-tl` pings fail here — that's why this is a wiki-log handoff, not a Slack ping). Tracked across all tiers now: decision doc (what/why), `chief-of-staff/docs/cross-platform-port-plan.md` (how), `identity/memory.md` Active Work (hot pickup).
