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
- **Decay scripts (Polaris + Atlas):** now cloud cron (`decay.yml`). First real archival run ~Oct 2026 once 180-day cutoff bites.
- **CineVault redesign:** roadmap at `C:\Workspace\Personal Projects\media-theater\docs\redesign\roadmap.md` is source of truth.
- **mailchimp-cc PR #16 (open):** Reviewed Helen's dark mode fix. Two bugs found and fixed on branch `fix-dark-mode-email-rendering` (commit `01f23ad`, local only). Push blocked — mgbotoe is read-only on WomenDefiningAI/mailchimp-cc.
- **WDAI PR #598 (open):** Brigitte's Mailchimp one-click cohort registration. Review posted 2026-05-09. 2 must-fix: (1) /events path doesn't write DB or emit PostHog unlike /courses; (2) route.ts:37-41 swallows Mailchimp errors without checking response.ok.
- **WDAI PR #603 (open, MERGE-READY, Helen tagged 2026-06-11):** `/api/intro/suggest-matches` — replaces Gumloop+Airtable matcher with live DB. Contract: `slackUserId` OPTIONAL + endpoint accepts `text/plain` body. Security advisor: GO. 375 tests, CI green (`8b59e45`). Gumloop flow REBUILT. **Cutover pending:** merge → set PROD env vars → Gumloop URL→prod + drop bypass header + channels automation-test→intros → disable original flow. Dina TODO: delete test intro + bot replies from #intros; confirm rotated secret.
- **WDAI Compound Engineering (active):** PR #689 (docs-only, 6 commits) — CE plugin adoption + ADR-003 + CLAUDE.md coexistence routing table. Open: (1) admin must mark `Check for destructive migrations` as required CI check; (2) fast-follow: AGENTS.md `docs/solutions/` pointer once ce-compound runs; (3) cross-tool CE optional per-machine.
- **WDAI team-OS (active):** PRs #4, #11 pending review. PR #4 (ADR-0007) awaiting Helen ack + has conflicts. PR #11 (Section 5 Linear refresh + 4 doc-gap fixes) clean, ready. ~25 C-series rows still tribal knowledge. C4 admin access doc NOT yet drafted (highest SPOF priority). C47 update-current-state skill = build to self-sustain. READ `memory/project_team_os_one_brain.md` before any team-OS architecture decision.
- **Team OS Beacon (POC):** WDAI Slack app built, installed, round-trip DM tested. PR #9 merged. `wdai-slack` MCP wired in `dev-agent/.mcp.json` (needs session restart). Tokens in Windows Credential Manager (`wdai-slack` service).
- **Cross-platform port (branch `chore/cross-platform-agnostic`, not yet merged):** OS-agnostic path derivation, gather-context.py (fixes 0GB disk bug), cloud cron for decay/self-improve (PR-gated), heartbeat→/loop watchdog, per-machine workspace map via `_workspace.py` + gitignored `workspace.local.json`. Extracted custom-skills → private `mgbotoe/claude-skills` marketplace + `mgbotoe/my.claude` (683→29 tracked files). `sync-skills.py` SessionStart hook (self-healing marketplace pulls). `/advisor` skill (fork-based — NOT wired to council yet; flag for Dina). `bin/scan-paths.py` + `port-guard.yml` CI path-leak guard. **Open:** verify `settings.local.json` hooks merge next session; delete `custom-skills.bak-directory-source`; commit `f0ff7e7` (orphaned May-12 source) may need push check; Atlas `.ps1` meeting-prep port (pipeline DEAD since 2026-05-12); CE-overlap consolidation; wire `/advisor`→council discussion with Dina.
- **Atlas meeting-prep pipeline DEAD since 2026-05-12** — Task Scheduler killed in 2026-05-07 cloud migration, `.ps1` never ported. Missed WDAI Core Team Syncs May 19 / Jun 2 + Helen sessions. Posted #atlas-cos. Atlas `.ps1` port is open work.
- **Self-awareness instrumentation (2026-05-19):** delegation-scope warning hook, multi-repo daily-log commit logger, lite session-snapshot on SessionEnd+PreCompact, prior-art surveying. 6 commits to agents repo.
- **Pending Dina:** (1) `ctx-upgrade` — context-mode v1.0.75 broken (EBUSY); requires closing Claude Code first. (2) `slack-watcher/test-singleton.mjs` — commit or delete. (3) self-improve.yml needs repo setting "Allow GitHub Actions to create and approve pull requests" enabled. (4) `/advisor` → council vs fork: confirm fork approach.

