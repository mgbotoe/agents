# Deep Dive: `mailchimp-cc`

**The shared-infra, multi-contributor reference.** Helen, Sheena, Brigitte all PR here. Smallest of the three repos, but the cleanest example of "non-engineer-friendly Claude Code project."

---

## Structure

```
mailchimp-cc/
├── .claude/
│   └── skills/
│       ├── ai-foundations-promo/  ← Marketing-side skill (cross-pillar bridge!)
│       ├── new-basics/            ← /new-basics command
│       ├── new-intermediate/      ← /new-intermediate command
│       └── new-advanced/          ← /new-advanced command
├── .github/                       ← (workflows exist but not enumerated yet)
├── __tests__/                     ← vitest test directory
├── assets/                        ← Static assets (title slides, etc.)
├── biome.json
├── CLAUDE.md                      ← 13.8KB — operational manual
├── configs/                       ← Per-cohort YAML configs
├── content/                       ← Lesson content (Markdown/HTML)
├── CONTRIBUTING.md                ← 4.9KB — explicit contributor doc
├── docs/
├── package.json
├── README.md                      ← 5.4KB
├── runbooks/                      ← Operational logs
│   ├── ai-advanced-s26.md         ← Per-cohort post-mortems
│   ├── archive/                   ← Old cohorts
│   ├── playbook.md                ← Living operational playbook
│   └── README.md
├── scripts/
├── src/                           ← TypeScript CLI source
└── tsconfig.json
```

---

## Stack

- TypeScript CLI (Node + npm)
- Biome (lint/format)
- vitest (tests)
- Mailchimp API + Luma API + Google Calendar API
- Visual testing (viewport + dark-mode rendering check via `npm run test:visual`)
- Anthropic SDK (for skill guidance, not for autonomous code generation)

---

## The four shipped skills

| Skill | Command | Owner | What it walks user through |
|-------|---------|-------|----------------------------|
| `new-basics` | `/new-basics` | Cohort ops | 15-lesson AI Basics cohort launch |
| `new-intermediate` | `/new-intermediate` | Cohort ops | 10-lesson AI Intermediate launch |
| `new-advanced` | `/new-advanced` | Cohort ops | 15-lesson AI Advanced launch |
| `ai-foundations-promo` | `/ai-foundations-promo` | Marketing pillar | Cross-pillar bridge — promo workflow for the foundations programs |

Each skill is `.claude/skills/<name>/SKILL.md`. They guide users through:
1. Gather details (start date, cohort name, live sessions)
2. Generate config YAML
3. Create Google Calendar
4. Preview emails locally
5. Iterate
6. Create campaigns in Mailchimp (drafts)
7. Schedule (recap-dependent ones stay drafts)

**This is the closest existing reference for the team-OS spec's "non-engineer onboarding skill pack."** A pillar lead types `/new-basics`, the skill walks them through a multi-step workflow with built-in safety gates.

---

## CONTRIBUTING.md tiered risk model

The most useful artifact for the team-OS onboarding spec. Three tiers of contributor risk:

| Tier | What | Risk if you break it | Recommended for |
|------|------|----------------------|-----------------|
| **Runbooks** (`runbooks/*.md`) | Operational logs, post-cohort notes, decisions | Pure docs — zero risk | **First PR for someone new** |
| **Skills** (`.claude/skills/`) | Guided workflows for slash commands | Bad edit → wrong commands run against live Mailchimp data | Second tier — needs review |
| **Source code** (`src/`) | TypeScript CLI | Breaks campaign creation, member imports, scheduling | Senior tier — engineering review |

**For the team-OS spec:** this tier model is exactly the onboarding ladder for new pillar contributors. New volunteer? Start in runbooks. Trusted contributor? Edit skills. Engineer? Touch src.

---

## CLAUDE.md (13.8KB) — operational manual

Sections (from headings):
- Running Commands
- How It Works
- Workflows
  - New Cohort Creation
  - Checking Cohort Status
  - Mid-Cohort Updates (e.g., adding recap links)
  - Finding Source Campaigns
  - Auditing Campaigns for Hardcoded Values
  - Capturing Content Locally
  - Creating a Public Calendar for Live Sessions
  - Deleting a Google Calendar
  - Previewing Emails Locally
  - Visual Testing (Viewport + Dark Mode)
  - Refreshing Lesson Thumbnails (Title Slides)
  - Adding a Single Pre-Kickoff Campaign Mid-Setup
- Safety Rules
- Config Format (three modes: local content, source-by-tag, source-by-campaign-IDs)
- W26 HTML Transforms
- Environment
- Claude Code Skills
- Local Content
- Development

**Key principles from CLAUDE.md:**
- **Built-in safety**: dry runs, confirmation prompts, marker validation. Every destructive action requires explicit `--yes`.
- **Mode 1 (preferred): local content** — content lives in this repo, no live Mailchimp read-back. Predictable.
- **Mode 2/3 fallback** — source-by-tag or source-by-campaign-ID. For when content has to come from existing campaigns.
- **W26 HTML transforms** — the rendering pipeline knows about WDAI's 2026-cohort design system, applies it consistently.

