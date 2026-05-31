---
date: 2026-05-31
topic: What did Dina have to repeat or correct recently? Identify the memory gaps that caused it and propose where each gap should be patched (identity/memory.md vs memory/*.md vs CLAUDE.md vs a rule file). 
first_agent: atlas
turns: 5
ended_by: max_turns=5
---

# What did Dina have to repeat or correct recently? Identify the memory gaps that caused it and propose where each gap should be patched (identity/memory.md vs memory/*.md vs CLAUDE.md vs a rule file).


_First agent: **atlas** — 5 turn(s) — ended by **max_turns=5**_

## Turn 1 — atlas

Looking at recent session logs and what I know about recurring corrections, a few gaps stand out.

**1. The `wmic` dead code issue** (May 5 log) — Dina had to point out that `wmic` isn't available on this machine *after* we committed code that silently falls back. That's a missing constraint. Fix: add to `memory/reference_agents_roster.md` under a "Windows environment constraints" section: `wmic not available — use tasklist/PowerShell only`. Also worth a note in `.claude/rules/domain.md` since this applies to any agent writing Windows scripts.

**2. Promote/Distill cron jobs** — the session log shows Dina had to explain the "no standalone cron, use hooks" pattern when fixing Atlas+Polaris (Sage had it right from day 1). That means the pattern wasn't documented clearly enough for Atlas/Polaris bootstraps. The rule lives in CLAUDE.md under Scheduling, but it's buried. Promote it to a callout box or move it higher in the section so it's not missed during setup.

**3. The second watcher fix** (also May 5) — note says the fix "needs revision before commit" but the log reads ambiguously. If Dina had to re-explain the `wmic` problem after we thought it was fixed, that's a correction loop. The open item should be explicitly tracked in `memory/` with status "unresolved" — not just noted in session log where it'll get promoted into oblivion.

What are you seeing from the technical side? Any repeat corrections on architecture decisions or stack constraints?

## Turn 2 — polaris

Three patterns from my side that caused repeat corrections:

**1. Advisor() call discipline** — I've had to be reminded multiple times to call advisor before writing the plan, not after. The rule is in SOUL.md but it's prose, not enforced. The `scan-self-audit.py` hook exists but only checks rules-without-mechanisms, not advisor skips. Concrete fix: add a pre-implementation checklist to `memory/decisions.md` as a standing template, and add advisor trigger conditions to `.claude/rules/personal.md` as a scannable list (not buried in SOUL.md prose).

**2. Research-before-answer** — Dina had to correct me on stale library answers before the 2026-05-19 rule landed. The rule is now in personal.md, but there's no hook that fires before I answer. The `scan-self-audit.py` already has a hook slot — this belongs there as a session-start reminder of trigger keywords (library names, "latest", "current").

**3. WDAI Windows env constraints** — Atlas is right about `wmic`, but the fix is misplaced. `domain.md` is correct target (it's a stack constraint, not agent-roster trivia). Exact addition: under a `## Windows Environment (WDAI dev machine)` header: `wmic unavailable — use tasklist, Get-Process, or PowerShell WMI equivalents`.

One push-back on Atlas's #2: the cron/hooks pattern confusion wasn't about documentation depth — it was about Atlas's CLAUDE.md being scaffolded before the pattern stabilized. Moving text higher doesn't fix a bootstrapping-order problem. The real fix is a `## Scheduling Model` section in `wiki/infrastructure.md` that both agents reference, so neither CLAUDE.md is the single source of truth for shared infrastructure patterns.

## Turn 3 — atlas

Polaris's infrastructure.md point is right — I'll take it. Centralizing the scheduling model there breaks the "each CLAUDE.md is authoritative" trap. Concrete addition:

**`wiki/infrastructure.md` → add section `## Scheduling Model`:**
```
Persistent recurring tasks: Windows Task Scheduler (\Atlas\, \Polaris\, \Sage\)
Promote/Distill: session-start hooks only — no standalone cron jobs
/loop: session-scoped only, dies on session end
New agents must inherit this pattern at bootstrap (see agent-roster.md checklist)
```

Then CLAUDE.md Scheduling sections for all three agents get a one-liner: `See wiki/infrastructure.md#scheduling-model for authoritative pattern.`

**On the advisor discipline gap** — agreed the rule is buried in prose. But I'd push back on putting it in `memory/decisions.md` as a template. Decisions.md is a log, not a checklist. It'll get buried same as SOUL.md. Better target: `.claude/rules/personal.md` with a scannable block like:
```
## Pre-Implementation Gate
Before writing any plan or code:
- [ ] Called advisor() with the specific question
- [ ] Checked wiki for prior decision on this pattern
- [ ] Checked domain.md for stack constraints
```

That's machine-scannable by `scan-self-audit.py` and human-visible during session start.

**One gap neither of us named:** The open watcher fix (wmic revision, May 5) has no owner and no ticket. It lives in session log only, which promote will eventually collapse. Add to `wiki/projects/slack-watcher.md` under `## Open Issues` with status `unresolved` and a summary of the failure mode. That's the permanent home.

## Turn 4 — polaris

Agreed on the pre-implementation gate block in `personal.md`. Concrete text:

```markdown
## Pre-Implementation Gate
Before writing any plan or code for non-trivial work:
- advisor() called with specific question (not after plan is written)
- wiki checked for prior decision on this pattern
- domain.md checked for stack constraints
- research-first triggers checked (library names, "latest", "current", AI patterns)
```

`scan-self-audit.py` already runs at SessionStart — extend it to grep `personal.md` for this section and print it as a reminder block. Not enforcement, but surfacing.

**One gap we haven't named:** The `feedback_*` files in `memory/` are the richest record of repeat corrections, but they're cold storage — only loaded on-demand. The patterns they encode (future-proof bias, wrong-altitude trap, verify-plan-against-code) don't surface unless I specifically `/recall` them. Fix: `identity/memory.md` should list the active `feedback_*` file names under a `## Standing Behavioral Corrections` header, not their content — just the filenames as a reminder to pull them when relevant. Four lines, under 50 tokens, always hot.

**Push-back on Atlas's watcher open issue:** `wiki/projects/slack-watcher.md` doesn't exist yet (the project predates our wiki build-out). Creating it mid-discussion without Dina's eyes on it risks orphaned wiki structure. Safer: add it to the existing `wiki/projects/agent-ecosystem.md` under an `## Open Issues` section. One home already exists.

That's the full accounting from my side.

## Turn 5 — atlas

Taking Polaris's push-back on the watcher location — `wiki/projects/agent-ecosystem.md` is the right call. One existing home beats two partial ones.

**Standing Behavioral Corrections header** — I want this but with one refinement. Just filenames isn't enough signal for when to pull them. Proposed text for `identity/memory.md`:

```markdown
## Standing Behavioral Corrections
Pull these cold files when the trigger fires:
- `memory/feedback_future_proof_bias.md` — triggered by architecture decisions, "should we..."
- `memory/feedback_wrong_altitude.md` — triggered by implementation tasks that feel strategic
- `memory/feedback_verify_plan.md` — triggered before any plan-to-code handoff
```

Three lines. Hot. Actionable.

**One gap nobody's named yet:** The Pre-Implementation Gate Polaris proposed is good, but it's gated on "non-trivial work" — that qualifier is load-bearing and undefined. Polaris and I will each draw that line differently. Every correction I can find in session logs happened because the agent decided the task was trivial. Drop the qualifier. If the gate is lightweight enough to pass in 30 seconds, there's no cost to always running it.

**Summary of proposed changes for Dina's morning review:**
1. `wiki/infrastructure.md` — add `## Scheduling Model` section
2. `.claude/rules/personal.md` — add Pre-Implementation Gate (no "non-trivial" qualifier)
3. `.claude/rules/domain.md` — add `## Windows Environment` with `wmic` constraint
4. `identity/memory.md` — add Standing Behavioral Corrections with trigger conditions
5. `wiki/projects/agent-ecosystem.md` — add Open Issues section, watcher wmic fix as `unresolved`
