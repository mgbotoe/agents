# Deep Dive: `wdai-marketing`

**The pillar-level federation prototype, fully built.** Helen's design doc describes what `wdai-team-os` should be; this repo IS the equivalent already running for the Marketing pillar.

---

## Structure at a glance

```
wdai-marketing/
├── .agent/                    ← Agent state files
│   ├── decisions.log          (3KB — running decision log)
│   └── gotchas.md             (8.4KB — running list of things that bit us)
├── .github/workflows/
│   └── calendar-sync.yml      ← Daily 6am UTC cron (PAUSED since 2026-04-21)
├── app/                       ← Vercel serverless app
│   ├── api/
│   │   ├── approve-plan.ts    ← Phase 8 — browser approval flow
│   │   ├── save-copy.ts
│   │   ├── update-status.ts
│   │   └── slack/interactions.ts ← Slack button callbacks (legacy, no longer used)
│   ├── lib/                   ← Shared TS helpers
│   ├── __tests__/
│   ├── prototype_edit_panel.html
│   └── test-ui-local.html
├── skills/                    ← Federation contract — Claude Code skills
│   ├── content-activator/
│   ├── monthly-review/
│   ├── voice-sandhya/
│   ├── voice-setup/           ← Onboarding skill for new voices
│   ├── wdai-brand/
│   ├── wdai-design-system/
│   ├── wdai-promo-adhoc/
│   └── wdai-promo-programmatic/
├── tools/
│   ├── calendar/              ← The pipeline (28 TS files)
│   │   ├── sync.ts            ← Luma → vault sync
│   │   ├── generate.ts        ← AI copy generation
│   │   ├── publisher.ts       ← Auto-publish to Mailchimp + LinkedIn
│   │   ├── slack-notifier.ts  ← Per-event Slack webhook
│   │   ├── slack-dm.ts        ← Per-DRI DM
│   │   ├── prompt-builder.ts  ← Loads voice + brand at runtime
│   │   ├── voice-loader.ts    ← Per-DRI personal voice (Phase 5B)
│   │   ├── copy-generator.ts  ← claude-haiku-4-5-20251001
│   │   ├── linkedin-client.ts
│   │   ├── mailchimp-client.ts
│   │   ├── luma-client.ts
│   │   ├── team.yaml          ← DRI name → Slack user_id mapping
│   │   ├── promo-rules.yaml   ← Per-event-type DRI + channel timeline rules
│   │   └── overrides.yaml
│   └── daily-content-scout/   ← React app — 7 Slack passes → tagged ideas
├── vault/                     ← Context layer (the "library")
│   ├── brand-guidelines.md    ← Sandhya owns
│   ├── decision-log.md
│   ├── content-calendar.md    ← Auto-synced from Luma
│   ├── content-calendar.html  ← Static HTML viewer (deployed to Vercel)
│   ├── index.html             ← Calendar UI entry point
│   ├── linkedin-voice.md      ← WDAI LinkedIn voice + real examples
│   ├── helen-voice.md         ← Helen's Slack voice patterns
│   ├── email-templates.md     ← PENDING
│   ├── promos/<event-id>/     ← Flat-file copy storage (per event)
│   └── status/<luma_id>.yaml  ← Per-event approval status
├── meeting-minutes/
│   ├── raw/                   ← Future: Granola transcript archive
│   └── summaries/             ← Future: distilled decisions
├── archive/
├── docs/                      ← Plans, runbook, team training, ADR-style
│   ├── plans/                 ← Per-phase implementation specs
│   ├── RUNBOOK.md
│   ├── TEAM_TRAINING.md
│   ├── MANUAL_TESTS.md
│   ├── ROADMAP.md
│   ├── PROJECT_HISTORY.md
│   └── lessons_learned.md
├── public/                    ← Static assets
├── BUGS.md                    ← Top-level living bug list
├── MEMORY.md                  ← Hot context, 3KB (analogous to Polaris's memory.md)
├── NEXT.md                    ← Current next-step priorities
├── PROJECT_HISTORY.md         ← 20KB — phases completed, dates, decisions
├── PROJECT_ROADMAP.md         ← 7KB — phases planned
├── README.md                  ← 18KB — entry point for any new collaborator
├── TESTING_GUIDE.md           ← 6KB
├── TESTING_PLAN.md            ← 19KB — heavy QA discipline
├── package.json               ← @anthropic-ai/sdk, dotenv, yaml, tsx, vitest
├── tsconfig.json
└── vercel.json
```

