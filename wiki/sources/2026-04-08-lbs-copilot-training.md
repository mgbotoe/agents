---
name: LBS Copilot Training — Day 1
source_type: transcript
meeting_type: demo/workshop
date: 2026-04-08
tags: [danaher, lbs, github-copilot, training, san-diego, mcp]
participants: [Madina Gbotoe]
---

# LBS Copilot Training — Day 1

Full-day GitHub Copilot training session at LBS San Diego. Covered architecture, CLI agents, code review, customization, context management, and testing use cases.

## Copilot Architecture

- Copilot is an orchestrator, not an LLM — takes prompts, applies safety checks, sends to selected model, returns filtered responses
- User maintains control as "pilot"; AI assists, doesn't replace engineering judgment
- BitBucket integration possible through MCP (Model Context Protocol) — git-based engines support PR inspection/summary locally
- Same functionality available for GitLab and other git servers

## CLI & Background Agents

- CLI enables background agent work without staying in GitHub.com
- Background agents run independently, return results when complete — different from chat (no conversation history)
- Must spawn new CLI agent for continued work
- VS Code offers background agent option for local ticket work

## Customization System

- `Instructions.md` — common Copilot chat behavior rules
- `Prompts.md` — reusable lengthy prompts
- `Agents.md` — custom scoped agents
- `Skills.md` — specialized capabilities
- Organization-wide repos can share agents across teams

## Licensing

- Business license: 300 premium requests/month per developer
- Enterprise license: 1,000 premium requests/month per developer
- Auto mode: 10% discount on premium requests
- Overage: ~$0.04 per additional request

## Context Management

- Context window max ~50K tokens (20K ideal)
- AI forgets unreferenced info due to memory compression
- Solutions: write important info to files, use implementation plans as docs, start new sessions with project/instruction summaries
- Claude 4.6 showed 200K token capacity with usage indicator

## Plan Mode

- Essential for complex tasks — AI creates multi-step implementation plans with acceptance criteria
- Custom planning agents recommended over default (more focused/deterministic)
- Plans should be saved as markdown documents for persistence
- Can be shared across global teams for handoff work

## Testing Use Cases

- Test case creation possible with proper context (requirements, architecture, UI/UX specs, front-end code)
- Creates step-by-step test procedures, strategies, and plans
- Melbourne team very far ahead — has full AI roadmap for implementation
- Use case identified: agent to scan code and identify manual test opportunities

## Madina's Notes

- Melbourne team significantly ahead on AI adoption — has structured roadmap
- Team using Copilot 365 instead of GitHub Copilot (confusion between products)
- MCP as integration layer is key architectural concept for teams on non-GitHub platforms

## Key Sources

- [[sources/2026-04-08-ai-tools-training-interactive|Training Interactive Session Planning (Apr 8)]]
- [[sources/2026-04-10-eai-workshop-debrief|EAI Workshop Debrief (Apr 10)]]
- [[projects/github-copilot-adoption|GitHub Copilot Adoption]]
