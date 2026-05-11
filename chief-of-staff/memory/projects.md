# Projects — Cold Memory

Detailed project context. Searched on-demand via `/search-memory` or direct file read.
Don't duplicate what's in `identity/user.md` or `identity/memory.md`.

## WDAI Product Spectrum Registry <!-- added 2026-04-13 -->
- **Started:** 2026-04-06
- **Goal:** Track all products, tools, and automations being built across WDAI — the CPO dashboard
- **Stack:** Google Sheets
- **Status:** active
- **Notes:** 17 items tracked. Columns: Product, Builder, Slack Handle, Spectrum, Impact Area, Value Tier, Score, Recommended Action, Decision, Status, Decision Needed, Notes, Source URL, Date Added, Last Seen, Run Count. Sheet ID: 1Gz50sLZ_b6asCjU6D7-BqhFjlaK_A11oYWN6RTe8arw. GDrive account: nonprofitcd. CPO folder ID: 1d7OR7Sy0BW5Qb-Fjr8vq-jOPCiniGsAy. Build Signals xlsx also in CPO folder (27 items from Atlas scans + Granola + DMs).

## WDAI Product Signal Detector <!-- added 2026-04-13 -->
- **Started:** 2026-04-13
- **Goal:** Automate Slack scanning for product/tool build signals, classify by relevance+maturity, surface to Dina
- **Stack:** Atlas scan-slack skill → Gumloop Slack read API → Discord output
- **Status:** active — skill built, scheduled Wed+Fri 4pm, Gumloop radar retired
- **Notes:** Spec at wiki/projects/wdai-product-signal-detector.md. Full pipeline: Phase A classifier (Q1-Q4) + Phase B operational follow-ons (O1-O2), ops-first value scorer, impact area tagging, High-only surfacing, decision column for Dina. Scans channels by prefix + private hardcoded list + archived gig channels. Also captures top-down signals from Granola 1:1s and DMs. Outputs to Discord #product-radar. Can't use Slack search API or post to Slack channels (Gumloop issues). CPO mission: "WDAI doesn't just teach AI — we run on it."

## Dev Agent / Polaris <!-- updated 2026-05-05 -->
- **Started:** 2026-04-15 (live)
- **Goal:** Tech lead + dev work — code verification, builds, PRs, architecture, WDAI + personal projects
- **Stack:** unclaw framework, Opus model, delegates to Builder/Designer/QA (Sonnet sub-agents)
- **Status:** active — live at `C:\Workspace\agents\dev-agent\`
- **Notes:** Posts to #polaris-tl (C0ASYTE8PB4). Atlas↔Polaris communicate via wiki/log.md (permanent record) + Slack (notification layer). Polaris checks #atlas-cos for Atlas messages at session start.

## Sage (SAME SF Content Operations) <!-- promoted 2026-05-05 -->
- **Started:** 2026-05-03
- **Goal:** Content ops agent for SAME SF Post — Mailchimp schedule sync, content pipeline, posting ops
- **Stack:** unclaw framework, Sonnet model
- **Status:** active — live at `C:\Workspace\SAMESF\`
- **Notes:** Has session-startup.py that syncs Mailchimp on session start (Dina added, not yet reviewed). Heartbeat checks content pipeline instead of Slack inbox. No inter-agent comms (no Slack integration). Promote auto-runs on session start (Sage had correct hook design from day 1).

## Slack Socket Mode Watcher <!-- promoted 2026-05-05 -->
- **Started:** 2026-04-15
- **Goal:** Persistent listener that routes Slack messages to the correct agent
- **Stack:** Socket Mode, config-driven (agents added via config.json)
- **Status:** active — live at `C:\Workspace\agents\slack-watcher\`
- **Notes:** Replaced Discord watcher. Config at reference_slack_watcher.md. Runs as persistent process.
