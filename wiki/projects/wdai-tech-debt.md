# WDAI Tech Debt Audit

**Living document.** Updated as items are resolved. Linked from [[projects/wdai-platform|WDAI Platform]].

- **Phase 1 complete:** 2026-04-19 — architecture, critical paths, security, DevOps (see [Scope](#scope))
- **Phase 2 pending:** duplication, file-size, deps, test coverage, docs audit
- **Auditor:** Polaris (independent read against `wdai-foundation-platform` @ 2026-04-19)

---

## TL;DR

**3 P0 findings, one of which is root cause for several others.** The team's discipline on idempotency, type strictness, critical-path conventions, and schema design is real — this is not a sloppy codebase.

| Severity | Count |
|---|---|
| Must Fix | 9 |
| Nice to Fix | 19 |
| Negligible | 4 |

**Biggest finding:** `MainProtection` ruleset is active on `main` but configured with `required_approving_review_count: 0` AND `require_code_owner_review: false`. CODEOWNERS doesn't even exist on main yet (PR #574 supplies it). For a team of non-developers where review gating is the safety net, this is ceiling-level important.

**Root-cause finding:** **8 improvement PRs are open, passing CI, and not merging.** The absent review gate (MF-01) means there's no forcing function. Helen is a single-point-reviewer bottleneck for everything. Many of the other findings below are already fixed in these branches — they just aren't shipping.

**Biggest false alarm:** CLAUDE.md is genuinely excellent and the code largely follows it. Several audit pre-seeds turned out to be stale assumptions (CODEOWNERS "missing" — coming via #574; "no staging env" — Vercel previews → persistent Supabase staging per CLAUDE.md line 907).

---

## Audit State — What Was Audited

This audit was run against **Dina's local working branch** `tmp/all-tests-local`, which includes changes from 8 open PRs. **`origin/main` is substantially weaker.**

**Delta between main and local (critical paths only):**

| File | `main` | local | What's in local |
|---|---|---|---|
| `.github/CODEOWNERS` | ❌ absent | ✅ 49 LOC | PR #574 |
| `web/app/api/stripe/webhook/route.ts` | 746 LOC, check-first idempotency (race) | 765 LOC, insert-first P2002 (race-safe) | PR #569 |
| `web/app/api/clerk/webhook/route.ts` | 247 LOC | 308 LOC (+ user.deleted cascade) | PR #571 |
| `web/lib/middleware-helpers.ts` | ❌ absent | ✅ 48 LOC (HMAC allow-list, cron auth) | PR #568 |
| `web/middleware.ts` | 117 LOC | 141 LOC (firewall-narrowed admin, cron gate) | PR #568 |
| `web/lib/env.ts` | ❌ absent | ✅ zod env validation | PR #568 |
| `web/tests/integration-v2/*` | ❌ absent | ✅ MSW + real Postgres harness | PR #567 + #569/#571/#572 |

Where findings differ by branch, each item below is tagged **[MAIN]** (exists today) or **[POST-MERGE]** (about to exist when PRs land). Unmarked findings apply to both.

---

## Must Fix

### MF-01 — Branch protection is theater [MAIN]
**File:** GitHub → Repo → Rules → MainProtection ruleset (id 10793853)
**Impact:** On `main` right now: (a) no CODEOWNERS file, (b) `required_approving_review_count: 0`, (c) `require_code_owner_review: false`. Anyone with write access can merge with zero approvals. Given the team is non-developers and much of the code is AI-authored, this is the single highest-leverage fix in the audit.
**Evidence:** `gh api repos/WomenDefiningAI/wdai-foundation-platform/rulesets/10793853` returns:
- `required_approving_review_count: 0`
- `require_code_owner_review: false`
- `dismiss_stale_reviews_on_push: false`

Required status checks (Build, Database Schema & Seed Test) **are** enforced — that's the only real gate right now.

**Fix sequence:**
1. Merge **PR #574** (adds CODEOWNERS). Already open, CI green.
2. Helen toggles the ruleset on GitHub: `required_approving_review_count: 1` + `require_code_owner_review: true`. The PR description on #574 includes setup instructions.
3. Add `Test`, `Integration Tests` to required status checks (currently only Build + DB test are required).

**Scope:** S (merge + settings toggles)
**Confidence:** HIGH — verified via API and git show origin/main
**Cross-ref:** Blocks MF-09.

---

### MF-02 — PR backlog stalled (8 open PRs, all CI-green) [MAIN]
**Evidence:** `gh pr status` returns 8 open PRs from Dina against `main`, all passing checks:
- **#574** chore: CODEOWNERS (blocks MF-01 fix)
- **#573** docs+test(enrollment): ADR-001 + integration tests
- **#572** feat(content-proposals): round-trip invariant + sanitization tests
- **#571** feat(clerk-webhook): user.deleted cascade + race fix
- **#569** test+fix(webhook): Stripe idempotency race fix + concurrent test
- **#568** feat(security): middleware firewall + boot-time env validation
- **#567** test(integration): integration-v2 harness (MSW + real Postgres)
- **#564** Staging refresh pipeline (v1, no anonymization)

**Impact:** Real security and reliability improvements are sitting in branches not reaching prod. The Stripe webhook race condition (#569), Clerk ghost-user gap (#571), middleware firewall (#568) are all latent on main until these merge. The absent review gate (MF-01) removed the forcing function — nothing escalates these PRs. Helen is a single-point-of-review bottleneck with no SLA.

**Fix sketch:** Either (a) work through the backlog with Helen in a batch review session, or (b) land MF-01 first so that subsequent PRs force-function through CODEOWNERS assignment. Consider a "critical fixes first" sequence: #569 (Stripe race), #571 (Clerk cascade), #568 (firewall) — these three close real vulnerabilities and have strong test coverage via #567's harness.

**Scope:** Process fix. Doesn't need code.
**Confidence:** HIGH

---

### MF-03 — Abandoned monorepo migration (structural trap)
**Files:**
- `apps/web/` — contains only `next-env.d.ts` + stale `tsconfig.tsbuildinfo`
- `apps/admin/` — same
- No root `package.json` or `turbo.json`
- `.turbo/` cache directory exists
- `_poc/apps/` + `_poc/packages/` mirror the same structure

**Impact:** New contributors (human or AI) will guess wrong about where code lives. The directory layout signals "Turbo monorepo with web + admin apps" but the actual app is at top-level `web/` and the `apps/` subtree is inert. Every onboarding → wasted hour.
**Fix sketch:** Pick one direction and commit. Either (a) finish the migration: move `web/` → `apps/web/`, create `apps/admin/` stub or implementation, wire up `turbo.json`, make `packages/*` consumable. Or (b) delete the stubs: `rm -rf apps/ _poc/ .turbo/`, keep single-app layout.
**Scope:** L (migration) or S (deletion). Recommend deletion until there's a real need for admin-as-separate-app.
**Confidence:** HIGH

---

### MF-04 — Three Prisma schemas with model overlap (drift time bomb)
**Files:**
- `web/prisma/schema.prisma` (615 LOC, 22 models)
- `packages/course-update-agent/prisma/schema.prisma` (49 LOC, 2 models: `LessonContent`, `Resource`)
- `packages/website-agent/prisma/schema.prisma` (64 LOC, 6 models: `User`, `Membership`, `CachedEvent`, `EventRsvp`, `LessonContent`, `Resource`)

**Impact:** Same Postgres cluster, three Prisma clients. Verified: both agent schemas read `env("DATABASE_URL")`; workflows inject `AGENT_DATABASE_URL` secret as that variable. CLAUDE.md disable-rls.sql comment confirms agents share the web DB ("unblock service accounts like the website-agent"). If web's `User` model adds a required field, the agent schemas won't know — runtime errors or silent data corruption when agents write to shared tables. Classic drift risk. Currently OK because agents are append-mostly (proposals in, reads out), but the pattern is a trap.
**Fix sketch:** Publish web's schema as a shared package (`packages/database`) and have agents import from it. The empty `packages/database` folder already exists, which suggests someone started this and didn't finish. Alternative: agents use raw SQL / @prisma/client generic, never their own schema.
**Scope:** L (cross-package refactor + CI update)
**Confidence:** HIGH

---

### MF-05 — No error observability (Sentry absent)
**Evidence:** Zero `@sentry/*` dependencies in `web/package.json`. 27 `console.error` calls in stripe webhook alone, 12 in clerk webhook. All payment/auth/webhook errors land in Vercel log scroll with no alerting, no context binding, no release tracking.
**Impact:** A silently failing webhook (Stripe payment processed, DB update fails, user locked out) is invisible until the user complains. In a non-dev team, users complain via Slack with "it's broken" — debugging requires live log scanning during the incident window.
**Fix sketch:** Add `@sentry/nextjs`, wrap middleware + webhook handlers, replace `console.error` in critical paths with `Sentry.captureException(error, { extra: { event } })`. Wire cron failure alerts (`postCronAlert` in `lib/slack.ts` already posts to Slack — extend to webhook failures).
**Scope:** M (install + config + 10-15 replaces + 1 Slack wire)
**Confidence:** HIGH

---

### MF-06 — Stripe webhook complexity (765 LOC, 28 changes in 6 months)
**File:** `web/app/api/stripe/webhook/route.ts` (765 lines, 12 event types handled, 15 try/catch blocks, 27 console.error calls)
**Impact:** Highest-churn file in the repo is also the most payment-critical. Each change is a risk. Single-file means cognitive load for any edit; test file at 784 LOC matches the complexity. 12 event types share one handler with no clear routing layer.
**Fix sketch:** Extract per-event handlers into `web/app/api/stripe/webhook/handlers/*.ts` (one file per event type). Keep `route.ts` as a dispatcher: signature verify + idempotency + handler lookup. Apply same pattern to clerk webhook. Paired with MF-04, each handler gets its own Sentry scope.
**Scope:** M (pure refactor, no logic change, preserves idempotency pattern)
**Confidence:** HIGH

---

### MF-07 — CLAUDE.md + code both have the old webhook idempotency pattern on main [MAIN]
**File on main:** `CLAUDE.md` lines 78-88 AND `web/app/api/stripe/webhook/route.ts` line 72/162 both use **check-first-then-process**:
```ts
// CLAUDE.md example:
const existing = await prisma.webhookEvent.findUnique(...)
if (existing) return 200
await prisma.$transaction(...)

// main code:
const existingEvent = await prisma.stripeWebhookEvent.findUnique(...)  // line 72
// ... process
await prisma.stripeWebhookEvent.create(...)  // line 162
```
This has a race: two concurrent deliveries of the same `event.id` both see no row at line 72, both process, one hits unique-constraint violation at line 162 — infinite Stripe retry loop on the loser. PR #569 fixes it using insert-first + P2002.

**Impact on main:** Live race condition on Stripe webhook. Low likelihood (requires concurrent delivery of same event.id within ms), but real. Clerk webhook has the same pattern — PR #571 fixes that one.

**Fix sketch:** Merge **PR #569** (Stripe) and **PR #571** (Clerk). **Then** update CLAUDE.md lines 78-88 to match the new insert-first pattern — current example will be stale after those merges.

**Scope:** S (merges + one doc edit post-merge)
**Confidence:** HIGH — verified on origin/main

---

### MF-08 — Manual SQL file bypasses migration tracking
**File:** `web/prisma/migrations/manual_add_resource_features.sql` (sibling to the 18 timestamped migrations)
**Impact:** Prisma's migration tracker doesn't know this file exists. CI's schema-push validation will succeed against the Prisma schema, but a fresh environment that applies only tracked migrations will diverge from prod. Exactly the drift scenario CLAUDE.md line 777 warns about.
**Fix sketch:** Either (a) fold into a proper timestamped migration and remove the manual file, or (b) confirm the changes are already in the schema and delete the SQL file. Re-run CI's schema validation to catch drift.
**Scope:** S
**Confidence:** HIGH

---

### MF-09 — Scripts directory bypasses lint + type-check (4285 LOC)
**Files:** `web/scripts/*` — 18 files, 4285 total lines. Top offenders: `seed-course-advanced.ts` (1727), `seed-course-intermediate.ts` (1028), `seed-course.ts` (384), `seed-slack-members.ts` (290), `migrate-vercel.js` (hot churn).
**Impact:**
- `tsconfig.json` excludes `scripts/` — no type safety
- `biome.json` excludes `**/scripts` — no lint
- `migrate-vercel.js` runs **during `npm run build`** — every production build invokes an unchecked script
- Seed scripts at 1700 LOC silently go wrong (field mismatch, missing relation) and only surface at runtime
**Fix sketch:** Remove the excludes. Run `biome check scripts/` + `tsc --noEmit` over scripts at least once and fix. Add to CI's `biome:check` scope. If some scripts genuinely need looser rules, target specific files rather than excluding the whole tree.
**Scope:** M (initial cleanup likely surfaces real bugs)
**Confidence:** HIGH

---

## Nice to Fix

### NF-01 — `lib/slack.ts` at 1380 lines has multiple concerns
**File:** `web/lib/slack.ts` — 15 exports mixing message formatting, user lookup, cron alerts, profile intros, reflection sharing, new-event/resource posts, weekly digests.
**Fix sketch:** Split into `slack/messages.ts` (postToChannel, postToSlack, postCronAlert, postStaleCacheAlert), `slack/digests.ts` (postWeeklyEventsDigest), `slack/formatters.ts` (formatReflectionMessage), `slack/users.ts` (lookupSlackUserByEmail, updateProfileIntroPhoto), `slack/share.ts` (shareReflectionToSlack). Section markers already exist in the file at lines 334/595/703/852/965 — natural split points.
**Scope:** M
**Confidence:** HIGH

### NF-02 — `lib/subscription.ts` at 683 lines
**File:** `web/lib/subscription.ts` — constants (TIER_NAMES, TIER_PRICES), formatters, Stripe client mutations, DB reads/writes, reconciliation.
**Fix sketch:** Extract `lib/subscription/constants.ts`, `lib/subscription/stripe-ops.ts` (upgrade/cancel/uncancel/schedule), `lib/subscription/reconcile.ts`, keep `lib/subscription/index.ts` as the barrel.
**Scope:** M
**Confidence:** HIGH

### NF-03 — `lib/server-data.ts` at 714 lines
**File:** Mixes `'use cache'` wrappers + raw queries + user-overlay helpers per CLAUDE.md's caching pattern. Legitimately complex — split carefully.
**Fix sketch:** Per-entity split (`server-data/events.ts`, `server-data/resources.ts`, `server-data/members.ts`) keeping the cache-tag convention intact.
**Scope:** M
**Confidence:** MEDIUM (unconfirmed internal structure; may reveal non-obvious coupling)

### NF-04 — Other oversized files
| File | Lines | Kind |
|---|---|---|
| `app/(app)/admin/content-updates/[batchId]/BatchDetailClient.tsx` | 1249 | admin UI |
| `app/(app)/admin/courses/[courseId]/lessons/LessonEditorClient.tsx` | 1052 | admin UI |
| `app/(app)/courses/[courseSlug]/[lessonNumber]/LessonViewerClient.tsx` | 1014 | member UI |
| `app/(marketing)/our-leaders/components/LeadersMapLeaflet.tsx` | 897 | marketing UI |
| `app/(app)/dashboard/DashboardClientV2.tsx` | 809 | member UI |
| `app/(app)/admin/membership-health/MembershipHealthClient.tsx` | 795 | admin UI |
| `lib/sync-event-guests.ts` | 794 | cron/integration |
| `app/api/stripe/__tests__/webhook.test.ts` | 784 | test |
| `app/(app)/directory/DirectoryClient.tsx` | 780 | member UI |
| `lib/google-meet.ts` | 740 | integration |
| `app/(app)/admin/AdminDashboardClient.tsx` | 722 | admin UI |
| `prisma/seed-ci.ts` | 703 | seed |
| `app/(app)/admin/slack/SlackLinkingClient.tsx` | 693 | admin UI |
| ...49 more files in the 200-300 warning zone |

All over CLAUDE.md's "mandatory split" threshold (300+). Biggest wins: the admin content-updates + lessons editors + DashboardClientV2.
**Scope:** L across multiple PRs — defer to Phase 2 Builder delegation.
**Confidence:** HIGH

### NF-05 — Dependabot not configured
**File:** `.github/dependabot.yml` missing. API endpoints for vulnerability-alerts return 404 (ambiguous — may mean disabled OR insufficient scope).
**Impact:** CI comment in `ci.yml` line 215 says "Security scanning handled by Dependabot (repo settings)." Either someone disabled it, or it's config-less and using defaults.
**Fix sketch:** Add `.github/dependabot.yml` with weekly npm + github-actions schedules. Also confirm "Dependabot alerts" + "Dependabot security updates" are on at repo settings → Security.
**Scope:** S
**Confidence:** MEDIUM (API 404 doesn't definitively mean disabled)

### NF-06 — ESLint + Biome dual config (vestigial ESLint)
**Files:** `web/.eslintrc.json` + `biome.json` both present. `package.json` has `"lint": "next lint"` (runs ESLint) and `"biome:check": "biome check"` (runs Biome). **CI only runs `biome:check`, not `lint`.** ESLint is vestigial.
**Fix sketch:** Remove `.eslintrc.json`, `eslint-config-next`, `eslint` from devDeps, drop the `lint` npm script. Or if ESLint provides rules Biome doesn't, wire it into CI and keep it — but currently it's inert config and noise.
**Scope:** S
**Confidence:** HIGH

### NF-07 — CLAUDE.md rule overstates "NEVER subscriptions.update()"
**File:** `CLAUDE.md` line 37 ("NEVER use direct updates — breaks cancellation") and critical rule #2 ("NEVER use `subscriptions.update()` for plan changes").
**Impact:** The actual code (`lib/subscription.ts`) uses `subscriptions.update()` **three times** — at lines 265 (upgradeSubscriptionNow, canonical Stripe pattern for immediate price change with proration), 415 (cancelAtPeriodEnd — canonical), 440 (uncancel — canonical). The rule is more nuanced: "never for downgrades" (because cancel_at_period_end state is lost). A future contributor reading CLAUDE.md will either panic or ignore the rule entirely.
**Fix sketch:** Update CLAUDE.md rule 2 to: "NEVER use `subscriptions.update()` for **downgrades or plan migrations away from an active state**. Use Subscription Schedules for these. `subscriptions.update()` is fine for immediate upgrades, cancel/uncancel toggles, and metadata." Point to `lib/subscription.ts` as the reference.
**Scope:** S
**Confidence:** HIGH

### NF-08 — `checkMembershipStatus` swallows all errors as "no access"
**File:** `web/lib/auth.ts:117-121`
```ts
} catch (error) {
  console.error('Error checking database membership:', error);
  return false;
}
```
**Impact:** DB timeout, connection pool exhaustion, transient Prisma error → user denied access with no alarm. The fallback on line 162 (Clerk metadata) catches this for authenticated users with `hasActiveMembership: true` set, so real impact is lower, but a full DB outage = invisible access denial to everyone whose Clerk cache is stale.
**Fix sketch:** Distinguish "no membership found" (return false) from "error checking" (throw, let caller decide). At minimum, fire a Sentry alert on catch. Requires MF-04 to be useful.
**Scope:** S
**Confidence:** HIGH

### NF-09 — `fetchWithAuth` in `server-auth.ts` calls own API via HTTP
**File:** `web/lib/server-auth.ts:41-63`
**Impact:** Server component calls its own `/api/*` endpoint via HTTP with a Bearer token. Extra serialization round-trip, extra failure mode (DNS, timeout), extra TLS handshake on cold start. Direct function call would be simpler and faster.
**Fix sketch:** Find callers of `fetchWithAuth` and replace with direct imports of the underlying service function. If the Clerk token propagation is genuinely needed, document why.
**Scope:** M (dependent on caller count — not audited yet)
**Confidence:** MEDIUM (usage pattern unverified)

### NF-10 — Agent Anthropic SDK is ~5 versions behind
**Files:** `packages/course-update-agent/package.json` + `packages/website-agent/package.json` both pin `@anthropic-ai/sdk: ^0.39.0`. Current is 0.50+. Missing improvements: extended thinking, prompt caching, tool use refinements.
**Fix sketch:** Bump to latest in both packages, rebuild agent containers, verify monthly cron runs still succeed. Confirm API surface changes (particularly around tool use and messages) don't break the agents.
**Scope:** S+test
**Confidence:** HIGH

### NF-11 — website-content-agent has `contents: write` + `pull-requests: write`
**File:** `.github/workflows/website-content-agent.yml`
**Impact:** Monthly cron bot can create PRs that modify any file. Currently fine because CODEOWNERS would gate — except MF-01 means CODEOWNERS doesn't actually block. Low likelihood of compromise (runs Anthropic SDK monthly against your own data), but high blast radius if it ever is.
**Fix sketch:** Once MF-01 is fixed, this is acceptable (Helen reviews). Alternatively, scope token to a specific path (e.g., `content/`) via a fine-grained deploy key. Lower priority than fixing MF-01.
**Scope:** blocked by MF-01
**Confidence:** HIGH

### NF-12 — `CohortRsvp` model: 2 relations, 1 index (N+1 risk)
**File:** `web/prisma/schema.prisma` — `CohortRsvp` has two `@relation` declarations but only one `@@index`. The unindexed FK will seq-scan on joins.
**Impact:** Scales linearly with cohort size. For a cohort of 200 members, currently imperceptible; at 2000+ it'll show up in query plans.
**Fix sketch:** Add `@@index([<second-fk-field>])` or composite index covering both relations depending on query patterns.
**Scope:** S (one migration)
**Confidence:** MEDIUM (heuristic — needs query plan check)

### NF-13 — Integration tests advisory in CI (not blocking)
**File:** `.github/workflows/ci.yml` line 166 — `# Advisory while the harness stabilizes — flip to blocking once proven.`
**Impact:** Integration test failures don't block merge. The CI already runs them against a real Postgres — tests that aren't gates are noise.
**Fix sketch:** Once the harness has 2-4 weeks of stable passes, flip to `needs: integration-test` on the `build` job (or remove the advisory status).
**Scope:** S (one workflow edit)
**Confidence:** HIGH

### NF-14 — Tests don't block build in CI
**File:** `.github/workflows/ci.yml` — the `build` job `needs: lint-and-typecheck` only, not `test` or `database-test`.
**Impact:** A PR with failing unit tests but passing types/lint will still report a green build, which satisfies the "Build" required-status-check. Combined with MF-01, a broken PR can merge.
**Fix sketch:** Add `test` and `database-test` to `needs:` on the `build` job. Or add them to the required status checks list on MainProtection directly.
**Scope:** S
**Confidence:** HIGH

### NF-15 — No `npm audit` in CI
**File:** `.github/workflows/ci.yml` has no `npm audit` step.
**Impact:** Supply-chain vulns discovered after a dependency is merged go unnoticed until Dependabot fires (if enabled — see NF-05).
**Fix sketch:** Add `npm audit --audit-level=high` step to `lint-and-typecheck` job (not blocking at first; flip to blocking after baselining).
**Scope:** S
**Confidence:** HIGH

### NF-16 — E2E coverage is thin
**Files:** `web/e2e/smoke.spec.ts` (119 LOC), `web/e2e/accessibility.spec.ts` (307 LOC). No E2E for payment, auth, enrollment, cohort registration, admin flows.
**Impact:** The highest-risk paths (Stripe checkout, Clerk signup→membership, cohort Mailchimp subscribe, admin dashboards) rely entirely on unit tests + manual verification.
**Fix sketch:** Add E2E specs for: (a) full Stripe checkout happy path using Stripe test card, (b) Clerk signup → webhook → DB user creation → membership activation, (c) cohort registration via MailchimpForm (can't verify delivery, but can verify form POST + success UI), (d) admin auth refusal for non-admin user.
**Scope:** L — defer to Phase 2 QA delegation
**Confidence:** HIGH

### NF-17 — Mailchimp cohort registration has no error telemetry
**File:** `web/app/(app)/courses/MailchimpForm.tsx:72-75`
```ts
onSubmit={() => {
  onSubmitted?.();
  setTimeout(() => setSubmitted(true), 500);
}}
```
**Impact:** 500ms setTimeout assumes success. If Mailchimp POST fails (invalid audience, rate limit, network), user sees "Thank you for registering" but nothing happened. No backend visibility. Combined with "cohort registration uses Mailchimp NOT Luma" critical rule, this is load-bearing UX for the live cohort flow.
**Fix sketch:** Wire the hidden iframe's `load` event to distinguish success vs failure. Log Mailchimp responses to Sentry (once MF-04 lands). Optional: mirror the subscribe to a lightweight backend endpoint for DB-side tracking.
**Scope:** M
**Confidence:** HIGH

### NF-18 — Cron header dependency locks deployment to Vercel
**File:** `web/lib/middleware-helpers.ts:30`
```ts
if (headers.get('x-vercel-cron')) return { ok: true };
```
**Impact:** `x-vercel-cron` is stripped from external requests on Vercel infra. If the app is ever migrated off Vercel, cron auth either breaks or (worse) becomes spoofable. Acceptable today; document as a platform dependency.
**Fix sketch:** Add a comment-level ADR entry. Consider dropping the Vercel-header path and requiring `CRON_SECRET` everywhere once you're confident all crons have it set in env.
**Scope:** S (doc) or M (remove header path)
**Confidence:** HIGH

### NF-19 — `migrate-vercel.js` runs on every prod build
**File:** `web/package.json` build script: `node scripts/migrate-vercel.js && prisma generate && next build`
**Impact:** A JS file in `scripts/` (which is lint+type-check excluded per MF-08) runs on every production deploy. Hot churn (15 changes in 6 months). Any bug here = failed deploy. High-criticality code in the least-checked directory.
**Fix sketch:** Move `migrate-vercel.js` out of `scripts/`, rewrite as `.ts`, include in type-check + lint. Unit-test it if logic is non-trivial.
**Scope:** M
**Confidence:** HIGH

---

## Negligible

### NG-01 — Mailchimp honeypot field name hardcodes audience ID
`web/app/(app)/courses/MailchimpForm.tsx:89` — `name="b_2d96a9bbb62cb78204424c6d0_4c064b167f"`. Tightly coupled to the audience referenced in `content/product/courses.ts`. When the audience changes, both break together. **Not worth fixing** — the coupling is inherent to Mailchimp's embed-form contract.

### NG-02 — Cohort dates hardcoded in `content/product/courses.ts`
3x/year cadence means 3 PRs/year to update. Making this DB-driven or CMS-driven adds surface area for a low-frequency change. Keep as code.

### NG-03 — `noExplicitAny` is "warn" not "error" in `biome.json`
With only **6** `any` usages in all of `lib/` + `app/` and **0** `@ts-ignore`, effectively strict. Flipping to error would fail the existing 6; low-value tightening.

### NG-04 — Custom UI primitives vs a component library
`Button`, `Modal`, `DataTable` are custom (CLAUDE.md documents this as intentional). Only `@radix-ui/react-focus-scope` is pulled in. If the design system needs ever grow beyond current primitives, Radix Primitives or Ark UI is the low-friction path. Today, not a gap.

---

## Pre-seed Verification

Some assumptions from the original audit brief turned out stale — documenting so they don't get re-litigated.

| Pre-seed | Reality |
|---|---|
| CODEOWNERS missing or incomplete | **Wrong.** Exists and is thorough (Helen gates Stripe/Prisma/middleware/Clerk webhook/package.json). Issue is enforcement (MF-01). |
| Branch protection not enforced on main | **Nuanced.** Ruleset exists and is active, but configured to not require approvals or CODEOWNERS review (MF-01). |
| No dedicated staging environment | **Wrong.** CLAUDE.md line 907 documents persistent Supabase staging via Vercel PR previews. Staging DB ref saved in Polaris memory: `qfcjtidvmzvppxbkxupk`. |
| Abandoned monorepo migration | **Confirmed** (MF-02). |
| PostHog cleanup pending | **Partially.** 40 distinct events firing across the codebase; looks actively used. Needs dashboard cross-check to identify truly dead events — defer to Phase 2. |
| Analytics CI skill not built | **Confirmed** — no related CI job or skill. Future work. |
| On-call agent not scoped | **Confirmed** — no on-call agent. Related: no Sentry (MF-04). |

---

## Scope

### Covered in Phase 1
- Architecture (module structure, three-Prisma-schema drift, monorepo state)
- Critical paths (Stripe webhook, Clerk webhook, subscription ops, middleware, auth lib, CORS, Mailchimp cohort form)
- Security (CODEOWNERS enforcement, admin auth pattern sample, RLS state, cron auth, signature verification, ruleset config)
- DevOps (CI jobs, branch protection, Dependabot, ruleset config, scripts directory lint gap)
- Data layer (Prisma schema gaps, index coverage, migration tracking, manual SQL file)

### Deferred to Phase 2
- **Duplication scan** (defrag-style across `web/app/components/`, `web/components/`, `web/lib/`) — needs Builder delegation
- **Full file-size scan + split plan** — initial list in NF-04; Builder produces per-file split proposals
- **Dependency audit** — outdated, CVEs, unused, duplicates via `npm outdated`, `npm audit`, `depcheck` — needs Builder
- **Test coverage heatmap** — which critical paths are covered vs not, mock-vs-real analysis in existing unit/integration tests — needs QA
- **E2E reality check** — what `smoke.spec.ts` + `accessibility.spec.ts` actually cover; NF-16 gaps — needs QA
- **Full docs audit** — CLAUDE.md line-by-line vs code, README freshness, ADR gaps beyond MF-06 / NF-07 / NF-18 — standalone pass
- **Performance** — N+1 queries, bundle size, ISR opportunities, query plans for the CohortRsvp index suspicion — needs profiling
- **PostHog live-vs-dead event analysis** — needs dashboard access
- **Rate limiting** on public endpoints (Mailchimp proxy path, any unauthenticated API) — no current gate observed
- **Security headers / CSP** — `next.config.ts` has no `headers()` function; no CSP, HSTS, X-Frame-Options policy observed
- **Secrets rotation posture** — STRIPE_WEBHOOK_SECRET, CRON_SECRET, ANTHROPIC_API_KEY, AGENT_DATABASE_URL — no documented rotation cadence
- **PII-in-logs audit** — 27 `console.error` in Stripe webhook alone, no log redaction surface seen
- **Backup/DR for Supabase** — beyond PR #564's staging refresh, no tested restore procedure documented

---

## Log

- **2026-04-19 (Polaris)** — Phase 1 complete. 9 Must Fix / 19 Nice to Fix / 4 Negligible. MainProtection ruleset misconfiguration + stalled 8-PR backlog identified as top findings. Audit done against local branch `tmp/all-tests-local`; main is substantially weaker — 8 open PRs contain security + reliability fixes (#568 firewall, #569 Stripe race, #571 Clerk cascade) that are passing CI but not merging.
