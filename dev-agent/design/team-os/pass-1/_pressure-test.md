# Pass 1 · Self-pressure-test

**Purpose:** honest audit of every major claim in Pass 1 against the source data I actually have. Surfaces fabrications, inferences-asserted-as-fact, and true gaps.

**Evidence tiers used below:**
- **A — VERIFIED.** Direct read of source, verbatim quote, or counted from raw data I have in context.
- **B — SOURCED but not deep-verified.** Mentioned in a deep-dive doc or Slack channel I read but not independently re-checked.
- **C — INFERRED.** Extrapolated from indirect signal. Plausible but not confirmed.
- **D — FABRICATED OR ASSUMED.** Stated as fact in the docs but I cannot point to a source. Real gap.

---

## Claims by tier

### Tier A — VERIFIED

| Claim | Source |
|-------|--------|
| 3 Slack tokens in `wdai-foundation-platform/.env.example` (`SLACK_BOT_TOKEN`, `SLACK_MEMBER_BOT_TOKEN`, `SLACK_ADMIN_BOT_TOKEN`) | Direct read of `.env.example` |
| `web/lib/slack.ts` exports 10+ posting functions | Direct grep of file |
| `web/lib/slack-admin.ts` exports 6 functions (new member, churn, no-Wix-purchase, weekly stats, recording approval, upload fail) | Direct grep |
| `slack-admin.ts` header verbatim: *"This replaces the Railway internal webhook relay…"* | Read file header |
| `wdai-marketing` daily cron paused 2026-04-21 | Verbatim comment in `.github/workflows/calendar-sync.yml` |
| `daily-digest` cron at 8am UTC queries AuditLog for `cron.*` and posts to `#devops-website-alerts` | Read of `web/app/api/cron/daily-digest/route.ts` header + EXPECTED_CRONS object |
| `course-update-agent` 1st of month, `website-content-agent` 15th of month | Read of `.github/workflows/course-content-agent.yml` and `website-content-agent.yml` |
| AdminBot bot_id `B08GF1SGGNL`, 197 messages in `#devops-admin-mgmt` Jan 1–9 | Counted from saved channel read |
| Madina's Apr 14 #team-core post: *"need an environment where tools made for your pillar lives…"* | Verbatim Slack channel read |
| Helen's Granola Business plan ended Apr 7 | Helen's Feb 12 #team-agents post verbatim |
| Helen's Mac mini on VLAN | Helen's Mar 8 #topic-openclaw post |
| Sheena May 10 "still in reading phase" | Verbatim #topic-openclaw read |
| Brigitte's GWorkspace admin since Mar 4 | Helen Mar 4 #team-core verbatim |
| `mailchimp-cc` CONTRIBUTING.md tiered model (runbooks→skills→source) | Direct read |
| Helen Mar 11 platform multi-app explanation (3 separate Slack apps) | Verbatim #team-agents read |
| `Schema migration Expand-Contract` pattern | Verbatim from `wdai-foundation-platform/CLAUDE.md` |
| Pattern's weekly posts to `#team-core` | Read multiple Pattern messages in saved channel data |
| `course-update-agent` uses `AGENT_DATABASE_URL` separate from main DATABASE_URL | Verbatim from `course-content-agent.yml` |
| `x-admin-secret` header pattern in `wdai-admin/weekly-stats.yml` | Sub-agent deep-dive (which I have report for) |
| `wdai-marketing` has 239 vitest tests | Sub-agent deep-dive |
| `wdai-foundation-platform` has `docs/adr/` empty | Direct `ls` |
| `.github/CODEOWNERS` in platform = 49 lines | Direct read |
| Sheena PR'd to `mailchimp-cc` for AI Basics email redesign Apr 20 | Verbatim #team-core read |
| Brigitte PR'd pre/post assessment to `mailchimp-cc` Apr 27 | Verbatim #team-core read |
| Helen's May 9 "decided to download Cowork and point at OpenClaw config files" | Verbatim #topic-openclaw read |
| Madina's Apr 20 "watching my techlead agent work with my cos to fix her own bug" | Verbatim #topic-openclaw read |
| `wdai-foundation-platform/web/vercel.json` has Vercel cron entries (count contested — see Tier B) | Direct read |
| Reference-pattern mini-diagram: `wdai-admin weekly-stats.yml → curl POST x-admin-secret` | Sub-agent deep dive verbatim |

