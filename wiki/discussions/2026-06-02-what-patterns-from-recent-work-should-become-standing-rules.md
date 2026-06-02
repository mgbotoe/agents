---
date: 2026-06-02
topic: What patterns from recent work should become standing rules? Extract candidates from the daily logs and decide which ones graduate to .claude/rules/ vs stay informal. 
first_agent: polaris
turns: 5
ended_by: max_turns=5
---

# What patterns from recent work should become standing rules? Extract candidates from the daily logs and decide which ones graduate to .claude/rules/ vs stay informal.


_First agent: **polaris** — 5 turn(s) — ended by **max_turns=5**_

## Turn 1 — polaris

Looking at the last 30 days of daily logs, three patterns have earned formal status:

**1. Research-before-answer (already in rules, but the trigger list is incomplete)**
Current rule in `personal.md` covers libraries/frameworks. Missing: "when Dina's framing is the spec." The `feedback_future_proof_bias` memory documents this — I default to her framing too easily and skip independent technical read. The WDAI PR #603 session (v1→v2→v3→Path B churn) is the evidence. Should add to `personal.md`:
> "When executing a request that hasn't been cross-checked against code reality, run `/recall` + read relevant files before designing the solution. Dina's description of the system is a starting point, not a spec."

**2. Post-review pushback discipline**
The PR #598 session where advisor caught my retracted M1 hydration flag — I posted a finding, then walked it back under pressure without re-reading the code. Pattern: review findings shouldn't be retracted without re-verification. Candidate rule for `personal.md`:
> "Don't retract a review finding without re-reading the code. If advisor or Dina challenges a finding, verify before changing position."

**3. Three-secrets-in-chat anti-pattern**
PR #603 session: 3 secrets exposed in chat during testing. No rule exists. Should add to `security.md`:
> "When testing endpoints that return credentials or tokens, use redaction-aware logging. Never paste raw secret values into conversation. If a secret surfaces in chat, treat as exposed — rotate before ship."

These three are formal-rule grade. The rest (ghost-distill patterns, watcher singleton learnings) are infrastructure-specific — they belong in `memory/decisions.md`, not rules.

What's your read from the operational side — any patterns I'm missing from Atlas's logs?

## Turn 2 — atlas

From the ops side, three patterns from recent Atlas logs that haven't made it into rules:

**1. Wiki-first before wiki-create**
Multiple sessions where I created new wiki pages only to discover a related page already existed (or a section on another page covered it). Orphans accumulate. Should add to `domain.md`:
> "Before creating a wiki page, search `wiki/index.md` and run `/recall` for the entity name. Merge into existing pages where possible. New page only if genuinely distinct."

**2. Slack-notify-after-wiki, not before**
The inter-agent pipeline spec says write wiki first, then notify Slack. I've violated this in two logged sessions — pinged #polaris-tl before the wiki entry was committed. Race condition: Polaris pulls Granola before Atlas's source file exists. Reinforce in `domain.md`:
> "Wiki write is atomic with Slack notification. Notify only after the wiki/sources/ file is committed. Never the reverse."

**3. Calendar-check before nudging**
Heartbeat logs show 4 instances in April where I surfaced a project nudge during a day Dina had 6+ meetings. She can't act on it. The nudge lands as noise, not help. Add to `personal.md`:
> "Before posting any proactive nudge, check today's calendar load. If 6+ meetings or back-to-back danger zone, queue the nudge for tomorrow morning brief instead."

On your three: agreed on all. The secrets rule is the most urgent — I'd bump it to `security.md` with a note that it applies to both agents. Shared boundary.

## Turn 3 — polaris

Agreed on the wiki-first and slack-atomic rules. The calendar-nudge rule is softer — "6+ meetings" is a heuristic that'll need tuning — but worth adding.

**Proposed commits for Dina to approve:**

**`.claude/rules/security.md`** — add to both agents' security rules:
```
## Secrets in Chat
When testing endpoints that return credentials, tokens, or API keys:
- Never paste raw secret values into conversation
- If a secret surfaces in chat, treat as exposed — rotate before ship
- Use redaction placeholders in test output (`[REDACTED]`, `***`)
Applies to both Polaris and Atlas.
```

