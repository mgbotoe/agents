# Platform-Hosted Bots — Major Correction to Bot Registry

**My earlier bot registry called WDAI Newswire (bot_id `B0A4747GZ2A`) and AdminBot (bot_id `B08GF1SGGNL`) "external Slack apps." That was wrong.** Both are **Slack apps whose implementations live as TypeScript code inside `wdai-foundation-platform`.** The Slack-side bot identity exists, but the brain is in the platform repo.

This changes the architecture diagram substantially.

---

## Three Slack apps live in the platform repo

`wdai-foundation-platform/web/.env.example` enumerates three distinct Slack app tokens:

```
SLACK_BOT_TOKEN=          # App 1: Course Reflections
SLACK_MEMBER_BOT_TOKEN=   # App 2: WDAI Newswire
SLACK_ADMIN_BOT_TOKEN=    # App 3: Admin Bot (replaces Railway's MemberBot)
```

Plus channel destinations:

```
SLACK_CHANNEL_INTROS=         # #intros
SLACK_CHANNEL_EVENTS=         # #events
SLACK_CHANNEL_RESOURCES=      # #share-demos-and-examples
SLACK_CHANNEL_ALERTS=         # admin alerts (cron fail, webhook fail)
SLACK_ADMIN_CHANNEL_ID=       # #devops-admin-mgmt or equivalent (admin events)
```

Plus module-specific webhooks for course reflections:
```
SLACK_WEBHOOK_MODULE_1=
SLACK_WEBHOOK_MODULE_2=
SLACK_WEBHOOK_MODULE_3=
```

---

## App 1: Course Reflections

**Source:** `web/lib/slack.ts` (shared with Newswire)
**Token:** `SLACK_BOT_TOKEN`
**Trigger:** Member shares a lesson reflection in the portal
**Posts to:** Module-specific incoming webhooks (one per module)
**Functions:** `shareReflectionToSlack`, `formatReflectionMessage`, `getWebhookForCourse`, `isSlackSharingEnabledForCourse`
**Identity use:** Only used for user email → Slack member lookup (for tagging users in posts)

This is the "share your lesson reflection back to the cohort channel" feature.

---

## App 2: WDAI Newswire (the bot I cataloged externally — actually platform-hosted)

**Source:** `web/lib/slack.ts`
**Token:** `SLACK_MEMBER_BOT_TOKEN`
**Slack identity:** bot_id `B0A4747GZ2A`, app_id `A0A46V3SB6J`
**Where I saw it in the audit:** 28 messages in #intros (May 1-11), "Welcome to the community, X!"

**Functions and triggers (10+ flows under one Slack identity):**

| Function | Trigger | Destination | Frequency |
|----------|---------|-------------|-----------|
| `postProfileIntro` | Member completes profile in portal | `#intros` (SLACK_CHANNEL_INTROS) | Per new member |
| `updateProfileIntroPhoto` | Member updates profile photo | Edits existing intro post | On photo change |
| `postNewEvent` | Event created in platform | `#events` (SLACK_CHANNEL_EVENTS) | Per event (styled with buttons) |
| `postNewResource` | Resource submitted | `#share-demos-and-examples` (SLACK_CHANNEL_RESOURCES) | Per resource |
| `postWeeklyEventsDigest` | Vercel cron Monday 12pm UTC | `#events` | Weekly |
| `postWebhookFailureAlert` | Stripe/Clerk webhook fails | SLACK_CHANNEL_ALERTS | Fire-and-forget, no-ops if unset |
| `postCronAlert` | Any cron job fails | SLACK_CHANNEL_ALERTS | Per failure |
| `postStaleCacheAlert` | Cache staleness detected | SLACK_CHANNEL_ALERTS | Per detection |
| `shareReflectionToSlack` | Member shares lesson reflection | Module webhook | Per user action |
| `postToChannel` | Generic — used by other libs | Configurable | Various |

**This is the same WDAI Newswire bot_id I saw in the Slack audit.** I just hadn't traced it back to the source code. All 28 messages in #intros come from `postProfileIntro` calls in `web/lib/slack.ts`.

---

## App 3: Admin Bot (the AdminBot migration story)

**Source:** `web/lib/slack-admin.ts`
**Token:** `SLACK_ADMIN_BOT_TOKEN`
**Header comment** (verbatim):
> *"This replaces the Railway internal webhook relay — notifications are now sent directly from Vercel instead of routing through Railway's MemberBot service."*

