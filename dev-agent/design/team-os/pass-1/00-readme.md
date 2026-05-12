# Pass 1 — WDAI Operational System Context

**Pass 1 documents WDAI's current operational state.** It is the audit-grounded evidence base that frames Pass 2 (coordination surface) and Pass 3 (federation design).

**Important: "team-OS" refers to a proposed future federation that Pass 3 will design. It does not exist today.** Where this document set says "Pass 3 must X" or "any federation design must Y," it means "X / Y is a constraint surfaced by current state" — not an existing obligation.

---

## Reading order

| # | File | When to read |
|---|------|--------------|
| 0 | **`00-readme.md`** (this file) | First. Five-minute index. |
| 1 | **`01-system-context.md`** | Always. Framing, the 7 Pass-3 design questions, C4 system overview, cross-cutting structural views, findings, open questions, audit gaps. |
| 2 | `02-process-flows.md` | When you need to see HOW the system runs — member journeys, ops journeys, agent flows. |
| 3 | `03-operational-architecture.md` | When you need deployment topology, SLA tiers, on-call routing, or external integration risk. |
| 4 | `04-data-architecture.md` | When you need data flow / residency or the Prisma ER model. |
| 5 | `05-people-and-process.md` | When you need per-person current tool stack or stakeholder expectations. |

If you only have time for one file, read `01-system-context.md`.

---

## The seven Pass-3 design questions (lifted from `01`)

Every observation in this Pass 1 set connects to one of these. Pass 3 must produce answers; Pass 1 produces evidence.

| # | Question | One-line framing |
|---|----------|------------------|
| **Q1** | Where does the team-OS live? | Helen's doc says Cowork; reality has paradigm 2 retreating into paradigm 4; Madina's direction is GitHub Actions. |
| **Q2** | How do agents propose, humans approve? | `course-update-agent`, `website-content-agent`, marketing `/approve-plan` already ship the pattern. |
| **Q3** | How do we observe what's running? | Platform's `AuditLog` + `daily-digest` is the existing self-monitoring primitive. |
| **Q4** | How do we onboard non-engineers? | Sheena is zero-state today; `mailchimp-cc`'s tiered runbooks → skills → source code is the working reference. |
| **Q5** | How do we coordinate cross-repo migrations? | Airtable → Supabase will break Lumabot's guest approval unless coordinated; silent cross-repo dependency. |
| **Q6** | How do we ingest per-user Granola → shared wiki? | Each Granola account is private; multi-attendee meetings produce duplicate transcripts needing dedup. |
| **Q7** | How does identity/auth federate? | CODEOWNERS only in platform; three Slack tokens; Gumloop is single-user-many-flows internally anonymous. |

---

## Companion deep-dive docs (one level up, in `design/team-os/`)

| File | What it carries |
|------|-----------------|
| `deep-dive-wdai-foundation-platform.md` | Main product + 14 Vercel crons + 3 platform Slack apps + 2 monthly autonomous PR agents |
| `deep-dive-wdai-marketing.md` | Pillar federation prototype (vault/skills/promos) |
| `deep-dive-wdai-admin.md` | Paradigm 2 reference, in retreat as platform absorbs |
| `deep-dive-wdai-lumabot.md` | Paradigm 2 always-on Slack Bolt service |
| `deep-dive-mailchimp-cc.md` | Multi-contributor shared infra + tiered risk model |
| `deep-dive-member-surface.md` | ~30 member touch points |
| `platform-hosted-bots.md` | The 3 Slack apps that live inside the platform repo |
| `cowork-automations.md` | Zero Cowork-scheduled automations in production WDAI |
| `bot-registry.md` | 34 bots, 6 execution paradigms |
| `repo-scan.md` | All 15 repos in the WDAI GitHub org |

---

## What Pass 1 deliberately is NOT

- Recommendations or proposals
- A coordination-surface map (Pass 2's job)
- An exhaustive bot or member-surface inventory (companion deep-dives)
- An assumption that team-OS already exists or has obligations

If you find a "team-OS should X" statement anywhere in these files, that's a bug — flag it.

---

## Self-pressure-test (read before trusting any claim in Pass 1)

**`_pressure-test.md`** is a candid audit of every major claim in Pass 1 against the source data. It categorizes claims into A (verified) / B (sourced, not deep-verified) / C (inferred) / D (fabricated or assumed) tiers and surfaces:

- Where the Pass 1 docs assert things I cannot directly confirm
- Specific corrections applied (bot ownership count · Wit host caveat · Vercel cron count clarification · stakeholder matrix flagged as inference · others)
- True gaps that Pass 3 must NOT plan against as if verified

**Read `_pressure-test.md` before treating any specific finding in Pass 1 as ground truth.** Six of eight stakeholder expectation rows are inference. Wit's host is inferred. Several Anthropic API key claims are unconfirmed. The Prisma ER FK relationships are inferred from entity names, not schema body.

---

## What Pass 2 and Pass 3 will do

- **Pass 2 — coordination surface (current state, descriptive):** Slack channel typology, Drive tier split, Linear usage, Granola pipeline mechanics, alert channels, decision-log surface.
- **Pass 3 — federation design (prescriptive):** answers to the seven design questions, runtime choice, onboarding plan, observability hookups, identity federation contract, migration coordination plan.

Recommendations belong in Pass 3, never Pass 1 or Pass 2.
