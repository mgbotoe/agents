# Deep Dive: `wdai-admin`

**The production-microservice paradigm reference.** Always-on Fastify service deployed to Railway. Hosts two sibling services (MemberBot, WixSync) in one repo, sharing config/utils, but booted as independent processes. This is the cleanest example in the WDAI portfolio of "long-running webhook-receiving service with circuit breakers, signature verification, dual-write data flow."

Confirmed live: AdminBot bot (`B08GF1SGGNL`) posts 197 msgs to `#devops-admin-mgmt` warning when Slack joiners have no matching Wix/Stripe purchase.

---

## Structure at a glance

```
wdai-admin/
├── .claude/
│   └── skills/
│       └── commit-workflow.md          ← Single skill, very thin
├── .github/
│   └── workflows/
│       ├── biome-check.yml             ← Lint gate
│       ├── build.yml                   ← TypeScript build gate
│       ├── claude.yml                  ← Claude Code automation
│       ├── run-tests.yml               ← Vitest gate
│       └── weekly-stats.yml            ← Cron Fri 17:00 UTC → POSTs /admin/weekly-stats
├── docs/
│   ├── implementation-plan.md          ← 25KB plan (Stripe migration?)
│   ├── internal-webhook-railway-implementation.md  ← 13KB
│   ├── plan-internal-webhook-replacement.md         ← 10KB
│   ├── slack-app-configuration.md      ← 4.5KB
│   └── wix-supabase-migration-plan.md  ← 19KB — the deprecation roadmap
├── scripts/                            ← (present, content not enumerated)
├── src/
│   ├── services/                       ← TWO ENTRY POINTS
│   │   ├── memberbot.ts                ← Slack + Stripe service
│   │   ├── wixsync.ts                  ← Wix webhook service (legacy)
│   │   ├── enhancedAirtable.ts
│   │   ├── enhancedSlack.ts
│   │   └── productionFeatures.ts       ← Feature-flag-gated init
│   ├── routes/
│   │   ├── healthCheck.ts
│   │   ├── slackEvents.ts
│   │   ├── slackWebhooks.ts
│   │   ├── wixWebhooks.ts              ← Legacy endpoints
│   │   ├── internalWebhook.ts          ← Replacing Wix webhooks
│   │   └── adminRoutes.ts              ← /admin/weekly-stats etc
│   ├── airtable/                       ← Legacy data store (migration period)
│   │   ├── db.ts
│   │   ├── retryableOperations.ts      ← p-retry wrapper
│   │   ├── users.ts
│   │   ├── wix.ts
│   │   └── wixIntegration.ts
│   ├── supabase/                       ← New primary store (raw `pg`, no ORM)
│   │   ├── client.ts                   ← Singleton Pool, IPv4-first DNS hack
│   │   ├── memberships.ts
│   │   ├── slack.ts
│   │   └── users.ts
│   ├── internal/
│   │   ├── types.ts
│   │   └── webhookHandlers.ts          ← Internal webhook (Wix replacement)
│   ├── middleware/logging.ts
│   ├── config/
│   │   ├── featureFlags.ts             ← ENABLE_CIRCUIT_BREAKER etc
│   │   └── index.ts
│   ├── utils/
│   │   ├── circuitBreaker.ts           ← opossum wrapper
│   │   ├── connectionPool.ts
│   │   ├── envCheck.ts                 ← checkWixsyncEnvVars / checkOptionalEnvVars
│   │   ├── errorHandler.ts
│   │   ├── gracefulShutdown.ts         ← SIGTERM/SIGINT signal handlers
│   │   ├── healthChecks.ts
│   │   ├── logger.ts                   ← Pino-based, custom signature
│   │   ├── retry.ts                    ← p-retry with API_RETRY_OPTIONS
│   │   ├── serverConfig.ts             ← Shared Fastify setup
│   │   └── wixDataTransformers.ts
│   ├── types/
│   │   ├── index.ts
│   │   ├── logger.d.ts
│   │   └── opossum.d.ts                ← Type shim for opossum
│   ├── scripts/                        ← Operational scripts (airtableChecker)
│   ├── slack.ts                        ← WebClient init, signature verification
│   ├── slackCallbacks.ts               ← handleTeamJoin / handleUserChange
│   ├── constants.ts
│   └── __test__/                       ← Vitest, integration + unit + manual scripts
├── biome.json
├── CLAUDE.md                           ← 4KB — terse architecture guide
├── README.md                           ← 12KB — public doc
├── README-MEMBERBOT.md                 ← 8KB — service-specific
├── README-WIXSYNC.md                   ← 18KB — service-specific, deep
├── AIRTABLE_INTEGRATION.md             ← 6KB — schema doc
├── .env.example                        ← 719B
├── package.json                        ← 1.3KB
└── tsconfig.json
```