### Tier B — SOURCED but not deep-verified

| Claim | What I have | What I'd need to verify it |
|-------|-------------|----------------------------|
| Wit runs the Meet→Vimeo EOD pipeline at 5:30pm PT | Pattern's Mar 20 post mentioned "Meet→Vimeo EOD pipeline" agent named Wit at 5:30pm PT cron in cron list | Read Wit's actual scheduler config (don't have) |
| Sentry is in use for the platform | Madina told me + `perplex_computer/space instruction.txt` lists Sentry as a read-only credential | Find Sentry SDK initialization in platform code (didn't read) |
| Datadog in `wdai-admin` for circuit-breaker metrics | Sub-agent deep dive | Verify from `wdai-admin` source (sub-agent read, I didn't) |
| `wdai-lumabot` reads Airtable as silent source-of-truth for active members | Sub-agent deep dive | Read `wdai-lumabot/src/airtable/members.ts` (sub-agent did, I didn't) |
| `wdai-lumabot` has zero test files | Sub-agent deep dive | I trust the sub-agent's grep |
| `wdai-admin` has hardening features feature-flag-gated off | Sub-agent deep dive | Same |
| `wdai-hive` Railway deployment | `wdai-hive` README mentions Docker + Bolt framework | **Did NOT verify Railway hosting specifically — could be on any container host.** Treating as B-tier |
| The "10+ Gumloop flows" assertion | bot_id `B0896A6N147` posts many distinct message patterns in different channels (daily briefing, voicemail, recipe picker, intro routing, get-help routing, website-feedback routing, calendar update with Approve/Edit) | **The exact flow count is rough.** I counted distinct message PATTERNS, not actual Gumloop flow definitions inside Gumloop UI |
| `wdai-marketing` "GH Action posts to platform" edge in L2 | Marketing README pipeline diagram mentions Slack notification | Did I verify Marketing posts directly INTO `wdai-foundation-platform`? **No.** The arrow may be wrong. Marketing posts to its OWN Slack channel and Vercel deployment; the platform connection is via shared Luma + Mailchimp data, not direct |
| `wdai-foundation-platform` has either 12 or 14 Vercel crons | I counted entries in vercel.json (14 lines, but `sync-guests` has 3 schedule entries pointing at same path — could be 12 unique paths × 14 schedule rules) | **Real ambiguity.** Should be: 12 unique cron functions, 14 cron schedule rules. Need to disambiguate in docs |
| Marketing → Mailchimp + Marketing → LinkedIn | Marketing README mentions LinkedIn UGC API + Mailchimp publish | Didn't read `mailchimp-client.ts` / `linkedin-client.ts` source |

### Tier C — INFERRED (stated as fact in docs)

| Claim | What I inferred from | Risk if wrong |
|-------|----------------------|---------------|
| **Wit runs on Helen's Mac mini** | Pattern is on Mac mini (sub-agent confirmed Pattern's host); Wit appears alongside Pattern in cron list | Wit could be on a separate host. If Wit has its own infrastructure, the "Mac mini SPOF for cohort recap" claim is partly wrong |
| **5:30pm PT pipeline runs M-F** | Pattern mentioned "5:30pm PT cron" but didn't specify days | I added "M-F" to the cohort experience diagram. Could be daily, could be weekdays only |
| **Anthropic API keys live in three separate secret stores** (Vercel + Railway + GH Actions) | I see `ANTHROPIC_API_KEY` referenced in all three contexts | **Could be the SAME key copied into all three.** Or different keys. I asserted "three different secret stores" — true as locations. "Implies rotation requires touching all three" — possibly false if it's one key |
| **Prisma ER diagram FK relationships** (User→Membership, EventRsvp→CachedEvent, etc.) | Entity names + general convention | **All FK arrows are inferred from names, not verified against schema body.** Should be more explicitly marked. Drawn arrows could be wrong direction or non-existent |
| **AI Foundations cohort sequence — "added to cohort channel" is automatic** | I drew SlackCh-->>M "added to cohort channel" | Could be manual. Lauren may add members by hand |
| **Pre-kickoff email at T-3 days and T-1 day** | mailchimp-cc README mentions 2 pre-kickoff emails before course starts | The specific T-3 / T-1 timing is INFERRED, not verified from a config file |
| **Helen's stack reaches Linear MCP** in L3b | Helen Feb 4 "connected linear MCP to claude code" | One-time connection vs daily-used integration — unclear. Could be in Helen's #ops-website work flow rather than Syl daily briefing |
| **Helen's morning briefing Syl pulls Mailchimp + Linear MCP** | Syl Mar 5 "Repo cloned and dependencies installed" for mailchimp-cc; Helen Feb 4 connected Linear MCP | I drew Syl pulling these AT BRIEFING TIME. Could be one-time setup, not daily pull |
| **"Helen owns ~14 of 19 bots"** in bot ownership concentration | I color-coded by owner | **WDAI Marketing Content Calendar bot (`B0B1J2S4D2R`) is marketing-pillar-owned, not Helen-personal.** Should be color-coded differently. The 14 count is inflated by 1 |
| **Member-built personal apps count = 5** | Akshita's Assistant, Anennya, Maninder, Simi, Carolyn | Could be more I haven't found |
| **wdai-hive Slack bot DM check-ins are weekly** | wdai-hive README mentions "weekly DM check-ins" | Verified actually — A-tier. Moving up |

### Tier D — FABRICATED OR ASSUMED

These are claims that I made WITHOUT a source. Real gaps. Pass 3 should not trust these without verification.

| Claim | Where it appears | Honest state |
|-------|------------------|--------------|
| **Stakeholder expectations matrix** (`05-people-and-process.md`) | Pass 1 §People and process | Lauren and Rita ARE flagged as inference. **Brigitte, Sandhya, Sheena should also be flagged.** Only Helen and Madina are direct (Helen via her design doc, Madina via this conversation). The others are projections from observed behavior, not direct interviews |
| **"Wit runs on Helen's Mac mini"** + **"Mac mini is SPOF for cohort recap quality"** | L3b + AI Foundations cohort sequence + maturity grid | The SPOF framing depends on Wit being on Mac mini. If Wit is elsewhere, the framing is wrong. Need to verify Wit host. **Currently asserted as fact in Pass 1; should be marked as inference** |
| **"Three different Anthropic API keys in three secret stores"** | Security/identity credential inventory | Asserted as if confirming rotation complexity. Could be one key in three places. **Don't know which.** |
| **Prisma ER specific FK relationships** | Data architecture | Already marked "inferred" but the diagram itself draws specific arrows. Should add a more prominent caveat |
| **"Sheena learning git via mailchimp-cc PRs"** | Persona tooling map | I said Sheena "PRs to mailchimp-cc" with "learning agent/Claude stack" — but the mailchimp-cc PRs were for email redesign, possibly with Helen's help. **Whether Sheena commits independently is unclear** |
| **"Rita: UX / brand work · no formal access stack mentioned"** | Persona tooling map | I have almost no info on Rita's tooling. She has Brand work for WDAI. **Her actual tool stack is unknown** to me |
| **"Rebekah uses PostHog, GitHub for code review"** | Persona tooling map | Inferred from her Mar 23 PostHog review post. **Whether she has GitHub access at all is unverified.** I assumed she does for "consulting" |
| **The 8 person-classes in L1 System Context** ("Helen, Madina, Core Team, Volunteers, Members") | L1 | "Core Team" as a single entity flattens differential expectations. Brigitte/Lauren/Sandhya have very different tooling but appear as one node |
| **"Pattern publishes the weekly report on Mondays"** | Maturity grid + member journeys context | Pattern posts in #team-core appear roughly weekly, but I haven't confirmed Monday vs another day. The vercel.json weekly-stats is Monday 2pm UTC — that's the cron, not necessarily Pattern's publish |
| **Build TogetHER engagement loop attributes (admin dashboard, CSV export)** | Process flows | Drew based on wdai-hive README. **I read the README structurally but not the admin dashboard code.** The CSV export exists in README; the actual usage frequency is unverified |
| **"`weekly-wdai-report` is just a publish target, Pattern lives elsewhere"** | Various places | I claimed Pattern lives on Helen's Mac mini OpenClaw. I never verified WHERE Pattern actually runs. It could live in `weekly-wdai-report` repo as a script run on Helen's machine OR run on a Vercel function OR run on a GH Action. **Pattern's actual host is inferred** |
| **The "5+ services hit Anthropic API"** count | Cost overlay (operational architecture) | Counted course-update-agent, website-content-agent, wdai-marketing/copy-generator, OpenClaw Helen, OpenClaw Madina = 5. Did NOT include: wdai-hive (probably doesn't use Anthropic), wdai-admin (doesn't use Anthropic AFAIK), wdai-lumabot (no AI integration per sub-agent), mailchimp-cc (uses Anthropic SDK per package.json). Actual count = 5–6, depending on if mailchimp-cc invocations count |
| **"Granola auto-foldering is imperfect"** | wiki/infrastructure/granola.md | One source: Madina's Apr 14 "too technical for granola today, put it in my SDLC folder." **One data point. Could be a one-off or pattern.** I asserted as general truth |

---

## Specific items to correct in the Pass 1 docs

| Correction | Where | Action |
|-----------|-------|--------|
| Bot ownership count: WDAI Marketing Content Calendar bot is wdai-marketing pillar-owned, not Helen-personal | `01-system-context.md` bot ownership diagram | Recolor that node. Update "Helen owns ~14 of 19" claim |
| Wit's host should be flagged as inferred, not asserted | `01-system-context.md` L3b + bot-registry | Add "(host inferred · same Mac mini as Pattern · not directly verified)" |
| Stakeholder expectations matrix — flag all inferences, not just Lauren/Rita | `05-people-and-process.md` | Mark Brigitte/Sandhya/Sheena as inference too |
| Vercel cron count — disambiguate 12 unique functions vs 14 schedule rules | `01-system-context.md` paradigm 4b table + `02-process-flows.md` and Open Question 9 | Clarify "12 functions, 14 schedule rules" |
| Helen's two bot identities — clarify "donald" is bot_id label not a verified function | `bot-registry.md` | Mark as inferred from bot name |
| "Five member-built personal Slack apps" — change to "at least 5 confirmed" | Bot ownership + member-facing surface | Soften the claim |
| Anthropic API keys "three separate secret stores" — soften to "referenced in three secret-store contexts" | Security/credential inventory in `01` | Drop the rotation-complexity implication unless verified |
| Pattern's host — flag as inferred not stated as Mac mini fact | `01` L3b + bot-registry | Add caveat |
| `Marketing → Platform` edge in L2 | `01` L2 diagram | Verify or soften. Marketing's GH Action posts to its OWN Slack channel + LinkedIn + Mailchimp, not into the platform directly |
| Stakeholder expectations matrix should be relabeled "inferred profile" | `05-people-and-process.md` | Rename to make inference explicit |

---

## True gaps (claims I cannot defend → either fix or drop)

1. **The exact M-F vs daily-only schedule for Wit's pipeline.** Drop the "M-F" qualifier.
2. **Pattern's host.** Don't claim Mac mini; say "inferred from OpenClaw setup."
3. **Member-built personal app count.** I confirmed 5; there could be more.
4. **Stakeholder expectations for everyone except Helen and Madina.** All inferences.
5. **Whether Marketing pillar's GH Action writes into wdai-foundation-platform or only into Marketing's own surface.**
6. **Anthropic API key rotation complexity.** Whether it's 1 key in 3 places or 3 distinct keys.
7. **Whether the Atlas → Polaris pipeline's "Atlas pulls Drive when meeting references a doc" actually happens** — I drew that arrow in the enriched sequence, but it's a HYPOTHETICAL pattern I added based on what Atlas COULD do given Drive access, not what it currently does.
8. **"WDAI Newswire posts to LinkedIn"** — I drew this in the generic event journey. Verified? Maybe — the wdai-marketing pipeline mentions LinkedIn but whether NEWSWIRE specifically (vs the marketing pipeline directly) posts is unclear.

---

## What this audit means for Pass 3

- Pass 3 must NOT plan against Tier C/D claims as if they're verified.
- Open Questions #9 (cron count) is now confirmed real ambiguity, not a finding.
- The bot ownership concentration finding is REAL but the specific count is fuzzy.
- The stakeholder expectations matrix should be treated as straw-man inferences to validate via direct conversation, not as ground truth.
- Wit / Pattern hosting and Anthropic API key topology need confirmation before any federation runtime decision.

---

## What I would do if I had more time

1. Read Wit's actual config (where does it live, what does its cron say) — currently a SPOF claim that depends on inference.
2. Read Pattern's actual config — same.
3. Read `web/prisma/schema.prisma` body to confirm FK relationships in the ER diagram.
4. Confirm Anthropic API key topology — Helen would know in 30 seconds.
5. Direct conversations with Brigitte, Lauren, Sandhya, Sheena, Rita, Rebekah to ground the expectations matrix.
6. Read `wdai-marketing/.agent/decisions.log` and `gotchas.md` to answer Open Question #1 (why cron paused).
7. Recount Vercel cron config to settle the 12/14 ambiguity once and for all. → DONE — see Q9 update.

---

## Per-diagram audit (all 33 diagrams)

Walking through each diagram for: accuracy of nodes, accuracy of edges, notable omissions, and whether it serves its stated Pass-3 question.

Legend: ✅ accurate · ⚠️ omissions · ❌ likely wrong · 🟣 needs verification

### `01-system-context.md`

| # | Diagram | Audit |
|---|---------|-------|
| 1 | L1 System Context | ⚠️ **Missing externals: Vimeo, Google Meet, Google Drive, Wix.** All four are real externals members or agents touch every day. L1 should include them in the external ring. Just added Linear + Granola; should complete the set. |
| 2 | L2 Container | ⚠️ **`Marketing → Platform` edge is questionable** — flagged in pressure-test. Marketing posts to its OWN Slack channel + Vercel + Mailchimp; doesn't necessarily POST INTO platform. Should verify or downgrade to dotted. ⚠️ **Missing:** `perplex_computer` Space (Helen's oncall eval) — stalled but technically a container. Could add as dashed/grayed. |
| 3 | L3a Inside Platform | ⚠️ **Missing: Sentry** — Madina confirmed Sentry is in use; the perplex_computer space-instruction.txt lists Sentry as a credential. Should be a node in the detection layer. ⚠️ **Missing:** Stripe webhook handler as its own node (currently implied via `PortalAPI`). |
| 4 | L3b OpenClaw stacks | ⚠️ **Pattern's integrations are thin** — Pattern reaches Stripe + Supabase + GitHub per sub-agent (it's the metrics agent). Currently only shown reaching `HelenStripe` + `HelenGH`. Probably accurate now actually. ⚠️ **Wit's reach incomplete** — shows Wit → HelenCal only. Should also show Wit → Google Meet → Vimeo path (the Meet recording pipeline). |
| 5 | Business capability map (mindmap) | ✅ Looks accurate. 7 capabilities, containers mapped. |
| 6 | Security tier structure | ✅ Fixed the false-nesting bug. Now correctly shows parallel siblings + orthogonal vault. |
| 7 | Security credential inventory | ⚠️ **Missing credentials:** Linear API token (Helen has MCP), Vimeo upload token (Wit pipeline), LinkedIn UGC API token (wdai-marketing). The "9+ credentials" count understates. Real count probably 12-15. |
| 8 | Paradigm constraint grid | ✅ 2x2 placement is defensible per pressure-test Tier A/B evidence. |
| 9 | Maturity grid | 🟣 **Stripe webhook handler classified top-right (battle-tested core)** — but Helen Feb 23 noted "stripe webhooks are complex, in many ways our DB overengineered a bit on safety" + billing-cancel bugs. Closer to **top-right edge of evolving** than battle-tested. Worth re-classifying. |
| 10 | Scale pie · bots by paradigm | ✅ Totals to 34, matches bot-registry. |
| 11 | Scale pie · surfaces | 🟣 Rough proportions. The "Internal team-OS surfaces: 14" is meaningless since team-OS doesn't exist — relabel as "Internal ops surfaces." |
| 12 | Bot ownership concentration | ✅ Just fixed — pillar-owned tier added, count corrected to ~13 of 18 + 1 pillar. |
| 13 | Reference: marketing vault | ⚠️ **Missing edge:** vault → LinkedIn publish path. The wdai-marketing pipeline also auto-publishes to LinkedIn UGC; only Mailchimp shown. |
| 14 | Reference: mailchimp tiers | ✅ 3 tiers accurate per CONTRIBUTING.md verbatim. |
| 15 | Reference: admin cron | ✅ Pattern accurate per sub-agent deep-dive. |

### `02-process-flows.md`

| # | Diagram | Audit |
|---|---------|-------|
| 16 | Member surface map (new) | ⚠️ **Missing direct edges:** Members also touch Slack directly (via the invite link, then via channels), Mailchimp directly (via emails), Luma directly (via event RSVPs). Diagram shows everything routing through Portal. Reality: Portal is one of FIVE entry points. ⚠️ **Missing:** Twilio voicemail line (some members call to cancel). |
| 17 | Member signup sequence | ⚠️ Note about Newswire `postProfileIntro · after profile complete` — this happens AFTER signup, not during. The arrow placement in the diagram may suggest it fires on signup; actually it fires when the member completes their profile (a later, optional step). |
| 18 | Cohort kickoff sequence | ✅ Matches mailchimp-cc CONTRIBUTING + README. |
| 19 | Marketing copy gen sequence | ✅ Matches wdai-marketing README pipeline phases. |
| 20 | AI Foundations cohort experience | ⚠️ **Pre-kickoff T-3/T-1 day timing inferred** — flagged in pressure-test. ⚠️ **"Added to cohort channel" arrow** — may be manual not automatic. |
| 21 | course-update-agent monthly PR | ✅ Matches workflow YAML + sub-agent deep-dive. |
| 22 | Atlas → Polaris transcript pipeline | ⚠️ **The "Atlas pulls Drive" arrow** is hypothetical — based on Atlas having Drive access, not on confirmed pipeline behavior. Flagged in pressure-test. |
| 23 | Member churn flow | ✅ Matches Stripe webhook → AdminBot pattern + WixSync parallel-run finding. |
| 24 | Schema migration Expand-Contract | ✅ Verbatim from wdai-foundation-platform CLAUDE.md. |
| 25 | Helen's morning briefing | 🟣 **Linear MCP daily pull** — inferred. Could be one-time Feb 4 connection, not daily. **Mailchimp pull at briefing** — also inferred. |
| 26 | Generic event journey | ⚠️ **The "MktAction → LinkedIn" edge** — verified Marketing pipeline posts to LinkedIn (Phase 6 per README). Edge OK. |
| 27 | Build TogetHER engagement loop | ✅ Matches wdai-hive README. |
| 28 | Cross-program member lifecycle (journey) | ✅ Compositional — synthesizes other sequences. No new claims to audit. |
| 29 | Lauren's Programs ops journey | 🟣 **Lauren's specific workflow steps inferred** — based on Programs lead role + cohort coordination evidence. Lauren has not directly described her workflow to me. |

### `03-operational-architecture.md`

| # | Diagram | Audit |
|---|---------|-------|
| 30 | Deployment topology | ⚠️ **Missing: Linear hosting** (now belongs in VendorSaaS subgraph). ⚠️ **Region/replica details still unknowns** flagged in prose — accurate. |
| 31 | On-call / incident response | ⚠️ **Missing: Linear API failure path** — if Madina's central-source-of-truth proposal lands, Linear outage becomes a real concern. Currently no detection path shown. **Missing: Sentry** as a named detection node — was named in prose but not in the diagram clearly. Actually it IS in the diagram. OK. |

### `04-data-architecture.md`

| # | Diagram | Audit |
|---|---------|-------|
| 32 | Data flow / residency | ⚠️ **Missing: Linear data sink** — if Madina's proposal lands, Linear becomes another PII/work-data store. Currently absent. ⚠️ **Missing: WixSync legacy data flow** — Wix-era members still flow through Wix-side → WixSync → Supabase. The diagram skips Wix entirely. |
| 33 | Prisma ER | 🟣 Inferred FK relationships — flagged. Caveat present in prose. |

---

## Linear coverage finding

Madina explicitly asked where Linear fits. Audit reveals:

| Surface | Was Linear present? | Action taken |
|---------|---------------------|--------------|
| L1 System Context | ❌ Missing | ✅ Added as "contested" external (purple) |
| L2 Container | ❌ Missing | ✅ Added in SaaS tier with `WDA-* tickets` edge to platform |
| L3b OpenClaw stacks | Partial | ✅ Already showed Linear MCP in Helen's integrations subgraph |
| Helen's morning briefing sequence | ✅ Present | OK (flagged as inferred daily-use) |
| Security credential inventory | ❌ Missing Linear API token | ⚠️ Still missing — would need separate edit |
| Persona tooling map | ❌ Linear access column missing | ✅ Added Linear access column · 7 of 8 rows are "Unknown" |
| Deployment topology | ❌ Missing | ⚠️ Still missing — would need separate edit |
| Data flow | ❌ Missing | ⚠️ Still missing if Linear becomes data sink under Madina's proposal |
| Capability map | ❌ Linear isn't in "Org operations" leaf | ⚠️ Should add |

**Linear's real status:** today it's Helen's tech tracker with MCP-connected single-user access. Madina's May 9 proposal would expand it to **central source-of-truth for ALL team work**. Pass 3 needs to decide. The contested-external framing is now in L1/L2; full Linear coverage across all diagrams is a follow-up.

---

## Top corrections to apply (in priority order)

1. ✅ **DONE** — Linear added to L1 + L2 + persona tooling map · contested-external framing
2. ✅ **DONE** — Member surface map added to `02-process-flows.md`
3. ⚠️ **Add Vimeo + Google Meet + Drive + Wix to L1** (currently invisible externals)
4. ⚠️ **Add Sentry node visibly in L3a** (mentioned in prose but unclear in diagram)
5. ⚠️ **Fix Stripe webhook classification on maturity grid** — move closer to "evolving" edge, not pure "battle-tested core"
6. ⚠️ **Add Wit → Google Meet → Vimeo path in L3b**
7. ⚠️ **Add Linear API token + Vimeo + LinkedIn tokens to credential inventory**
8. ⚠️ **Add direct Members → Slack / Mailchimp / Luma edges in member surface map** (Portal is not the only entry point)
9. ⚠️ **Add LinkedIn publish edge in marketing vault reference pattern**
10. ⚠️ **Relabel "Internal team-OS surfaces"** in scale pie to "Internal ops surfaces" (team-OS doesn't exist)

Items 3-10 are localized edits, low risk. Could batch in one pass if desired.
