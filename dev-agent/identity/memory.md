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
