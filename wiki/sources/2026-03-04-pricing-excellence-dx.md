---
name: "Pricing Excellence Strategy — Danaher Diagnostics (McKinsey)"
source_type: transcript
meeting_type: strategy
date: 2026-03-04
attendees: [Madina Gbotoe, McKinsey team, Eugene]
granola_id: "dd2af4ed-897d-43bc-97bb-aa04aec9360f"
tags: [danaher, pricing, mckinsey, beckman, cepheid, dds, contract-ai, architecture]
---

# Pricing Excellence Strategy — Danaher Diagnostics

Granola meeting: `dd2af4ed-897d-43bc-97bb-aa04aec9360f`

## Summary

Implementing DDS (Dynamic Deal Scoring) and Contract AI for Beckman and Cepheid. Phase 1 (diagnosis design) 80–90% complete. MVP design follows business case approval. Aggressive 8-week sprint schedule targeting DDS by late April, Contract AI by May.

## Architecture

- OpCo systems → OpCo Snowflake → Danaher Data Lake → Azure deployment
- Separate DDS + Contract AI instances per OpCo
- Beckman: all data in Snowflake. Cepheid: partial, work needed.
- Unstructured (contracts): Salesforce → SharePoint → Azure Blob crawling

## Governance

- Architecture Review Board approval required (weekly sessions, can expedite)
- Beckman: Legal + InfoSec + AI steering committee sign-off
- Legal approval needed for cross-OpCo contract data sharing

## Resources by Phase

- Phase 1: McKinsey heavy, light OpCo involvement
- Phase 2: 50/50, 3–4 full-stack devs from Danaher
- Phase 3: Danaher ownership, McKinsey support available

## Contract AI Demo

- Converts unstructured PDFs to structured data (LLM + traditional SE)
- Human-in-the-loop validation
- 1–4% value leakage identification in other deployments
