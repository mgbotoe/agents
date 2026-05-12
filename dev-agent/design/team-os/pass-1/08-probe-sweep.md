# Pass 1 · Probe sweep (2026-05-12) — live-system verification

> **Status:** Sweep 2026-05-12 · Confidence: **highest in Pass 1** — every claim has a primary source (file path, URL response, or workflow line). Caught 6 errors Pass 1 v5 had asserted with confidence. Treat as the ground-truth tier for tech-stack claims.

**What this file is:** results of probing the actual running WDAI tech stack against Pass 1's documentary claims. Probes were: DNS · HTTP HEAD on URLs · grep across repos · `vercel.json` reads · `.env.example` reads · GH Actions workflow inspection · git log recency.

**Discipline:** every claim below has a primary source. Where probes contradicted Pass 1's documentary claims, Pass 1 is wrong unless it can show fresher evidence.

---

## Hosting + DNS (Wave 1)

| URL | Probe | Result |
|-----|-------|--------|
| `https://www.womendefiningai.org` | `curl -I` | `Server: Vercel` · `X-Powered-By: Next.js` · `X-Clerk-Auth-*` headers · 200 OK |
| `https://www.womendefiningai.com` | `curl -I` | `Server: cloudflare` · 301 → `.org` |
| `https://womendefiningai.com` | `curl -I` | `Server: cloudflare` · 301 → `.org` |
| `https://weekly-wdai-report.vercel.app` | `curl -I` | 200 OK · cached 1d (Pattern's report — live) |
| `https://built-by-wdai.lovable.app` | `curl -I` | 200 OK · Cloudflare-fronted Lovable hosting |
| `https://curriculum.helenleekupp.com` | `curl -I` | 200 OK · cached 2hr (Helen actively iterating AI Intermediate) |

**Wix:** dead. Both `.com` and `.org` go through Vercel/Cloudflare. No Wix in any response header.

---

## Repo activity (Wave 2)

`git log --since='30 days ago'` per repo:

| Repo | Last commit | State |
|------|-------------|-------|
| `wdai-foundation-platform` | 2026-05-10 (Madina, intro-matcher) | **ACTIVE** |
| `wdai-marketing` | 2026-05-05 (Sandhya, Phase 8 approve-plan) | **ACTIVE** |
| `mailchimp-cc` | 2026-05-05 (Madina + Helen, dark-mode fix) | **ACTIVE** |
| `wdai-admin` | **>30 days ago** | **DORMANT** |
| `wdai-lumabot` | **>30 days ago** | **DORMANT** |

**Implication:** Pass 1's "wdai-admin draining" is verified by zero recent activity. wdai-lumabot is also dormant — Pass 1 didn't flag it.

---

## Wix code residue (Wave 2)

`grep -ril wix` across all repos:

All Wix references live in `wdai-admin` exclusively:
- `src/airtable/wix.ts`, `wixIntegration.ts`
- `src/routes/wixWebhooks.ts`
- `src/services/wixsync.ts`
- `src/utils/wixDataTransformers.ts`
- `src/__test__/wixsync/` test suite
- `package.json` (`dev:wixsync` + `start:wixsync` scripts)

**Verification:** zero Wix env keys in any active `.env.example`. Wix is fully retired at the integration level. Wix code lives only in dormant `wdai-admin` as dead path.

---

## Repo structure correction (Wave 3)

`wdai-foundation-platform/` is a **Turborepo with 6 packages** + the main `web/` app. Pass 1 only audited `web/`:

```
wdai-foundation-platform/
├── web/                       # main Next.js app (Pass 1 audited this)
├── apps/web/                  # 2-file stub (abandoned migration)
├── packages/
│   ├── course-update-agent/   # @wdai/course-update-agent npm package
│   ├── website-agent/         # @wdai/website-agent npm package
│   ├── database/              # shared DB layer (Prisma)
│   ├── lib/                   # shared library code
│   ├── test-utils/            # test helpers
│   └── ui/                    # shared UI components
├── _poc/                      # proof-of-concept artifacts
├── docs/
└── CLAUDE.md (36 KB)
```

No `turbo.json` in root — Turborepo wiring is incomplete or stalled. Each agent is a separate npm package consumed by both the `web/` app (potentially) and the GH Actions workflows.

---

## Cron inventory — DEFINITIVE (Wave 3)

### Vercel Crons (verified via `web/vercel.json`)

14 schedule rules / 12 unique paths:

| Path | Schedule | Cadence |
|------|----------|---------|
| `/api/cron/heartbeat` | `0 */12 * * *` | every 12hr |
| `/api/cron/refresh-events` | `0 2 * * *` | daily 2am UTC |
| `/api/cron/sync-stripe` | `0 3 * * *` | daily 3am UTC |
| `/api/cron/sync-slack-links` | `30 3 * * *` | daily 3:30am UTC |
| `/api/cron/sync-guests` | `0 13 * * *` | 13:00 UTC |
| `/api/cron/sync-guests` | `0 19 * * *` | 19:00 UTC |
| `/api/cron/sync-guests` | `0 0 * * *` | midnight UTC |
| `/api/cron/check-cache-health` | `0 */6 * * *` | every 6hr |
| `/api/cron/weekly-events-digest` | `0 12 * * 1` | Monday 12pm UTC |
| `/api/cron/weekly-stats` | `0 14 * * 1` | Monday 2pm UTC |
| `/api/cron/collect-recordings` | `0 0 * * *` | daily midnight UTC (5pm PDT) |
| `/api/cron/process-uploads` | `0 1-23/2 * * *` | every 2hr odd hours |
| `/api/cron/daily-digest` | `0 8 * * *` | daily 8am UTC |
| `/api/cron/weekly-trend-digest` | `0 12 * * 5` | Friday 12pm UTC |

### GitHub Actions Crons (verified by reading workflow `on.schedule` blocks)

**4 cron-scheduled workflows** (not 5 as Pass 1 finding #4 claimed):

| Workflow | Repo | Schedule | What it does |
|----------|------|----------|--------------|
| `course-content-agent.yml` | platform | `0 9 15 * *` | **15th of month** 9am UTC — course updates |
| `website-content-agent.yml` | platform | `0 9 1 * *` | **1st of month** 9am UTC — website content updates |
| `calendar-sync.yml` | marketing | (PAUSED 2026-04-21) | daily marketing copy cron |
| `weekly-stats.yml` | wdai-admin | weekly | calls Railway admin service |

### NOT scheduled (event-triggered, miscategorized as cron in Pass 1)

- `claude.yml` (wdai-admin): `issue_comment` / `pull_request_review` triggers — the `@claude` mention bot

### Total scheduled automations

- 12 Vercel cron paths (14 rules)
- 4 GH Actions crons
- 1+ Slack Workflow Builder (Educational Content Reminder)
- **Total: 17 scheduled automations** (Pass 1 finding #4 said 18+; correcting)

---

## CRITICAL: course-update-agent and website-content-agent dates are REVERSED in Pass 1

**Pass 1 claimed:**
- `course-update-agent` runs 1st of month
- `website-content-agent` runs 15th of month

**Actual (verified by reading workflow files):**
- `website-content-agent.yml`: `cron: '0 9 1 * *'` — **1st of month** at 9am UTC
- `course-content-agent.yml`: `cron: '0 9 15 * *'` — **15th of month** at 9am UTC (workflow file comment: *"offset from website-agent on 1st"*)

**Affected Pass 1 locations to correct:**
- `01-system-context.md` finding #11: "course-update-agent 1st, website-content-agent 15th" → reverse
- `02-process-flows.md` course-update-agent flow header: "Every 1st of the month" → 15th
- `06-system-summary.md` Q2 design questions row

---

## CRITICAL: Wit pipeline is NOT on Helen's Mac mini

**Pass 1 claimed (L3b):**
> Wit pulls Google Meet recordings into Vimeo. These are one-way emissions, not federation — Helen's stack writes out, no one writes back in.

**Verified by `web/app/api/cron/collect-recordings/route.ts`:**
The Meet→Vimeo pipeline runs as a **Vercel cron** in the platform repo, scheduled `0 0 * * *` (daily midnight UTC / 5pm PDT). It uses:
- Google Meet API (`@/lib/google-meet`)
- Google Drive Service Account (`GOOGLE_SERVICE_ACCOUNT_KEY`)
- Prisma `RecordingUpload` table
- `postRecordingApprovalRequest` from `slack-admin.ts` to admin Slack channel
- Companion cron `process-uploads` every 2 hours handles the actual Vimeo upload after approval

**3 phases in `collect-recordings`:**
1. **DRAIN:** Move recent files from organizer's My Drive "Meet Recordings" folder → `GOOGLE_MEET_CONTENT_FOLDER_ID` shared folder
2. **TRACKED:** Process `EventMeeting` records for platform-created events, create `RecordingUpload` with status `approved`
3. **SWEEP:** Scan shared folder for orphan videos, create `RecordingUpload` with status `pending_approval`, post to admin Slack for approval

**Implication for Pass 1:**
- Wit may not exist as a real Helen-OpenClaw agent. "Wit" is either a defunct local agent OR a label for the cron pipeline that has since migrated to the platform.
- L3b's claim that Helen's stack has 3 agents (Syl + Pattern + Wit) needs verification — Wit at minimum is contradicted by the live system.
- The "no bridge between OpenClaw stacks" finding still stands but with one less agent to bridge.

**Affected Pass 1 locations:**
- `01-system-context.md` L3b: remove Wit as Helen-OpenClaw agent (or flag as defunct/migrated)
- `02-process-flows.md` AI Foundations cohort experience: replace `Wit` with `collect-recordings cron` (platform paradigm 4b)
- `06-system-summary.md` Helen-operates-X bot count
- `bot-registry.md` Wit entry — reclassify as platform cron, not OpenClaw agent

---

## Integration footprint per repo (verified via `.env.example`)

### `wdai-foundation-platform` (30+ env keys)
- **Auth:** Clerk (3 keys) · CRON_SECRET
- **Data:** Supabase (DATABASE_URL, DIRECT_URL) · Vercel Blob (BLOB_READ_WRITE_TOKEN)
- **Mailchimp:** ENABLED flag + 3 keys (graceful-degradation pattern)
- **Luma:** 3 keys
- **Gumloop:** 4 keys (API + CRON_WEBHOOK + USER_ID + WEBHOOK — bidirectional confirmed)
- **Google Workspace:** Service Account + Maps + Meet folder ID + Workspace events email
- **Analytics:** GA Measurement ID + API Secret
- **NEW: Intro-matcher:** `INTRO_MATCHER_ENABLED` + `MATCHER_API_SECRET` (Madina, May 10)
- **NEW: Content Proposals:** `CONTENT_PROPOSALS_API_KEY` (for course/website agents)
- **Stripe:** not in `.env.example` (production-only)
- **NO Wix key**

### `wdai-marketing` (12 env keys)
- Anthropic API
- GitHub Token + Owner + Repo
- Luma + LUMA_MOCK flag
- Mailchimp (3 keys)
- Slack (3 keys)
- **LinkedIn token NOT in `.env.example`** despite `linkedin-client.ts` using `com.linkedin.ugc.ShareContent` — production-only credential

### `mailchimp-cc` (2 env keys)
- Mailchimp API only — confirms pure CLI tool

### `wdai-admin` (13 env keys)
- Airtable (2 keys — still active reads)
- Luma (1 key)
- Slack (4 keys including team_id, admin channel, leaders channel)
- Circuit breaker + connection pool feature flags
- HOST/PORT (Fastify)
- **NO Wix key** despite `wixsync.ts` source still present

### `wdai-lumabot` (16 env keys)
- Airtable (4 keys — full read coverage)
- Luma (3 keys including webhook secret)
- Slack (5 keys + user/usergroup allowlists)
- Google OAuth (3 keys including refresh token)

---

## New features Pass 1 missed

### `intro-matcher` (Madina, May 10 commits)
- New API endpoint: `/api/intro/suggest-matches`
- Env vars: `INTRO_MATCHER_ENABLED`, `MATCHER_API_SECRET`
- Replaces stale Gumloop+Airtable matcher with live DB-backed logic
- Path: `web/app/api/intro/suggest-matches/route.ts`
- Multiple commits May 10 (setup docs, PR body cleanup, test plan iteration)
- This was the WDAI PR #603 work — Pass 1 should reference the new live-DB matcher as the migration off Gumloop-intro-flow

### `MAILCHIMP_ENABLED` feature flag
- Implies graceful degradation if Mailchimp is unavailable or being migrated
- Not visible in any Pass 1 file

### `CONTENT_PROPOSALS_API_KEY`
- Suggests the autonomous agents (course-update + website-content) authenticate against the platform's API with this key
- The companion to `AGENT_DATABASE_URL` for scoped agent access
- Not visible in Pass 1's agent-credential framing

---

## Things needing further verification (gaps)

| Claim | Status | Probe needed |
|-------|--------|--------------|
| Lumabot Railway service actively running | UNVERIFIED (railway.json exists, dormant 30+d) | Railway dashboard check or HTTP probe on its endpoint |
| wdai-admin Railway service actively running | UNVERIFIED (no railway.json in repo, dormant 30+d) | Same |
| Marketing calendar-sync STILL paused since 2026-04-21 | UNVERIFIED | Check GH Actions runs page directly |
| Pattern's weekly report last published when | URL up, age 1d (cached) | Pull actual page content + look for date |
| Helen's Sev0 incident date | UNVERIFIED | Q2 planning quote says "recently" — no date |
| Whether `claude.yml` in wdai-admin has been used recently | UNVERIFIED | Recent issue/PR activity check |
| #get-help support bot's Slack bot_id | UNVERIFIED | Slack workspace probe |
| Stripe webhook handler current state | UNVERIFIED (deferred in Pass 1 audit gaps) | Read `web/app/api/stripe/webhook/route.ts` |

These are Pass 2 (coordination surface) work.

---

## Updated Pass 1 corrections — to apply in this commit

1. **Finding #4:** "5 GH Actions crons" → "4 GH Actions crons" + total automations 17, not 18+
2. **Finding #11:** course-update-agent on **15th**, website-content-agent on **1st** (reversed)
3. **L2 container diagram + prose:** add Turborepo + packages structure to platform container
4. **L3b:** remove Wit as Helen-OpenClaw agent; redirect to platform cron `collect-recordings`
5. **L3a:** add `intro-matcher` API + `MAILCHIMP_ENABLED` flag + `CONTENT_PROPOSALS_API_KEY` to credential inventory
6. **02 course-update-agent flow:** date 1st → 15th
7. **02 AI Foundations diagram:** Wit → platform cron
8. **bot-registry:** reclassify Wit, note Helen-OpenClaw count drops to 2 (Syl + Pattern) unless Wit is verified as a separate local agent
9. **03 risk register:** drop Wix as in-flight migration (already done in earlier commit), add Lumabot Railway state UNVERIFIED
10. **06-system-summary diagram:** update Helen-OpenClaw box from "Syl Pattern Wit" → "Syl Pattern" pending Wit verification

---

## What this audit taught us about discipline

The probe sweep caught **6 errors Pass 1 had asserted with confidence**:
1. Wix as live integration → retired
2. course/website agent date assignment → reversed
3. Wit pipeline location → not OpenClaw, it's Vercel cron
4. GH Actions cron count → off by one (claude.yml miscategorized)
5. Platform repo structure → Turborepo missed
6. intro-matcher → entirely missed (active May-10 development)

All 6 errors would have been caught by **probing the live system before writing the claim**. The Pass-1 discipline failure was the same in every case: trusted slack/docs/sub-agent-deep-dives over `vercel.json` + `.github/workflows/` + `web/app/api/` source.

**Pass 2 rule going forward:** every tech-stack claim is sourced from code/config/deployment-logs, not from documentation or conversation. Documentation answers WHY. Probes answer WHETHER.
