---
name: "VOC — Keith Brewer: AI Tools & Productivity (LBS)"
source_type: transcript
meeting_type: voc
date: 2026-03-06
attendees: [Madina Gbotoe, Keith Brewer]
granola_id: "ccfb542d-0d48-4a6d-94a2-0e86384e52ed"
tags: [danaher, lbs, keith, voc, cursor, mcp, contractor, tech-debt, sierra]
---

# VOC — Keith Brewer: AI Tools & Productivity (LBS)

Granola meeting: `ccfb542d-0d48-4a6d-94a2-0e86384e52ed`

## Summary

Keith built custom MCP connecting Cursor to JAMA, JIRA, Bitbucket, and FogBugs. Generated software revision history in 5 min vs 2–3 weeks manual. Project Sierra (GT Scanner) accelerated from 2-year to ~1-year timeline. Keith's monthly compute could reach $3K unrestricted.

## Contractor Problem

- 7 hours fixing contractor work per 1 line of code written
- Contractors lack investment in product/team
- Leica spent $1.1M on Glorium contractors (12–13 devs) last year
- Keith prefers eliminating contractors → unlimited AI compute for internal team

## Tech Debt

- Node.js from 2009, Boost library 11 years old, 14+ years accumulated
- Artifactory access blocks modern CI/CD, automated reviews, testing
- Manual code review: 2 devs per PR, manual compilation on each machine

## Cursor > Copilot

- More stable, better context structuring, bleeding-edge features
- Planning mode, ask mode, automatic mode
- Higher quality code output with same underlying models

## Proposed Solutions

- 2-day hands-on training tailored to tech stack
- Cross-OpCo power user committee for monthly sharing
- Sandbox environments, Claude CLI / ChatGPT API access, shared Bedrock for MCP
- Connect Keith's Confluence MCP to Microsoft Copilot
