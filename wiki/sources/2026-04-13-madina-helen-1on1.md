---
name: Madina <> Helen 1:1 — Signal Framework & Product Prioritization
source_type: transcript
date: 2026-04-13
meeting_type: 1:1
participants: [Madina Gbotoe, Helen Kupp]
tags: [wdai, cpo, product-signal, prioritization, value-scoring]
granola_id: 26397983-c862-468f-9418-e25f8f4f5b0e
---

# Madina <> Helen 1:1 — Signal Framework & Product Prioritization

Follow-up to the Mar 30 CPO framework discussion. Madina presented her signal detection + value scoring work; Helen provided strategic direction on prioritization philosophy.

## Signal Detection Framework Review

### What Madina Built
- Agent-based signal detection scanning WDAI Slack for product/tool signals
- Gumloop v0 was too wide — picked up MailChimp, LinkedIn, etc. — descoped to focus
- New version classifies signals: standalone vs deeply integrated
- Each signal gets a value score: member impact, ops impact, brand impact, uniqueness
- Links back to source conversations for traceability

### Helen's Feedback on Approach
- **Lean less on automation, more on judgment** — given limited capacity, the goal is fewer projects done well, not more projects surfaced
- Signal scanner is good for catching conversations they might miss, but not for generating a huge backlog
- Default stance: "We cannot take on very much" — capacity is the binding constraint
- Don't think of it as marketing sourcing ideas; think of it as CPO triage

### Product Spectrum Status
- **Built/standalone items** (portal, Google Meet, Meet-to-Vimeo pipeline, MailChimp automation, weekly dashboard, Pattern bot) — all fine, no action needed
- **Deeply integrated items** — these are the ones worth discussing:
  - Redesign intros/matching (currently Gumloop, should integrate into portal)
  - Customer support bot (Helen thinks they need one, but scoping is the hard part)
  - Leaders training system
- Biggest bottleneck is **product scoping, not coding** — that's Madina's pitch to herself

### Value Scoring Discussion
- Helen's key reframe: **ops impact should weigh more than member impact** for prioritization
- Things that save operational time (Helen, Lauren, Brigitte) compound — they free up capacity to do more
- Member-facing features are important but shouldn't outrank things that reduce operational drag
- "Anything that makes it on the list means you would have eyes on it — do you want eyes on that many things?"
- Goal of the framework: help them cut, not add

### Volunteer Engagement Model
- Standalone prototypes: volunteers can build without repo access, just need schema
- Graduation path: prototype → read access to Supabase → commit access to codebase
- Trigger for access escalation: case-by-case, but classification helps scope decisions
- Regional matching feature: example of something volunteers could prototype standalone first

### Decisions
- **Value scoring: ops impact first** — flip priority so operational efficiency outranks member-facing features (previously captured as [[decisions/2026-04-13-value-scoring-ops-first]])
- **Framework purpose is cutting, not adding** — prioritization should reduce scope, not expand it
- Core team members should each apply their own judgment to the signal list — serves as VOC for strategic alignment

### Personal Notes
- Dina mentioned potential summer travel (2 trips foreseen)
- Manager (Martin) keeps pulling her into new things — "doing my job well or enjoying my company"
- Helen had to jump to a 1:1 with Brigitte after this call

## Cross-References
- [[decisions/2026-04-13-value-scoring-ops-first|Value Scoring — Ops Impact First]]
- [[projects/wdai-product-signal-detector|WDAI Product Signal Detector]]
- [[projects/wdai-platform|WDAI Platform]]
- [[people/helen-kupp|Helen Kupp]]
- [[organizations/wdai|Women Defining AI]]
- [[sources/2026-03-30-madina-helen-1on1|Previous Helen 1:1 (Mar 30)]]
