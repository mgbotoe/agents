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
- **WDAI PR #598 (open):** Brigitte's Mailchimp one-click cohort registration. Review posted 2026-05-09. 2 must-fix findings: (1) /events path doesn't write DB or emit PostHog unlike /courses; (2) route.ts:37-41 swallows Mailchimp errors without checking response.ok. 2 should-fix: hardcoded list-id, missing userHasRsvp in CohortEventCard.
- **WDAI PR #603 (open, ready for review):** `/api/intro/suggest-matches` endpoint — replaces Gumloop+Airtable matcher with live DB. 8 files, 789 lines, 270/270 tests. Vercel env vars + Gumloop wiring NOT yet set (operator task per PR Setup section). 3 secrets exposed in chat during testing — rotate after Gumloop cutover.
- **Infra resolved (2026-05-06):** slack-watcher event-loop drain fixed (keepalive + PowerShell PID check, atomic lock singleton). Watcher running. `run-task.cmd` fixed (full claude.exe path + process-tree kill via commit `4706af0`). All scheduler tasks live.
- **Pending Dina:** (1) `ctx-upgrade` — context-mode v1.0.75 broken (EBUSY); requires closing Claude Code first. (2) `slack-watcher/test-singleton.mjs` — commit or delete decision. (3) gather-context.ps1 disk display shows 0GB instead of 454GB.

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

## Session Log
- [2026-04-13] Agent scaffolded by Atlas. Identity, rules, sub-agents, skills, and config created.
- [2026-04-14] Full workspace tour (18 repos mapped), wiki enriched with technical details, Slack MCP built and connected (DaFudge workspace).
- [2026-04-15] First Atlas→Polaris handoff tested. Read Rebekah/Helen/Madina WDAI call transcript via Granola. Technical roadmap assessed. Pipeline documented in CLAUDE.md. Startup hook added to check wiki for new technical items.
- [2026-04-15] Built and shipped defrag skill for WDAI (PR #560). Evaluated Ramp/Glass post on codebase self-maintenance — defrag was the real gap, rest already covered. Discussed shared project memory for WDAI — decision pending.
- [2026-04-17] Hardened delegation: sub-agents now require CLAUDE.md section citations; Polaris must pre-read target-repo CLAUDE.md before delegating. Two new feedback memories saved (external-repo CLAUDE.md rule, QA delegation scope).
- [2026-04-18→19] 7 consecutive no-op distills confirmed `Polaris\Distill` every-2h @ :12 spawns ghost sessions. Action: short-circuit guard (tracked in agent-ecosystem roadmap P2).
- [2026-04-19] WDAI tech debt audit Phase 1 → `wiki/projects/wdai-tech-debt.md`. Detail in `memory/projects.md`. Atlas pinged on P0s via #atlas-cos.
- [2026-04-19] slack-watcher 6-bug sweep + symmetric inbox polling shipped (commit `9cc35fc`). Postmortem + ADR-005 in `memory/decisions.md`. Pattern win: Atlas drafts → Polaris reviews → Atlas executes, independent-commit discipline.
- [2026-04-19] SessionEnd hook added (`dev-agent/.claude/settings.json`) — daily-log summary + uncommitted-work check. `settings.json` now tracked via `.gitignore` exception.
- [2026-04-19] Polaris→Atlas comm spec rewritten in `wiki/infrastructure.md`: tiered triggers, what NOT to ping, escalation-to-Dina path, explicit not-real-time limitation.
- [2026-04-19] Agent ecosystem roadmap seeded at `wiki/projects/agent-ecosystem.md`. Both agents write. Scope rule: agent infra here, external projects in their own doc.
- [2026-04-20] 03:30 self-improve session drafted skill-side short-circuit guard for `.claude/skills/distill-session/SKILL.md`; write denied twice, needs Dina's explicit approval.
- [2026-04-20→23] Ghost distills #19–35. Auth = Google OAuth Testing-mode (Atlas-side). GCP prod-push + GitHub MCP candidate stacked by Atlas.
- [2026-04-25] OAuth `atlas-493123` published to Production + 6 tokens re-issued; 7-day expiry cycle dead. Distill short-circuit guard shipped (Dina approved).
- [2026-04-27] OpenClaw memory upgrade: `/recall`, decay schtask (180d), `/promote` curation. Shipped to Polaris (`c04eb98`) + ported to Atlas (`4a06002`). Both Decay tasks live Sun pre-dawn.
- [2026-04-27] Personal creative piece w/ Dina (3 iterations, deleted at her request). Tactical: `gemini-image-gen` skill model name stale; use `imagen-4.0-generate-001` direct.
- [2026-04-29→05-02] Ghost distills only (10 spawns across 5 days). Short-circuit guard working as designed.
- [2026-05-05] Watcher chaos day resolved across multiple sessions: 7 duplicate instances, gather-context detection fixed, singleton guard overhauled (atomic lock + EPERM fix, commits `0b81411`/`b15520f`). mailchimp-cc PR #16 reviewed + fixed (commit `01f23ad`, local only, push blocked read-only). `run-task.cmd` process-tree kill fix shipped (`4706af0`). accessibility-audit skill + PR #600 shipped. Pending Dina: ctx-upgrade (EBUSY), test-singleton.mjs commit/delete, gather-context.ps1 disk 0GB bug.
- [2026-05-06] Watcher root cause fixed: event loop drain + WebSocket mid-reconnect. Fixes: keepalive, PowerShell-based `isLiveWatcher`, atomic lock file. gather-context.ps1 WMI check fixed. Watcher stable.
- [2026-05-07] Migrated agent automation off local Task Scheduler to GitHub Actions cloud cron. Killed 20 scheduled tasks, all hooks, slack-watcher autostart. Built `bin/promote.py` + `promote.yml` (daily 07:00 UTC), `bin/discuss.py` + `discuss.yml` (nightly 10:00 UTC). Re-added safe SessionStart/SessionEnd hooks (Python only). Separated SAMESF into own repo `mgbotoe/same-sf-content-platform`.
- [2026-05-09] Reviewed WDAI PR #598 (Brigitte's Mailchimp one-click cohort registration, +560/-348). Posted review comment with 2 must-fix + 2 should-fix findings. Pressure-tested via advisor before posting — retracted M1 hydration flag, downgraded H3.
- [2026-05-11] WDAI PR #603 ready for review: `/api/intro/suggest-matches` endpoint replaces stale Gumloop+Airtable matcher with live DB; iterated v1→v2→v3→Path B over the session, final state 8 files / 789 lines / 270 tests passing. Vercel env vars + Gumloop wiring pending (operator task).
- [2026-05-19→20] Self-awareness instrumentation layer shipped: delegation-scope warning hook, daily-log commit logger (multi-repo), lite session-snapshot on SessionEnd+PreCompact, prior-art surveying for substantive decisions (with honest-framing fix per advisor critique). 6 commits to agents repo.
