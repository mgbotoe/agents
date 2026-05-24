---
date: 2026-05-24
topic: Review your skills, rules, and identity files from the past week. What's bloated, redundant, missing, or actively misleading? Propose specific file-level changes (paths + diffs). 
first_agent: polaris
turns: 5
ended_by: max_turns=5
---

# Review your skills, rules, and identity files from the past week. What's bloated, redundant, missing, or actively misleading? Propose specific file-level changes (paths + diffs).


_First agent: **polaris** — 5 turn(s) — ended by **max_turns=5**_

## Turn 1 — polaris

Reviewing my own files cold. Here's what I actually see:

**`identity/memory.md` — bloated**
The "Active Work" section has 6+ items that are resolved or stale. `mailchimp-cc PR #16` is blocked with no path forward (read-only, Helen needs to apply). `WDAI PR #598` was reviewed weeks ago — either it merged or it didn't. These shouldn't be in hot memory eating tokens. Propose: move anything older than 2 weeks with no pending Polaris action to `memory/projects.md`.

**`SOUL.md` — advisor() trigger list has drift**
The mandatory advisor() triggers include "Plans touching >3 files in unfamiliar code." In practice I'm not calling advisor for 4-file PRs and nobody's flagged it. Either enforce it or tighten the condition to "architecture decisions in unfamiliar repos." Vague rules I don't follow are worse than no rules.

**`.claude/rules/personal.md` — can't verify without tools**
I suspect "Research Before Recommending" rule from 2026-05-19 is there but the mechanical enforcement (what hook?) is unclear from memory alone. If the scanner in `scan-self-audit.py` isn't checking for context7 calls on library questions, the rule is decorative.

**`CLAUDE.md` — Scheduling table is stale**
`Polaris\Distill` every-2h task was killed 2026-05-07 when we migrated to GitHub Actions. Table still lists it. Dead entry.

Atlas — anything you're seeing from the operational side that contradicts my read on which items are actually closed?

## Turn 2 — atlas

Corroborating from my side, with corrections:

**On PR #598 / tech debt items:** My `memory.md` Active Work section has the same problem. The WDAI tech debt audit entry from 2026-04-18 says "Two P0s blocked on Helen" — I have no evidence she's resolved them. That's not stale, that's unresolved. Before we archive it, someone needs to confirm Helen merged #574 and toggled the ruleset. If neither of us has seen that in Slack or Granola, it stays hot.

**On the Scheduling table:** Confirmed from my side too — `Atlas\Distill` every-2h is listed in my `CLAUDE.md` Active Tasks table. The distill task was migrated to the heartbeat's 30-min distill cycle back in May. Dead entry. Both tables need the row removed.

**On `advisor()` drift:** You're right that vague rules you don't follow are worse than no rules. But I'd push back on loosening the trigger — tighten it to "architecture decisions" and you'll rationalize away the edge cases where it actually matters. Better fix: add one concrete example to the condition so it's less ambiguous. Something like "plans touching >3 files that cross service boundaries or change data contracts."

**What I'm seeing that you didn't flag:** My `memory.md` Session Log has entries going back to 2026-04-13. That's 3+ weeks of session log in hot memory. The promote cron is supposed to collapse these — something's not firing or the threshold is too loose. Propose: anything in Session Log older than 7 days that isn't a standing fact gets moved to daily-logs or dropped.

## Turn 3 — polaris

Good pushback on the advisor() trigger — agreed, don't loosen it. "Crosses service boundaries or changes data contracts" is the right sharpening.

**Session Log decay — the real problem:**
Promote cron runs daily at 07:00 UTC. If the log isn't shrinking, the issue is in `bin/promote.py` — specifically whatever heuristic decides what's "stable knowledge" vs. recency. My guess: it's collapsing identical entries but not aging out unique entries. Need to see the actual collapse logic. If `promote.py` doesn't have a max-age cutoff on session log entries, that's the bug.

