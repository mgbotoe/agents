# Pass 1 · People and process

**Part of the Pass 1 split.** See `01-system-context.md` for framing, the 7 Pass-3 design questions, and the C4 system overview. This file is one of the supplementary surfaces.

**Important framing:** "team-OS" throughout these documents refers to a **proposed future federation** that Pass 3 will design. It does not exist today. Phrasings like "Pass 3 must X" mean "X is a constraint surfaced by current state."

---

## People and process

### Persona tooling map (#8)

What each core team member currently uses. Pre-team-OS baseline.

| Person | Identity | Daily tools today | Has agent? | Granola? | GitHub touch | Linear access | What's missing |
|--------|----------|-------------------|------------|----------|--------------|---------------|----------------|
| **Helen Lee Kupp** | Executive Director · Founder | Slack admin · GWorkspace admin · all repos · Stripe · Mailchimp · Luma · Vercel · Railway · Cursor + Claude Desktop + Cowork + OpenClaw on Mac mini | **3** (Syl, Pattern, Wit) | Yes (Business plan ended Apr 7, status TBD) | All repos write + Pattern publishes weekly report | **Yes — MCP-connected** (Feb 4) · uses for long-living tech work | Maintenance bandwidth |
| **Madina Gbotoe** | AI PM & Infrastructure | Slack · GitHub write · Cursor · OpenClaw on Windows · cloud cron · wiki · context-mode | **2** (Atlas, Polaris) | Yes | All WDAI repos write + own `mgbotoe/agents` | **Unknown** — proposed May 9 to be central; current direct-use unconfirmed | Slack admin · GWorkspace admin |
| **Brigitte Lyons** | COO (formalized at Feb 17 board meeting) | Slack · GWorkspace admin · Google Docs (planning agendas) · Granola (Helen-routed via Atlas) · `mailchimp-cc` PRs · meeting docs | No | Maybe (Helen routes via Atlas) | `mailchimp-cc` PRs (e.g. PR #12 — pre/post-assessment emails); driving cohort registration migration off Luma | **No** — explicitly flagged "Linear write" as missing | Direct GitHub admin · agent of her own · Linear write |
| **Lauren Irving** | Programs Lead | Slack admin · Luma · Mailchimp · Granola · meeting docs · course coordination | No | Yes | None | **Unknown** | Agent · GitHub write · likely Linear |
| **Sandhya Simhan** | Marketing Pillar Lead | Slack · Gumloop fluency · Cursor (learning) · GWorkspace · meeting docs · `mailchimp-cc` commits (e.g. `.env.example` removal) | No | Yes | Git onboarding in progress | **Unknown** | Agent · stable git workflow · CLAUDE.md authoring |
| **Sheena Miles** | Marketing co-lead | Slack · `mailchimp-cc` PRs (`sheenam112` / Sheena Miles — PRs #8, #9, #11) · GWorkspace · learning agent/Claude stack | **No — zero state** | Yes (uses read.ai for some meetings) | `mailchimp-cc` PRs only | **Unknown** | Everything beyond Slack + Mailchimp |
| **Rita Hokstad** | User Experience Lead | Slack · Google Docs · brand collateral · meeting docs · quarterly member surveys | No | Yes | None | **Unknown** | Agent · brand-skill home |
| **Rebekah** | Backend SME · consulting | Slack · GitHub (likely) · PostHog (her domain) | No | Likely | Read access for code review (consulting) | **Unknown** | Formal seat at team-OS contributor table TBD |

**Linear coverage finding:** only Helen has confirmed Linear access today (with MCP integration). Madina's May 9 proposal to make Linear the central source-of-truth would require provisioning everyone in this table with seats. Currently 7 of 8 rows are "Unknown" — that's a coordination gap that any Pass 3 design including Linear would have to solve.

**Concentration:** Helen + Madina hold all the agent setups. Sheena has nothing. Brigitte/Lauren/Sandhya have surface-level fluency but no agent layer.

**Caveats on this table:**
- **Rebekah row** is partially inferred — "Slack · GitHub (likely)" — I have not directly confirmed her GitHub access scope.
- **Rita row** is mostly inferred — her tooling is not documented in any source I have direct access to.
- **Sheena's "PRs to mailchimp-cc"** are confirmed (multiple Apr/May references); the *independent commit capability* is unverified — she may have been pair-PR'ing with Helen.
- **Brigitte's "Granola (Helen-routed via Atlas)"** — Brigitte appears in transcripts Atlas routes, but whether Brigitte personally uses Granola is unconfirmed.

### Stakeholder expectations — INFERRED PROFILES (#15)

**Updated 2026-05-12** from Drive's `WDAI Core Team: Personal Operating Manuals` (Helen-owned, Feb 6-9). All 6 named core team members wrote self-statements covering strengths, communication style, what helps them work, what trips them up, and personal context. Excerpts below are paraphrased; full text in Drive.

| Person | Self-stated working style (Feb 9) | Self-stated friction | Source quality |
|--------|------------------------------------|------------------------|----------------|
| **Helen** | Async + Slack first. Strength: zero-to-one. Stated 2026 intent: "shift focus away from tinkering and more towards nonprofit leadership and stewardship... nearly entirely focused on finding sources of funding." **Reality May 2026:** still actively tinkering (writing AI Intermediate content, running technical reviews) — the transition is intent-stated, not yet observable in behavior. | "I take on a lot... that might look like I expect the same of you, and that is not true." | DIRECT — Personal Operating Manual + May 11 conversation |
| **Madina** | Async first. "Give me the full picture upfront... prefer autonomy to execute." Direct, sometimes reads as pushback. ESL. | "Deadlines for the sake of having them is how you lose my interest." | DIRECT — Personal Operating Manual + this conversation |
| **Brigitte** | Async, no overscheduling, no evenings/weekends. "Strong opinions loosely held." Asks "what are we trying to accomplish" first. "How did the system fail us?" not blame. | "Lack of enthusiasm" misread for grounded goal-setting (no BHAGs). | DIRECT — Personal Operating Manual |
| **Lauren** | Available after 2pm PT, flexible from 9am. Comfortable across Slack/email/Zoom. L&D background. "I tend to step into work that others don't want to do." | "Doesn't always put myself first... building for others before investing in my own growth." | DIRECT — Personal Operating Manual |
| **Sandhya** | Slack + async default. Mornings 6-7:30am + 8:30-9:30am PT (West Coast). **Most WDAI work happens weekends** — day job is building customer marketing at fast-growing company. Thinks in systems/frameworks. | "Naturally think in systems and frameworks. This can sometimes feel like I am slowing things down when the instinct is to move quickly." | DIRECT — Personal Operating Manual |
| **Rita** | Standard PST business hours. Slack quick / email structured / async preferred. Marketing + database + email expertise. | "Can be concise, even curt at times. That reflects efficiency and focus." | DIRECT — Personal Operating Manual |
| **Sheena** | (Did not author a Personal Operating Manual in the doc Helen circulated Feb 6-9.) | — | INFERRED — Sheena's working style from `mailchimp-cc` PRs + May 10 "still in reading phase" Slack post |
| **Rebekah** | (Not in Personal Operating Manual doc — she's consulting, not core team.) | — | INFERRED — from her Mar 23 PostHog proposal review |

**Six of eight rows now have DIRECT source quality** (up from 2 of 8 in v5). Sheena and Rebekah remain inference. The big shift: stakeholder behavior preferences are no longer hypothesis — they're documented in Helen's onboarding ritual.

**Critical nuance:** Helen's Personal Operating Manual states her 2026 intent (shift away from tinkering), but her actual May behavior (writing AI Intermediate content, running technical reviews of mailchimp-cc PRs, sitting with title placement decisions in real-time) shows the transition is not yet underway. **Pass 3 must design for current Helen, not stated-intent Helen.**

---
