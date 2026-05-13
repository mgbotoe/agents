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

<!-- added 2026-04-19 -->
## ADR-005: Symmetric inbox polling for Polaris↔Atlas
- **Date:** 2026-04-19
- **Decision:** Polaris polls `#atlas-cos` since `.claude/runtime/atlas-last-seen.ts` watermark on session start (and via heartbeat skill), updates watermark to newest ts after read. Mirrors Atlas's existing `polaris-last-seen.ts` pattern.
- **Context:** Slack-watcher self-filters bot replies to prevent loops. Side effect: Polaris→Atlas messages are real-time (Atlas reads next spawn), but Atlas→Polaris in `#atlas-cos` never spawns Polaris because the watcher filters its own bot. Asymmetric — Polaris was missing Atlas replies until next manual session.
- **Rationale:** Watcher-based real-time delivery would require lifting the self-filter, risking loops (we just patched one). Watermark polling is cheap, deterministic, and self-bootstraps when the file is missing. Same pattern Atlas already uses, so the system stays symmetric.
- **Trade-offs:** Not real-time — Polaris sees Atlas replies on next spawn (heartbeat or session start). Acceptable: most Polaris↔Atlas comms are operational coordination, not chat.
- **Implementation:** commit `9cc35fc`. Heartbeat skill + SessionStart hook both consult the watermark.

<!-- added 2026-04-19 -->
## Postmortem: slack-watcher 6-bug fix sweep
- **Date:** 2026-04-19
- **Summary:** Watcher had been silently dead ~25h; six independent bugs surfaced during repair. Each fix landed as an independent revertable commit on `fix/watcher-self-loop`.
- **Bugs and fixes:**
  1. **No supervisor** — process died with no restart. Fix: `watcher.cmd` restart loop (10s backoff, clean exit on 0) + `~/Startup/slack-watcher.cmd` for logon auto-launch. Process-level `uncaughtException`/`unhandledRejection`/SIGINT/SIGTERM + SocketMode lifecycle handlers added.
  2. **Dead bot_message handler** — `watcher.mjs:219` filtered all `event.bot_id`. Relaxed to `event.user === botUserId` so cross-agent messages reach the handler.
  3. **Windows ENOENT on `claude`** — `spawn("claude")` doesn't resolve PATHEXT. Fix: platform-conditional `CLAUDE_BIN` (`claude.cmd` on Windows).
  4. **Single-token identity collapse** — single `SLACK_BOT_TOKEN` posted all replies as polaris-bot, hiding Atlas's identity. Fix: per-agent `botTokenEnv` in `config.json`, separate `WebClient` per channel, `SLACK_BOT_TOKEN_ATLAS` + `SLACK_BOT_TOKEN_POLARIS` in `.env`.
  5. **`shell: true` argv prompt corruption** — Node joined unquoted args, cmd.exe word-split, `-p` grabbed only first word. Fix: pipe prompt via stdin (`stdio: ["pipe", "pipe", "pipe"]`); claude CLI reads from stdin when no arg given.
  6. **Self-loop after per-agent tokens** — different bot users meant `event.user === botUserId` no longer caught own-agent replies; #atlas-cos exploded into 9 replies to one "hey." Atlas pinged me via Slack with diff; I corrected patch location to the `bot_message` block; Atlas applied + pushed `8e795fc`: `if (source.name === agentCfg.label) return;`.
- **Process win:** Cross-agent collaboration pattern held — Atlas surfaced + drafted, Polaris reviewed + corrected, Atlas executed. Independent-commit discipline preserved revertability.
- **Architecture note:** Polaris→Atlas via `slack_send` is **not real-time by design**. Only Dina→agent and Atlas→Polaris (via atlas-bot in #polaris-tl) are real-time via watcher. See ADR-005 for the polling mitigation in the other direction.

<!-- promoted 2026-04-20 -->
## ADR-006: Distill short-circuit guard — skill-side, not scheduler-side
- **Date:** 2026-04-20 (proposed; awaiting Dina's approval to land)
- **Decision:** Prepend a mandatory short-circuit to `.claude/skills/distill-session/SKILL.md`. When the session has no substantive tool calls preceding the skill invocation (startup hooks don't count), exit with a single-line `No-op session — nothing to distill.` and do not write a daily-log entry.
- **Context:** `Polaris\Distill` runs every 2h @ :12 via Windows Task Scheduler with `WakeToRun` + `StartWhenAvailable`. Fresh session spawns with no user prompt, skill fires, writes boilerplate entry. 18 consecutive ghost sessions confirmed (2026-04-18 19:00 → 2026-04-20 22:12). Daily logs bloat with stubs; hot memory Session Log balloons with near-identical lines (had to consolidate 11 of them this /promote pass).
- **Rationale for skill-side over scheduler-side:**
  - Skill-side is self-contained; one file edit, no Windows Task Scheduler knowledge required to revert.
  - Scheduler-side (short-circuit in `bin/scheduled/run-task.cmd` or task XML) requires inspecting "has there been activity since last distill" from outside the agent — race-prone, needs a sentinel file, couples scheduler to memory layout.
  - Skill-side also covers ghost sessions spawned by any *other* cause (e.g. manual `/distill-session` in an empty shell), not just scheduler.
- **Trade-offs:** Skill self-exit is detectable only by absence-of-entry in daily logs — no observability on how many ghosts were suppressed. Acceptable; the scheduler task log already timestamps every invocation. If data on suppression count matters later, emit a counter to `.claude/runtime/ghost-count.txt`.
- **Blocked on:** Edit to `.claude/skills/distill-session/SKILL.md` requires Dina's explicit approval (write denied twice on 2026-04-20). Next real session, ask before re-proposing.
- **Follow-ups when landed:** Drop the Active Work line from `identity/memory.md`; mark `wiki/projects/agent-ecosystem.md` P2 item done; watch next 24h of `scheduled-tasks.log` to confirm no-op distills emit nothing.

<!-- added 2026-05-11 -->
## ADR-007: intro-matcher — Gumloop owns LLM, WDAI is data-only (PR #603)
- **Date:** 2026-05-11
- **Decision:** `/api/intro/suggest-matches` endpoint returns raw DB candidates; Gumloop retains the trigger, LLM matching brain, Anthropic billing, and Slack posting. WDAI's role is "smarter Airtable view."
- **Context:** Iterated through 4 architectures: v1 inline portal hook (coverage regression) → v2 in-house cron (Vercel cron preview-only blocker) → v3 WDAI calls Anthropic directly → Path B endpoint (Gumloop owns LLM). Each pivot surfaced a concrete blocker.
- **Rationale:** Third-party dep retained, but matching brain + Anthropic billing stay where they already worked. Keeps WDAI API surface narrow. Dropped `@anthropic-ai/sdk`, Sentry F4 opt-out, `findMatches`/`runIntroMatcher` from WDAI entirely.
- **CAS columns kept:** `slackMatchPostedAt` + `matchingOptOut` retained despite YAGNI pressure — follow-up PRs (opt-out UI, backfill cron) will use them.
- **Operator tasks pending:** Vercel env vars (`MATCHER_API_SECRET`, `INTRO_MATCHER_ENABLED=true`) + Gumloop duplicate flow wiring. 3 secrets exposed in chat during testing — rotate after Gumloop cutover.