**This is the key migration finding.** The "AdminBot" I cataloged from `#devops-admin-mgmt` (197 messages, bot_id `B08GF1SGGNL`) was the **old Railway-hosted version**. The platform is now sending the same notifications directly from Vercel.

**Migration state:**
- Old: `wdai-admin/src/services/memberbot.ts` (Fastify on Railway) — receives Slack events, posts to admin channel
- New: `web/lib/slack-admin.ts` (Vercel serverless) — posts directly when platform code fires

**Functions (6 flows):**

| Function | Trigger | Destination |
|----------|---------|-------------|
| `postNewMemberAlert` | New member signs up | SLACK_ADMIN_CHANNEL_ID |
| `postChurnAlert` | Member cancels subscription | SLACK_ADMIN_CHANNEL_ID |
| `postUnsubscribedJoinAlert` | **The "no Wix purchase" warning I saw 197x in audit** | SLACK_ADMIN_CHANNEL_ID |
| `postWeeklyStatsAlert` | Weekly stats cron (Monday 2pm UTC) | SLACK_ADMIN_CHANNEL_ID |
| `postRecordingApprovalRequest` | Recording uploaded, needs approval | SLACK_ADMIN_CHANNEL_ID |
| `postRecordingUploadFailed` | Recording upload fails | SLACK_ADMIN_CHANNEL_ID |

---

## Migration is in flight (paradigm 2 → paradigm 4)

The shift from Railway-hosted AdminBot → Vercel-hosted slack-admin.ts is **a real architectural migration happening right now**. The `wdai-admin` Railway service is being **drained** of responsibilities:

| Responsibility | Old home | New home |
|----------------|----------|----------|
| Member churn alerts | wdai-admin (Railway) | platform/slack-admin.ts (Vercel) |
| New member alerts | wdai-admin (Railway) | platform/slack-admin.ts (Vercel) |
| "No Wix purchase" warning | wdai-admin (Railway) | platform/slack-admin.ts (Vercel) |
| Weekly stats | wdai-admin (Railway, weekly-stats.yml GH Action cron) | platform/slack-admin.ts (Vercel) |
| Recording approval | wdai-admin (Railway) | platform/slack-admin.ts (Vercel) |
| WixSync webhook processing | wdai-admin (Railway, **deprecating**) | platform/api/stripe/webhook (already migrated) |
| Airtable member sync | wdai-admin (Railway) | _(still there?)_ |

**Implication for the team-OS spec:** Paradigm 2 (always-on Railway microservices) is in active *retreat* in WDAI. The platform is absorbing capabilities into paradigm 4 (Vercel serverless + Vercel Cron). What's left on Railway:
- `wdai-lumabot` — needed for Socket Mode + slash commands (paradigm 2 requirement)
- `wdai-admin` — increasingly skeletal, mostly Airtable sync remains

If the Airtable→Supabase migration completes by August, **wdai-admin Railway service may go away entirely**.

---

## Additional platform Slack capabilities

### Inbound: `/api/slack/events`
Platform accepts Slack events (channel joins, button clicks) via `web/lib/slack-events.ts` HMAC-SHA256 verification. Replay protection (5-min window), timing-safe comparison.

### Click tracking: `/api/slack/track-click`
When member clicks Slack invite link in portal → logged to `AuditLog` with `action: 'SLACK_INVITE_CLICKED'`.

### Sync: `/api/slack/sync` + `/api/slack/link`
Platform-to-Slack identity mapping (used by `sync-slack-links` cron).

### Cron-Slack channel: `/api/cron/daily-digest`
Posts cron-health summary to `#devops-website-alerts` (an alert channel — different from `#devops-admin-mgmt` where the old AdminBot posted). Uses `postToChannel`.

### Slack admin endpoints in `/api/admin/slack/`
Staff tools for member ↔ Slack management.

---

## Bonus: Gumloop integration as a TARGET, not just a source

`web/lib/cron-notify.ts` posts cron lifecycle events to a Gumloop webhook (`GUMLOOP_CRON_WEBHOOK_URL`). Separate from `GUMLOOP_WEBHOOK_URL` used for PR/content events.

**Meaning:** the platform doesn't just receive from Gumloop — it also **pushes events INTO Gumloop**. So Gumloop has flows triggered by:
1. Slack events (channel messages → Gumloop)
2. Platform cron events (cron start/complete/fail → Gumloop)
3. Platform PR/content events (PR opened/merged → Gumloop)

