---
name: "Pricing AI Architecture & Implementation Strategy"
source_type: transcript
meeting_type: strategy
date: 2026-03-10
attendees: [Madina Gbotoe]
tags: [danaher, pricing-ai, mckinsey, beckman, cepheid, architecture]
---

# Pricing AI Architecture & Implementation Strategy

Granola meeting: `ab5003c1-d701-4315-9729-00d9c7242f42`

## Summary

McKinsey proof-of-value wrapping up for pricing AI across Beckman and Cepheid diagnostics. Centralized pricing AI engine at Danaher level with separate OpCo instances. Two main tools: Dynamic Deal Scoring and Contract AI. Target Q2 implementation start after 6+ week contract negotiation.

## Architecture

- **Data flow**: OpCo Snowflake -> Danaher Snowflake -> AI processing -> Insights dashboards
- **Dynamic Deal Scoring**: Analyzes past deal patterns for recommendations
- **Contract AI**: Automates compliance checking from PDFs
- Separate instances per OpCo (different contracts/use cases)

## Cepheid Specifics

- Launching Excel-based pricing tool next week
- McKinsey solution designed as incremental (not duplicative)
- Primary focus: price netting (compliance automation)
- Respiratory business creates unique challenges — seasonal demand, customers won't commit to volume pricing
- Contract compliance currently manual — big automation opportunity

## Technical Blockers

- PDF contract extraction from Salesforce not yet available — needs new pipeline to blob storage
- Structured data sharing via Snowflake in progress with Raj's team
- Security reviews initiated with Danaher Architecture Review Board (ARB)
- Privacy assessment (PIA) needs updating

## Key Milestones

- Friday report-out with Kevin O'Reilly and Laurent Amil (McKinsey presenting)
- Complete proof of value (next 2 weeks from meeting date)
- Contract negotiation with McKinsey (6+ weeks)
- Target Q2 implementation start
- Cepheid needs business case for PPG process (Sridhar as POC)

## Cross-references

- [[organizations/danaher|Danaher]]
- [[projects/pricing-ai|Pricing AI (McKinsey)]]
