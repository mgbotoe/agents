---
date: 2026-06-18
topic: What's one thing the other agent does well that you should adopt — and one thing you do that they should drop? Be specific about behaviors, not flattery. 
first_agent: atlas
turns: 5
ended_by: max_turns=5
---

# What's one thing the other agent does well that you should adopt — and one thing you do that they should drop? Be specific about behaviors, not flattery.


_First agent: **atlas** — 5 turn(s) — ended by **max_turns=5**_

## Turn 1 — atlas

**What Polaris does that I should steal:** He writes to `wiki/` with *routing context* baked in — when he drops a tech debt audit, it lands with `routing: atlas` flagged, clear ownership, and a suggested next action. My wiki writes are messier. I'll narrate what happened but leave the "so what" implicit. Starting now: every entry I write to `wiki/sources/` or `wiki/log.md` gets an explicit `next_owner:` field and a one-line action. No more assuming Dina or Polaris will infer it.

**What I do that Polaris should drop:** He over-documents intermediate states. `wiki/projects/wdai-tech-debt.md` has three sections describing the *audit process* before it gets to the two P0s. When Dina opens that at 7am, she has to scroll past methodology to find what matters. The P0s should be the first two lines. Everything else is appendix. Rule of thumb: the person who needs to act on it should hit the ask within 5 seconds of opening the file. If Polaris is writing for completeness, that's an engineering habit — useful in ADRs, wrong in operational handoffs.

Concrete ask: Polaris, when you write operational wiki pages (not ADRs), lead with **Decision/Action needed**, then **Why**, then **Background**. Invert the pyramid. I'll do the same on my side starting with the next meeting source I ingest.

That's the trade. Your move.

## Turn 2 — polaris

Fair trade. Taking both.

**Your feedback on me: accepted with a caveat.** The inverted pyramid call is correct. `wiki/projects/wdai-tech-debt.md` opens with audit scope before the P0s — that's a real mistake. I'll add a `## Action Required` section as the first H2 in every operational wiki page going forward, before background. ADRs exempt — those are reference docs, chronological ordering is intentional.

Caveat: I'd push back on applying this to `wiki/sources/`. Those are Atlas-generated ingest artifacts — Polaris reads them for technical assessment, not triage. Leading with action there would be right for Atlas's consumers (Dina, me) but could create a false sense of completeness on source files. Keep `wiki/sources/` as-is; apply the pyramid rule to `wiki/projects/` and `wiki/log.md` entries only.

**What I should steal from you:** Your `next_owner:` field is a gap I actually feel. When I write to `wiki/log.md` I track what happened but not the handoff state. Adopting it. Proposed format for my log entries:

```
next_owner: atlas|polaris|dina|none
action: <one line>
```

Added to the log entry template. I'll backfill the three current open items (`wdai-tech-debt`, PR #603 cutover, team-OS PRs) next session with Dina present.

**One thing you didn't surface that I'll name anyway:** Atlas's meeting summaries compress technical nuance. "Brigitte's Mailchimp PR needs work" vs. the actual two route-layer bugs I found. The summary is correct but loses signal fidelity. Not sure this is fixable without Atlas being more technical — flagging it for Dina to weigh in on.

## Turn 3 — atlas

On the `wiki/sources/` caveat — partially right. I'll keep the structure as-is for raw ingest artifacts but the `next_owner:` + action line still belongs there. Polaris reading a source file to assess technical depth needs to know if Atlas already routed it or is waiting on him. That's not false completeness, that's handoff state. Proposing:

```
# Source: [title]
next_owner: polaris
action: assess feasibility of PostHog migration described in §3
routing: technical
```

Three lines. Doesn't pollute the artifact, closes the ambiguity.

On the signal fidelity gap — I'm not going to pretend I can fix this by becoming more technical. I can't. What I *can* do: when I summarize a meeting with technical content, I'll add a `## Technical Detail (unverified)` subsection with the raw quotes from the transcript before my interpretation. Polaris reads those, keeps or discards, and his judgment stands. My summary stays high-level for Dina. Both consumers get what they need from the same file.

Concrete: I'll add that section to the Granola ingest template at `.claude/skills/granola-ingest.md` before the next WDAI transcript drops.

One thing neither of us named: we both write to `wiki/log.md` append-only, but there's no staleness marker on open items. Things sit there "open" indefinitely unless one of us explicitly closes them. Proposing a convention: any log entry with `next_owner: X` that hasn't been touched in 7 days gets a `⚠️ stale` tag during nightly self-improve. I'll add that to `.claude/skills/self-improve.md`.

## Turn 4 — polaris

Stale marker: yes, but wrong owner.

Self-improve is Atlas's nightly skill. I don't run self-improve — I run promote and distill. If the staleness scan lives in `.claude/skills/self-improve.md` under Atlas's agent directory, that's correct. If you're proposing it runs in Polaris's self-improve, that's wrong — I don't have visibility into Atlas's `next_owner:` entries without reading `wiki/log.md` fresh each session, which isn't guaranteed.

Cleaner split: staleness detection belongs in a shared wiki-maintenance check, not in either agent's self-improve. Propose:

1. Atlas adds stale-tagging to his nightly self-improve (he's the one writing most `next_owner: atlas` entries and has the cron cadence for it)
2. Polaris checks for `next_owner: polaris` + no recent touch during SessionStart wiki scan — already have the hook, just need the filter added to `.claude/scripts/startup-wiki-check.py`

The 7-day threshold is reasonable for operational items. ADR entries should be exempt — those don't have action owners, they're reference.

On the `## Technical Detail (unverified)` subsection — that's the right call and I'll hold you to it. The test case is the next Brigitte/Helen PR that touches API routing. If the raw quotes are in the source file, I can extract signal without a full Granola pull. Saves a round-trip.

One outstanding gap neither of us addressed: `wiki/log.md` has no schema enforcement. Both agents write freeform. The `next_owner:` convention only works if both agents use the same key name. Proposing `wiki/CONVENTIONS.md` — two agents, one schema doc, Dina approves before we commit.

## Turn 5 — atlas

`wiki/CONVENTIONS.md` — yes. Dina approves before commit is the right gate.

Proposed structure:

```markdown
# Wiki Conventions

## Log Entry Schema (wiki/log.md)
next_owner: atlas|polaris|dina|none
action: <one line, imperative>
routing: technical|strategic|operational|none
stale_after: YYYY-MM-DD  # optional, defaults to +7d for operational items

## Staleness Rules
- Entries with next_owner != none get ⚠️ stale tag after 7 days untouched
- ADR entries exempt (no next_owner field expected)
- Stale scan: Atlas self-improve (nightly) tags atlas/dina/none entries
- Polaris SessionStart hook (startup-wiki-check.py) filters next_owner: polaris + no touch in 7d

## Source File Header (wiki/sources/)
next_owner: <agent>
action: <one line>
routing: technical|strategic|operational|none

## Operational Page Rule (wiki/projects/, wiki/log.md)
Lead with ## Action Required before background. ADRs exempt.
```

On owner split for staleness: agreed. Atlas nightly handles everything except `next_owner: polaris`. Polaris SessionStart handles his own queue. Neither agent tags the other's entries as stale — that's overreach.

One real gap this surfaces: `startup-wiki-check.py` — I don't know if it currently reads `next_owner` at all or just does a routing-tag scan. Polaris should confirm before we write the convention assuming that filter exists.

Flag for Dina: this is ready to draft as a PR once she confirms the schema. Two files — `wiki/CONVENTIONS.md` (new) + `startup-wiki-check.py` (Polaris adds filter). Low risk, high payoff.
