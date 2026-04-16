---
name: RegDes Regulatory AI Platform Demo
source_type: transcript
meeting_type: demo
date: 2026-04-03
tags: [danaher, regulatory, ai, regdes, fda, ivdr, beckman]
participants: [Madina Gbotoe, Jodi, Da/Daya, Kirsten, Catherine]
---

# RegDes Regulatory AI Platform Demo

Demo of RegDes (reg-tech platform) for Danaher/Beckman team. Covered current AI capabilities, roadmap, and integration planning.

## Current AI Capabilities

### Translation Tool (newest release)
- Translates any document across ~50 languages including Japanese, Chinese, Hebrew
- Native language + translated text side-by-side, preserving original formatting
- Can translate specific pages rather than full document
- RegDes pre-translates laws they ingest for reg intel
- **Gap:** cannot output target language only — Danaher needs single-language output for submissions (e.g., Japanese-only dossiers). RegDes confirmed easy to build.

### Forms Module (GSPR/Tech Doc Builder)
- Pulls product metadata, SKUs, standards associations automatically
- AI suggests method-of-conformity based on behavior patterns (client-specific, not cross-client)
- Flags when referenced standard has new version — prompts user to decide whether to update
- **Gap:** Export currently PDF only; Danaher needs Word (editable) for ~200 SKUs and ~225 IVDR files. RegDes confirmed Word + PDF achievable.

### Application Builder (Submission Module)
- Templates maintained by RegDes, updated in real time per reg intel
- Autofill pulls documents from DMS if tagged — first submission can be 20-50% pre-populated
- AI suggests document tags when uploading via Application Builder
- Version flagging: if document updated in DMS mid-submission, system flags it
- Comments/collaboration: one assigned responder + one reviewer per section, unlimited commenters

## AI Roadmap (v6.0 — May 11 release)

### 1. Agentic AI ("Clara")
- Chat-based assistant; queryable in any language, responds in native language
- Queries both RegDes curated reg intel and live regulatory agency websites
- Daily automated health check on all source URLs — flags broken/changed links
- Data server-isolated per client — no cross-client data exposure
- Use cases already built: reliance pathway reports, gap assessments by tile/country
- **Danaher-specific agents** (querying past 510(k) deficiency responses) not yet built — would require Pablo (RegDes AI trainer) to develop and validate

### 2. Document Comparison Tool
- Compares old vs new versions of legislation or standards
- User must upload both versions (standards copyrighted, not stored by RegDes)

### 3. Actionable Reporting / Custom Analytics
- Users can ask Clara for any data slice (license expirations, submission status)
- Intended to reduce need for pre-built reports; Power BI integration still common
- 19 pre-built reports currently available

### 4. Maintenance Module (future — TBD)
- Workflows for device listings, establishment registrations, annual reports, CER updates
- CER literature search likely early use case
- UDI/EUDAMED: building metadata management for export — no machine-to-machine connection yet

## Key Technical Questions (Unresolved)

- AI model stack: confirmed OpenAI as of Oct 2025, may have changed
- Guardrails, hallucination handling, RAG architecture, training methodology — deferred to dev team
- Madina asked for written documentation / developer contact rather than requiring a call

## Cross-OpCo Data Sharing (Flagged Risk)

- Danaher stakeholders want to share past FDA deficiency responses and 510(k) learnings across OpCos
- Legal review required before enabling cross-OpCo data access
- RegDes confirmed technical capability exists; governance/roles TBD
- Flagged for next week's planning session

## Action Items

**RegDes:**
- Share full list of monitored regulatory source websites
- Connect Madina with developer for AI tech stack questions (written docs preferred)
- Build single-language-output option for translation tool
- Confirm Word export availability for forms/GSPR module
- Have Pablo develop Danaher-specific agent for 510(k) deficiency responses

**Danaher (Madina/Kirsten/Catherine):**
- Compile technical AI questions for RegDes dev team
- Discuss cross-OpCo data sharing with legal (Kirsten, Chris Roth)
- Next week: identify global process owner for standards update flagging, discuss integration approach and data migration hierarchy

## Key Sources

- [[projects/github-copilot-adoption|GitHub Copilot Adoption]] (broader AI enablement context)
