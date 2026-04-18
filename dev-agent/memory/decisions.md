# Decisions — Cold Memory

Key technical decisions with reasoning. Includes ADRs and architecture choices.

<!-- This file will be populated as Polaris makes decisions -->

## ADR-001: Agent Architecture — Polaris as Tech Lead
- **Date:** 2026-04-13
- **Decision:** Polaris runs as a tech lead orchestrating 3 sub-agents (Builder/Sonnet, Designer/Sonnet, QA/Sonnet) rather than a single monolithic dev agent.
- **Context:** Needed a dev agent that covers the full SDLC. Single-agent approach would overload context with conflicting concerns.
- **Rationale:** Mirrors real eng team structure. Tech lead makes decisions, delegates execution, reviews output. Sub-agents stay focused on their domain.
- **Trade-offs:** More overhead per delegation (context transfer cost), but better quality through separation of concerns and independent review.

<!-- added 2026-04-17 -->
## ADR-002: WDAI cohort RSVP state — UI state cache, not registration record
- **Date:** 2026-04-17
- **Decision:** `cohort_rsvps` table is a **UI state cache** answering "should the button read RSVP'd?" — Mailchimp remains canonical source for actual registrations.
- **Context:** WDAI's cohort RSVP button state was client-only; reloading the page reverted RSVP'd users to "Join the Live Cohort." Product doc conflated UI persistence with shadow-registration architecture.
- **Rationale:** Separation of concerns. Registration logic stays at Mailchimp (source of truth). UI cache is cheap to maintain, doesn't try to sync with Mailchimp, degrades gracefully if the row is missing (shows "Join" — conservative default).
- **Key design:**
  - Unique key: `(user_id, course_id, cohort_date)` — cohort date in the PK so content-file date changes naturally orphan old rows (no cleanup cron needed).
  - Optimistic write on form submit (not webhook). Mailchimp posts to a hidden iframe; no JS callback on actual success. Webhook infra not justified for UI cache.
  - No RLS — matches the rest of the app (application-layer auth via Clerk).
  - `cohort_end_date` added as optional prep for future Lauren-owned admin portal. Content file `marketing.cohortEndDate` populated when program leads schedule cohorts.
- **Trade-offs:** Possible false positives if Mailchimp rejects the email (invalid format, duplicate). Acceptable — user sees missing confirmation email, can resubmit. Cost of a webhook listener outweighs correctness benefit at current scale.

<!-- added 2026-04-17 -->
## ADR-003: Staging refresh pipeline — scripts + GH Actions, V1 no anonymization
- **Date:** 2026-04-17
- **Decision:** Weekly prod→staging data sync via 3 discrete shell scripts (`dump`/`transform`/`restore`) orchestrated by a GitHub Actions workflow. V1 copies raw prod data; V2 (deferred) adds PII anonymization.
- **Context:** WDAI staging DB had drifted from prod for months — continuous PR-preview test writes with no refresh mechanism. Planned GitHub Action from `docs/plans/test-staging-setup.md` was aspirational, not implemented.
- **Rationale:**
  - Three-script pipeline makes V2 anonymization a slot-in replacement for `transform.sh` — no orchestration rewrites.
  - Hand-crafted migration files (bypassing `prisma migrate dev`) sidestep an existing broken shadow-DB migration in the repo history.
  - 4-layer access defense (repo write access + branch protection + read-only prod role + layer-1-gates-layer-4-runs) instead of GitHub Environment protection (which breaks on `schedule` triggers).
  - `StagingMeta` single-row observability table + `/api/staging-status` endpoint give at-a-glance freshness signal.
  - Pre-flight validation script runs 7 checks on manual triggers before any real work (disk, pg17 client, RO role permissions probe, prisma migration prefix-alignment).
  - `FAILED_DIRTY` state marker + 7-day rollback snapshot artifact for mid-flight failure recovery.
- **V2 deferral triggers (any one):** staging access broadened beyond core team, breach/near-miss, compliance review, user count > 500, new vendor integration.
- **Rejected alternatives:**
  - Supabase PITR clone — restores to a new project URL, would require weekly re-pointing across Vercel/Clerk/Stripe integrations. Worse operationally.
  - Per-table COPY loop — YAGNI. FK ordering + enum sync complexity not justified for weekly refresh.
  - Neon branching — explicitly punted per existing `docs/plans/test-staging-setup.md`; revisit when multiple maintainers regularly ship competing migrations.

<!-- added 2026-04-17 -->
## ADR-004: Sub-agent CLAUDE.md citation — instrumentation over trust
- **Date:** 2026-04-17
- **Decision:** Builder/Designer/QA sub-agent definitions require a `**CLAUDE.md sections read:**` field in their report-back citing specific section headings from the target repo's CLAUDE.md. Missing citation = task bounced.
- **Context:** Mid-session, Builder shipped code to WDAI without reading WDAI's CLAUDE.md end-to-end — missed explicit rules (Updating Seed File, Testing mocking patterns, PostHog event conventions). Only surfaced at code review, required rework commit.
- **Rationale:** Sub-agent definitions already said "read CLAUDE.md first" but there was no audit trail, so the skip went undetected. Instrumentation creates a verifiable signal; two independent reads (Polaris pre-delegation + sub-agent execution) is the defense.
- **Polaris's own obligation:** `.claude/rules/domain.md` now requires Polaris to read target-repo CLAUDE.md end-to-end BEFORE delegating, and cite applicable sections in the delegation prompt. Pre-filters the sub-agent's map rather than making them discover blind.
- **Trade-offs:** Adds a formal field to every sub-agent report. Small friction. Pays for itself on the first prevented rework.
