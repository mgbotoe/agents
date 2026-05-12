# Deep Dive: `wdai-lumabot`

**The production microservice reference (paradigm 2).** Internal Slack bot integrating Luma + Airtable, deployed on Railway, running scheduled jobs and slash-command handlers. Smallest service in the WDAI fleet by surface area but the one that runs 24/7 and has the longest refactor history. The canonical "single-purpose Node service, no UI tier" template.

## Structure at a glance

```
wdai-lumabot/
├── .cursor/                     ← Cursor IDE config (no .claude/ directory)
├── .env.example                 ← 1.5KB — all required secrets enumerated
├── .github/
│   └── workflows/
│       └── lint-format.yml      ← Single workflow: Biome check on PR
├── .gitignore
├── biome.json                   ← Lint/format config
├── docs/                        ← 6 design/refactor markdowns, no auto-generated docs
│   ├── api_efficiency_refactor_plan.md   (8.0KB)
│   ├── lumabotprd.md                     (3.7KB — original PRD)
│   ├── lumabottechspec.md                (2.0KB)
│   ├── lumabot_plan.md                   (10.9KB — phased plan)
│   ├── lumabot_refactor.md               (5.9KB — refactor postmortem)
│   └── Luma_ListEvents.md                (4.9KB — Luma API notes)
├── package.json                 ← 11 deps total. Tiny dependency surface.
├── package-lock.json
├── railway.json                 ← Deploy spec (Nixpacks + restart policy)
├── README.md                    ← 8.4KB — single source of operational truth
├── src/                         ← All code; 19 TS files, flat-ish topology
│   ├── airtable/
│   │   ├── client.ts
│   │   └── members.ts            ← Active-member lookup (the source of truth for approval)
│   ├── cache/
│   │   └── index.ts              ← In-memory TTL cache (single file)
│   ├── config/
│   │   ├── index.ts
│   │   └── types.ts
│   ├── luma/
│   │   ├── client.ts             ← LumaClient with retry + rate limit
│   │   └── types.ts
│   ├── scheduler/
│   │   ├── approveGuests.ts      ← node-cron, every 12h, 6-month window
│   │   └── fridayDigest.ts       ← node-cron, Fri 16:00 UTC = 9 AM LA
│   ├── slack/
│   │   ├── app.ts                ← Bolt app entrypoint (= dist/slack/app.js)
│   │   ├── commands.ts           ← /luma-create-event slash handler
│   │   ├── actions.ts            ← Button/modal interaction handlers
│   │   ├── home.ts               ← App Home dashboard renderer
│   │   └── users.ts              ← Slack user info lookups
│   ├── utils/
│   │   ├── async.ts              ← Concurrency helpers (p-limit wrappers)
│   │   └── date.ts
│   ├── auth.ts                   ← Authorization checks (who can create events)
│   ├── constants.ts              ← THE TUNABLE FILE — only thing non-devs edit
│   └── errors.ts                 ← notifyError / notifySuccess to DevOps channel
└── tsconfig.json
```

No `CLAUDE.md`. No `.claude/skills/`. No `tests/` directory (Jest is installed but no test files). The repo is single-author-AI-friendly but has no autonomous-agent scaffolding — it's classic backend code maintained the human way.

## Stack

- **Runtime:** Node.js + TypeScript 5.8
- **Slack:** `@slack/bolt` v4 (Socket Mode bot)
- **HTTP:** `axios`
- **Concurrency:** `p-limit` (pinned to v3.1, CommonJS — see history below)
- **Scheduling:** `node-cron` (in-process, single replica)
- **External APIs:** Luma, Airtable (member registry), Slack
- **Build:** raw `tsc` → `dist/`
- **Linter:** Biome
- **Tests:** Jest installed, **zero test files committed**
- **Deploy:** Railway with Nixpacks builder
- **CI:** Biome check on PR (no test job, no type-check job)

## Railway deploy spec

