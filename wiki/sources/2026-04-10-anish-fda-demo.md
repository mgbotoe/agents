---
name: FDA Slide Scanning Automation — Anish Demo
source_type: transcript
date: 2026-04-10
meeting_type: demo
participants: [Madina Gbotoe, Anish, Keith, Ty, LBS team]
tags: [danaher, lbs, fda, automation, cursor, ai-tools, demo]
granola_id: 5fc2cc03-4248-4302-8369-221197c52203
---

# FDA Slide Scanning Automation — Anish Demo

Anish demonstrated a full project management dashboard he built using AI agents/coding tools for an FDA clinical submission project (VPA/G180 device validation).

## Project Context
- FDA clinical submission for G180 device (same optical/staging/software as GT450)
- Goal: prove new device images are pixel-equivalent to old device images — avoids expensive clinical study with pathologists
- Last year: ~3,000 screenshots; FDA came back wanting 30x more data
- This year: ~40,000 screenshots needed — manual approach impossible at this scale

## What Anish Built

### Dashboard & Automation Pipeline
1. **Slide scanning** — manual scan + automated file verification (counts images, ensures completeness)
2. **ESM integration** — reverse-engineered the ESM API using Postman exports + AI prompts; automated slide assignment to 3 pathologist reviewers (one in China, Dr. Ferber traveling)
3. **Annotation tracking** — monitors async review progress across 3 reviewers; backup annotations via API
4. **Annotation combining** — pulls all annotations + comments from ESM, combines into single export
5. **Cloning** — automated duplication to 3 ESM bridge versions for testing
6. **Screenshot automation** — Playwright-based; required 2 physical workstations (can't run headless); each workstation runs a companion app that pulls tasks from the dashboard
7. **FDA report generation** — scripts generate formatted comparison reports for FDA submission

### Technical Details
- Built with Cursor (Opus model preferred — "changed my view on AI in last 3 months")
- Database-backed (tracking annotations, slide data, screenshots, scoring)
- Total cost: ~$350 in API credits for 80% of the app, ~$150 for refinement
- Timeline: ~1.5 months (would have been 2-3 months manually, and Anish wasn't full-time on it)
- Scoring script reused from last year (validated for FDA)
- UI redesigned using a design agent

### Key Quotes
- "Code is so cheap to generate now. Don't worry about making things useful for the team until you can prove it to yourself."
- "Treat it like you're an idiot and just see how far you can get"
- "I don't write code by hand anymore — you can't even estimate it anymore"
- On custom agents: "Build agents where you find gaps only — for most common scenarios, existing coding agents work better"

## FDA Relationship
- Being transparent with FDA about AI usage — they're interested in it
- FDA also trying to enable AI internally due to staffing shortages
- Only the scoring/comparison script needs formal validation (the setup/automation doesn't)

## Strategic Implications
- This is a model case for AI ROI at Danaher: 40,000 automated comparisons vs impossible manual effort
- Anish is #4 on Danaher Cursor leaderboard
- Team wants to reconvene in ~1 month to discuss agent design patterns and tool sharing
- Pattern emerging: individual purpose-built tools first, then identify shared infrastructure later

## Cross-References
- [[projects/github-copilot-adoption|GitHub Copilot Adoption]]
- [[sources/2026-04-10-lbs-ai-tools-pulse|LBS AI Tools Pulse]]
- [[sources/2026-04-10-eai-workshop-debrief|EAI Workshop Debrief]]
- [[organizations/danaher|Danaher]]