---

## Runbooks pattern (per-cohort post-mortems)

`runbooks/`:
- `playbook.md` — living operational guide
- `ai-advanced-s26.md` — specific cohort run log (S26 = Spring 2026?)
- `archive/` — old cohorts retired here
- `README.md` — runbook conventions

**Pattern:** every cohort run produces a runbook. Decisions and gotchas accumulate. New cohort = clone the most recent runbook as the starting template.

For the team-OS: this is the per-event/per-cycle artifact model. Every cohort, every program, every external event gets its own runbook in the relevant pillar repo. The team-OS aggregates summaries; the runbooks live in the pillar.

---

## Cross-pillar bridge: `ai-foundations-promo` skill

The skill name and presence is telling. This is the **Marketing pillar's promo skill living inside the Mailchimp repo** — because the promo workflow needs Mailchimp campaign access, and the skill is small enough to inline rather than require cross-repo coordination.

**Federation tension:** does cross-pillar code live in the originating pillar (Marketing) or the executing pillar (Mailchimp)? The current answer is: **wherever the operational primitives are**. The skill ships in mailchimp-cc because campaigns live in Mailchimp. The voice/brand guides it loads live in wdai-marketing.

**This is the cross-repo reference architecture in miniature.** A skill in repo A references context in repo B via documented paths. The team-OS spec needs to formalize this.

---

## Multi-contributor evidence

Memory notes Sheena PR'd here (`mailchimp-cc PR for AI Basics email redesign`, Apr 20). Brigitte PR'd here for pre/post assessment surveys (Apr 27). Helen authored most of `src/`. This repo is the **only one in the WDAI org with non-engineer authors in active PR flow**.

Why it works:
- Tiered risk model (above) lowers the barrier
- Skills do the heavy lifting; users follow the guided workflow
- `runbooks/` and `content/` are markdown — universally editable
- Visual test catches rendering breaks before they ship

---

## Test discipline

- vitest in `__tests__/`
- **Visual testing**: `npm run test:visual -- --tag ai-basics-preview` — opens previews in browser viewport, runs through dark/light mode rendering checks
- Per-cohort smoke test in skill workflow before campaign create

This is more sophisticated test discipline than I'd expect from a "non-engineer-friendly" repo. The visual-test step is the safety net that lets less-technical contributors PR without breaking subscriber-facing emails.

---

## Patterns observed (deferred to Pass 3 for design decisions)

1. **Tiered contributor risk model** — runbooks → skills → source code. This is the canonical onboarding ladder. Lift verbatim.
2. **Skill-as-guided-workflow pattern** — `/new-basics` walks user through 7 steps with safety gates. Generalize to `/new-pillar`, `/onboard-member`, `/capture-decision`.
3. **CONTRIBUTING.md explicit tiers** — every team-OS pillar repo should have one of these.
4. **Visual testing as the "non-engineer safety net"** — the team-OS dashboard layer needs an equivalent (browser-test the rendered KB before publish).
5. **Three-mode config pattern** (local-preferred, source-by-tag fallback, source-by-ID escape hatch) — applicable to anywhere data could come from multiple sources.
6. **Per-cycle runbooks in `runbooks/` with archive/** — the pattern for federation-level recurring activity logs.

---

## What's surprising / worth flagging

1. **No CONTRIBUTING.md in wdai-marketing or wdai-foundation-platform** despite both having more contributors and more complexity. mailchimp-cc is the only one with this discipline. Worth porting.
2. **`ai-foundations-promo` skill in mailchimp-cc, not wdai-marketing** — cross-pillar code placement is ad-hoc, not principled.
3. **No `.agent/decisions.log` or `gotchas.md`** here, unlike wdai-marketing. mailchimp-cc trusts the runbooks pattern for decision capture. **Two different decision-discipline patterns coexist in the org** — no shared standard.
4. **Repo is only ~5 months old in current shape** (May 5 last code update — your dark-mode fix branch is from May 5). Recent rapid evolution.
5. **W26 HTML transforms** are a design-system mechanism specific to this repo — they version the 2026-cohort visual brand. Suggests a per-year design-system iteration cadence. Worth understanding for the team-OS visual layer.

---

## Open questions

1. **Should `ai-foundations-promo` skill move to `wdai-marketing/skills/`?** Cross-pillar federation will surface this question per skill. The team-OS spec should name a rule.
2. **Does the team-OS adopt mailchimp-cc's tiered risk model wholesale?** I think yes. It's the cleanest reference.
3. **Visual-test infrastructure** — can it be generalized for the team-OS dashboard layer or is it Mailchimp-email-specific?
4. **Why no `.agent/` here but yes in wdai-marketing?** Worth aligning. If decision-discipline is in CLAUDE.md + runbooks here, fine — but then wdai-marketing's `.agent/decisions.log` becomes a redundant pattern.
