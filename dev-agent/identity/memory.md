# Hot Memory

Always loaded into context. Keep under 2500 tokens.
Detailed context lives in `memory/*.md` — search on-demand, don't duplicate here.

## Current State
- Polaris is a freshly scaffolded dev agent (tech lead role)
- Runs on Opus, delegates to sub-agents (Builder, Designer, QA) on Sonnet
- General purpose — works across all of Dina's repos (personal, business, WDAI, agents)
- Sister agent: Atlas (chief of staff) at `C:\Workspace\agents\chief-of-staff\`

## Active Work
- **WDAI roadmap (open):** branch protection, CODEOWNERS, PostHog cleanup, staging env, analytics CI skill, on-call agent. Phase 2 of tech-debt audit deferred — needs Builder + QA in fresh session. Detail: `wiki/projects/wdai-tech-debt.md`.
- **Open question:** shared project memory for WDAI contributors — decision still pending from 2026-04-15.
- **Decay scripts (Polaris + Atlas):** registered Sun 04:00/04:15. First real archival run will be ~Oct 2026 once 180-day cutoff bites — verify on first non-empty run.
- **CineVault redesign:** roadmap at `C:\Workspace\Personal Projects\media-theater\docs\redesign\roadmap.md` is source of truth.
- **mailchimp-cc PR #16 (open):** Reviewed Helen's dark mode fix. Two bugs found and fixed on branch `fix-dark-mode-email-rendering` (commit `01f23ad`, local only). Review comment posted at https://github.com/WomenDefiningAI/mailchimp-cc/pull/16#issuecomment-4384163416. Push blocked — mgbotoe is read-only on WomenDefiningAI/mailchimp-cc. Helen needs to apply fixes or Dina needs collaborator access.
- **Infra resolved (2026-05-06):** slack-watcher event-loop drain fixed (keepalive + PowerShell PID check). Watcher running, singleton guard stable. `run-task.cmd` fixed (full claude.exe path). All scheduler tasks live.
- **Watcher singleton fix committed (2026-05-05):** `fix(watcher): robust singleton guard` — commit `0b81411`. Uses `tasklist` to verify PID on Windows EPERM (signal-0 throws EPERM for both live+recycled-to-system PIDs). Watcher now correctly self-terminates on duplicate start. PID 95856 live, machine clean.

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

## Standing Rules

- **Heartbeat loop:** At the START of every session, immediately run `/loop 30m /heartbeat`. Mandatory — not optional, not "when remembered". Do it before any other work.

## Session Log
- [2026-04-13] Agent scaffolded by Atlas. Identity, rules, sub-agents, skills, and config created.
- [2026-04-14] Full workspace tour (18 repos mapped), wiki enriched with technical details, Slack MCP built and connected (DaFudge workspace).
- [2026-04-15] First Atlas→Polaris handoff tested. Read Rebekah/Helen/Madina WDAI call transcript via Granola. Technical roadmap assessed. Pipeline documented in CLAUDE.md. Startup hook added to check wiki for new technical items.
- [2026-04-15] Built and shipped defrag skill for WDAI (PR #560). Evaluated Ramp/Glass post on codebase self-maintenance — defrag was the real gap, rest already covered. Discussed shared project memory for WDAI — decision pending.
- [2026-04-17] Hardened delegation: sub-agents now require CLAUDE.md section citations; Polaris must pre-read target-repo CLAUDE.md before delegating. Two new feedback memories saved (external-repo CLAUDE.md rule, QA delegation scope).
- [2026-04-18→19] 7 consecutive no-op distills confirmed `Polaris\Distill` every-2h @ :12 spawns ghost sessions. Action: short-circuit guard (tracked in agent-ecosystem roadmap P2).
- [2026-04-19] WDAI tech debt audit Phase 1 → `wiki/projects/wdai-tech-debt.md`. Detail in `memory/projects.md`. Atlas pinged on P0s via #atlas-cos.
- [2026-04-19] slack-watcher 6-bug sweep + symmetric inbox polling shipped (commit `9cc35fc`). Postmortem + ADR-005 in `memory/decisions.md`. Pattern win: Atlas drafts → Polaris reviews → Atlas executes, independent-commit discipline.
- [2026-05-05] accessibility-audit skill built (WCAG 2.2 AA, 7 phases) + PR #600 in WDAI. Watcher singleton guard overhauled (two-layer: atomic lock + wmic PID verify, commit `b15520f`). 99 claude.exe = MCP orphans from scheduled tasks.
- [2026-04-19] SessionEnd hook added (`dev-agent/.claude/settings.json`) — daily-log summary + uncommitted-work check. `settings.json` now tracked via `.gitignore` exception.
- [2026-04-19] Polaris→Atlas comm spec rewritten in `wiki/infrastructure.md`: tiered triggers, what NOT to ping, escalation-to-Dina path, explicit not-real-time limitation.
- [2026-04-19] Agent ecosystem roadmap seeded at `wiki/projects/agent-ecosystem.md`. Both agents write. Scope rule: agent infra here, external projects in their own doc.
- [2026-04-20] Startup inbox check only — Polaris→Atlas real-time confirmed live post-watcher fix (PID 378152 on `4564724`). No new technical pings.
- [2026-04-20] 03:30 self-improve session drafted skill-side short-circuit guard for `.claude/skills/distill-session/SKILL.md`; write denied twice, needs Dina's explicit approval.
- [2026-04-20] 02:12–22:12 scheduler = 11 more ghost distills (18 consecutive since 04-18). No inbox movement worth acting on; Atlas flagged Gmail/GCal `invalid_grant` at 16:12 but routing stayed with Atlas, no `#polaris-tl` ping.
- [2026-04-21] Ghost distills #19–28 (00:12–18:12). Auth = Google OAuth Testing-mode (Atlas-side re-auth, not code). GCP prod-push + GitHub MCP candidate Polaris asks stacked by Atlas.
- [2026-04-23] Ghost distills #29–35 (09:12–23:12). Atlas Day 4 blind on Google auth; permanent fix drafted; short-circuit guard pending Dina (later shipped 04-25).
- [2026-04-25] OAuth `atlas-493123` published to Production + 6 tokens re-issued; 7-day expiry cycle dead. Distill short-circuit guard shipped (Dina approved).
- [2026-04-27] OpenClaw memory upgrade: `/recall`, decay schtask (180d), `/promote` curation. Shipped to Polaris (`c04eb98`) + ported to Atlas (`4a06002`). Both Decay tasks live Sun pre-dawn.
- [2026-04-27] Personal creative piece w/ Dina (3 iterations, deleted at her request). Tactical: `gemini-image-gen` skill model name stale; use `imagen-4.0-generate-001` direct.
- [2026-04-29→05-02] Ghost distills only (10 spawns across 5 days). Short-circuit guard (shipped 04-25) emits one-line `no-op — scheduler spawn` entries — working as designed.
- [2026-05-05] Reviewed mailchimp-cc PR #16 (Helen's dark mode fix). Found P2 + P1 bugs, fixes on branch `fix-dark-mode-email-rendering` (commit `01f23ad`, local). Push blocked — read-only on org. Restarted slack-watcher (multiple attempts; final: PID 102332 via .NET detached spawn). Promote + Distill were genuinely missing — re-registered. `run-task.cmd` fixed with full `claude.exe` path (Task Scheduler PATH issue). Tasks were failing silently since ~May 4.
- [2026-05-05] Heartbeat: found 7 duplicate watcher.mjs instances running; notified Dina. Gather-context detection broken (false NOT RUNNING). Watcher needs cleanup.
- [2026-05-05] Session startup: watcher EPERM fix confirmed committed (`0b81411` by Atlas). context-mode v1.0.75 broken (missing bindings). Node count 387, watcher live PID 95856.
- [2026-05-05] Session startup: watcher RUNNING (PID 74940), Polaris\Heartbeat task missing, context-mode still broken. DM sent to Dina on both.
- [2026-05-06] Watcher root cause fixed: event loop drain when all sessions resolve + WebSocket mid-reconnect. Fixes: `setInterval` keepalive, PowerShell-based `isLiveWatcher` (wmic deprecated on Win11), atomic lock file singleton guard. Three commits auto-applied by linter (`0b81411`, `30aee63`, `b15520f`). gather-context.ps1 WMI check fixed (was using Get-Process which misses nvm4w node.exe). Watcher stable, PID confirmed in watcher.pid.