## Key Facts
- Slack: DaFudge workspace, channel C0ASYTE8PB4 (polaris-slack MCP, `slack_dm_owner` shortcut) — full read/write working
- Discord: #polaris (1493421025881493636) — shared bot with Atlas, can't run simultaneously
- Sub-agents: Builder (sonnet), Designer (sonnet), QA (sonnet)
- GDrive/Gmail/GCal MCPs ARE available to Polaris for technical work. Atlas handles calendar/email scheduling + routing.
- Code tools: context-mode, Playwright, gh CLI, GDrive/Gmail/GCal MCPs (technical-use)
- Granola MCP: available via claude.ai account — can pull meeting transcripts directly
- WDAI team is all non-developers/vibecoders — CI gates + smoke testing + defrag are the safety net
- Helen's GitHub username: helenlkupp (not helenkupp)
- WDAI local dev DB: Docker Postgres on `localhost:5433`, seed via `bash ./scripts/db-local.sh reset` (from `web/`).
- WDAI staging DB: Supabase project ref `qfcjtidvmzvppxbkxupk` (us-east-2 pooler). Staging creds at `web/.env.local.staging` (gitignored).
- WDAI Prisma client + Windows: `pnpm db:generate` fails with EPERM DLL lock if dev server is running. Stop server first.
- **WDAI team-OS is a federated KB, NOT a doc.** READ `memory/project_team_os_one_brain.md` before any team-OS architecture decision. Wrong-altitude trap: see `memory/feedback_team_os_wrong_altitude.md`.
- **Strict workspace boundary:** `polaris-slack` MCP = DaFudge personal; `wdai-slack` MCP = WDAI org. No cross-posting.
- **Dina is CAIO + WDAI decision-owner** — route WDAI decisions to Dina, not Helen.
- **Cross-machine config:** 3 repos (`mgbotoe/my.claude`, `mgbotoe/claude-skills`, agents) + declarative `extraKnownMarketplaces` + per-machine hooks in `settings.local.json` + marketplace freshness via sync-skills.py SessionStart hook.

## Atlas → Polaris Pipeline
- Atlas monitors WDAI meetings hourly via MeetingPrep (7 AM–3 PM) — **PIPELINE DEAD since 2026-05-12; Atlas .ps1 not yet ported to cloud**
- Writes summaries to `wiki/sources/` with `routing:` and `granola_id:` in frontmatter
- Technical items get pinged to #polaris-tl; Polaris checks wiki on startup for new items
- Polaris pulls full Granola transcripts for own technical assessment — never relies on Atlas's summary for technical judgment

## Standing Rules
- **Dina is CAIO + WDAI decision-owner.** Do not route WDAI cross-cutting decisions to Helen — corrected twice in 2026-06-13 session.
- **Read target repo before building.** Check for existing CI guards before adding new ones — caught duplicate destructive-migration guard 2026-06-13.
- **Verify, don't assert.** Dina catches unwired prose passed off as real tools (e.g. advisor() call). Always confirm a thing actually works before claiming it does.

