# AI Governance Taxonomy — Industry Crosswalk Research

**Date:** 2026-04-22
**Purpose:** Pressure-test draft 20-topic taxonomy against tool vendors, published crosswalks, and enterprise policies.

---

## 1. Tool Taxonomy Comparison

| Draft topic | OneTrust | Credo AI | Trustible | Holistic AI | Collibra | IBM watsonx.gov | AWS | AI Verify (SG) |
|---|---|---|---|---|---|---|---|---|
| prohibited_practices | Intake gate | Policy Pack | Risk intake | — | Risk template | — | — | — |
| ai_literacy_training | — | — | — | — | — | — | — | — |
| risk_classification | Lifecycle checkpoints | Risk/impact | Attribute-based risk engine | Red/Amber/Green | Risk levels | — | — | Bounding risk |
| risk_management_system | Evaluate AI risk | Controls layer | Orchestration | Risk verticals | Risk/controls | Risk categories | Governance | Bounding |
| data_governance_quality | Asset inventory | Privacy/fairness | Risk intake | — | Data lineage tie-in | Data mgmt | — | Data (dim) |
| technical_documentation | Model cards | Reports | Vendor docs | — | Asset metadata | Model facts | Service Cards | — |
| logging_traceability | Continuous monitor | — | MLOps integration | — | Lineage | Drift/quality monitor | — | Incident reporting |
| transparency_explainability | Transparency dashboards | Transparency | — | Transparency vertical | — | Explainability | Explainability + Transparency (2 sep.) | — |
| human_oversight | Governance committees | Controls | Approvals workflow | — | Approvals | Workflows | Controllability | Accountability |
| accuracy_robustness_cybersecurity | Perf monitoring | Security (separate) | — | Efficacy + Robustness (split) | — | Performance | Safety + Veracity/Robustness + Security (3 sep.) | Security + Testing |
| conformity_assessment | Assessment workflows | Policy Pack report | Audit docs | Red/Amber/Green | Assessments | Compliance mapping | Audit Manager | Testing/Assurance |
| post_market_monitoring | Real-time monitor | — | — | — | — | Drift | — | Incident reporting |
| incident_management | Real-time alerts | — | — | — | — | Alerts | — | Incident reporting |
| third_party_vendor_risk | — | — | Vendor eval | — | — | — | — | — |
| governance_accountability | AI governance | Governance Graph | Governance program | — | Operating model | — | Governance | Accountability |
| privacy_data_protection | Privacy (core OneTrust) | Privacy (separate) | — | Privacy vertical | — | Privacy IA | Privacy/Security | — |
| clinical_safety (FDA) | — | — | — | — | — | — | — | — |
| predetermined_change_control | — | — | — | — | — | — | — | — |
| aims_scope_policy (ISO) | — | — | — | — | — | — | — | — |
| genai_model_obligations | GenAI monitor | Policy Pack | Yes | — | — | GenAI guardrails | Bedrock Guardrails | GenAI framework |
| **Missing from draft — bias/fairness** | Standalone | Standalone (1 of 16) | Standalone | **Standalone (top vertical)** | — | Bias monitor | **Standalone (Fairness)** | — |
| **Missing — environmental/sustainability** | — | — | — | — | — | — | **Standalone (Sustainability)** | AI for Public Good |
| **Missing — safety/content harms** | — | Standalone | — | — | — | Toxic/abusive filters | **Standalone (Safety)** | Safety+Alignment R&D |
| **Missing — content provenance** | — | — | — | — | — | — | — | **Standalone** |
| **Missing — inventory/intake** | **Core pillar** | Governance Graph | **Core pillar** | — | **Core pillar** | Catalog | — | — |

Key patterns:
- **Bias/fairness is a top-level category in 5 of 8 tools** (Credo, Holistic AI explicitly, AWS, IBM, widely in NIST). My draft folds this into data_governance_quality — contra industry practice.
- **AWS splits accuracy/robustness/cybersecurity into 3 categories** (Safety, Veracity & Robustness, Privacy & Security); Holistic splits into Efficacy + Robustness + Privacy. EU Art. 15 bundles them; practitioners routinely split.
- **AI inventory / use-case intake is a top-level pillar in OneTrust, Trustible, Collibra** — not present in my draft. (Arguably an *activity*, not a topic; but vendors treat it as a bucket.)
- **AI literacy/training** (EU Art. 4) not appearing as a distinct tool category anywhere surveyed.
- **Third-party/vendor risk** only explicit in Trustible and ISO 42001 (A.9). OneTrust folds into general vendor risk module.

---

## 2. Crosswalk Findings

