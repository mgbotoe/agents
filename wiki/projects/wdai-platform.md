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
- **Repos:** `wdai-foundation-platform` (main app), `claude-code-skills` (open source skill library)
- **Stack:** Next.js 16, React 19, TypeScript (strict), Tailwind CSS, Framer Motion
- **Auth:** Clerk (roles: visitor, member, leader + admin flag)
- **Database:** PostgreSQL (Supabase) + Prisma v6 — 19+ models
- **Payments:** Stripe Subscription Schedules API (never direct updates)
- **Events:** Luma API with 48h cache + Google Geocoding
- **Testing:** Vitest (unit), Playwright (E2E smoke)
- **CI/CD:** GitHub Actions + Vercel
- **Key patterns:** App Router, webhook idempotency via `webhookEvent` table, Clerk metadata for onboarding, minimal useEffect
- **Features:** Member directory, resource library, courses/LMS, Luma events, Stripe subscriptions, weekly trend digest, Slack sync