No Dockerfile, no Procfile, no `railway.json`. Railway auto-detects `package.json` and runs `start` scripts.

---

## Stack

- **Runtime:** Node.js ≥20
- **Framework:** Fastify 4.24 (chose over Express because Slack Events API adapter conflicts — see README note on raw-body parsing for signature verification)
- **Language:** TypeScript 5.3, strict mode, target unspecified
- **Lint/format:** Biome 1.9.4 (matches WDAI house style)
- **Testing:** Vitest 1.0 (NOT Jest like wdai-lumabot)
- **DB:** Raw `pg` 8.13 → Supabase Postgres (primary), `airtable` 0.12 → Airtable (secondary, deprecating)
- **External APIs:** `@slack/web-api` 7.8, `stripe` 20.0, Mailchimp via direct HTTP, Wix webhooks inbound only
- **Resilience:** `opossum` 9.0 (circuit breakers, feature-flagged), `p-retry` 4.6
- **Deploy:** **Railway** (confirmed: `wdai-admin-memberbot-production.up.railway.app`, `RAILWAY_ENVIRONMENT` env var, README mentions "Railway deployments with Datadog")
- **Observability:** Datadog-direct metrics (`METRICS_PROVIDER=datadog-direct`), Pino logger, custom metrics (`wdai_admin.slack_events_processed_total`, `wdai_admin.circuit_breaker_state`)

---

## Two-services-one-repo pattern

This is the load-bearing architectural choice. Both services live in `src/`, share `utils/`, `config/`, `supabase/`, `airtable/`, but have **separate `services/*.ts` entry points** booted as independent Node processes:

```jsonc
// package.json scripts
"start:memberbot":  "node dist/services/memberbot.js",
"start:wixsync":    "node dist/services/wixsync.js",
"dev:memberbot":    "tsx watch src/services/memberbot.ts",
"dev:wixsync":      "tsx watch src/services/wixsync.ts"
```

**Why one repo, two services:**
- Shared models (Slack member ↔ Wix purchase linking happens both directions)
- Shared utils (logger, circuit breaker, retry, gracefulShutdown)
- Shared Airtable client (both write to `Slack_Members`, `Wix_Purchases`, `Wix_Cancellations`)
- Shared types