## Session Log
- [2026-04-13] Agent scaffolded by Atlas. Identity, rules, sub-agents, skills, and config created.
- [2026-04-14] Full workspace tour (18 repos mapped), wiki enriched, Slack MCP built and connected.
- [2026-04-15] First Atlas→Polaris handoff. WDAI technical roadmap assessed. Pipeline documented. Startup hook added.
- [2026-04-15] Built + shipped defrag skill for WDAI (PR #560). Shared project memory decision pending.
- [2026-04-17] Hardened delegation: sub-agents require CLAUDE.md section citations; two new feedback memories saved.
- [2026-04-18→20] Ghost distill sweep: 18 consecutive no-ops; short-circuit guard drafted (Dina approval pending).
- [2026-04-19] WDAI tech debt audit Phase 1 → `wiki/projects/wdai-tech-debt.md`.
- [2026-04-19] slack-watcher 6-bug sweep + symmetric inbox polling shipped (`9cc35fc`). Postmortem + ADR-005.
- [2026-04-19] SessionEnd hook added. `settings.json` now tracked via `.gitignore` exception.
- [2026-04-19] Polaris→Atlas comm spec rewritten in `wiki/infrastructure.md`.
- [2026-04-19] Agent ecosystem roadmap seeded at `wiki/projects/agent-ecosystem.md`.
- [2026-04-25] OAuth `atlas-493123` published to Production + 6 tokens re-issued. Distill short-circuit guard shipped.
- [2026-04-27] OpenClaw memory upgrade: `/recall`, decay schtask (180d), `/promote` curation shipped to Polaris + Atlas.
- [2026-04-27] Personal creative piece w/ Dina (deleted at her request). `imagen-4.0-generate-001` model name note.
- [2026-04-29→05-02] Ghost distills only. Short-circuit guard working.
- [2026-05-05] Watcher chaos day resolved. mailchimp-cc PR #16 reviewed + fixed (`01f23ad`, push blocked). accessibility-audit skill + PR #600 shipped.
- [2026-05-06] Watcher root cause fixed: event loop drain + WebSocket mid-reconnect. gather-context.ps1 WMI check fixed.
- [2026-05-07] Migrated agent automation off local Task Scheduler to GitHub Actions cloud cron. Built `bin/promote.py` + `bin/discuss.py`. Separated SAMESF into own repo.
- [2026-05-09] Reviewed WDAI PR #598 (Brigitte's Mailchimp one-click cohort registration). Posted review with 2 must-fix + 2 should-fix.
- [2026-05-11] WDAI PR #603 ready for review: `/api/intro/suggest-matches` — 8 files / 789 lines / 270 tests.
- [2026-05-19→20] Self-awareness instrumentation layer shipped: delegation-scope warning, daily-log commit logger, lite session-snapshot, prior-art surveying. 6 commits.
- [2026-05-20] WDAI team-OS build session: PRs #5-8 opened (22 C-series rows filled), VALUE_FIRST hook shipped.
- [2026-05-20] Team OS Beacon Slack app built + installed in WDAI workspace. PR #9 opened. wdai-slack MCP wired.
- [2026-05-20 PM] PRs #7+#9+#10 merged; ADR-0008 content synthesis shipped.
- [2026-05-20→22] Beacon Slack app shipped; first verification ping to Helen captured (PR #12). 6 PRs merged.
- [2026-05-22] Reviewed Helen's PR #667 (foundation CLAUDE.md 1217→228); hybrid branch naming converged.
- [2026-06-05] Single-source cross-tool agent context shipped: AGENTS.md canonical + CLAUDE.md @import shim (PR #675/#25).
- [2026-06-06] AGENTS.md PRs opened; CE plugin eval'd; CAIO formalized; Helen design brief + "context compounds" thesis.
- [2026-06-11] WDAI PR #603 driven to merge-ready w/ Dina pairing on Gumloop side. Secret ROTATED. Helen tagged.
- [2026-06-13] Drove Compound Engineering adoption on WDAI → PR #689. ADR-003 + CLAUDE.md coexistence routing. Standing Rule solidified: Dina is CAIO+decision-owner.
- [2026-06-14] PR #689 finalized: ADR-003 + coexistence routing table + pr-merge-workflow clarification. Luma→GCal sync PR #686 merged.
- [2026-06-18] Cross-platform overhaul: OS-agnostic path derivation, gather-context.py (fixed 0GB bug), cloud cron for decay/self-improve (PR-gated), heartbeat→/loop, per-machine workspace map, mgbotoe/claude-skills + my.claude repos, sync-skills.py SessionStart hook, /advisor skill (fork), path-leak CI guard. Atlas meeting-prep pipeline found DEAD since 2026-05-12 — posted #atlas-cos.