```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": { "builder": "NIXPACKS", "buildCommand": "npm run build" },
  "deploy": {
    "startCommand": "npm start",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

Two things to note:

1. **Single long-running process.** No worker/web split, no queue. The Bolt app holds the WebSocket + the cron timers in the same process.
2. **Restart-on-failure with 10 retries** is the entire reliability strategy. No health check spec, no replica count. Railway's defaults do the rest.

## The `constants.ts` pattern — the non-developer config surface

This is the deliberate design choice that defines the repo. One file, four exported objects, all `as const`:

| Group | What it controls | Sample value |
|-------|------------------|--------------|
| `TIME_CONSTANTS` | Cache TTLs + cron schedules + look-ahead windows | `GUEST_APPROVAL_INTERVAL: "0 */12 * * *"` |
| `RATE_LIMIT` | Per-endpoint concurrency caps for `p-limit` | `LUMA_CONCURRENT_REQUESTS: 3` |
| `PAGINATION` | Page sizes + max-pages safety stops | `LUMA_GUEST_PAGE_LIMIT: 100` |
| `UI_CONSTANTS` | App Home limits, modal field max-lengths | `APP_HOME_MAX_EVENTS: 20` |

Also exports `ERROR_MESSAGES` and `SUCCESS_MESSAGES` so user-facing copy lives outside business logic.

README explicitly tells non-developers: "Tune these to change behavior. Lower `*_CONCURRENT_REQUESTS` if you hit rate limits." That's the contract — config-as-code, but the config file is a flat data table.

This is the **strongest pattern in the repo for the team-OS spec.** It's the "your service should have one tunable surface" rule made concrete.

## Scheduled jobs

Two cron jobs run in-process via `node-cron`. Both write status to a `DEV_OPS_CHANNEL_ID` Slack channel.

### `approveGuests.ts` — every 12 hours
1. Fetch future Luma events (6-month window).
2. Use Luma's server-side filter to list pending guests per event.
3. Cross-reference against cached Airtable active-member emails (5-min TTL).
4. Approve matching guests. Skip non-members (manual review).
5. `notifySuccess` with stats; `notifyError` with stack trace on failure.

Uses **two separate `p-limit` limiters** — one for event processing, one for guest approvals — because the August 2025 deadlock was caused by sharing a single limiter (parent and child tasks competing for the same slot).

### `fridayDigest.ts` — Fri 9 AM LA (16:00 UTC)
Posts a formatted interactive summary of the next 7 days of events to a designated Slack channel. Uses pagination with a safety cap (`WEEKLY_DIGEST_MAX_PAGES: 10`).

## Slack surface

| Feature | File | Trigger |
|---------|------|---------|
| `/luma-create-event` | `slack/commands.ts` | Slash command opens modal |
| Modal submit / button actions | `slack/actions.ts` | View submission events |
| App Home dashboard | `slack/home.ts` | `app_home_opened` event |
| Bolt app boot + listener registration | `slack/app.ts` | Process start |

Authorization is centralized in `auth.ts` (gated by Slack group membership, cached for 10 min).

## Observability

Three primitives, no APM:

1. **`notifyError(error, context)`** — formats a Slack message with stack trace, posts to DevOps channel.
2. **`notifySuccess(stats)`** — posts approval task stats (events processed, guests approved, skipped, duration).
3. **Console logs** — Railway captures stdout/stderr.

No Sentry, no metrics, no distributed tracing. Slack IS the observability layer. The README even names the symptom-to-diagnosis mapping: "no Slack notifications" → check `DEV_OPS_CHANNEL_ID` env var; "task hanging" → look for the "All events scheduled" log line.

## Caching

In-memory only, in `cache/index.ts`. TTLs from `TIME_CONSTANTS`:

| Cache | TTL | Why |
|-------|-----|-----|
| `USER_PERMISSIONS` | 10 min | Auth checks must be fast on every Slack interaction |
| `GROUP_MEMBERSHIPS` | 30 min | Slack group lookups are slow |
| `USER_INFO` | 15 min | Display names for digest formatting |
| `APP_HOME_EVENTS` | 5 min | App Home re-renders frequently |
| `MEMBER_EMAILS` | 30 min | Airtable. Bumped from 5 → 30 in August 2025 to avoid stale-data flapping |

Cache is process-local. Restart = cache wipe. Acceptable because Railway only runs one replica.

## Refactor history (the most-valuable section of the README)

The README maintains a running log of structural changes. Worth reading verbatim for the team-OS spec — this is the "what production teaches you" curriculum:

1. **Parallelization** — sequential cohost adds replaced by `Promise.all` + `p-limit`.
2. **API discovery** — initial assumption that Luma supported batch guest approval was wrong; refactored to per-guest loop after error analysis.
3. **Dependency management** — `p-limit` v7 broke prod with `ERR_REQUIRE_ESM` because the build was CommonJS. Downgraded to v3.1. **Pinned in package.json forever.**
4. **Deadlock prevention** (Aug 2025) — shared concurrency limiter caused parent/child task starvation. Split into two limiters.
5. **Extended event window** (Aug 2025) — 3 → 6 months because events were being scheduled further in advance and getting missed.
6. **Enhanced observability** (Aug 2025) — added the `notifySuccess` stats payload + `DEV_OPS_CHANNEL_ID` enforcement.

All six items would have been invisible without production traffic. None of them are findable in a unit test.

## Patterns observed (deferred to Pass 3 for design decisions)

1. **`constants.ts` as the single tunable surface.** Every paradigm-2 service in the team-OS gets one of these. Non-developers can edit it without touching business logic; PRs that change behavior change `constants.ts` first.
2. **README-as-runbook.** No separate ops doc. Symptoms → diagnosis → fix mapping lives in the README. Every paradigm-2 service should have a "Debugging & Monitoring" section in its README.
3. **Refactor history kept in-repo, in the README.** Six bullets, durable across context windows. This is the cheapest possible ADR substitute and it works.
4. **`notifyError` / `notifySuccess` to a single DevOps channel as the observability MVP.** No APM until you need one. The team-OS spec should formalize this as the baseline: every service ships with a DevOps channel ID and posts task status.
5. **Two-limiter rule for nested concurrent work.** A specific anti-pattern (single shared `p-limit`) was named and codified. Worth lifting into a shared utilities doc.
6. **Railway + Nixpacks + restart-on-failure** as the deploy template for stateful Slack bots. Vercel handles the platform repo's HTTP surface; Railway is the right home for things with WebSocket lifetimes or in-process cron.

## What's surprising

1. **No tests committed despite Jest being installed.** This is the inverse of `wdai-marketing` (239 tests) and `mailchimp-cc` (vitest discipline). The repo relies entirely on production traffic for QA. Survivable here because the bot is internal-only and failures are observable in Slack, but it sets a different bar than the rest of the WDAI fleet.
2. **No `CLAUDE.md` and no `.claude/` directory.** Every other repo in the WDAI org has these. Lumabot was authored before the Claude-native pattern propagated, and nobody backfilled it. Means: if you delegate work here, you have no project memory to lean on.
3. **`.cursor/` directory** instead of `.claude/`. Indicates the original author used Cursor. The repo predates the team's standardization on Claude Code.
4. **CI is Biome-only.** No type-check job, no test job. The TypeScript build runs at deploy time on Railway, so a type error ships and crashes the restart loop — discovered via the 10-retry restart policy and the DevOps channel.
5. **Airtable is the source of truth for active members**, despite the platform repo planning to migrate off Airtable. This is the cross-repo coupling that the team-OS spec needs to surface: when (if?) the platform migrates membership to Postgres, lumabot has to swap its data source. Today: silent dependency.
6. **`docs/` contains design artifacts** (PRD, tech spec, refactor plans, Luma API exploration) but is **not** a runbook directory. It's the project-history archive. `wdai-marketing` has `.agent/decisions.log`, `mailchimp-cc` has `runbooks/`, lumabot has `docs/` — three different conventions for the same need.
7. **Cache wipes on every deploy** are acceptable because there's only one replica. The day this service needs horizontal scale, the cache layer becomes a Redis-shaped problem.

## Open questions for the team-OS spec

1. **Does paradigm-2 require tests, or is "production traffic + Slack alerts" an acceptable QA model for low-stakes internal services?** Lumabot's track record says yes; the rest of WDAI says no. The spec needs a stance.
2. **Should every paradigm-2 service get a `CLAUDE.md` backfilled?** If yes, who owns the work, and is it the same template as platform/marketing or a leaner "service-shaped" template?
3. **Where does the refactor-history log live in the spec template?** README section, `docs/CHANGELOG.md`, `.agent/decisions.log`, or `docs/adr/`? Pick one — three conventions across three repos is the federation tax.
4. **Airtable → Postgres member migration**: when platform migrates, who updates lumabot? Is there a contract test or just a "ping the bot owner" Slack message? The team-OS spec needs a cross-repo dependency manifest.
5. **`constants.ts` editability for non-engineers** — this is asserted in the README but there's no PR review gate enforcing "only constants.ts changed = auto-approve." Worth formalizing: a `constants-only` PR label that triggers a different reviewer pool.
6. **Single-replica assumption** is currently silent. Should the spec require services to declare their replica-count assumption explicitly so future scaling work knows what to break?
