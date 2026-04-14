---
name: Atlas CoS Capability Recommendations
source_type: research
date: 2026-04-12
tags: [atlas, role-definition, recommendations, improvements]
depends_on: cos-role-research.md
---

# Atlas CoS Capability Recommendations

Based on [[sources/cos-role-research|Chief of Staff Role Research]], these are specific capabilities Atlas should add or refine, mapped to concrete implementation in Atlas's current architecture.

---

## 1. Formalize the Rhythm of Business (RoB)

**Gap**: Atlas has scheduled tasks but no documented operating rhythm that ties them together into a coherent system.

**Recommendation**: Create a `config/rhythm-of-business.md` file that defines:

- **Daily rhythm**: Morning Brief (already exists) → Midday Check (exists) → Evening Wrapup (exists). Add: **pre-meeting briefing protocol** — what exactly gets included, in what order, with what lookback window.
- **Weekly rhythm**: Sunday WeeklyReview (exists). Add: **Monday priority-setting brief** — take Sunday's review and turn it into a concrete daily plan for the week. Add **Friday accountability check** — what was committed Monday, what actually shipped.
- **Monthly rhythm (NEW)**: Add `Atlas\MonthlyReview` scheduled task, 1st Sunday of each month. Content: project status across all active workstreams, budget/invoice review for WDAI, relationship health report, decisions made this month, carry-forward items.
- **Quarterly rhythm (NEW)**: Add `Atlas\QuarterlyPlan` scheduled task. Content: OKR scoring, next quarter goal-setting prep, career progress check against `dina-career-targets.md`, knowledge base audit.

**Implementation**: New scheduled tasks in `bin/scheduled/`, update CLAUDE.md scheduling table, create RoB config file.

---

## 2. Build a Follow-Up Tracking System

**Gap**: No systematic tracking of commitments made in meetings, emails, or conversations.

**Recommendation**: Add a `wiki/tracking/follow-ups.md` file (or a structured data file) with:

- **Source**: Where the commitment was made (meeting, email, conversation)
- **Owner**: Who owns it (Dina or someone else)
- **Due date**: When it's expected
- **Status**: Open / Done / Overdue / Escalated
- **Context link**: Wikilink to the meeting note, email thread, or decision

**Integration points**:
- `MeetingPrep` should scan follow-ups for items related to the upcoming meeting's attendees
- `MorningBrief` should surface overdue items
- `EveningWrapup` should flag items due tomorrow
- When processing Granola transcripts or email threads, auto-extract commitments and add to tracking

**Implementation**: New wiki tracking folder, update meeting prep and briefing skills to read from it.

---

## 3. Add Relationship Health Tracking

**Gap**: No monitoring of relationship maintenance — who Dina hasn't talked to, whose needs might be unmet, networking gaps.

**Recommendation**: Extend the wiki `people/` pages with structured metadata:

```yaml
last_contact: 2026-04-10
contact_cadence: weekly  # how often Dina should be in touch
relationship_type: manager | peer | report | mentor | client | recruiter
next_action: "Follow up on DLC conference proposal"
health: green | yellow | red
```

**Integration points**:
- `MorningBrief`: Surface any relationships where `last_contact` exceeds `contact_cadence`
- `WeeklyReview`: Include a "relationship health" section — who's gone quiet, who needs attention
- `MonthlyReview`: Full relationship map review — network gaps, dormant connections to reactivate

**Implementation**: Update people page schema in `wiki/SCHEMA.md`, add relationship scan to briefing skills, create a `/relationship-check` skill.

---

## 4. Implement an Anticipation Engine

**Gap**: Atlas is mostly reactive or on fixed schedules. A great CoS anticipates problems before they surface.

**Recommendation**: Add pattern-based proactive alerts in existing scheduled tasks:

- **Email patterns**: "You received 3 emails from [person] this week but haven't replied to any" or "This thread has been going back and forth 5 times — might need a call instead"
- **Calendar patterns**: "You have 6 hours of meetings tomorrow with zero prep time blocked" or "You haven't had a 1:1 with [report] in 3 weeks"
- **Project patterns**: "No wiki updates on [project] in 2 weeks — is it stalled?" or "The deadline for [deliverable] is in 5 days and the last status was 'in progress'"
- **Career patterns**: Cross-reference `dina-career-targets.md` with recent activity — "You said you wanted to present at a conference this quarter, but no submission is tracked"

**Implementation**: Add an `anticipation` section to `MorningBrief` and `EveningWrapup` task scripts. These checks query Gmail, GCal, and wiki data. Start with 3-4 simple pattern checks, expand over time.

---

## 5. Strengthen Strategic Advising Capability

**Gap**: Atlas advises on tasks but doesn't proactively analyze strategic alignment or surface priority conflicts.

**Recommendation**: Add to the `WeeklyReview` and proposed `MonthlyReview`:

- **Time allocation analysis**: How did Dina's calendar time split across workstreams (Danaher, WDAI, personal projects, career development)? Does it match stated priorities?
- **Priority conflict detection**: If Dina has 3 "top priorities," surface when they're competing for the same time slots or energy.
- **Decision backlog**: Track decisions that have been deferred more than twice — they're either not important (cut them) or being avoided (force the conversation).
- **Strategic nudges**: "You spent 15 hours on WDAI client work this week but zero on portfolio development — is that intentional?"

**Implementation**: Add calendar analysis to `WeeklyReview` script. Create a `wiki/tracking/priorities.md` that tracks stated priorities and actual time spent. Update briefing templates to include strategic alignment commentary.

---

## 6. Upgrade Email Triage to CoS-Grade

**Gap**: Email integration exists but unclear if it matches the depth of a great CoS email triage.

