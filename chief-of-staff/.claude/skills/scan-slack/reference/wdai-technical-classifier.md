---
name: wdai-technical-classifier
description: 'Classifies WDAI-adjacent projects onto the technical spectrum: Deeply
  Integrated / Middle Ground / Standalone / Unclear. Use whenever a qualifying project
  needs spectrum classification before scoring its strategic value.'
---

## Formatting Principle
Each output has three parts — all three are required:

WHAT: 2-3 sentences describing what the project actually
does, who built it, what problem it solves, and any
relevant context about its current state or scope.
This must be specific enough for Madina to brief Helen
without needing to look up the original message.

WHY: One sentence on which question triggered this
classification and the key reason.

DECISION: One specific actionable yes/no question.
Not vague. Not general. The exact call Madina needs to make.

## The 5-Question Framework
Run in order. Stop at the first clear answer.

Q1 — Member data dependency
Needs WDAI portal login, member records, profiles,
directory data, or Supabase database access?
→ YES → 🔴 Deeply Integrated
→ NO → Q2

Q2 — WDAI system dependency
Needs to connect to: Slack (WDAI workspace), MailChimp/WDAI
email lists, WDAI GitHub repo, portal content, or any
WDAI-owned infrastructure?
→ YES → 🟡 Middle Ground
→ NO → Q3

Q3 — Self-contained test
Can it be deployed independently, used without WDAI
credentials, maintained by its builder, and linked as
an external resource?
→ YES to all → 🟢 Standalone
→ NO to any → Q4

Q4 — Ownership
If this breaks, who fixes it?
→ WDAI core team → bumps toward 🔴 or 🟡
→ Original builder → stays 🟢
Q4 overrides Q3 if they conflict.

Q5 — Scale sensitivity
Needs to grow as WDAI membership grows?
→ YES → bumps one level toward 🔴
→ NO → stays at current

If still unclear after all five → ❓ Unclear

## Middle Ground Rule
🟡 items: decision owner is always Madina alone.
Never assign to a group or to Helen.
Always state the specific decision needed.

## Output Format
Return exactly this every time:

SPECTRUM: [🔴 Deeply Integrated / 🟡 Middle Ground /
           🟢 Standalone / ❓ Unclear]

WHAT: [2-3 sentences — what it does, who built it,
what problem it solves, current state/scope]

WHY: [One sentence — which question triggered it and
the key reason]

DECISION NEEDED: [One specific yes/no question Madina
needs to answer — or "None"]
