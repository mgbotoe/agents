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

## Dev Agent (General Purpose) <!-- added 2026-04-13 -->
- **Started:** planned, not started
- **Goal:** Standalone unclaw agent for dev work — code verification, builds, PRs, technical tasks
- **Stack:** unclaw framework (github.com/shahshrey/unclaw)
- **Status:** planned — scoping later, intentionally NOT WDAI-specific
- **Notes:** Atlas handles product/strategy signals (CoS work). Dev agent handles code/build/deploy (dev work). Discord watcher routes conversations to the right agent.
