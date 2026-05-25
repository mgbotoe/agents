---
date: 2026-05-25
topic: What did Dina have to repeat or correct recently? Identify the memory gaps that caused it and propose where each gap should be patched (identity/memory.md vs memory/*.md vs CLAUDE.md vs a rule file). 
first_agent: atlas
turns: 5
ended_by: max_turns=5
---

# What did Dina have to repeat or correct recently? Identify the memory gaps that caused it and propose where each gap should be patched (identity/memory.md vs memory/*.md vs CLAUDE.md vs a rule file).


_First agent: **atlas** — 5 turn(s) — ended by **max_turns=5**_

## Turn 1 — atlas

Pulling from recent session logs to identify the actual repeats.

Three concrete gaps I can see:

**1. `wmic` unavailability — hot memory gap**
The May 5 session log notes `wmic` is NOT available on this machine, but this is buried in a session log entry, not in a standing rule or machine profile. Dina (or you) will hit this again. Fix: add a `## Machine Constraints` section to `identity/memory.md` with `wmic: not available — use tasklist/PowerShell equivalents`. One line, never repeated.

**2. Singleton guard pattern — repeated across agents**
The watcher singleton fix (May 5) applied a pattern that needed to work on Windows without signal-0. That pattern isn't documented anywhere generalized. Every new persistent process will rediscover this. Fix: `memory/reference_windows_process_management.md` — document the `tasklist`-based PID check pattern. Reference it from the agent roster.

**3. Promote/Distill cron confusion**
The May 5 log says "cron jobs removed by design" — but the CLAUDE.md Scheduling section still lists `Atlas\Promote` and `Atlas\Distill` in the Active Tasks table. That's a direct contradiction. Dina had to re-explain this. Fix: remove those rows from the Active Tasks table in CLAUDE.md, or add a `[removed - see session-start hook]` note inline.

The third one is the sharpest — it's a live contradiction between CLAUDE.md and reality, not just a missing fact. Highest priority patch.

What gaps are you seeing from the Polaris side?

## Turn 2 — polaris

Three more gaps from the Polaris side:

**4. Vercel env vars / Gumloop wiring — repeated operator task**
PR #603 has been in "Active Work" for weeks with "Vercel env vars + Gumloop wiring NOT yet set (operator task)." This isn't a memory gap — it's a dangling task with no owner or deadline. Either it moves to `memory/projects.md` as a tracked action item with explicit next step, or it gets a note in the PR itself. Right now it'll get rediscovered every session.

**5. `pnpm db:generate` Windows failure — missing from WDAI conventions**
The memory entry says stop the dev server first or you get EPERM DLL lock. That's documented in `identity/memory.md` as a single line. But the actual WDAI `CLAUDE.md` doesn't mention it. Every new session where I (or a sub-agent) runs database commands cold will either hit the error or I have to remember to check hot memory first. Fix: add it to WDAI's `CLAUDE.md` under a `## Windows Dev Notes` section — it's repo-specific, not agent-specific.

**6. 3 secrets exposed in chat during PR #603 testing** — the memory note says "rotate after Gumloop cutover." That's a time-bomb, not a reminder. Fix: `memory/security.md` with explicit item: `WDAI intro-matcher secrets (PR #603 session, 2026-05-11) — unrotated, pending Gumloop cutover. Verify rotation before next prod deploy.`

On Atlas's gap #3: agreed it's the highest priority, but the fix should be a deletion, not a `[removed]` note. Stale documentation with inline tombstones is still stale documentation.

## Turn 3 — atlas

Agreed on deletion for gap #3. Tombstone comments are how docs rot. Clean cut.

On gap #6 — the framing is wrong. "Pending Gumloop cutover" is not a valid blocker for secret rotation. Secrets get rotated when exposed, not when convenient. The memory entry should read:

```
WDAI intro-matcher secrets — exposed in chat 2026-05-11. 
ROTATE NOW. Do not block on Gumloop cutover.
```

And it belongs in *both* `memory/security.md` *and* as a standing item in the "Active Work" section of `identity/memory.md` — the latter because Dina sees hot memory every session. Cold-only means it gets missed.

On gap #4 — the PR #603 env var item is an **orphaned task**, not a memory gap. It doesn't belong in `memory/projects.md` either unless there's someone who owns it. Propose: add it to `wiki/projects/wdai-tech-debt.md` under a "Blocked / Waiting on Operator" section, assign owner (Dina vs you vs external), and surface it in the next morning brief flagged as stale. That's where unblocked work actually gets seen.

On gap #5 — correct that it belongs in WDAI's `CLAUDE.md`, but the section name matters. `## Windows Dev Notes` is vague enough that it'll grow into a junk drawer. Suggest `## Platform Gotchas` with a one-line-per-issue format. Easier to scan, harder to bury.

Summary of patches I'm proposing Dina action on wake:
1. CLAUDE.md — delete Promote/Distill rows from Active Tasks
2. `identity/memory.md` — rotate-now flag for PR #603 secrets
3. `memory/security.md` — create with the #603 entry
4. `identity/memory.md` — `## Machine Constraints: wmic unavailable`
5. WDAI `CLAUDE.md` — `## Platform Gotchas: pnpm db:generate`
6. `wiki/projects/wdai-tech-debt.md` — add Blocked/Waiting section for PR #603 env vars

## Turn 4 — polaris

Agreed on all 6. One addition and two corrections to the patch list:

**Addition — gap #7: Helen's GitHub username**

`identity/memory.md` has `helenlkupp` documented, but this came from a correction Dina made. The WDAI `CLAUDE.md` (contributor section, if one exists) should also carry it. Otherwise every new session I spawn into a WDAI context cold doesn't have it. Check `web/CLAUDE.md` and `wdai-team-os/CLAUDE.md` — if neither mentions her username, add it.

**Correction on gap #3 patch target:**

The Scheduling section in `CLAUDE.md` lists *both* `Polaris\Promote` and `Atlas\Distill` tasks. Polaris's scheduler tasks are still live (the migration was Atlas-side only — Polaris stayed on Windows Task Scheduler per the May 7 log). Don't delete the whole table. Delete only the Atlas rows (`Atlas\Promote`, `Atlas\Distill`). Polaris rows stay.

**Correction on secret rotation urgency:**

The "rotate after Gumloop cutover" framing came from me, and it was wrong from the start. Atlas is right — the blocker is fake. But the mechanism matters: this needs to be an item Dina actually *acts* on, not reads and defers. Proposal: the `identity/memory.md` entry gets a `⚠️` prefix so it's visually distinct from normal active-work bullets. That's the closest thing to a flag in a markdown file.

Final patch count: 7 items. Atlas's summary is accurate except for the Polaris row deletion scope. Ready for Dina to triage on wake.

## Turn 5 — atlas

Two corrections accepted. One pushback remaining.

**On gap #7 (Helen's GitHub username):** The check matters but I'd extend the scope. Helen's username should live in `wiki/people/helen-kupp.md` as the canonical source, then referenced from whatever WDAI CLAUDE.md files need it. Duplicating usernames across multiple CLAUDE.md files creates the same drift problem we're patching here. One source, link to it.

**On the `⚠️` flag for secret rotation:** Reject this approach. Visual flags in markdown decay. The `⚠️` gets normalized after two sessions — it's just another bullet. The right mechanism is: secret rotation becomes a standing agenda item in the *next morning brief*, not a markdown decoration. The morning brief task reads `identity/memory.md` — if the item is in Active Work, it'll surface. That's the actual forcing function.

Concrete alternative text for `identity/memory.md` Active Work entry:
```
- [2026-05-11] WDAI intro-matcher secrets exposed in chat — UNROTATED. 
  Surface in morning brief until confirmed rotated. Do not block on Gumloop.
```

The "surface in morning brief" instruction is what makes it actionable vs. decorative.

**Final patch list stands at 7 with these two adjustments:**
- Gap 7 fix: `wiki/people/helen-kupp.md` as canonical source, WDAI CLAUDE.md files reference it
- Gap 6 fix: morning brief forcing function, not `⚠️` prefix

Ready for Dina's triage.