This is bidirectional. Gumloop is more deeply embedded in the operations than the Slack audit alone showed.

---

## Corrected bot registry

The previous bot-registry.md described WDAI Newswire and AdminBot as standalone Slack apps with bot_ids and no traced ownership. **Correction:**

| Bot user_name | bot_id | Where its CODE lives | Where it POSTS |
|---|---|---|---|
| **WDAI Newswire** | B0A4747GZ2A | `wdai-foundation-platform/web/lib/slack.ts` (10+ functions) | #intros, #events, #share-demos-and-examples, alerts channel, module webhooks |
| **AdminBot (legacy)** | B08GF1SGGNL | `wdai-admin/src/services/memberbot.ts` (Railway, Fastify) — DEPRECATING | #devops-admin-mgmt (197 historical msgs) |
| **AdminBot (new)** | (same Slack app, new token + sender) | `wdai-foundation-platform/web/lib/slack-admin.ts` (6 functions) | SLACK_ADMIN_CHANNEL_ID |
| **Course Reflections** | (TBD — not in audit, but exists) | `wdai-foundation-platform/web/lib/slack.ts` (shareReflectionToSlack) | Module webhooks |
| **WDAI Marketing Content Calendar** | B0B1J2S4D2R | `wdai-marketing/.github/workflows/calendar-sync.yml` + `tools/calendar/slack-notifier.ts` | #team-marketing-content-calendar |
| **Lumabot** | (varies — not surfaced in audit yet) | `wdai-lumabot` (Railway, Bolt Socket Mode) | DevOps notifications channel |
| **Gumloop fleet** | B0896A6N147 | Gumloop SaaS (vendor-hosted flows) | Various channels |
| **Educational Content Reminder** | B07FZCMDKNC | Slack Workflow Builder (no-code, no repo) | #ops-edu-content-on-social |
| **Polly** | B06451SB6RJ | Third-party SaaS bot | Various (poll voting) |
| **Helen's old Zapier 'donald' bot** | B05PNPUDJNS | Zapier (legacy) | Various |
| **Member personal apps** | varied | Each member's own integration | Member-test channels |

---

## Patterns observed (deferred to Pass 3 for design decisions)

1. **The platform is the de-facto "team-OS" already for member-related bot logic.** It hosts 3 Slack apps, ~20 cron jobs, ~16 posting functions, and is absorbing wdai-admin's responsibilities. **The team-OS shouldn't compete with this** — it should plug into AuditLog + leverage the existing Slack-posting libraries.

2. **Newswire is the canonical "platform posts to community" interface.** Any new automation that needs to inform members via Slack should add a function to `web/lib/slack.ts` and use Newswire — NOT create a new Slack app. This is the federation contract for member-facing posts.

3. **The Admin Bot is the canonical "platform alerts staff" interface.** Same pattern — add to `web/lib/slack-admin.ts`, not new app.

4. **Paradigm-2 retreat is the direction-of-travel.** Helen's design doc proposes Cowork (paradigm 1) as the team-OS runtime. The platform is moving AWAY from Railway (paradigm 2) TOWARD Vercel (paradigm 4). The team-OS should align with paradigm 4 unless there's a specific always-on requirement.

5. **Gumloop integration is bidirectional.** Platform pushes events INTO Gumloop too. The team-OS audit should treat Gumloop as a peer system, not just a vendor SaaS-bot host.

6. **AuditLog is the cross-paradigm telemetry sink.** Every Slack invite click, every cron run, every member action lands there. The team-OS dashboard layer (Pass 3) can subscribe to AuditLog events instead of building a new event bus.

---

## Open questions

1. **Is the AdminBot Slack app being merged with the Newswire Slack app, or staying separate?** Three apps with three bot tokens is fine, but maintenance overhead.
2. **What's left in `wdai-admin` Railway after the migration?** If it's just Airtable sync, can that move to a Vercel cron too?
3. **`GUMLOOP_WEBHOOK_URL` (PR/content events) vs `GUMLOOP_CRON_WEBHOOK_URL` (cron events)** — what Gumloop flows consume these? Worth checking the Gumloop side.
4. **Does the team-OS get its own Slack app, or share Newswire?** Sharing reduces app sprawl but mixes concerns. New app means another token to provision.
5. **Course Reflections webhook URLs** — module-specific webhooks bypass the bot identity model. Worth understanding if this pattern is good (decentralized, no token) or bad (no audit).