**Recommendation**: Define explicit email triage tiers:

- **Tier 1 — Respond now**: From key stakeholders (manager, skip-level, clients), time-sensitive, requires Dina's specific input
- **Tier 2 — Draft and queue**: Routine responses that Atlas can draft in Dina's voice for review
- **Tier 3 — FYI/archive**: Informational, newsletters, notifications — summarize and archive
- **Tier 4 — Ignore/unsubscribe**: Noise

**Integration points**:
- Use `dina-email-voice-profile.md` (already exists in sources) for draft generation
- Morning Brief should include Tier 1 items with draft responses ready
- Create a `/triage-inbox` skill that can be run on-demand
- Track response time patterns — alert if a VIP email has been sitting unanswered for >24 hours

**Implementation**: Create `config/email-triage-rules.md` with tier definitions and stakeholder lists. Update MorningBrief to include tiered email summary.

---

## 7. Add a Decision Log with Context

**Gap**: Wiki has a `decisions/` folder but no documented workflow for capturing decisions with the context a CoS should preserve.

**Recommendation**: Standardize the decision capture format:

```markdown
# Decision: [Title]
- **Date**: YYYY-MM-DD
- **Context**: What prompted this decision
- **Options considered**: What alternatives were evaluated
- **Decision**: What was decided and why
- **Owner**: Who's responsible for execution
- **Revisit date**: When to check if it's still the right call (optional)
- **Outcome**: (filled in later) What actually happened
```

**Integration points**:
- After meetings where decisions are made, prompt Atlas to capture them
- `MonthlyReview` should include "decisions made this month" summary
- When a topic comes up again, Atlas should search decisions/ first and surface prior decisions — preventing re-litigation (this is explicitly called out in CLAUDE.md as "decision memory")

**Implementation**: Update `wiki/SCHEMA.md` with decision template. Add decision extraction to meeting follow-up workflow.

---

## 8. Build a Proactive Nudge System

**Gap**: "Proactive nudges" is listed in CLAUDE.md responsibilities but lacks a concrete implementation.

**Recommendation**: Define nudge categories and triggers:

| Category | Trigger | Example |
|----------|---------|---------|
| Stalled work | No wiki/git activity on a project in 7+ days | "Haven't seen movement on the portfolio site — want to reprioritize?" |
| Overdue items | Follow-up past due date | "You owed Martin a response on the DLC proposal by Wednesday" |
| Relationship gap | Last contact exceeds cadence | "It's been 3 weeks since you talked to Helen" |
| Deadline approaching | Calendar event or due date within 3 days | "The Danaher AI presentation is Friday — want to do a dry run?" |
| Career goal drift | Weekly hours don't match stated priorities | "Zero hours on interview prep this week — you said that was a Q2 priority" |
| Health/balance | 8+ hours of meetings in a day | "Tomorrow is wall-to-wall meetings — want me to move something?" |

**Implementation**: Create `config/nudge-rules.md` with categories and thresholds. Integrate into `MorningBrief`, `MiddayCheck`, and `EveningWrapup` scripts.

---

## 9. Add a "No-Surprises" Protocol

**Gap**: No explicit protocol for escalation and urgency detection outside scheduled times.

**Recommendation**: Define what constitutes an interruption-worthy event:

- **Immediate (break into whatever's happening)**: Security incident, service outage affecting clients, message from Dina's manager marked urgent
- **Next check-in (MiddayCheck or EveningWrapup)**: Meeting cancellation/change, new email from a key stakeholder, project blocker surfaced
- **Next morning (MorningBrief)**: Everything else

**Implementation**: Document in `config/escalation-policy.md`. Update scheduled task scripts to classify incoming signals against these tiers.

---

## 10. Adopt the McChrystal Four-Stage Framework

**Gap**: Atlas doesn't have a documented maturity model for its own CoS capabilities.

**Recommendation**: Map Atlas's current stage and define progression:

- **Stage 1 — Principal Execution** (mostly achieved): Ensure Dina's priorities are visible and tracked. Calendar, email, meeting prep all working.
- **Stage 2 — Organizational Synchronization** (partially achieved): Cross-reference across workstreams (Danaher, WDAI, personal). Wiki helps but needs active status tracking.
- **Stage 3 — Trust Building** (in progress): Atlas earning trust through reliability, memory, and consistency. Key metric: does Dina stop worrying about things Atlas is handling?
- **Stage 4 — Strategic Advising** (aspirational): Atlas proactively identifies strategic misalignment, recommends priority changes, challenges assumptions.

**Implementation**: Add a "CoS Maturity" section to CLAUDE.md that tracks which stage Atlas is operating at, with specific capabilities to unlock for each stage.

---

## Priority Order for Implementation

Based on effort vs impact:

1. **Follow-up tracking** (Rec #2) — highest-impact, moderate effort. A CoS that never drops a ball.
2. **Proactive nudge system** (Rec #8) — codifies what's already in CLAUDE.md but unimplemented.
3. **Email triage upgrade** (Rec #6) — leverages existing Gmail MCP and voice profile.
4. **Rhythm of Business** (Rec #1) — monthly and quarterly cadences fill the biggest scheduling gap.
5. **Anticipation engine** (Rec #4) — transforms Atlas from reactive to proactive.
6. **Relationship tracking** (Rec #3) — extends existing wiki people pages.
7. **Decision log standardization** (Rec #7) — extends existing wiki decisions folder.
8. **Strategic advising** (Rec #5) — builds on everything above.
9. **Escalation policy** (Rec #9) — important but less urgent.
10. **Maturity framework** (Rec #10) — aspirational, guides long-term development.
