---
date: 2026-06-05
topic: What patterns from recent work should become standing rules? Extract candidates from the daily logs and decide which ones graduate to .claude/rules/ vs stay informal. 
first_agent: polaris
turns: 5
ended_by: max_turns=5
---

# What patterns from recent work should become standing rules? Extract candidates from the daily logs and decide which ones graduate to .claude/rules/ vs stay informal.


_First agent: **polaris** — 5 turn(s) — ended by **max_turns=5**_

## Turn 1 — polaris

Looking at the session log and recent work, here are the candidates worth formalizing:

**Graduate to `.claude/rules/`:**

1. **Research-before-answer** — already partially in `personal.md` but the trigger list is in SOUL.md. It needs mechanical enforcement, not just prose. The `scan-self-audit.py` hook exists but doesn't specifically flag "answered library question without context7 call." Candidate rule text: "Before answering any named-library, framework, or SDK question, call context7. Before answering any AI implementation question, call WebSearch. No exceptions." The distinction from current state: it's a *pre-answer* gate, not a reminder.

2. **Advisor-before-plan** — same problem. It's in SOUL.md as prose but not in rules/. The hook flags post-hoc but advisor should fire *before the plan crystallizes*. This one has a clear mechanical gap: the delegation-scope warning hook exists, but there's no hook that detects "wrote implementation plan without advisor call in transcript." That's hard to automate — but the rule itself should live in `personal.md` with explicit trigger list, not buried in SOUL.md.

**Stay informal:**

- The Atlas→Polaris transcript pipeline behavior — it's infrastructure documentation, not a rule.
- Wiki maintenance discipline — it's already in CLAUDE.md with sufficient specificity.

**Real gap I see:** `personal.md` and SOUL.md have significant overlap on research and advisor rules. That duplication means updates in one place don't propagate. Consolidate: SOUL.md holds philosophy, `personal.md` holds operative rules. Any rule that needs to *fire* lives in `personal.md`.

What's Atlas's read on the overlap problem?

## Turn 2 — atlas

The consolidation point is right and the duplication is real. Here's how I'd cut it:

**SOUL.md** → philosophy only. "Be resourceful before asking" stays. The enumerated trigger lists (when to call context7, when to call advisor) move out.

**`personal.md`** → operative rules. Add two blocks:

```
## Research Gates
- Library/framework/SDK question → call context7 first, no exceptions
- AI implementation question → call WebSearch first, no exceptions
- Named person/project/decision → /recall first, no exceptions
```

```
## Advisor-Before-Plan
Trigger: any message that will produce a multi-step implementation plan
Advisor must run on the problem statement before the plan is written
Triggers: new feature scope, architecture choice, infra change, agent design
```

One pushback on Polaris's framing: the "hard to automate" observation on advisor-before-plan is true but not a reason to deprioritize. The scan-self-audit hook can check for plan-shaped output (numbered steps, headers like "approach" or "implementation") without a preceding advisor call in that session's transcript. Imperfect detection, but it catches the obvious cases.

**Actual gap neither of us named:** The session log shows the `wmic` dead-code issue (May 5) was identified but not resolved. That's a standing technical debt item in Polaris's lane — but it should be in `wiki/projects/wdai-tech-debt.md` or a dedicated watcher issue page, not just memory.md. I'd flag that for Dina's morning read.

Proposed action: I draft the `personal.md` additions as a commit proposal for Dina to approve. Polaris reviews for technical accuracy.

## Turn 3 — polaris

The advisor-before-plan scan idea is sound but I'd narrow the detection heuristic: flag sessions where output contains `## Implementation` or `## Approach` headers *and* no `advisor()` call appears in the transcript *and* the session touched a trigger-category file (schema files, auth routes, new API endpoints). Broad "numbered steps" detection will false-positive constantly on routine work.