**Official NIST-published crosswalks** ([airc.nist.gov/airmf-resources/crosswalks](https://airc.nist.gov/airmf-resources/crosswalks/)): NIST publishes several, including NIST AI RMF ↔ ISO/IEC 42001. The join key is the **NIST Govern / Map / Measure / Manage** function structure mapped to ISO 42001 clauses and Annex A controls.

**Practitioner crosswalks mapping all three (EU AI Act ↔ NIST AI RMF ↔ ISO 42001):**
- [euaicompass EU AI Act vs ISO 42001 vs NIST](https://euaicompass.com/eu-ai-act-iso-42001-nist-ai-rmf-crosswalk.html) — uses EU AI Act articles (8–15) as join key, with ISO 42001 controls and NIST functions mapped in.
- [RSI Security crosswalk](https://blog.rsisecurity.com/nist-ai-risk-management-framework-iso-42001-crosswalk/) — uses NIST functions (Govern/Map/Measure/Manage) as join key.
- [CSA: using ISO 42001 + NIST AI RMF for EU AI Act compliance](https://cloudsecurityalliance.org/blog/2025/01/29/how-can-iso-iec-42001-nist-ai-rmf-help-comply-with-the-eu-ai-act)
- [EC Council plain-English comparison](https://www.eccouncil.org/cybersecurity-exchange/responsible-ai-governance/eu-ai-act-nist-ai-rmf-and-iso-iec-42001-a-plain-english-comparison/)
- [FairNow NIST↔ISO 42001 practical guide](https://fairnow.ai/map-nist-ai-rmf-iso-42001/)
- [ResearchGate control crosswalk table](https://www.researchgate.net/figure/Control-crosswalk-to-NIST-AI-RMF-EU-AI-Act-ISO-42001_tbl2_397089419)

**Surprise finding:** there is **no consensus join-key taxonomy**. The two dominant conventions:
1. **EU AI Act Articles 9–15 as the join spine** (Risk Mgmt, Data Governance, Technical Doc, Record-Keeping, Transparency, Human Oversight, Accuracy/Robustness/Cybersecurity). My draft topics 3–10 closely mirror this spine — that's the "industry" backbone.
2. **NIST Govern/Map/Measure/Manage** — lifecycle-based, not topic-based.

No FDA ↔ ISO 42001 ↔ EU AI Act crosswalk surfaced from major law firms (Baker McKenzie, Cooley, Norton Rose not returning hits). FDA content is treated in isolation in the sources found.

---

## 3. Enterprise Policy Structure

**Microsoft Responsible AI Standard v2** ([PDF](https://cdn-dynmedia-1.microsoft.com/is/content/microsoftcorp/microsoft/final/en-us/microsoft-brand/documents/Microsoft-Responsible-AI-Standard-General-Requirements.pdf)): 17 goals grouped under 6 principles — Accountability (Impact Assessment, Oversight, Fit for Purpose, Data Governance, Human Oversight), Transparency (Intelligibility, Communication), Fairness, Reliability & Safety, Privacy & Security, Inclusiveness.

**Pfizer AI Policy Position** ([PDF](https://cdn.pfizer.com/pfizercom/AI_Policy_Position_12112023.pdf)): Human-centered, Privacy, Transparency, Accountability, Safety/Validity/Security, Equity.

**Novartis Responsible Use of AI** ([PDF](https://www.novartis.com/sites/novartis_com/files/novartis-responsible-use-of-ai-systems.pdf)): 4 principles + EU-AI-Act-aligned risk classification (low/mid/high/forbidden), Ethical Use of Data & Technology Policy, AI Handbook, AI Risk & Compliance Framework.

**Federal agencies under OMB M-25-21** (e.g., [DHS](https://www.dhs.gov/sites/default/files/2025-09/25_0926_cio_dhs_compliance_plan_for_omb_m-25-21_508.pdf), [Fed Reserve](https://www.federalreserve.gov/publications/files/compliance-plan-for-OMB-memorandum-m-25-21-202509.pdf), [State](https://www.state.gov/wp-content/uploads/2025/09/DOS-Compliance-Plan-with-M-25-21.pdf), [HHS](https://www.hhs.gov/sites/default/files/2025-hhs-ai-compliance-plan.pdf)): Driving AI Innovation, AI Governance, Agency Policies, Use Case Inventory, High-Impact Determinations, Risk Management Implementation, Waivers.

**Recurring cross-policy patterns:**
- Every enterprise policy has: **Accountability/Governance, Transparency, Fairness/Bias, Safety/Reliability, Privacy, Human Oversight**.
- **Fairness/bias is always a top-level bucket** in MS, Pfizer, Novartis, Google, and federal plans — never folded.
- **Inventory/use-case catalog** is the organizing axis in federal plans, not a topic bucket.
- **Impact assessment** shows up as a distinct artifact/process in MS and federal plans — more activity than topic.

---

## 4. Gaps & Surplus in Draft

**Gaps (missing):**
- **bias_fairness** — standalone in 5+ tools, all 4 enterprise policies surveyed, NIST AI RMF ("Valid and Reliable" + "Fair with Harmful Bias Managed"), ISO 42001 A.6.2. Strong evidence this should be lifted out of data_governance_quality.
- **safety_content_harms** — NIST GenAI Profile lists Dangerous/Violent/Hateful Content, Obscene Content, CBRN Capabilities as distinct risks ([NIST AI 600-1](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf)). Currently unrepresented; could fold into genai_model_obligations but only covers the GenAI surface.
- **ai_system_inventory** — OneTrust/Trustible/Collibra/federal plans treat as core pillar. Arguably an orthogonal axis to "topics," but worth considering.

**Surplus (weakly supported):**
- **ai_literacy_training** — EU Art. 4 creates the obligation but no tool surveyed treats it as a category. Could be a single policy item rather than a full topic. Keep if EU-Act fidelity matters; cut if condensing.
- **conformity_assessment** — distinctive to EU AI Act; tools fold into "assessment workflows." Reasonable to keep since your user is FDA+global, but be aware it rarely has crosswalk partners outside EU.
- **environmental/sustainability** — appears only in AWS and AI Verify. NIST AI 600-1 includes "Environmental Impacts." WEF/Salesforce pushing for reporting. **Weak** as a standalone in Fortune 500 enterprise policy, but emerging.
- **user_rights / individual_redress** — not in your draft and not a standard tool category. Present in GDPR-adjacent guidance and Article 85 of EU AI Act (right to lodge complaint). Usually folded into privacy.

**Bundled vs split mismatches:**
- **accuracy_robustness_cybersecurity** — EU Art. 15 bundles; AWS splits into 3; Holistic splits into 2. Practitioners routinely split. Recommendation: at minimum split **cybersecurity** out — it has its own lineage (NIST CSF, ISO 27001) and maps to different controls than accuracy/robustness.
- **logging_traceability** — your draft bundles; ISO 42001 keeps A.5 lifecycle separate from A.7 system information. Probably fine bundled for MVP.
- **transparency_explainability** — AWS splits; MS keeps as one "Transparency." Defensible either way; keep bundled.

**Framework-specific topics 17–20:**
- **clinical_safety (FDA)** — no vendor surveyed has this. It's real as a distinct concept for FDA-regulated systems but none of your crosswalks have a partner category. Keep as framework-specific.
- **predetermined_change_control (FDA)** — FDA-native concept ([FDA PCCP guidance](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/marketing-submission-recommendations-predetermined-change-control-plan-artificial-intelligence)). No non-FDA partners. Correctly isolated.
- **aims_scope_policy (ISO)** — maps to ISO 42001 Clause 4 + Annex A.2. Fine as isolated ISO topic; low crosswalk value.
- **genai_model_obligations** — both EU AI Act Art. 53/55 ([Art. 53](https://artificialintelligenceact.eu/article/53/), [Art. 55](https://artificialintelligenceact.eu/article/55/)) and NIST AI 600-1 cover this distinctly. Strong justification for its own bucket. Could split into systemic-risk-GPAI vs base-GPAI.

---

## 5. Confidence-Ranked Recommendations

**HIGH confidence:**
- **Lift bias_fairness out as a standalone topic.** Evidence: Microsoft RAI, Pfizer, Novartis, Google, NIST AI RMF trustworthy characteristics, NIST AI 600-1 "Harmful Bias/Homogenization," ISO 42001 A.6.2, AWS (Fairness), Holistic AI (Bias), Credo AI (Fairness). Source saturation is the highest in the dataset.
- **Split cybersecurity out of accuracy_robustness_cybersecurity.** Evidence: AWS (Privacy & Security separate), NIST AI 600-1 (Information Security distinct), ISO 42001 references ISO 27001 lineage, EU AI Act Art. 15 bundles but practitioner crosswalks routinely separate (RSI, FairNow).

**MEDIUM confidence:**
- **Add a content_harms / safety topic** distinct from genai_model_obligations. Evidence: NIST AI 600-1 lists CBRN, Dangerous/Violent/Hateful, Obscene content as distinct risks; AWS Bedrock Guardrails has 6 safeguard categories; AI Verify Singapore has Safety & Alignment R&D. Counter-evidence: most enterprise policies fold this under "Reliability & Safety."
- **Cut or demote ai_literacy_training.** Evidence: no vendor category; only EU Art. 4 requires it. Absence from enterprise policy structures suggests it's an *obligation* not a *topic*. Counter: keeping it lets you explicitly tag the EU requirement.
- **Consider explicit content_provenance topic** if GenAI-heavy (EU Art. 50 watermarking, AI Verify dimension, C2PA). Counter: can fold into transparency_explainability.

**LOW confidence:**
- **Add environmental_sustainability.** Evidence: NIST AI 600-1 (Environmental Impacts), AWS (Sustainability). Counter: not present in any Fortune 500 enterprise AI policy surveyed; emerging rather than established. For MVP, likely skip.
- **Add explicit user_rights topic.** Evidence: EU AI Act Art. 85 right to complain; GDPR Art. 22 automated decision-making. Counter: almost universally folded into privacy_data_protection. Fold rather than split.
- **Add ai_system_inventory as topic or axis.** Evidence: OneTrust/Trustible/Collibra/federal plans treat as core. Counter: this is arguably the *object being governed* not a topic. Treat as data-model axis rather than taxonomy topic.

**Could not confirm from public sources:**
- OneTrust's exact internal control category list (beyond the 4 pillars surfaced: Build Inventory / Evaluate Risk / Monitor / Demonstrate Trust).
- Trustible's full "expert-curated taxonomy" of risks — described as such in vendor copy but specific category list not public.
- Govscape taxonomy — search returned AI Verify (Singapore) instead; unable to confirm Govscape as a real product/category set from public sources.
- Whether any Big 4 / major law firm has published an FDA ↔ EU AI Act ↔ ISO 42001 triple crosswalk (none surfaced).

---

## Sources (inline citations above, consolidated)

Tool vendors: [OneTrust AI Governance](https://www.onetrust.com/solutions/ai-governance/), [Credo AI Policy Intelligence](https://www.credo.ai/policy-intelligence), [Trustible](https://trustible.ai/), [Holistic AI Platform](https://www.holisticai.com/), [Collibra AI Governance](https://productresources.collibra.com/docs/collibra/latest/Content/AIGovernance/co_about-ai-governance.htm), [IBM watsonx.governance](https://www.ibm.com/products/watsonx-governance), [AWS Responsible AI](https://aws.amazon.com/ai/responsible-ai/) + [Bedrock Guardrails](https://aws.amazon.com/bedrock/guardrails/).

Frameworks: [NIST AI RMF Crosswalks hub](https://www.nist.gov/itl/ai-risk-management-framework/crosswalks-nist-artificial-intelligence-risk-management-framework), [NIST AI 600-1 GenAI Profile](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf), [ISO 42001 Annex A overview](https://orbit.reconn.io/iso-42001-controls-guide/), [EU AI Act Chapter III](https://artificialintelligenceact.eu/chapter/3/), [FDA AI/ML SaMD](https://www.fda.gov/medical-devices/software-medical-device-samd/artificial-intelligence-software-medical-device), [AI Verify Singapore](https://www.imda.gov.sg/resources/press-releases-factsheets-and-speeches/press-releases/2026/new-model-ai-governance-framework-for-agentic-ai).

Enterprise policies: [Microsoft RAI Standard v2](https://cdn-dynmedia-1.microsoft.com/is/content/microsoftcorp/microsoft/final/en-us/microsoft-brand/documents/Microsoft-Responsible-AI-Standard-General-Requirements.pdf), [Pfizer AI Policy](https://cdn.pfizer.com/pfizercom/AI_Policy_Position_12112023.pdf), [Novartis Responsible AI](https://www.novartis.com/sites/novartis_com/files/novartis-responsible-use-of-ai-systems.pdf), [Google AI Principles](https://ai.google/principles/), OMB M-25-21 plans (DHS/Fed Reserve/State/HHS linked inline).

Crosswalks: [euaicompass](https://euaicompass.com/eu-ai-act-iso-42001-nist-ai-rmf-crosswalk.html), [RSI Security](https://blog.rsisecurity.com/nist-ai-risk-management-framework-iso-42001-crosswalk/), [FairNow](https://fairnow.ai/map-nist-ai-rmf-iso-42001/), [CSA](https://cloudsecurityalliance.org/blog/2025/01/29/how-can-iso-iec-42001-nist-ai-rmf-help-comply-with-the-eu-ai-act), [EC Council](https://www.eccouncil.org/cybersecurity-exchange/responsible-ai-governance/eu-ai-act-nist-ai-rmf-and-iso-iec-42001-a-plain-english-comparison/).

Word count: ~2,370