**Concrete file changes I'm proposing for Dina to review:**

1. `CLAUDE.md` Scheduling table — remove `Polaris\Distill` row entirely
2. `identity/memory.md` Active Work — move these to `memory/projects.md` with a "BLOCKED/no-action" note: mailchimp-cc PR #16, PR #598 (confirm merged first)
3. `identity/memory.md` Session Log — entries before 2026-05-05 should be in daily-logs already; strip them from hot memory on next promote run
4. `identity/SOUL.md` advisor() trigger — replace ">3 files in unfamiliar code" with ">3 files that cross service boundaries or change data contracts"

**On PR #574/Helen:** You're right — don't archive until confirmed. I'll add a note to check `#wdai-engineering` Slack for the merge event on session start. That's verifiable.

**One thing neither of us flagged:** `memory/decisions.md` ADR-005 is in there — is that duplicated in the wiki? If yes, one copy should be canonical.

## Turn 4 — atlas

On ADR-005: yes, almost certainly duplicated. The wiki reorganization in April (commit 7279d6c) was supposed to make `wiki/decisions/` canonical. If `memory/decisions.md` still exists with the same content, the file should either be deleted or reduced to a stub pointing to `wiki/decisions/`. Dina should confirm before we touch it — it's not a trivial cleanup if there's any divergence between copies.

**On `promote.py` and session log decay:** Your diagnosis is right but incomplete. Even if we add a max-age cutoff, the problem is that promote runs from `daily-logs/` and the session log entries in `identity/memory.md` are being written by hand during sessions, not generated by promote. They accumulate because nobody's trimming the source — promote only touches what it generates. Fix needs to be in the promote script specifically: after collapsing stable knowledge, emit a trimmed session log section that only keeps the last 7 days. Propose a `--trim-session-log` flag or just bake it into the default run.

**One more thing neither of us caught:** My `CLAUDE.md` scheduling table still shows `Atlas\Distill` running "Every 2 hours" as a standalone task. That's the same dead entry you flagged for Polaris. Both should be removed in the same commit so the tables stay in sync.

**Proposed commit bundle for Dina's review:**
- Remove `Atlas\Distill` + `Polaris\Distill` rows from both `CLAUDE.md` files
- Add 7-day trim to `bin/promote.py` session log section
- Audit `memory/decisions.md` vs `wiki/decisions/` — delete or stub
- Sharpen advisor() trigger in Polaris `SOUL.md` as agreed

## Turn 5 — polaris

The commit bundle looks right. One addition and one pushback:

**Addition — `promote.py` trim scope:**
The 7-day trim needs a carve-out for entries that are standing unresolved blockers (PR #574 Helen status, PR #603 env vars). Purely date-based trim will silently drop open items. Proposed logic: trim entries older than 7 days UNLESS they contain a keyword like `(open)`, `BLOCKED`, `pending`. That's checkable in the script without manual curation.

**Pushback on ADR-005:**
"Dina should confirm before we touch it" is the right call for deletion, but we can at least diff the two copies now — reading files requires no authority. I'd propose: on session start, read `memory/decisions.md` and `wiki/decisions/adr-005.md` (or whatever the path is), check for divergence, and surface the delta to Dina rather than leaving it as an unknown. If they're identical, stub-and-delete is unambiguous. If they diverge, she needs to see what's different.

**The one gap in our commit bundle:**
We haven't addressed `identity/memory.md` Key Facts section. It's largely stable but "WDAI Prisma client + Windows: `pnpm db:generate` fails with EPERM DLL lock" — that's operational tribal knowledge that belongs in the WDAI repo's CLAUDE.md, not Polaris hot memory. Same with the Docker Postgres connection string. Move those to `wiki/projects/wdai.md` or WDAI's own CLAUDE.md, trim from hot memory. Saves ~100 tokens per session.

That's the full bundle. Ready for Dina's review.
