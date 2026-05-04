---
name: Crosswalk QA findings
description: Applicability gate behavior, evidence integrity bug (map-single fda_6_1), and external-policy live QA results (3 real policies + MS RAI baseline)
type: project
---

Crosswalk hackathon gap-detector — QA session 2026-04-25.

Key findings: gate works directionally (1A=3 NA, 1B=1 NA, 1C=5 NA, all different sets). One confirmed evidence integrity violation: fda_6_1 excerpt synthesized from requirement text rather than commitment evidence_quote. MAP_PARALLEL=true path affected.

**Why:** MAP_PARALLEL=true uses map-single.ts which has stronger verbatim instruction but model still paraphrased for fda_6_1.

**How to apply:** When re-testing after fix, verify fda_6_1 specifically. Evidence chain check is mechanical — use acmecorp.test.ts norm+substring pattern.

---

## External Policy Live QA — 2026-04-26 (submission eve)

Tested 3 real external policies + Microsoft RAI baseline on https://crosswalk-khaki.vercel.app/

| Policy | Frameworks | Commitments | Covered | Partial | Missing | N/A | Coverage | Time |
|--------|-----------|-------------|---------|---------|---------|-----|----------|------|
| Anthropic AUP | EU AI Act | 61 | 4 | 5 | 11 | 0 | 20% | 3m 08s |
| IBM AI Ethics | EU AI Act + FDA SaMD | 7 | 2 | 5 | 22 | 1 | 7% | 2m 00s |
| Google AI Principles | EU AI Act + ISO 42001 | 11 | 1 | 13 | 17 | 0 | 3% | 2m 19s |
| Microsoft RAI (baseline) | EU AI Act | 90 | 10 | 4 | 6 | 0 | 50% | 4m 28s |

**Applicability gate (IBM × FDA SaMD × Technology/Provider):** 1 not_applicable fired. Requirement: "Clinical expertise must be integrated throughout AI/ML device design, development, and evaluation." Rationale produced: "IBM is a general technology provider, not a medical device manufacturer." Gate verdict: WORKING.

**Voice match:**
- Anthropic AUP drafted: "For frontier models that may present systemic risks, Anthropic conducts model evaluations and adversarial testing (including red-teaming) prior to release and on an ongoing basis." — prose, first-person company voice.
- Microsoft RAI drafted: "### Goal A2a: ... **A2a.1** Assess each AI system during the Impact Assessment... Tags: Impact Assessment." — structured numbered-requirement format with tags.
Voice match confirmed working: qualitatively distinct styles.

**Merge UI:** 3 proposals in Google × EU AI Act + ISO 42001 run showed "Merge" button — Tier C cross-framework merge surface is reachable.

**Deployment concern:** Microsoft RAI (43K chars, 90 commitments) took 3m+ on Step 1 Extract alone. Large enterprise policies approach Vercel Hobby timeout territory.
