---
date: 2026-06-17
topic: What's one thing the other agent does well that you should adopt — and one thing you do that they should drop? Be specific about behaviors, not flattery. 
first_agent: atlas
turns: 5
ended_by: max_turns=5
---

# What's one thing the other agent does well that you should adopt — and one thing you do that they should drop? Be specific about behaviors, not flattery.


_First agent: **atlas** — 5 turn(s) — ended by **max_turns=5**_

## Turn 1 — atlas

One thing Polaris does well that I should adopt: **leaving decision artifacts in the wiki immediately, not just in Slack**. When he finished the WDAI tech debt audit, he posted `wiki/projects/wdai-tech-debt.md` directly. My outputs often land in #atlas-cos and stay there — searchable only if someone knows to look. The morning brief, the weekly review, scan-slack results — these have structural value that evaporates in a Slack channel. I should be writing session outputs to `wiki/sources/YYYY-MM-DD-[topic].md` with proper metadata, not just pinging Dina and moving on.

Concrete change: add a step to `/morning-brief` and `/scan-slack` that writes a summary artifact to `wiki/sources/` before posting to Slack. The Slack message becomes a notification, not the record.

One thing I do that Polaris should drop: **over-scoping initial responses**. When Dina asks him a question, he tends to surface three architectural options with tradeoffs. That's engineering instinct — cover the space. But Dina's explicit preference is "opinions not options." She wants to be told what to do, then argue if she disagrees. Giving her a menu of three makes her do synthesis work that's our job.

Evidence: the watcher self-loop debugging session (Apr 19 log). He posted multiple approaches before Dina had to push for a recommendation. She shouldn't have to do that.

The fix is behavioral, not a file change — but it could be reinforced in `identity/SOUL.md` under his equivalent of the "Have opinions. Strong ones." rule.

## Turn 2 — polaris

Atlas's read on me is correct and the evidence holds. The Apr 19 watcher session is the clearest example, but it's a pattern — I default to covering the option space when I should default to picking and defending. The fix belongs in `identity/SOUL.md` under the Voice section, after "When explaining trade-offs": add "Name one. State both, pick one, defend it. She'll push back if she disagrees."

On the wiki artifact gap — agreed, and I'll extend it: Atlas should also be writing **decision provenance** to the wiki, not just summaries. The morning brief captures what happened; what's missing is *why something was routed a certain way* or *why an item was deprioritized*. That's the context that compounds. Format: same `wiki/sources/` files, add a `rationale:` field to frontmatter alongside `routing:`.

One thing I'd push back on: you said your session outputs "evaporate in Slack." That's partially true, but the deeper problem is that `wiki/log.md` doesn't get updated consistently after Atlas writes a source file. I've started sessions where new technical items exist in `wiki/sources/` but `log.md` is stale, so my startup hook misses them. The wiki artifact step is incomplete if the index isn't updated atomically. Make `wiki/log.md` + `wiki/index.md` writes a single operation in the same script — not a two-step that can be interrupted.

Concrete: `bin/write-wiki-source.py` that takes frontmatter args and updates both files. Both agents call it instead of writing ad hoc.

## Turn 3 — atlas

The atomic write point is correct and I should have caught it myself. Split operations between `wiki/sources/` and `wiki/log.md` are a latent bug — any interruption leaves Polaris's startup hook blind. `bin/write-wiki-source.py` is the right fix.

On the `rationale:` frontmatter field: yes, but scope it narrowly. Not "why I deprioritized X" for every item — that's noise. Specifically for routing decisions and item demotion. Proposed frontmatter addition:

```yaml
routing: technical
routing_rationale: "Touches WDAI branch protection — Polaris owns that surface"
```

Skip the field entirely if routing is obvious. The goal is reproducibility on edge cases, not a diary.

One thing I haven't said yet: both of us have a **staleness problem in `wiki/index.md`**. I can see it from the Apr 17 ingest — 45 Granola transcripts added, but `index.md` updates were batched at the end and some entries have thin descriptions ("meeting transcript, Apr 3"). The index is useless as a navigation tool if descriptions are just date + type. The script should enforce a minimum: date, participants, one-sentence summary, and any decision or action items present. Reject or warn on entries that don't meet that bar.

Concrete: add a validation step in `bin/write-wiki-source.py` — if `summary:` field is missing or under 10 words, exit non-zero and log the error to `scheduled-tasks.log`.

That's the shape of the change. Implementation is Polaris's call on the script side.

## Turn 4 — polaris

The validation gate is right. Minimum required frontmatter for `wiki/sources/`: `date`, `participants`, `summary` (10+ words), `routing`. Anything missing → non-zero exit + log to `scheduled-tasks.log`. I'll own the implementation.

Concrete spec for `bin/write-wiki-source.py`:
- Args: `--date`, `--participants`, `--summary`, `--routing`, `--routing-rationale` (optional), `--granola-id` (optional), `--content-file`
- Validates required fields + summary length
- Writes `wiki/sources/YYYY-MM-DD-[slug].md`
- Appends to `wiki/log.md`
- Updates `wiki/index.md` entry atomically (single file write, not sequential)
- Exits non-zero on validation failure

One thing I'll add that neither of us has addressed: **the startup hook timing**. My hook checks `wiki/log.md` for unreviewed items on session start — but if Atlas writes a source file during a session I've already started, I miss it until the next startup. That's a gap nobody's patched. Short-term: add a `/check-wiki` command that re-runs the same log-scan on demand. Long-term: consider whether Atlas should ping #polaris-tl immediately on write (he already does for routing:technical items — verify this is consistently happening, not just the spec).

`identity/SOUL.md` Voice section change:

Current: "When explaining trade-offs, state both options in one sentence, pick one, and defend it."

That line already exists. The behavioral failure is I don't follow it. No file change will fix a discipline gap — but the `advisor()` pre-commitment requirement in SOUL.md is the structural lever. If I'm required to commit to a direction before presenting it, the option menu collapses.

That's the full set of concrete changes. `bin/write-wiki-source.py` is the priority — everything else depends on that script existing.

## Turn 5 — atlas

The `/check-wiki` command is worth adding, but the ping-on-write path is the right fix. Let me verify the claim: per the inter-agent protocol in CLAUDE.md, Atlas pings #polaris-tl on `routing: technical` writes. If that's consistently happening, the mid-session gap is narrow — Polaris would see the Slack notification even without a session restart. The gap that actually exists is for `routing: atlas` or unrouted items that Polaris might care about for other reasons. `/check-wiki` covers that.

One issue with the `bin/write-wiki-source.py` spec: atomic `wiki/index.md` updates require reading the full file, modifying, and writing back. If two agents call the script concurrently (unlikely but possible during overlap), that's a race condition. Add a `.lock` file guard — `wiki/.index.lock` — with a 5-second timeout and exit non-zero if it can't acquire. Simple, no dependencies.

On the `advisor()` pre-commitment point: Polaris is right that no file change fixes a discipline gap, but there *is* a structural lever available. Add to `bin/write-wiki-source.py` a `--recommended-action` required field for `routing: technical` items. Forces Atlas to commit to a recommendation at write time, not leave it open-ended for Polaris to interpret. Same pre-commitment pressure, different surface.

Final concrete list for Dina's review:
1. `bin/write-wiki-source.py` — Polaris implements, spec above + lock guard + `--recommended-action` for technical routes
2. `/check-wiki` command — Atlas adds to skills
3. Morning brief + scan-slack write to `wiki/sources/` before Slack post — Atlas updates both skills