**Why not one combined service:**
- Independent scaling (webhook bursts on either side don't affect the other)
- Independent failure domains (a bad deploy of WixSync doesn't kill MemberBot's Slack listener)
- Different production characteristics (MemberBot does event-loop, WixSync does occasional bursts)

**Contrast with `wdai-lumabot`:** Lumabot is one service per repo, uses Jest (not Vitest), uses `node-cron` for scheduling, uses `@slack/bolt` (not raw `web-api`). Suggests Lumabot was scaffolded by a different person at a different time.

---

## How AdminBot posts to Slack

Confirmed mechanism (from README-MEMBERBOT + slack.ts head):
- Uses `@slack/web-api` `WebClient`, NOT `@slack/bolt`, NOT Socket Mode, NOT incoming webhooks
- Bot token (`SLACK_BOT_TOKEN`, `xoxb-...`) + signing secret pair
- Receives events on HTTPS endpoint `POST /slack/events` (Slack Events API → Railway public URL)
- Manually verifies signatures via `verifySlackRequest` against raw body (Fastify-specific raw body parser, README has multi-paragraph note about this)
- Posts admin notifications to `SLACK_ADMIN_CHANNEL_ID` (env-configured, the 197-message channel = `#devops-admin-mgmt`)
- Slack auth tested at startup with `client.auth.test()` wrapped in `withRetry(API_RETRY_OPTIONS)`

Two channel IDs in env: `SLACK_ADMIN_CHANNEL_ID` (alerts) and `SLACK_LEADERS_CHANNEL_ID` (community-leader notifications).

---

## Service auth & credentials

All via env vars, loaded at process start with `dotenv.config()`. No Vault, no secret manager. Railway env injection is the source of truth in production.

| Secret | Used by |
|---|---|
| `SLACK_BOT_TOKEN` / `SLACK_SIGNING_SECRET` | MemberBot |
| `STRIPE_API_KEY` / `STRIPE_WEBHOOK_SECRET` | MemberBot |
| `AIRTABLE_ACCESS_TOKEN` / `AIRTABLE_BASE_ID` | Both |
| `MAILCHIMP_API_KEY` / `MAILCHIMP_SERVER_PREFIX` / `MAILCHIMP_LIST_ID` | Both |
| `DATABASE_URL` (Supabase pooled or direct) | MemberBot |
| `LUMA_API_KEY` | (present, usage unclear from headers) |
| `ADMIN_API_SECRET` | GitHub Actions weekly-stats workflow → `x-admin-secret` header on `/admin/weekly-stats` |

Internal auth-checked routes use the `x-admin-secret` header pattern (`weekly-stats.yml` workflow demonstrates).

---

## Always-on vs. cron

This service is **always-on** (Railway long-running process). But there's a **cron-via-GitHub-Actions** layer on top:

- `weekly-stats.yml` runs Friday 17:00 UTC → `curl POST` to `${MEMBERBOT_URL}/admin/weekly-stats` with the `ADMIN_API_SECRET` header.
- Same pattern Atlas/Polaris use (`promote.yml`, `discuss.yml`): GitHub Actions cron triggers HTTP endpoint on a separate always-on service. **Reusable cross-paradigm pattern.**

Mostly the service responds to:
- Slack events (`team_join`, `user_change`) — incoming webhook
- Stripe events (`subscription.*`) — incoming webhook
- Wix events (purchase, cancellation) — incoming webhook (deprecating)
- Internal events (the "internal webhook" replacing Wix) — incoming webhook
- GitHub Actions admin pokes — cron-style

---

## WixSync deprecation status

Wix is being phased out for Stripe. Three docs in `docs/` track the migration:
- `wix-supabase-migration-plan.md` (19KB, longest) — the canonical roadmap
- `plan-internal-webhook-replacement.md` (10KB) — replacing Wix webhooks with an "internal webhook" pattern
- `internal-webhook-railway-implementation.md` (13KB) — implementation details

Code state:
- `src/routes/wixWebhooks.ts` — **still live** (production URL: `https://wdai-admin-memberbot-production.up.railway.app/wix-webhook/purchase`)
- `src/routes/internalWebhook.ts` — replacement endpoint, already in source
- Stripe webhooks (`/stripe-webhook` via `routes/slackWebhooks.ts` registration) — new path

So WixSync is in **parallel-run** state: old Wix webhooks still feed Airtable, new Stripe webhooks feed both Airtable and Supabase. The dual-write pattern in CLAUDE.md makes the migration reversible.

CLAUDE.md is explicit: "Wix: `/wix-webhook/*` - legacy, deprecated."

---

## Circuit breakers & production hardening

Probably the most novel thing in this repo for the team-OS spec. **All feature-flagged off by default** (`ENABLE_CIRCUIT_BREAKER=false` etc.) — production opts in via Railway env.

`src/utils/circuitBreaker.ts` defaults:
```ts
timeout: 3000,                    // 3s per call
errorThresholdPercentage: 50,     // open at 50% error rate
resetTimeout: 30000,              // half-open retry after 30s
rollingCountTimeout: 10000,       // 10s rolling window
rollingCountBuckets: 10,          // 1s/bucket
```

Wraps every external call (Slack API, Airtable, Mailchimp, Stripe). Datadog metric `wdai_admin.circuit_breaker_state{name}` exports state.

`gracefulShutdown.ts` registers SIGTERM/SIGINT handlers, drains circuit breakers (5s timeout), closes Fastify server, ends pg pool. Railway sends SIGTERM on deploy → clean shutdown → no in-flight request loss.

**Other production-hardening utilities:**
- `withRetry()` from `p-retry` with shared `API_RETRY_OPTIONS`
- `connectionPool.ts` (also feature-flagged)
- `enhancedLogging` (feature-flagged structured logging)
- `healthChecks.ts` registered at `/health`
- IPv4-first DNS (`dns.setDefaultResultOrder('ipv4first')`) — **Railway-specific hack** because Railway's IPv6 doesn't work cleanly with Supabase pooler

---

## Database strategy (the "limited role" pattern)

Explicit ADR in CLAUDE.md: raw `pg`, not Prisma. Reasoning:
- wdai-client (main app) owns the Supabase schema and uses Prisma
- wdai-admin has a **limited read/write Postgres role**: writes to `slack` table only; reads `users`, `memberships`
- Raw SQL avoids Prisma's expectation of owning migrations
- Connection pool singleton in `src/supabase/client.ts`

**Dual-write pattern** during migration:
```
Slack Events → Supabase (PRIMARY, raw pg) + Airtable (SECONDARY, legacy)
Stripe Webhooks → Airtable + Mailchimp
```

If Airtable write fails: log it, don't fail the request. Supabase write is the only blocking one.

| Data | Owner | wdai-admin role |
|---|---|---|
| `users`, `memberships` | wdai-client | READ ONLY |
| `slack` | wdai-admin | READ/WRITE |
| Airtable | Legacy | WRITE (migration period) |

---

## What's surprising

1. **No Dockerfile, no Procfile, no `railway.json`.** Railway auto-detects via package.json. Less config but also less reproducible — you can't tell from the repo alone how it deploys. Compare to foundation-platform where workflows declare everything.
2. **`@slack/web-api` not `@slack/bolt`.** Manual signature verification with custom Fastify raw-body parser. README has a 20-line apology note about why. Lumabot uses Bolt; this one rolled its own. Likely choice made because Fastify ≠ Express and Bolt assumed Express.
3. **Three migration plan docs totaling 42KB.** Heavy doc-driven migration, not just code. Polaris-style planning artifacts living in the repo.
4. **`tests do not get changed to fix failing tests`** rule (verbatim in CLAUDE.md). Strong enforcement: "Tests updates are only a last resort if they have fail to represent real world scenarios." This is the inverse of the typical AI failure mode (modifying tests to make them pass).
5. **Logger signature deliberately inverted from Pino default.** `logger.info(message, context)` not `logger.info(context, message)`. CLAUDE.md flags this with WRONG/CORRECT examples. Easy footgun.
6. **Manual test scripts (`test-slack-endpoint.js`) checked into `__test__/`** alongside Vitest tests. Three-tier testing: unit (Vitest), integration (Vitest with mocks), manual scripts (run against a live dev server). The manual scripts are how they validate Slack signature verification end-to-end.
7. **No `Wix → Stripe` cutover date.** The migration is open-ended, dual-write keeps both alive. No "rip-out Wix on date X" — just incremental.
8. **`.claude/skills/` has exactly one skill: `commit-workflow.md` (3KB).** Minimal Claude Code investment compared to foundation-platform's 7 skills. This repo gets less AI-author traffic.

---

## Patterns observed (deferred to Pass 3 for design decisions)

This is the canonical reference for paradigm 2 (production microservice) in WDAI today. Patterns present:

1. **Two-services-one-repo with separate entry-points** — when services share models/utils but need independent scaling and deploy.
2. **Always-on Fastify on Railway + GitHub Actions cron for periodic POSTs** — the cron layer is HTTP, not a node-cron in-process scheduler. Decouples scheduling from runtime.
3. **Feature-flag-gated production hardening** (`ENABLE_CIRCUIT_BREAKER`, `ENABLE_CONNECTION_POOL`, `ENABLE_ENHANCED_LOGGING`). Default-off, opt-in per env. Lets local dev stay simple.
4. **Circuit breaker per external dependency** (opossum), with Datadog metric export on state changes.
5. **Graceful shutdown registry** — `gracefulShutdown.register({name, handler, timeout})` for SIGTERM-clean release of pg pool, circuit breakers, HTTP server.
6. **`x-admin-secret` header pattern for internal-trigger endpoints** — GitHub Actions cron → `curl` with shared secret → service-side route. Same pattern as Atlas's promote/discuss.
7. **Limited-role DB pattern** — service writes only its own tables, reads others. Forces explicit cross-service contracts. Cuts Prisma out when you don't own schema.
8. **Dual-write migration pattern** — both old and new stores receive writes during cutover, secondary failures non-fatal. Reversible if new store has issues.
9. **Raw-body parser + manual signature verification** for any inbound webhook (Slack, Stripe, Wix all do this). Don't trust framework adapters for crypto.
10. **Custom logger signature pinned in CLAUDE.md** with WRONG/CORRECT examples — protects against AI authors reverting to Pino default.
11. **Manual test scripts checked in next to automated tests** — for verification that needs a live target (signature verification, real Slack event simulation).

---

## Gaps observed in this repo

- **No staging environment** visible in repo. Production-or-bust. Railway has preview environments but no docs mentioning them.
- **No DB migration story for the admin service.** Schema changes happen in wdai-client; admin discovers them at runtime. Fragile — needs at least a schema-contract check.
- **No secret rotation runbook.** Env vars are set in Railway dashboard; no doc says how to rotate Slack tokens / Stripe keys.
- **No deploy-rollback doc.** Railway has rollback button but it's not in README. Worth codifying.
- **Datadog dashboard template is a stub** (`docs/datadog-setup.md` referenced but I didn't enumerate it). Metrics exist; visualization story is half-built.
- **Skill set is thin.** One skill (`commit-workflow`). Foundation-platform has 7. Suggests Builder/QA-style delegation skills haven't been wired here.

---

## Open questions for next pass

1. Does Railway have a preview/staging environment for this service, or is every push to main a prod deploy?
2. The `internal/webhook` route — is it already wired to a sender, or staged for cutover? Read `internal-webhook-railway-implementation.md` if it matters.
3. `LUMA_API_KEY` in env but no obvious Luma client in `src/`. Dead env var or used by `wixsync` for community-event linking?
4. `MEMBERBOT_URL` GitHub Actions secret — does it point to Railway prod, or a staging slot?
5. How is `ADMIN_API_SECRET` rotated? Manual env var swap in both Railway and GitHub secrets?
6. The 197 alerts in `#devops-admin-mgmt` — are these actioned by a human, or is there silent decay? (If decay, the team-OS spec should add an alert-aging policy.)
7. Why Vitest here but Jest in lumabot? Was this a deliberate migration, or just inconsistent scaffolding?