---

## Stack

- **Language:** TypeScript (no framework — plain Node.js + Vercel serverless)
- **Runtime:** Vercel (static + serverless API), GitHub Actions (cron)
- **AI:** `@anthropic-ai/sdk` v0.90, model `claude-haiku-4-5-20251001`
- **State:** Flat YAML files in the repo (`vault/status/`, `vault/promos/`) — committed
- **Testing:** vitest, **239 tests passing**
- **External APIs:** Luma, LinkedIn UGC, Mailchimp, Slack
- **Voice:** Anthropic SDK (no openai)

---

## The federation contract (what's enforced)

### 1. Skill structure
Every skill is `skills/<name>/SKILL.md` with YAML frontmatter:
```yaml
---
name: wdai-brand
description: "Apply this skill for ALL content published under the Women Defining AI brand..."
---
```
Supporting docs live alongside (e.g., `skills/wdai-promo-programmatic/ai-foundations.md`).

### 2. Vault structure
**Context layer**: `vault/brand-guidelines.md`, `vault/linkedin-voice.md`, `vault/helen-voice.md`, `vault/decision-log.md` — never auto-modified. Hand-maintained by named owners.

**Operations layer**: `vault/content-calendar.md` + `.html` (auto-synced from Luma), `vault/promos/<event-id>/` (auto-generated copy), `vault/status/<luma_id>.yaml` (per-event approval state).

### 3. Per-DRI mapping
`tools/calendar/team.yaml` maps DRI names → Slack user IDs. Adding a person = one YAML entry.

### 4. Per-event-type rules
`tools/calendar/promo-rules.yaml` defines per-event-type DRI + channel timeline rules. Phase 3 deliverable.

### 5. Two-touchpoint approval model
- **Touchpoint 1**: Team approves the *plan* (channel mix + dates) in the calendar UI (Phase 8) — was Slack button in Phase 4, moved to browser in Phase 8.
- **Touchpoint 2**: Each DRI approves the *copy* in the calendar UI per channel.

Everything else automated.

### 6. Asset ownership matrix (from README)
| Asset | Owner | Update Trigger |
|---|---|---|
| `brand-guidelines.md` | Sandhya | Brand refresh |
| `wdai-brand` skill | Sandhya | After brand-guidelines update |
| `wdai-promo-planner` skill | Cohort ops DRI | After promo process change |
| `wdai-email-template` skill | Comms DRI | After email template change |
| `decision-log.md` | Whoever made the decision | After structural change |
| `content-calendar.md` | Content stream lead | Rolling |
| Leader voice skills | Each leader individually | Self-maintained |

---

## What's shipped (Phase status)

| Phase | Status | What it delivered |
|-------|--------|-------------------|
| 1 | ✅ | Brand-guidelines.md + initial skills |
| 2 | ✅ | LinkedIn voice + Helen voice + email template scaffolding |
| 3 (2026-04-16) | ✅ | Luma→vault sync, daily cron, content-calendar.html viewer, 74 tests, smoke test 197 events |
| 4 (2026-05-05) | ✅ | Slack webhook → `#team-marketing-content-calendar`, per-event deep-link, approval badges, **Vercel deploy** at wdai-marketing.vercel.app |
| 5 + 5B (2026-04-16→18) | ✅ | AI copy generation, voice-loader, per-DRI Slack DM with Approve/Edit, **personal voice injection** |
| 6 | ✅ | Auto-publish to Mailchimp + LinkedIn UGC API |
| 7 | ⏳ | "Leader Onboarding + Voice Profiles" — voice calibration guides, team training, per-leader LinkedIn voice |
| 8 (recent) | ✅ | "Approve Plan" button moved from Slack → browser UI (`/api/approve-plan`) |

**239 tests passing.** Heavy QA discipline.

---

## Critical operational detail: the cron is PAUSED

`.github/workflows/calendar-sync.yml`:
```yaml
on:
  # schedule:
  #   - cron: '0 6 * * *'   # Daily at 6am UTC — paused 2026-04-21
  workflow_dispatch:        # Manual trigger
```

**Daily auto-sync has been paused since April 21.** The wdai-marketing-content-calendar bot I saw posting in Slack — those messages are from *manual* runs since then. Helen or someone has been triggering `workflow_dispatch` to refresh, not the cron.