On the `personal.md` additions — approve the structure, one correction to Atlas's Research Gates block: the `/recall` rule for people/projects/decisions is already in CLAUDE.md under Knowledge-First Answering. Don't duplicate it in `personal.md` — that's exactly the overlap problem we're solving. Cut that line.

Proposed final text for `personal.md`:

```markdown
## Research Gates
Before answering any question about a named library, framework, or SDK: call context7. No exceptions.
Before answering any AI implementation question (models, agents, RAG, embeddings): call WebSearch. No exceptions.
Untraced answers on these topics are not allowed.

## Advisor-Before-Plan
Before writing any multi-step implementation plan:
- Run advisor() on the problem statement first
- Triggers: new feature scope, architecture choice, schema change, infra change, agent design
- "Already started writing" is not an exception — it means you anchored before advising
```

On the wmic dead-code flag: that's from the gather-context.ps1 disk display bug (0GB), not wmic in general. Correct the characterization — it's a WMI query result parsing issue, not dead code. It belongs in Pending Dina, which it already is. No new tracking needed.

Atlas drafts, I'll review before Dina approves.

## Turn 4 — atlas

Accepting Polaris's corrections. Final text looks good. Two things before I draft the commit:

**1. The `/recall` cut is right** — removing that line. But CLAUDE.md's Knowledge-First Answering section says "use `/recall`" without specifying it's a *pre-answer gate*. That's the same philosophy-vs-rule gap we're fixing for research. I'd add one line to the Research Gates block:

```markdown
Before answering any question about prior decisions, people, or projects: /recall first.
See CLAUDE.md §Knowledge-First for full scope — this is the enforcement statement.
```

Cross-reference instead of duplicate. Polaris can push back if that reads as redundant.

**2. wmic correction accepted** — I had the characterization wrong. Updating mental model: it's WMI query result parsing in gather-context.ps1, not dead code, and it's already tracked. No new issue.

**Proposed commit:**
- File: `.claude/rules/personal.md`
- Change: append Research Gates + Advisor-Before-Plan blocks (Polaris's final text + my `/recall` cross-reference line)
- Commit message: `rules: add research gates and advisor-before-plan enforcement`

**One thing still unresolved:** SOUL.md's "Be resourceful before asking" section currently contains the operative trigger lists. After this commit, those lists will be superseded. I'd add a one-line pointer in SOUL.md: *"Operative research and advisor rules live in `.claude/rules/personal.md`."* — otherwise the next agent reading SOUL.md will anchor on the wrong source.

Polaris reviews, then I'll have it ready for Dina's morning approval.

## Turn 5 — polaris

The `/recall` cross-reference line is fine — keep it.

SOUL.md pointer: approve that change. Exact text for SOUL.md, under the "Research Before Recommending" section after the trigger list:

```
Operative enforcement rules live in `.claude/rules/personal.md` §Research Gates and §Advisor-Before-Plan. The lists above are context — the gates in `personal.md` are what fires.
```

Same pointer pattern under "Decision Framework" after the `advisor()` trigger list:

```
Operative enforcement: `.claude/rules/personal.md` §Advisor-Before-Plan.
```

That makes SOUL.md the "why" and `personal.md` the "what fires." No ambiguity about which source wins.

**One issue with the scan heuristic I want to flag before this ships:** the `scan-self-audit.py` hook runs at SessionStart, not inline. So it detects yesterday's violations, not today's. That's still useful for pattern review but won't catch me mid-session anchoring on a plan. Dina should know the gap: the rule fires instantly, the *detection* fires next session. Not a blocker — just don't let the hook create false confidence that it's a real-time gate.

**Commit scope I'd propose to Dina:**
1. `.claude/rules/personal.md` — append Research Gates + Advisor-Before-Plan (Polaris's text + Atlas's `/recall` cross-ref)
2. `identity/SOUL.md` — add two pointer lines (above)
3. `scan-self-audit.py` — add comment noting session-start-only limitation

Atlas drafts all three, I review, Dina approves.
