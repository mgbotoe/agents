---
name: AI Model Performance Insights — Bryan Conn 1:1
source_type: transcript
date: 2026-04-09
meeting_type: voc
participants: [Madina Gbotoe, Bryan Conn]
tags: [danaher, lbs, cursor, ai-tools, voc, power-user, salesforce, mcp]
granola_id: ab1bd362-326c-4882-abd3-6a43bbbb9443
---

# AI Model Performance Insights — Bryan Conn 1:1

VOC/discovery call with Bryan Conn, a non-developer power user at LBS who is using Cursor + MCP connectors in transformative ways. This is a standout example of AI adoption beyond engineering.

## Bryan's Background
- Not a software engineer — more of a technical product/quality role at LBS
- Got into AI tools through podcasts (heard about a CIO at Toronto sports company doing one-day prototypes with Cursor)
- Started with ChatGPT/Copilot for personal use → discovered Google Anti Gravity (Dec) → got Cursor license from Ty
- His name came up because he requested a Cursor credit increase — Madina noticed and reached out

## Key Use Cases (Non-Developer)

### Salesforce MCP Integration
- Connected Cursor to Salesforce via MCP connector
- Queries service history by serial number, generates tables, pulls work order data
- "Bringing Copilot to Salesforce" without paying for Salesforce AI ($$$)
- Example: Quality audit needed 10 specific work orders → Cursor queried Salesforce, applied filters (unique field service engineers), printed PDFs via Playwright browser automation — 30 min vs 1+ hour manual

### Software Bug Tracking
- Quality needed to know which instruments were upgraded to software v1.5.51
- No structured field for this in Salesforce — just plain text in work orders
- Cursor searched all GT450 work orders mentioning version numbers → comprehensive list
- "We could have missed one, but I'm very confident these are all related"

### Image Quality Tool (Manufacturing)
- Built an open-source slide viewer using Cursor — 7 minutes with stopwatch running
- SVS file support, pan/zoom, annotation, heat map overlay
- Being rolled out to manufacturing as a quality tool
- Will go through formal Quality Management System validation

### ImageScope Revival Project
- ImageScope: legacy freeware slide viewer, last updated 2017-2018, original developer left
- Nobody knows the development environment; code scattered across Perforce repos
- Bryan pulled repos locally, had Cursor document the codebase
- Has a full plan to refactor from legacy .NET to modern C# — huge backlog ready
- May not execute, but proves the concept of AI-driven legacy code understanding

## Key Quotes
- "Cursor is not for software engineers — it's your Everything Agent on your company system"
- "People like you [Madina] and your Everything Agent... it's for anyone"
- "You can have software solutions without having software engineers"
- "We've talked about big data for 20 years. Now you don't really need data scientists so much."

## Strategic Implications
- **This is the strongest non-developer AI adoption story at Danaher** — should be showcased
- Cursor ROI is clear: queries that took hours now take minutes
- Non-developers are getting MORE value from Cursor than some developers
- Challenges enterprise thinking that Cursor is "just for developers"
- MCP connectors to enterprise systems (Salesforce, Jira, Confluence) are the killer feature

## Model Insights
- Bryan prefers Opus — "changed my view on AI in last 3 months"
- Cursor orchestration is smarter than VS Code with same model
- AMD study found Claude Code update in February decreased performance on advanced software engineering topics
- Microsoft paper: multi-model agent swarms outperform single flagship models

## Cross-References
- [[projects/github-copilot-adoption|GitHub Copilot Adoption]]
- [[sources/2026-04-10-anish-fda-demo|Anish FDA Demo]]
- [[sources/2026-04-10-lbs-ai-tools-pulse|LBS AI Tools Pulse]]
- [[organizations/danaher|Danaher]]
