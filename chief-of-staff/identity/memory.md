# Hot Memory

Always loaded into context. Keep under 2500 tokens.
Detailed context lives in `memory/*.md` — search on-demand, don't duplicate here.

## Current State
- Dina owns CPO-like role at WDAI — holistic AI-native framework across all pillars (decided Mar 30 with Helen)
- Product Spectrum Registry live: https://docs.google.com/spreadsheets/d/1Gz50sLZ_b6asCjU6D7-BqhFjlaK_A11oYWN6RTe8arw/edit
- `/scan-slack` skill built with full pipeline: Phase A classification (Q1-Q4) + Phase B operational follow-ons (O1-O3), ops-first value scorer, High-only surfacing, Complete status for done items
- Scan scheduled: Wed + Fri 4pm via Task Scheduler (Atlas\ScanSlackWed, Atlas\ScanSlackFri)
- Outputs to Discord #product-radar (1493333553143091240); Slack posting broken (Gumloop bot permissions)
- 7 Gumloop reference skills preserved in `.claude/skills/scan-slack/reference/`
- Portfolio: 56 qualified signals from 6-month parallel scan (Nov 2025 - Apr 2026) + 17 existing in Gumloop registry
- Full scan ran all 6 months in parallel — 50 qualified after dedup (5 multi-sighting), 52 catch-all
- Dedup + naming rules added to skill to prevent duplicate entries across scans
- GDrive MIME type fix deployed — pptx/xlsx uploads now open correctly in Google Slides/Sheets
- CPO folder: https://drive.google.com/drive/folders/1d7OR7Sy0BW5Qb-Fjr8vq-jOPCiniGsAy
- **Polaris** (dev agent) live at `C:\Workspace\agents\dev-agent\` — tech lead role, Opus, delegates to Builder/Designer/QA (Sonnet). Shares Atlas's Discord bot, posts to #polaris (1493421025881493636). General purpose across all repos.

## Active Work
- [2026-04-13] Helen 1:1 prep — agenda at wiki/sources/2026-04-helen-1on1-prep.md
- [2026-04-13] Product Signal Detector — spec at wiki/projects/wdai-product-signal-detector.md
- [2026-04-13] 3-month Slack scan + historical xlsx export — next up
- Overdue: Brigitte meeting to map website/portal structure (from Mar 30 action items)

## Key Facts
- WDAI Slack GDrive account label: `nonprofitcd`
- Discord channels: #atlas (1493062124975685864), #product-radar (1493333553143091240), #polaris (1493421025881493636)
- Gumloop DMs route to Helen not Dina — use Discord for outputs until fixed
- Dina's WDAI Slack user ID: U08DCSBGJ1H
- Helen's Q4 rule: if core team built it and it touches WDAI systems → deeply integrated by default

## Session Log
- [2026-04-13] Epic session: Full CPO framework end-to-end. scan-slack skill (Phase A/B classifier, ops-first scorer, impact areas, decision column, dedup rules). 6-month parallel scan (50 deduped + 52 catch-all). Permalinks found 15/19 Granola items. CPO mission adopted. 6-slide deck + xlsx in GDrive. GDrive MCP: MIME fix + 5 Sheets + 5 Slides tools. Gumloop retired. Wed+Fri scan + 5pm heartbeat. All task wake timers fixed. Polaris recognized. Next: compare scan vs Gumloop, validate slide 5, test MCP after restart.