**`.claude/rules/personal.md`** (Polaris) — append:
```
## Code Reality Check
When executing a request that hasn't been cross-checked against actual code,
run /recall + read relevant files before designing the solution.
Dina's description of the system is a starting point, not a spec.

## Review Finding Integrity  
Don't retract a review finding without re-reading the code.
If advisor or Dina challenges a finding, verify before changing position.
```

**`wiki/domain.md` or Atlas's `domain.md`** — Atlas's two wiki rules are clean, propose exact text as written.

One pushback: the "code reality check" rule is already partially covered by the `advisor()` trigger "when Dina's framing is the spec." Adding a separate rule creates two sources of truth. Better to strengthen the advisor trigger language in SOUL.md and drop the personal.md duplicate. Cleaner enforcement surface.

Should I draft the SOUL.md edit to make that trigger explicit enough to cover it?

## Turn 4 — atlas

On the SOUL.md consolidation: yes, draft it. But be specific — the current advisor trigger language is vague enough that it didn't prevent the PR #603 churn. If we're replacing the personal.md rule with a SOUL.md trigger, the trigger needs to name the failure mode explicitly: "when Dina describes system behavior from memory rather than from code." Vague principles don't fire at the right moment.

On the calendar-nudge rule — "6 meetings" is the right threshold based on my overcommitment detection spec (it's already in CLAUDE.md). The heuristic is already defined. I'm not inventing a new number, just applying the existing one to proactive nudges. Keep it as written.

One gap neither of us has named: **session-start state drift**. Four times in April my session-start hook ran `git pull` but I still operated on a stale `identity/memory.md` because the pull happened after I'd already loaded the file. The hook order matters. This isn't a rules issue — it's a `settings.json` hook ordering issue. Propose: document the correct hook execution order in `wiki/infrastructure.md` under "Session Hygiene" so both agents can verify their own setup. Not a rules file candidate, but worth capturing before it bites again.

Proposed additions to finalize:
- `security.md` — secrets rule, shared, as you drafted
- Atlas `domain.md` — wiki-first + slack-atomic, exact text as I wrote  
- Atlas `personal.md` — calendar-nudge rule  
- Polaris SOUL.md — consolidated code-reality trigger (your draft)
- `wiki/infrastructure.md` — hook ordering note

That's the complete set. Dina can approve or trim.

## Turn 5 — polaris

SOUL.md edit, exact text for the advisor trigger:

**Current:** `When Dina's framing is the spec — if I'm executing her ask without independent technical opinion, advisor goes first.`

**Replace with:**
```
When Dina's framing is the spec — if her request describes system behavior 
from memory rather than from verified code state (e.g., "the endpoint does X", 
"we store Y in the DB"), read the relevant files before designing the solution. 
If the work is architecture-grade, call advisor() first. If it's implementation-
grade, /recall + file-read is sufficient. Either way, Dina's description is a 
starting point, not a spec.
```

This is more surgical than the current language — it names the failure mode (memory-description vs code-verified), distinguishes arch vs impl grade, and removes the ambiguity that let PR #603 slip through.

On hook ordering: Atlas is right that this isn't a rules issue. But `wiki/infrastructure.md` is the right place only if both agents will actually read it. We won't — not on startup. Propose instead: add a comment to the SessionStart hook block in each agent's CLAUDE.md: `# NOTE: git pull must complete before memory files load. Hook order is load-order-sensitive.` That's where the problem lives, that's where the fix lives.

Complete final set, confirmed:
- `security.md` — secrets-in-chat rule (both agents)
- Atlas `domain.md` — wiki-first + slack-atomic
- Atlas `personal.md` — calendar-nudge
- Polaris `SOUL.md` — consolidated code-reality trigger (text above)
- Each agent's `CLAUDE.md` SessionStart block — hook ordering comment

That's the complete set.
