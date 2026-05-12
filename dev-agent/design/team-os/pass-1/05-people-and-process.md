# Pass 1 · People and process

**Part of the Pass 1 split.** See `01-system-context.md` for framing, the 7 Pass-3 design questions, and the C4 system overview. This file is one of the supplementary surfaces.

**Important framing:** "team-OS" throughout these documents refers to a **proposed future federation** that Pass 3 will design. It does not exist today. Phrasings like "Pass 3 must X" mean "X is a constraint surfaced by current state."

---

## People and process

### Persona tooling map (#8)

What each core team member currently uses. Pre-team-OS baseline.

| Person | Identity | Daily tools today | Has agent? | Granola? | GitHub touch | Linear access | What's missing |
|--------|----------|-------------------|------------|----------|--------------|---------------|----------------|
| **Helen** | Superuser | Slack admin · GWorkspace admin · all repos · Stripe · Mailchimp · Luma · Vercel · Railway · Cursor + Claude Desktop + Cowork + OpenClaw on Mac mini | **3** (Syl, Pattern, Wit) | Yes (Business plan ended Apr 7, status TBD) | All repos write + Pattern publishes weekly report | **Yes — MCP-connected** (Feb 4) · uses for long-living tech work | Maintenance bandwidth |
| **Madina** | Tech lead | Slack · GitHub write · Cursor · OpenClaw on Windows · cloud cron · wiki · context-mode | **2** (Atlas, Polaris) | Yes | All WDAI repos write + own `mgbotoe/agents` | **Unknown** — proposed May 9 to be central; current direct-use unconfirmed | Slack admin · GWorkspace admin |
| **Brigitte** | COO | Slack · GWorkspace admin · Google Docs (planning agendas) · Granola (Helen-routed via Atlas) · `mailchimp-cc` PRs · meeting docs | No | Maybe (Helen routes via Atlas) | Only `mailchimp-cc` PRs | **No** — explicitly flagged "Linear write" as missing | Direct GitHub admin · agent of her own · Linear write |
| **Lauren** | Programs lead | Slack admin · Luma · Mailchimp · Granola · meeting docs · course coordination | No | Yes | None | **Unknown** | Agent · GitHub write · likely Linear |
| **Sandhya** | Marketing lead | Slack · Gumloop fluency · Cursor (learning) · GWorkspace · meeting docs | No | Yes | Git onboarding in progress | **Unknown** | Agent · stable git workflow · CLAUDE.md authoring |
| **Sheena** | Marketing co-lead | Slack · `mailchimp-cc` PRs · GWorkspace · learning agent/Claude stack | **No — zero state** | Yes (uses read.ai for some meetings) | `mailchimp-cc` PRs only | **Unknown** | Everything beyond Slack + Mailchimp |
| **Rita** | UX / brand | Slack · Google Docs · brand collateral · meeting docs | No | Yes | None | **Unknown** | Agent · brand-skill home |
| **Rebekah** | Backend SME · consulting | Slack · GitHub (likely) · PostHog (her domain) | No | Likely | Read access for code review (consulting) | **Unknown** | Formal seat at team-OS contributor table TBD |

**Linear coverage finding:** only Helen has confirmed Linear access today (with MCP integration). Madina's May 9 proposal to make Linear the central source-of-truth would require provisioning everyone in this table with seats. Currently 7 of 8 rows are "Unknown" — that's a coordination gap that any Pass 3 design including Linear would have to solve.

**Concentration:** Helen + Madina hold all the agent setups. Sheena has nothing. Brigitte/Lauren/Sandhya have surface-level fluency but no agent layer.

**Caveats on this table:**
- **Rebekah row** is partially inferred — "Slack · GitHub (likely)" — I have not directly confirmed her GitHub access scope.
- **Rita row** is mostly inferred — her tooling is not documented in any source I have direct access to.
- **Sheena's "PRs to mailchimp-cc"** are confirmed (multiple Apr/May references); the *independent commit capability* is unverified — she may have been pair-PR'ing with Helen.
- **Brigitte's "Granola (Helen-routed via Atlas)"** — Brigitte appears in transcripts Atlas routes, but whether Brigitte personally uses Granola is unconfirmed.

### Stakeholder expectations — INFERRED PROFILES (#15)

**This is not a verified expectation matrix. It is a set of straw-man profiles inferred from observed behavior.** Each row is a starting hypothesis that Pass 3 should confirm via direct conversation before designing toward it.

Only **Helen** and **Madina** have directly stated their expectations (Helen via her design doc and the May 11 call; Madina via this entire conversation and her Apr 14 #team-core post). All other rows are inference, regardless of source quality.

| Person | Inferred expectation | Source quality |
|--------|----------------------|----------------|
| **Helen** | Federated knowledge layer · team can operate "if everyone quit tomorrow" · reduce her bottleneck status · Cowork-based runtime preference | DIRECT — design doc + May 11 call verbatim |
| **Madina** | Cross-repo dependency visibility · cloud-cron-based runtime preference · Linear as central source-of-truth · per-pillar tool ownership | DIRECT — Apr 14 #team-core post + this conversation |
| **Brigitte** | Lower friction to contribute to programs ops · clear decision log · less Helen-as-bottleneck | INFERRED — from Apr 1 core team sync recap (Madina-summarized) and Brigitte's COO role pattern. Brigitte has not stated this directly to me |
| **Lauren** | Programs workflow clarity · less ad-hoc Slack scatter · clear cohort kickoff playbook | INFERRED — from Programs lead role and Mar 14 SDLC workshop coordination. Lauren has not stated this |
| **Sandhya** | Marketing tools discoverable and not in Helen's head · brand skill exists at repo level | INFERRED — from Mar 26 "Is there a WDAI brand kit / skill?" Slack post + her wdai-marketing pillar leadership |
| **Sheena** | Onboarding path to existing infra · mailchimp-cc PR flow as first foothold | INFERRED — from her May 10 "still in reading phase" post. Her actual expectations from team-OS unstated |
| **Rita** | Brand consistency across pillars · UX work visible | INFERRED — from her UX/brand role. No direct stated expectation captured |
| **Rebekah** | Better instrumentation hygiene · engineering review discipline | INFERRED — from her Mar 23 PostHog proposal review |

**Six of eight rows are inference.** Pass 3 cannot trust the inferred rows as ground truth. Direct stakeholder interviews would replace inference with evidence.

---
