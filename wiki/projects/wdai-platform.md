---
name: WDAI Platform
org: Women Defining AI
type: contributor
status: active
path: C:\Workspace\Women Defining AI
tags: [wdai, code, active]
---

# WDAI Platform

Dina is a contributor to the WDAI platform codebase. This is the org's main project workspace.

## Workspace
`C:\Workspace\Women Defining AI\`

## Role
Active contributor — internal tooling, Slack automations, operational process design.
PRs require review from Helen's team before merge. Dina does not have unilateral deploy authority.

## Technical Details
- **Tech debt audit:** [[projects/wdai-tech-debt|WDAI Tech Debt Audit]] (Polaris, 2026-04-19) — 9 Must Fix / 19 Nice to Fix. Top findings: MainProtection ruleset misconfiguration + 8-PR stalled backlog.
- **Repos:** `wdai-foundation-platform` (main app), `claude-code-skills` (open source skill library)
- **Stack:** Next.js 16, React 19, TypeScript (strict), Tailwind CSS, Framer Motion
- **Auth:** Clerk (roles: visitor, member, leader + admin flag)
- **Database:** PostgreSQL (Supabase) + Prisma v6 — 19+ models
- **Payments:** Stripe Subscription Schedules API (never direct updates)
- **Events:** Luma API with 48h cache + Google Geocoding
- **Testing:** Vitest (unit), Playwright (E2E smoke), Vitest-integration-v2 harness (MSW + real Postgres, added 2026-04-18)
- **CI/CD:** GitHub Actions + Vercel
- **Key patterns:** App Router, webhook idempotency via `webhookEvent` table, Clerk metadata for onboarding, minimal useEffect
- **Features:** Member directory, resource library, courses/LMS, Luma events, Stripe subscriptions, weekly trend digest, Slack sync
- **Agent skills:** defrag (PR #560), council, commit-workflow, pr-merge-workflow, review-codex, seo-public-page
- **Team context:** All non-developers/vibecoders. CI + smoke testing + defrag are the quality safety net. No one manually reviews code.

## Test coverage status (2026-04-18)

Shipped via the test-coverage sequence — 7 PRs, all draft-ready for Helen's review:

- **#574** — CODEOWNERS (re-opens closed #565). Includes setup instructions for Helen to enable 'Require review from Code Owners' + required status checks (`Test`, `Database Schema & Seed Test`, `Integration Tests`) in MainProtection ruleset.
- **#567** — integration-v2 harness (MSW + real Postgres, via GitHub Actions Postgres service in CI or local Docker). Ships the smoke test and `test:integration` CI job (advisory today; goes mandatory when Helen adds to required checks post-merge).
- **#568** — middleware firewall (narrowed `isIgnoredRoute` for `/api/admin/*` to only HMAC-gated recording paths; `/api/cron/*` now gated via `checkCronAuth`; removed vestigial `/api/dev/*`) + boot-time env validation via zod in `lib/env.ts` + `instrumentation.ts`.
- **#569** — Stripe webhook claim-before-process race fix + concurrent-delivery integration test. Closed a real latent race.
- **#571** — Clerk `user.deleted` handler (previously unhandled; ghost-access/GDPR gap) + same claim-before-process race fix + cascade tests.
- **#572** — Content-proposal length cap (50k chars on `afterValue` to guard against LLM hallucinations bloating JSONB) + apply→rollback round-trip invariant test. XSS guard dropped on review (MarkdownRenderer is already rehype-raw-free).
- **#573** — ADR-001 at `web/docs/decisions/001-payment-enrollment-bridge.md` documenting the deliberate decoupling of Stripe payment and course enrollment (safety net = lesson-progress auto-enroll) + integration tests pinning the invariant.

Plan file: `C:\Users\Mgbot\.claude\plans\clever-doodling-platypus.md` (v3, final).

## Test coverage follow-up — integration tests not in the v1 stack

Ranked by honest value. Consider for a future session; none of these are critical.

1. **`invoice.payment_failed` webhook integration test** — handler sets `churnReason='payment_failure'`, no test verifies. Modest value, ~30min.
2. **Cron endpoint auth** — `/api/cron/*` parametrized test asserting all 10 routes reject unauthed traffic. Middleware dispatch exists (#568) but never test-covered. Small, real.
3. **`admin/clear-user-data` blast-radius test** — wrong-user wipe is irreversible; seed multiple users and verify only the target's rows are deleted. Medium effort.
4. **Lesson-progress auto-enroll fallback** — ADR-001 safety net, currently pinned only in prose. ~1 small test.
5. **Content-proposal apply at the route level** (`POST /api/admin/content-proposals/batches/[batchId]/apply`) — lib is tested; route adds auth + audit-log write. Incremental.

Explicitly deferred / low value:
- Other Stripe webhook events (`checkout.session.expired`, `subscription_schedule.*` × 6) — handlers exist, low-consequence drift
- Clerk `user.updated` profile sync — inspected as correct, drift is cosmetic
- Slack `/api/slack/events` inbound — already signature-verified, events are observational
- Admin course/cohort CRUD routes — human-gated, low attack surface
- Middleware at the full-request level — unit tests on helpers cover the branching
- Zod at route boundaries (the ex-#2a/b/c) — signature verification + typed SDK events already cover most of the concern

## Local Windows integration-test bug (2026-04-18)

`web/tests/integration-v2/setup.ts` uses `spawnSync(prismaBin, [...], { shell: false })` to run `prisma db push`. On Windows locally, `.bin/prisma.cmd` cannot be invoked by spawnSync without `shell: true`. CI (Linux) works fine. Fix is a small follow-up PR after the main stack merges — either pass `shell: isWindows` or invoke via `cmd.exe /c` on Windows. Not blocking.
