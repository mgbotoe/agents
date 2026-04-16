---
name: "Finance Use Case Part 2"
source_type: transcript
meeting_type: strategy
date: 2025-12-15
granola_id: c07efe23-6fd2-4dae-ba7b-636bcb67ad8e
attendees: [Madina Gbotoe]
tags: [danaher, finance-ai, strategy, data]
---

# Finance Use Case Part 2

Strategy session analyzing finance AI use cases and data integration approach.

## Key Findings

- 95% of finance projects are automation-focused (manual data pull/match/re-upload)
- Core problem: users download from ERP systems, websites, laptops — manually match and re-upload
- Most use cases show limited ROI (only saving manual hours)
- Some advanced cases include ML: credit assessments, data analytics (Sharan in Surface team)

## Data Integration Strategy

- Primary overlap across all use cases: enterprise search
- All teams need consolidated data from same sources (HR, book data, revenue, invoices)
- Current inefficiency: each team pulls same data separately
- Proposed: centralize all data first, then customize for specific use cases
- Revenue and invoice data most frequently used
- Workday integration needed for OPCO-level aggregation
- Metadata mapping needed (e.g., Blackbound Carter has 7 subsidiaries)

## Implementation Approach

- Create exhaustive data source inventory for all OPCOs
- Build reusable agents: 80% component reuse across finance use cases
- Modify table/entity targets rather than rebuilding
- Microsoft finance agent demo scheduled to evaluate third-party options
- Data consolidation required regardless of internal vs external tooling

## Cross-references

- [[organizations/danaher|Danaher]]
- [[projects/finance-ai|Finance AI]]
- [[sources/2025-12-15-finance-martin-siyu-madina|Finance Sync — Martin/Siyu/Madina (Dec 15)]]
