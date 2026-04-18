# Projects — Cold Memory

Detailed project context. Searched on-demand, not loaded every session.

<!-- added 2026-04-17 -->
## WDAI Foundation Platform — environment architecture

Location: `C:\Workspace\Women Defining AI\wdai-foundation-platform\`
Stack: Next.js 16 + Clerk + Stripe + Prisma + Supabase Postgres. Node 20, Biome, Vitest, Playwright.

**Three environments:**

| Env | DB | Auth | Stripe | Email/Mailchimp |
|---|---|---|---|---|
| **Local dev** | Docker Postgres on `localhost:5433` (seed: `bash ./scripts/db-local.sh reset` from `web/`) | Clerk test mode | Stripe test mode | Mailchimp API key absent server-side; form URL hardcoded to live audience (accepted risk) |
| **Staging** | Supabase project `qfcjtidvmzvppxbkxupk` (us-east-2) | Clerk test mode (separate app) | Stripe test mode | Same Mailchimp URL leak as local |
| **Production** | Separate Supabase project | Clerk live mode | Stripe live mode | Mailchimp live |

**Three services are the dev-onboarding foundation** (per Helen's framing): Clerk + Stripe + DB. Everything else (Luma, Mailchimp API, Vimeo admin, Slack, PostHog) gated to contributors actively working on those integrations — default `.env.local` only needs the three.

**Known drift sources:**
- Mailchimp cohort RSVP form URL hardcoded in `content/product/courses.ts` → preview deploys post to live audience. Accepted operational risk. Fix is env-driven URL resolution; future PR.
- `SLACK_DRY_RUN=true` in staging Vercel env no-ops Slack sends (confirmed via `grep -n SLACK_DRY_RUN lib/slack.ts`).

**Windows dev gotchas:**
- Prisma `db:generate` fails with EPERM DLL lock when the `next dev` server is running. Stop server first.
- `npm run db:local:reset` uses a bash script that PowerShell can't invoke — run `bash ./scripts/db-local.sh reset` instead.
- Biome line-ending warnings (`LF will be replaced by CRLF`) are Windows-only noise; CI on Linux is clean.
- Repo-wide biome sees ~240 errors locally (mostly CRLF); CI's `biome check . --diagnostic-level=error` passes on Linux.

**Pipeline architecture (added 2026-04-17 via PR #564):**
- `web/scripts/staging-refresh/{preflight,dump,transform,restore}.sh` — prod → staging refresh
- `.github/workflows/staging-refresh.yml` — weekly cron Sundays 11:00 UTC + `workflow_dispatch`
- `web/app/api/staging-status/route.ts` — leader-gated observability endpoint
- `web/prisma/schema.prisma` `StagingMeta` model (single-row, CHECK id=1)
- V1 ships without PII anonymization. V2 triggers documented in `docs/plans/staging-refresh-pipeline.md`.
