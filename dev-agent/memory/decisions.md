# Decisions — Cold Memory

Key technical decisions with reasoning. Includes ADRs and architecture choices.

<!-- This file will be populated as Polaris makes decisions -->

## ADR-001: Agent Architecture — Polaris as Tech Lead
- **Date:** 2026-04-13
- **Decision:** Polaris runs as a tech lead orchestrating 3 sub-agents (Builder/Sonnet, Designer/Sonnet, QA/Sonnet) rather than a single monolithic dev agent.
- **Context:** Needed a dev agent that covers the full SDLC. Single-agent approach would overload context with conflicting concerns.
- **Rationale:** Mirrors real eng team structure. Tech lead makes decisions, delegates execution, reviews output. Sub-agents stay focused on their domain.
- **Trade-offs:** More overhead per delegation (context transfer cost), but better quality through separation of concerns and independent review.