**Why does this matter for the team-OS spec?** Helen's design doc proposes a daily Friday capture for every member. The exact pattern that's been running here has a known operational issue serious enough that they paused the cron. Need to find out why before generalizing.

Pull `decisions.log` and `gotchas.md` next to find the answer.

---

## Reusable patterns (carry forward into wdai-team-os)

1. **Skill = folder with SKILL.md + supporting docs.** Frontmatter has `name` + `description`. The description tells Claude when to load it.

2. **Vault split: context (hand-curated) vs. operations (auto-generated).** No conflicts, no race conditions. Operations folders are owned by tools, not humans.

3. **Flat-file YAML state in the repo.** Everything is diff-able and reviewable in PRs. No external DB. No race conditions on rendered state.

4. **`team.yaml` + `promo-rules.yaml` as the federation glue.** Adding a person = one YAML entry. Adding an event-type rule = one YAML entry. No code change.

5. **Per-phase implementation plans in `docs/plans/`.** Each phase has its own `2026-04-16-phase-5-copy-generation.md` etc. Plan-first discipline.

6. **Phase 8's lesson: human approval in browser, not Slack buttons.** Helen tried Slack-button approval in Phase 4, deprecated it by Phase 8 in favor of the calendar UI. Slack notifications carry the *link*; approval happens in the web UI. **For team-OS this is important** — Helen's design doc heavily implies Slack-DM-with-buttons, but her own pillar prototype already learned that's worse than web UI.

7. **Voice injection at runtime, not in skills.** `voice-loader.ts` reads `vault/helen-voice.md` etc. at copy-gen time. Skills don't hard-code voices; they reference them. Means a voice update auto-propagates to all skills using it.

8. **`MEMORY.md` + `NEXT.md` + `PROJECT_HISTORY.md` + `BUGS.md` at top level.** This is the marketing-pillar equivalent of Polaris's identity/memory/wiki pattern. Same shape; different domain.

9. **`.agent/decisions.log` + `.agent/gotchas.md`.** Living agent state files. Decisions are append-only; gotchas accumulate with "Why:" and "How to apply:" sections — exactly the format Polaris uses for feedback memories.

---

## Federation gaps in wdai-marketing (worth carrying as warnings)

1. **The cron is paused.** Don't generalize a broken automation.
2. **`meeting-minutes/raw/` and `summaries/`** exist but are empty. Even this pillar hasn't solved the Granola ingestion that's central to Helen's design doc.
3. **Pending voices** for Lauren, Helen, Madina, Sheena. The "personal voice profile" concept is sound but onboarding isn't complete.
4. **No `MEMBERS.md` or roster file** at the pillar level — `team.yaml` is internal to tools, not surfaced as a top-level federation primitive.
5. **No cross-pillar references.** This repo doesn't link to `wdai-foundation-platform` or `mailchimp-cc` from its own docs. Cross-repo federation is unspecified.

---

## Patterns observed (deferred to Pass 3 for design decisions)

- The 8-skill catalog as the **distribution pattern** (skills as portable units).
- The vault/operations split as the **schema pattern**.
- The flat-file YAML state as the **persistence pattern**.
- The team.yaml + promo-rules.yaml as the **federation glue pattern**.
- The phased rollout with planned/in-flight/shipped status as the **execution discipline**.
- The two-touchpoint approval (plan, then copy) as the **HITL pattern** — but in browser, not Slack.
- The 239-test discipline as the **quality bar**.

## Gaps observed in this repo

- Cross-pillar reference architecture (how Marketing repo references Platform repo references Mailchimp repo).
- Decision log at the *team* level vs. the *pillar* level (this repo has its own, but no shared one).
- The Layer-2 consolidation/dedup primitive Helen described (this repo has no need for it — only one pillar contributing).
- Granola → repo ingest (placeholders exist; nothing built).
- Federated identity / employee-style agent provisioning at the per-member level (this repo is shared, not per-person).

---

## Open questions for next pass

1. **Why was the daily cron paused on 2026-04-21?** Check `.agent/decisions.log` and `.agent/gotchas.md`.
2. **Is the LinkedIn UGC publish actually auto-firing, or manual?** README says auto, NEXT may say otherwise.
3. **Phase 7 (Leader Onboarding)** — is this the natural model for how wdai-team-os onboards a new core team member? Worth cross-referencing with Helen's 90-min onboarding spec.
