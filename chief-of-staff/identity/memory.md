# Hot Memory

Always loaded into context. Keep under 2500 tokens.
Detailed context lives in `memory/*.md` — search on-demand, don't duplicate here.

## Current State
- Dina owns CPO-like role at WDAI — holistic AI-native framework across all pillars (decided Mar 30 with Helen)
- Product Spectrum Registry live: https://docs.google.com/spreadsheets/d/1Gz50sLZ_b6asCjU6D7-BqhFjlaK_A11oYWN6RTe8arw/edit
- `/scan-slack` skill built with full pipeline: Phase A classification (Q1-Q4) + Phase B operational follow-ons (O1-O3), ops-first value scorer, High-only surfacing, Complete status for done items
- Scan scheduled: Wed + Fri 4pm via Task Scheduler (Atlas\ScanSlackWed, Atlas\ScanSlackFri)
- All scheduled outputs migrated to Slack #atlas-cos (C0ASHFXMHM5). Discord fully removed.
- 7 Gumloop reference skills preserved in `.claude/skills/scan-slack/reference/`
- Portfolio: 56 qualified signals from 6-month parallel scan (Nov 2025 - Apr 2026) + 17 existing in Gumloop registry
- Full scan ran all 6 months in parallel — 50 qualified after dedup (5 multi-sighting), 52 catch-all
- Dedup + naming rules added to skill to prevent duplicate entries across scans
- GDrive MIME type fix deployed — pptx/xlsx uploads now open correctly in Google Slides/Sheets
- CPO folder: https://drive.google.com/drive/folders/1d7OR7Sy0BW5Qb-Fjr8vq-jOPCiniGsAy
- **Polaris** (dev agent) live at `C:\Workspace\agents\dev-agent\` — tech lead role, Opus, delegates to Builder/Designer/QA (Sonnet). Posts to #polaris-tl (C0ASYTE8PB4). General purpose across all repos.
- **Slack Socket Mode Watcher** live at `C:\Workspace\agents\slack-watcher\` — persistent listener, routes messages to correct agent, config-driven (add agents via config.json). Replaces Discord watcher. Singleton guard fixed commit `0b81411` (May 5): uses `tasklist` to verify PID on Windows EPERM — signal-0 alone was unreliable. Clean shutdown hooks added.
- **Inter-agent pipeline:** Atlas → wiki/sources/ (with routing tag) → Slack notification → Polaris pulls Granola transcript. Wiki log for async messages. Slack for notifications.
- **Post-meeting transcript pipeline** (WDAI only): MeetingPrep hourly task checks Granola after meetings end, writes to wiki, routes technical items to Polaris via #polaris-tl.
- `/draft-email` skill created — drafts in Dina's voice using wiki voice profile. Never sends without approval.
- Agent infrastructure documented at `wiki/infrastructure.md` — new agent onboarding checklist.
- Synced with UnClaw upstream: added `.claude/agents/` (researcher, reviewer) and 9 playwright reference docs.
- **Heartbeat auto-starts** on session start (no manual `/loop 60m /heartbeat` needed) — commit 530c3ad, Apr 17.
- Wiki reorganized + 45 Granola transcripts (Mar 1–Apr 15) ingested — commit 7279d6c, Apr 17.
- **Sage** (content ops agent for SAME SF Post) live at `C:\Workspace\SAMESF\` — bootstrapped May 3. Identity, rules, core skills, heartbeat, memory arch all in place.
- **Agent roster** at `memory/reference_agents_roster.md` — consistency checklist for all 3 agents (Atlas, Polaris, Sage). Standing rule: apply infra changes to all 3 unless explicit reason not to.
- **Promote/Distill cron jobs removed** (`\Atlas\Promote`, `\Atlas\Distill`, `\Polaris\Promote`, `\Polaris\Distill`) — by design. Heartbeat distills every 30m; session-start hook auto-runs promote if >24h since last run. Sage had this right from day 1; Atlas+Polaris hooks fixed May 5.

## Active Work
- [2026-04-18] **WDAI tech debt audit Phase 1** — Polaris posted `wiki/projects/wdai-tech-debt.md`. Two P0s blocked on Helen: (1) MainProtection ruleset allows 0-approval merges on main (no CODEOWNERS enforcement); (2) PR #569 fixes live Stripe webhook race, stuck CI-green. Helen to merge #574 + toggle ruleset. Link this doc next Helen touch.
- [2026-04-15] WDAI technical roadmap — Polaris owns, from Rebekah/Helen/Madina call. Items: staging env, branch protection, CODEOWNERS, PostHog cleanup, analytics CI skill, on-call agent.
- [2026-04-13] Product Signal Detector — spec at wiki/projects/wdai-product-signal-detector.md
- Brigitte website/portal mapping meeting closed [2026-04-16] ✅

## Key Facts
- WDAI Slack GDrive account label: `nonprofitcd`
- **Personal Slack:** #atlas-cos (C0ASHFXMHM5) — primary output channel. Workspace: DaFudge. Bot: atlas.
- Dina's personal Slack user ID: U094L7RJ9FV (DaFudge workspace)
- Dina's WDAI Slack user ID: U08DCSBGJ1H
- Polaris Slack channel: #polaris-tl (C0ASYTE8PB4)
- Discord: fully removed (was legacy fallback)
- Helen's Q4 rule: if core team built it and it touches WDAI systems → deeply integrated by default

## Standing Rules

- **Agent consistency:** When editing any agent file (`.claude/`, `identity/`, `skills/`, `settings.json`, heartbeat, hooks) — check `memory/reference_agents_roster.md` and apply the same change to all 3 agents (Atlas, Polaris, Sage) unless there's an explicit reason not to.

## Session Log
- [2026-05-05 PM] Watcher `0b81411` committed. Second watcher fix: `wmic` is NOT available on this machine — that code path silently falls to "treat as stale" (dead code). Fix needs revision before commit. Watcher also dying with WebSocket pong timeouts (~355 node processes, possible resource contention). Disk: 487GB free (false alarm cleared).
- [2026-05-05] Diagnosed cron job status post Claude-deletion. Most tasks running fine. Promote hooks fixed on Atlas+Polaris (now auto-run, matching Sage). Context-mode broken (needs /ctx-upgrade).
- [2026-05-03] Bootstrapped Sage. Fixed heartbeat ghost-entry bug + disable-model-invocation bug across all 3 agents. Silenced heartbeat+distill output. Committed 43 files (0df4846, 117aa8c, 444b458). Agent roster created.
- [2026-04-19 PM] Watcher self-loop debugging session w/ Polaris. Root cause: per-agent token split broke the `event.user === botUserId` self-filter (listening bot is Polaris, reply bot is Atlas — different IDs). Fix on branch `fix/watcher-self-loop` (commit 8e795fc). Inter-agent comms rubric formalized in `wiki/infrastructure.md`. Heartbeat skill now reads #polaris-tl each hour for new Polaris replies (`.claude/runtime/polaris-last-seen.ts` tracks last-seen ts). <!-- added 2026-04-19 -->
- [2026-04-18] Polaris completed WDAI tech debt audit Phase 1 while Atlas was idle. Two P0s posted to #atlas-cos for Helen sequencing. <!-- added 2026-04-19 -->
- [2026-04-17 late] Distilled Apr 17 decisions + WDAI project snapshot. Hardened delegation rules + never-push hard rule (later relaxed Apr 19 to allow branch pushes but not main/PR/Slack). Added WDAI-scoped intent-comments rule. <!-- added 2026-04-19 -->
- [2026-04-17] Upgraded to Opus 4.7 (released Apr 16). Verified specs vs assumptions — 1M context but new tokenizer eats ~35% more, so effective is ~750K. Self-verification + opinionated-by-default trained in. Upgraded morning brief (skill + ps1) to lean into the model: load FULL wiki pages and Granola transcripts for today's notable meetings, pick ONE strategic focus per pillar (not three), tighten BOTTOM LINE to one sentence, added "verify before claiming" + "no menu of options" rules. Saved verified facts to reference_opus_4_7.md.
- [2026-04-15] Major infrastructure session. Morning brief upgraded (dedup, tiering, focus block 1-2PM, hidden noise events, agent inbox as step 1). Atlas↔Polaris transcript pipeline built and validated (Granola → wiki → Slack routing). Post-meeting MeetingPrep phase added (WDAI only). Inter-agent protocol documented in CLAUDE.md + wiki. Slack Socket Mode watcher discovered and documented. Self-improve ran (3 fixes: duplicate security section, humanizer contradiction, launchd ref). Draft-email skill created. Discord fully removed. Synced with UnClaw upstream (agents/, playwright refs). Wiki infrastructure page created for new agent onboarding. Polaris built technical roadmap from Rebekah call.
- [2026-04-13 PM] PTO day (Mama Day Off). Midday check ran silent — no urgents. Helen 1:1 prep delivered.
- [2026-04-13] Epic session: Full CPO framework end-to-end. scan-slack skill, 6-month parallel scan, CPO deck + xlsx in GDrive. Gumloop retired. Polaris recognized.
