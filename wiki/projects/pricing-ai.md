---
name: Pricing AI (McKinsey)
org: Danaher
type: project
status: active — proof of value wrapping up
tags: [danaher, ai, pricing, mckinsey, beckman, cepheid]
participants: [Madina Gbotoe, Kevin O'Reilly, Laurent Amil, Raj, Sridhar]
---

# Pricing AI (McKinsey)

AI-enabled pricing transformation across Beckman and Cepheid diagnostics. McKinsey-led proof of value with centralized Danaher pricing AI engine. $51-71M opportunity.

## Architecture

- **Centralized engine** at Danaher level with separate OpCo instances
- **Data flow**: OpCo Snowflake -> Danaher Snowflake -> AI processing -> Insights dashboards
- Two main tools:
  1. **Dynamic Deal Scoring** — analyzes past deal patterns for recommendations
  2. **Contract AI** — automates compliance checking from PDFs

## Use Cases

- **Price setting**: Optimal pricing recommendations
- **Price getting**: Deal scoring and negotiation support
- **Price netting**: Compliance automation (primary Cepheid focus)

## Cepheid Specifics

- Excel-based pricing tool launching (as of Mar 2026)
- Respiratory business: seasonal demand, customers won't commit to volume pricing
- Contract compliance currently manual — big automation target
- Business case needed for PPG process (Sridhar as POC)

## Technical Blockers

- PDF contract extraction from Salesforce not available — needs new pipeline to blob storage
- Structured data sharing via Snowflake in progress (Raj's team)
- Security reviews with Danaher Architecture Review Board (ARB)
- Privacy assessment (PIA) needs updating

## Timeline

- Proof of value phase: wrapping up (as of Mar 10, 2026)
- Contract negotiation with McKinsey: 6+ weeks
- Target: Q2 implementation start
- Senior leadership expects ROI in 2026

## Leica-Specific Opportunity (Mar 31)

- $25-35M annual run-rate for Leica margin expansion (component of the $51-71M total)
- Current US business: $650M revenue (~5% potential impact)
- Timeline: $4-5M in 2026, $14-20M in 2027, full run-rate by 2028
- Priority areas: pricing/discounting guardrails, services pricing & attachment, contract compliance
- Specific recommendations: extended warranty bundling (start with microtomes), dynamic deal scoring, long-tail SKU pricing (27,000+ SKUs)
- Colin emphasized: select 2-3 high-impact initiatives, don't try everything

## Key Sources

- [[sources/2026-03-31-margin-expansion-leica|Margin Expansion — Leica (Mar 31)]]
- [[sources/2026-03-10-pricing-ai-strategy|Pricing AI Strategy (Mar 10)]]
- [[sources/2026-03-02-danaher-board-ai-presentation|Board Presentation (Mar 2)]]
- [[sources/2026-02-10-martin-1on1-dlc-conference|DLC Conference Debrief (Feb 10)]]
