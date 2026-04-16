---
name: AI & Microsoft 365 Productivity Tools Demo
source_type: transcript
date: 2026-04-10
meeting_type: demo
participants: [Madina Gbotoe, LBS team members]
tags: [danaher, lbs, m365-copilot, mcp, cursor, demo]
granola_id: 8b20f474-6f75-434d-a44f-328f9d475ce8
---

# AI & Microsoft 365 Productivity Tools Demo

Part of the LBS on-site training week. Team members demonstrated how they use M365 Copilot, MCP connectors, and Cursor for day-to-day project management and code exploration.

## MCP Connectors Demo

### Jira/Confluence Integration
- Team member built MCP connector to Jira — can query open stories, milestones, sprint status directly from AI chat
- Output in markdown → paste into Teams chat → renders as formatted table
- Can cross-reference Jira tickets with Confluence docs to check if documentation matches code behavior

### Safety Considerations Raised
- Shared MCP servers need guardrails — risk of accidental deletion in shared services
- Token/auth traceability issue: actions via MCP use the builder's token/identity, not the end user's
- If sharing MCPs, should be read-only or have explicit authorization flows
- "I was tempted to share this with the team, but some of what I'm doing uses my token"

## M365 Copilot Desktop Features

### Daily Productivity Patterns
- One team member built a "chief of staff" agent in M365 Copilot Studio
  - Morning: sends daily summary of tasks/meetings
  - Midday: summarizes what's been completed
  - Friday: generates to-do list for next week
- Desktop Copilot can search Teams messages, SharePoint, emails — unified context
- Custom agents can be deployed to browser (requires premium license)

### Code Exploration Use Case
- Using Copilot in VS Code "Ask Mode" (read-only) vs "Agent Mode" (can make changes)
- Generates Mermaid dependency diagrams from codebases — vector graphics, zoomable
- Useful for understanding large legacy codebases (700-page user manuals, etc.)
- Can summarize long documents, find specific info across pages

## Madina's Contribution
- Positioned as EAI team resource — "keep that conversation going"
- Encouraged team to build their own MCP connectors: "just prompt and tell it to build that MCP for you"
- Shared screen to continue the enablement conversation

## Cross-References
- [[projects/github-copilot-adoption|GitHub Copilot Adoption]]
- [[sources/2026-04-10-eai-workshop-debrief|EAI Workshop Debrief]]
- [[sources/2026-04-10-lbs-ai-tools-pulse|LBS AI Tools Pulse]]
- [[organizations/danaher|Danaher]]
