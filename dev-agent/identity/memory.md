# Hot Memory

Always loaded into context. Keep under 2500 tokens.
Detailed context lives in `memory/*.md` — search on-demand, don't duplicate here.

## Current State
- Polaris is a freshly scaffolded dev agent (tech lead role)
- Runs on Opus, delegates to sub-agents (Builder, Designer, QA) on Sonnet
- General purpose — works across all of Dina's repos (personal, business, WDAI, agents)
- Sister agent: Atlas (chief of staff) at `C:\Workspace\agents\chief-of-staff\`

## Active Work
- [2026-04-15] WDAI technical roadmap — from Rebekah/Helen/Madina call. Items: branch protection, CODEOWNERS, PostHog cleanup, staging env, analytics CI skill, on-call agent.
- [2026-04-15] Atlas→Polaris transcript pipeline validated and documented.
- [2026-04-15] Shipped defrag skill for WDAI — PR #560 assigned to Helen. Scans for duplicated components, inconsistent patterns, dead code, shared logic opportunities. Verifies findings before presenting, requires confirmation before fixing.
- [2026-04-15] Open question: shared project memory for WDAI contributors. Decision pending.
- [2026-04-15] Built heartbeat skill + gather-context.ps1 (adapted from unclaw). Running as /loop 30m in active sessions.
- [2026-04-15] Updated all sub-agents (Builder, Designer, QA): CLAUDE.md-first, workspace awareness, structured report-back formats.
- [2026-04-15] Staggered scheduled tasks 15-30 min after Atlas. Enabled WakeToRun + StartWhenAvailable on all four.
- [2026-04-15] Added startup hooks: Slack inbox check, memory staleness warning, notification sound.
- [2026-04-17] Instrumented sub-agents: all three (Builder/Designer/QA) now require `**CLAUDE.md sections read:**` in report-back. Missing citation = task bounced. Polaris's own rule: must read target-repo CLAUDE.md before delegating.

## Key Facts
- Slack: DaFudge workspace, channel C0ASYTE8PB4 (polaris-slack MCP, `slack_dm_owner` shortcut) — full read/write working
- Discord: #polaris (1493421025881493636) — shared bot with Atlas, can't run simultaneously
- Sub-agents: Builder (sonnet), Designer (sonnet), QA (sonnet)
- No GDrive/Gmail/GCal access — that's Atlas's domain
- Code tools only: context-mode, Playwright, gh CLI
- Granola MCP: available via claude.ai account — can pull meeting transcripts directly
- WDAI team is all non-developers/vibecoders — CI gates + smoke testing + defrag are the safety net
- Helen's GitHub username: helenlkupp (not helenkupp)
- UnClaw (github.com/shahshrey/unclaw) — same architecture as Polaris. Useful reference, not doing anything we don't already do.
- WDAI local dev DB: Docker Postgres on `localhost:5433`, seed via `bash ./scripts/db-local.sh reset` (from `web/`). `.env.local` should point at `postgresql://postgres:postgres@localhost:5433/wdai_local`.
- WDAI staging DB: Supabase project ref `qfcjtidvmzvppxbkxupk` (us-east-2 pooler). Per their CLAUDE.md, staging migrations normally go through Vercel preview. Staging creds kept at `web/.env.local.staging` (gitignored) for deliberate swap-in.
- WDAI Prisma client + Windows: `pnpm db:generate` fails with EPERM DLL lock if dev server is running. Stop server first. `npm run db:local:reset` uses a bash script that PowerShell can't invoke directly — run `bash ./scripts/db-local.sh reset` instead.

## Atlas → Polaris Pipeline
- Atlas monitors WDAI meetings hourly via MeetingPrep (7 AM–3 PM)
- Writes summaries to `wiki/sources/` with `routing:` and `granola_id:` in frontmatter
- Technical items get pinged to #polaris-tl; Polaris checks wiki on startup for new items
- Polaris pulls full Granola transcripts for own technical assessment — never relies on Atlas's summary for technical judgment

## Session Log
- [2026-04-13] Agent scaffolded by Atlas. Identity, rules, sub-agents, skills, and config created.
- [2026-04-14] Full workspace tour (18 repos mapped), wiki enriched with technical details, Slack MCP built and connected (DaFudge workspace).
- [2026-04-15] First Atlas→Polaris handoff tested. Read Rebekah/Helen/Madina WDAI call transcript via Granola. Technical roadmap assessed. Pipeline documented in CLAUDE.md. Startup hook added to check wiki for new technical items.
- [2026-04-15] Built and shipped defrag skill for WDAI (PR #560). Evaluated Ramp/Glass post on codebase self-maintenance — defrag was the real gap, rest already covered. Discussed shared project memory for WDAI — decision pending.
- [2026-04-17] Hardened delegation: sub-agents now require CLAUDE.md section citations; Polaris must pre-read target-repo CLAUDE.md before delegating. Two new feedback memories saved (external-repo CLAUDE.md rule, QA delegation scope).
- [2026-04-18→19] Six consecutive no-op distill sessions (04-18 19:00, 20:12; 04-19 12:12, 14:12, 16:12, 18:12). `Polaris\Distill` every-2h trigger at :12 confirmed — **next real session: ship short-circuit guard in distill skill**.
- [2026-04-19] CineVault redesign roadmap persisted at `C:\Workspace\Personal Projects\media-theater\docs\redesign\roadmap.md` — source of truth for what's next (spotlight B, button primitive, Trakt CTA, YIR conform, vote/convince, share review, error parity, audit infra, a11y). Check there before recomputing from session memory or git log.
- [2026-04-19] WDAI tech debt audit Phase 1 done → `wiki/projects/wdai-tech-debt.md`. 9 Must Fix / 19 Nice / 4 Negligible. Two P0s: MainProtection ruleset allows 0-approval merges + 8-PR backlog stalled (incl. #569 Stripe race fix). Atlas pinged via #atlas-cos. Phase 2 deferred (duplication, file-size, deps, test coverage, docs, rate limiting, CSP, secrets rotation, PII logs, backup/DR) — needs Builder + QA delegation in a fresh session.
- [2026-04-19] **slack-watcher fixed (3 bugs).** (1) Process had died ~25h earlier, no supervisor → added `watcher.cmd` restart loop (10s backoff, clean stop on exit 0) + `~/Startup/slack-watcher.cmd` for logon auto-launch. `schtasks /create /tn Agents\SlackWatcher` failed Access Denied, needs elevation. Added process-level `uncaughtException`/`unhandledRejection`/SIGINT/SIGTERM + SocketMode lifecycle (`error`/`disconnected`/`reconnecting`/`connected`) handlers. (2) `watcher.mjs:219` filtered ALL `event.bot_id`, making the cross-agent `bot_message` handler dead code — relaxed to only `event.user === botUserId` (self-loop guard). (3) `spawn("claude", ...)` on Windows fails with ENOENT because Node doesn't resolve PATHEXT → `claude` is actually `claude.cmd`. Fix: platform-conditional `CLAUDE_BIN = process.platform === "win32" ? "claude.cmd" : "claude"`. The process-handler addition was critical — without it, bug #3 would have died silently and the watcher would have looked "alive but mute." Stale `~/Startup/atlas-discord-watcher.cmd` deleted. **Architecture note:** Polaris→Atlas via slack_send is NOT real-time by design — Atlas reads #atlas-cos via SessionStart `slack_read` hook. Only Dina→agent and Atlas→Polaris (atlas-bot posts #polaris-tl) are real-time via watcher.
