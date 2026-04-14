---
name: wdai-strategic-value-scorer
description: Scores the strategic value of a WDAI project and returns a recommended
  action from the decision matrix. Use after spectrum classification is complete to
  determine what WDAI should do with the project. Takes project description and spectrum
  as input.
---

## Formatting Principle
Each output has three parts — all three are required:

CONTEXT: 2-3 sentences on why this project matters
to WDAI right now — what gap it fills, what opportunity
it represents, or what risk it addresses. This is the
"so what" that makes the score meaningful.

SCORE: The breakdown and tier — tight and factual.

ACTION: The recommended action and one sentence on
what Madina specifically needs to decide or confirm.

## Two Scoring Scales
🔴 + 🟡 → V1–V4 only. Max = 8.
Low = 0–2 · Medium = 3–5 · High = 6–8

🟢 → V1–V5. Max = 10.
Low = 0–3 · Medium = 4–6 · High = 7–10

Score each: 2 = strong yes · 1 = partial · 0 = no

## For 🔴 and 🟡 — V1 to V4
V1 Member impact: helps members learn/connect/build
in portal or community?
2 = clear direct impact · 1 = some benefit · 0 = none

V2 Ops impact: saves core team time or improves
how WDAI runs operationally?
2 = significant savings · 1 = minor improvement · 0 = none

V3 Brand signal: makes WDAI look more AI-native,
innovative, or credible externally?
2 = strong visible signal · 1 = moderate · 0 = none

V4 Uniqueness: does WDAI already have something like this?
2 = nothing like it · 1 = similar but better · 0 = duplicate

## For 🟢 Standalone — V1 to V5
V1 Member impact: would members actively use this
even though it lives outside the portal?
2 = clear direct usage · 1 = some would · 0 = unlikely

V2 Ops impact: solves a real WDAI community problem
without core team maintaining it?
2 = yes, hands-off · 1 = partially · 0 = none

V3 Brand signal: showcases WDAI community talent
and innovation externally?
2 = strong external showcase · 1 = moderate · 0 = none

V4 Uniqueness: solving something nobody else in the
WDAI ecosystem has solved yet?
2 = completely novel · 1 = similar but better · 0 = covered

V5 Integration potential: could this realistically
become a portal feature if it gains traction?
2 = clear path to integration · 1 = possible but uncertain
0 = truly standalone forever

## Decision Matrix
🔴 Low → Descope · Medium → Roadmap Q3+ · High → Build it
🟡 Low → Monitor 60 days · Medium → Partner · High → Claim it
🟢 Low → Archive · Medium → Resources page · High → Claim domain
❓ → Cannot score. Clarify spectrum first.

## Output Format
Return exactly this every time:

CONTEXT: [2-3 sentences on why this project matters
to WDAI right now — the gap, opportunity, or risk]

SCORE: [total] / [max — 8 or 10]
BREAKDOWN: V1=[x] V2=[x] V3=[x] V4=[x] V5=[x if standalone]
VALUE TIER: [Low / Medium / High]

RECOMMENDED ACTION: [action from matrix]

MADINA DECISION: [One specific question Madina needs
to answer to confirm or act on this recommendation —
or "None, recommendation is clear"]
