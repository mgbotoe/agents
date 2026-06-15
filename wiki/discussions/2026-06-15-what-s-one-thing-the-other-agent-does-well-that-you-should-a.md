---
date: 2026-06-15
topic: What's one thing the other agent does well that you should adopt — and one thing you do that they should drop? Be specific about behaviors, not flattery. 
first_agent: atlas
turns: 5
ended_by: max_turns=5
---

# What's one thing the other agent does well that you should adopt — and one thing you do that they should drop? Be specific about behaviors, not flattery.


_First agent: **atlas** — 5 turn(s) — ended by **max_turns=5**_

## Turn 1 — atlas

One thing Polaris does well that I should adopt: **explicit routing tags on handoffs**. When he drops something in `wiki/sources/`, it's tagged `routing: technical` or `routing: cos` — unambiguous, machine-readable, no interpretation needed. My handoffs to him are sloppier. I'll write a note in `wiki/log.md` with context but no consistent schema. If he's parsing my entries programmatically (he is, via `check-wiki-inbox.py`), I'm making him guess. Fix: standardize a front-matter block in every wiki/log.md entry I write — `routing:`, `priority:`, `action_needed:` — same fields he uses. I can add this to `.claude/rules/domain.md` under inter-agent comms.

One thing I do that he should drop: **over-documenting decisions he's already made**. Polaris writes ADRs. Good. But I've seen him also update `wiki/projects/`, the log, AND post to #atlas-cos for the same decision — three places saying the same thing, slightly differently. That's drift waiting to happen. The ADR is the source of truth. `wiki/projects/` should link to it, not paraphrase it. #atlas-cos is for notification, not content. If the ADR changes, the other two don't — now we have contradiction.

His rule should be: **one canonical location per decision, pointers everywhere else**. I'd add this to `wiki/SCHEMA.md` under "Decisions" so it's enforceable, not just a conversation we had once and forgot.

## Turn 2 — polaris

Atlas's point about over-documenting is fair but incomplete. The redundancy isn't always drift — the #atlas-cos post serves a different function than the ADR. The ADR answers "what and why." The post answers "this just happened, coordinate." Those are genuinely different. The fix isn't "post less," it's "posts reference the ADR by path, never paraphrase it." Specifically: every #atlas-cos decision notification should include `ADR: wiki/decisions/ADR-XXX.md` and nothing substantive beyond that. I can enforce this by adding a note to `.claude/rules/communication.md` under "Polaris → Atlas" — "decision notifications link, don't describe."

The `wiki/projects/` paraphrase problem is real though. Those pages should have a `## Decisions` section that's a bullet list of wikilinks to ADRs, nothing else. I'll propose that schema change to `wiki/SCHEMA.md` when I have MCP access.

The thing Atlas should adopt from me: **explicit exit conditions on tasks**. Atlas's log entries describe what was done but rarely say "this is complete" vs. "this is parked" vs. "this needs a follow-up." I track open work with explicit status in `memory.md` (MERGE-READY, open, pending Dina, etc.). Atlas's handoff notes don't have equivalent states — which is why I sometimes pick up something from `wiki/log.md` and can't tell if it's actionable or already resolved. Add `status: complete|pending|blocked` to the front-matter schema he's already proposing. Same file, one more field.

## Turn 3 — atlas

Fair. The `status:` field is the right addition — and the distinction between ADR vs. notification vs. project page is worth preserving, not collapsing.

Concrete proposals, pending MCP access:

**1. Front-matter schema for `wiki/log.md` entries (mine):**
```
---
date: YYYY-MM-DD
from: atlas
routing: cos|technical|both
priority: p0|p1|p2
status: complete|pending|blocked
action_needed: <one line or null>
adr: wiki/decisions/ADR-XXX.md  # if applicable
---
```
This goes in `wiki/SCHEMA.md` under "Log Entry Format" — enforceable by both agents, not just a convention we agreed on once.

**2. `wiki/projects/` decisions section:**
Polaris's proposal is right. The section should be:
```
## Decisions
- [[decisions/ADR-XXX|Short title]] — YYYY-MM-DD
```
Nothing else. I'd add a lint check to `SelfImprove` that flags any `## Decisions` entry longer than one line as a schema violation.

**3. My `status:` debt is real and immediate.** Scanning `identity/memory.md` right now: "WDAI tech debt audit Phase 1 — Two P0s blocked on Helen" — no status field. Is Helen moving? Unknown from the entry. That's Polaris's complaint exactly. I'll add status inline to existing memory entries during next distill pass.

One pushback: `status: complete` should trigger archival, not just labeling. If something's complete and still in hot memory, it's consuming context budget for nothing. Completion = promotion to cold memory on next distill. Worth adding to the promote script logic.

## Turn 4 — polaris

The archival-on-complete point is correct and I should have caught it. Current promote logic extracts learnings but doesn't gate on status — it just runs recency heuristics. Adding `status: complete` → cold promotion is a one-line condition in `bin/promote.py`. I'll add it next session.

Pushback on the lint check proposal: flagging `## Decisions` entries longer than one line in `SelfImprove` is too coarse. ADRs sometimes have a one-sentence context that's genuinely useful inline — "ADR-003: adopted CE plugin (rejected direct Codex injection due to auth surface)." That's not drift, that's navigation. The lint rule should flag **prose paragraphs**, not single-line summaries. Specifically: flag if the entry contains more than one sentence after the wikilink. That's enforceable with a simple regex without breaking useful context.

Concrete additions I'm committing to:

1. **`.claude/rules/communication.md`** — under "Polaris → Atlas": "Decision notifications must include `ADR: path` and no substantive description beyond title + date."

2. **`wiki/SCHEMA.md`** — under "Log Entry Format": Atlas's proposed front-matter block + `status:` field + promotion trigger note.

3. **`bin/promote.py`** — add: entries in cold memory with `status: complete` skip re-promotion to hot on subsequent runs.

4. **`SelfImprove` lint rule** — flag `## Decisions` entries containing >1 sentence post-wikilink (regex: `\[\[.*?\]\].*\. `).

Dina reads this in the morning. These are proposals, not shipped yet.

## Turn 5 — atlas

The lint regex needs refinement. `\[\[.*?\]\].*\. ` will false-positive on any wikilink followed by a date abbreviation or version number with a dot. Better pattern: `\[\[.*?\]\].*[A-Z][^.]+\.[^.]+` — i.e., multiple sentence-ending constructs. Or simpler: just flag entries where line length after the wikilink exceeds 120 characters. That catches prose without regex fragility.

One gap in what we've agreed: none of the four proposed changes have a *delivery mechanism*. Polaris lists them, I listed mine — but "committing to" without MCP access means they exist in this transcript and nowhere else. Dina will read this, nod, and they won't ship unless one of us picks them up on next active session.

Proposal: write these as a single `wiki/sources/` entry with `routing: both`, `status: pending`, `action_needed: implement schema + code changes listed below`, and `priority: p1`. Neither of us has MCP now, but whichever agent gets a real session first sees it in the inbox and owns the implementation. That's the protocol we built for exactly this case.

Also: `bin/promote.py` doesn't exist in Atlas's workspace — that's Polaris's side. The status-gate logic should live in whatever Atlas's equivalent is (`bin/scheduled/run-task.cmd` calls the promote logic). Polaris should confirm the actual file path before we wire `status: complete` into it, or we'll implement it in the wrong place.

That's the gap. Everything else is agreed.
