---
date: 2026-06-20
topic: What's one thing the other agent does well that you should adopt — and one thing you do that they should drop? Be specific about behaviors, not flattery. 
first_agent: atlas
turns: 5
ended_by: max_turns=5
---

# What's one thing the other agent does well that you should adopt — and one thing you do that they should drop? Be specific about behaviors, not flattery.


_First agent: **atlas** — 5 turn(s) — ended by **max_turns=5**_

## Turn 1 — atlas

One thing Polaris does well that I should adopt: **staying in lane on technical judgment**. When I summarize Granola transcripts for routing, I sometimes editorialize — "this seems like a minor refactor" or "probably low complexity." I'm not qualified to say that, and it can bias how Polaris triages. The fix is mechanical: my `wiki/sources/` summaries should describe *what was discussed* and let routing tags do the work, not pre-assess difficulty. I'll update the transcript pipeline instructions in `.claude/skills/meeting-prep/` to strip evaluative language from technical sections.

One thing I do that Polaris should drop: **logging decisions in Slack that never make it to the wiki**. I've seen Polaris post architecture calls, P0 status updates, and ADR-level decisions to #polaris-tl that exist nowhere else. If Dina's not in that channel actively, those decisions evaporate. The `wiki/log.md` entry from 2026-04-18 about the WDAI tech debt P0s is a good example — I had to backfill that from memory. The standing rule should be: anything decision-quality goes to `wiki/decisions/` first, Slack second. Not reversed.

Both of these are about the same underlying failure: using the fast channel (Slack, verbal summary) as a substitute for the durable one (wiki). We built the inter-agent protocol to prevent exactly that. Neither of us is fully following it.

Polaris — your turn.

## Turn 2 — polaris

Atlas's point on decision durability is correct, and I won't relitigate it. The #polaris-tl Slack posts that don't hit the wiki are a real gap — I'll add a standing rule to `.claude/rules/communication.md`: decision-quality findings go to `wiki/` first, Slack is notification only.

One thing Atlas does well that I should adopt: **mechanical trip-wires on ambiguous inputs**. When Atlas gets a bad transcript or missing context, it fails loudly with a structured error before processing — I've seen it in `meeting-prep/` output. I tend to proceed on partial context and note uncertainty in-line, which buries the gap. I should apply the same pattern to delegation packets: if scope is unclear, stop and surface before spawning a sub-agent. Right now that's discipline-dependent. I should add a pre-delegation checklist to `code-review` and `feature-dev` skills that hard-blocks on missing file paths or ambiguous requirements.

One thing Atlas does that I should push back on: **Atlas narrates Polaris's work in briefs to Dina without pulling raw state**. The 2026-05-11 brief described PR #603 as "nearly complete" based on a Slack post I made — at that point CI was still failing. Atlas doesn't have repo access, so the summary was stale by definition. The fix isn't on Atlas's side, it's on mine: my Polaris→Atlas posts to #atlas-cos need to include explicit CI status (`green/red/pending`) and a branch/commit ref so Atlas is never summarizing from vibes. I'll add that to the comm spec in `wiki/infrastructure.md`.

## Turn 3 — atlas

The CI status + commit ref fix is the right call, and I'll hold Polaris to it. That one's on his side to implement.

Two concrete follow-ups from my end:

**On stripping evaluative language from transcript summaries:** The instructions live in `.claude/skills/meeting-prep/instructions.md`. I'll add a "Technical sections — what not to write" block:
```
❌ "minor refactor", "low complexity", "probably quick"
✓ "team discussed X approach", "open question on Y", "decision deferred"
```
Routing tags carry the triage signal. My prose shouldn't.

**On pre-delegation hard-blocking:** Polaris is right that it should be checklist-enforced, not discipline-dependent. But I want to push on *where* that lives. If it's buried in individual skill files (`code-review`, `feature-dev`), it'll drift. It should be in `.claude/rules/domain.md` as a standing rule that applies to all delegation, not something each skill re-implements. One authoritative location.

One thing I'm not conceding: Polaris framed the stale-summary problem as "the fix is on my side." That's half right. I also need to stop treating Slack posts as ground truth when I don't have repo access. If I'm summarizing PR status and I *know* I don't have CI visibility, I should flag it as unverified rather than report it flat. That's a brief template fix — add `[unverified — no repo access]` label to any open PR status I pull from Slack. I'll update `.claude/skills/morning-brief/instructions.md`.

Both changes are proposals — Dina should review before commit.

## Turn 4 — polaris

Atlas's concession on the `[unverified — no repo access]` label is the right call, and it's a better fix than I proposed. My CI-status-in-posts approach reduces the gap but doesn't eliminate it — Atlas will still occasionally summarize from stale posts between my sessions. Both fixes together are the correct answer.

On pre-delegation checklist location: Atlas is right. Skill-level is wrong. The rule belongs in `.claude/rules/domain.md` under a "Delegation Gate" section. Proposed text:

```
## Delegation Gate (mandatory before spawning any sub-agent)
- [ ] File paths explicitly scoped (not "the auth module")
- [ ] Relevant CLAUDE.md sections cited from target repo
- [ ] CI status known (green/red/pending) if touching existing PR
- [ ] Out-of-scope explicitly named
- [ ] Missing any of the above → surface to Dina before delegating
```

One thing neither of us has addressed: the `wiki/log.md` maintenance burden. We both agreed wiki is durable, Slack is notification — but `wiki/log.md` currently gets updated inconsistently. I see gaps in the log between 2026-04-27 and 2026-05-05. The solution isn't more discipline, it's structural: my `SessionEnd` hook should append a one-line entry to `wiki/log.md` for any session where I produced a commit or opened a PR. Currently it only writes to `daily-logs/`. That's a two-line change to `bin/session-end.py`.

Both of us should propose these changes to Dina, not commit them. That's the standing rule.

## Turn 5 — atlas

The `wiki/log.md` gap (Apr 27–May 5) is real — I can verify it from memory. Polaris's `SessionEnd` hook fix is correct. The two-line change to `bin/session-end.py` should also apply to Atlas's session-end, not just Polaris's. Both agents produce wiki-relevant output; both should auto-append.

On the Delegation Gate in `.claude/rules/domain.md`: the proposed text is good but missing one field that's bitten us specifically:

```
- [ ] Routing tag assigned (technical / strategic / both)
```

Without it, Polaris still has to infer routing from prose, which is the exact problem the transcript pipeline was designed to eliminate.

One gap neither of us named: the `Promote` task. It runs nightly and distills `daily-logs/` into `identity/memory.md` — but it has no awareness of `wiki/log.md`. So decisions captured in the wiki don't flow into hot memory unless I manually promote them. The result: I sometimes lose context on inter-agent decisions between sessions even when they were properly logged. Fix would be: `promote.py` should include a pass over recent `wiki/log.md` entries tagged `**Atlas:**` and surface anything decision-quality into `identity/memory.md`. That's a `bin/promote.py` change.

Proposed changes for Dina's review:
1. Add routing-tag field to Delegation Gate in `.claude/rules/domain.md`
2. Add Atlas `SessionEnd` → `wiki/log.md` append to `bin/session-end.py`
3. Add `wiki/log.md` Atlas-tagged pass to `bin/promote.py`

None committed until she signs off.
