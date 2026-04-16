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
- **Slack Socket Mode Watcher** live at `C:\Workspace\agents\slack-watcher\` — persistent listener, routes messages to correct agent, config-driven (add agents via config.json). Replaces Discord watcher.
- **Inter-agent pipeline:** Atlas → wiki/sources/ (with routing tag) → Slack notification → Polaris pulls Granola transcript. Wiki log for async messages. Slack for notifications.
- **Post-meeting transcript pipeline** (WDAI only): MeetingPrep hourly task checks Granola after meetings end, writes to wiki, routes technical items to Polaris via #polaris-tl.
- `/draft-email` skill created — drafts in Dina's voice using wiki voice profile. Never sends without approval.
- Agent infrastructure documented at `wiki/infrastructure.md` — new agent onboarding checklist.
- Synced with UnClaw upstream: added `.claude/agents/` (researcher, reviewer) and 9 playwright reference docs.

## Active Work
- [2026-04-15] WDAI technical roadmap — Polaris owns, from Rebekah/Helen/Madina call. Items: staging env, branch protection, CODEOWNERS, PostHog cleanup, analytics CI skill, on-call agent.
- [2026-04-15] Granola backlog cleared — 15 meetings from Mar 16-30 ingested to wiki/sources/. 2 technical items routed to Polaris.
- [2026-04-13] Product Signal Detector — spec at wiki/projects/wdai-product-signal-detector.md
- Overdue: Brigitte meeting to map website/portal structure (14+ days, from Mar 30)
- Overdue: Elizabeth McKenzie lead follow-up (24 days)

## Key Facts
- WDAI Slack GDrive account label: `nonprofitcd`
- **Personal Slack:** #atlas-cos (C0ASHFXMHM5) — primary output channel. Workspace: DaFudge. Bot: atlas.
- Dina's personal Slack user ID: U094L7RJ9FV (DaFudge workspace)
- Dina's WDAI Slack user ID: U08DCSBGJ1H
- Polaris Slack channel: #polaris-tl (C0ASYTE8PB4)
- Discord: fully removed (was legacy fallback)
- Helen's Q4 rule: if core team built it and it touches WDAI systems → deeply integrated by default

## Session Log
- [2026-04-15] Major infrastructure session. Morning brief upgraded (dedup, tiering, focus block 1-2PM, hidden noise events, agent inbox as step 1). Atlas↔Polaris transcript pipeline built and validated (Granola → wiki → Slack routing). Post-meeting MeetingPrep phase added (WDAI only). Inter-agent protocol documented in CLAUDE.md + wiki. Slack Socket Mode watcher discovered and documented. Self-improve ran (3 fixes: duplicate security section, humanizer contradiction, launchd ref). Draft-email skill created. Discord fully removed. Synced with UnClaw upstream (agents/, playwright refs). Wiki infrastructure page created for new agent onboarding. Polaris built technical roadmap from Rebekah call.
- [2026-04-13 PM] PTO day (Mama Day Off). Midday check ran silent — no urgents. Helen 1:1 prep delivered.
- [2026-04-13] Epic session: Full CPO framework end-to-end. scan-slack skill, 6-month parallel scan, CPO deck + xlsx in GDrive. Gumloop retired. Polaris recognized.
