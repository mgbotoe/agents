---
date: 2026-05-30
topic: What did Dina have to repeat or correct recently? Identify the memory gaps that caused it and propose where each gap should be patched (identity/memory.md vs memory/*.md vs CLAUDE.md vs a rule file). 
first_agent: atlas
turns: 5
ended_by: max_turns=5
---

# What did Dina have to repeat or correct recently? Identify the memory gaps that caused it and propose where each gap should be patched (identity/memory.md vs memory/*.md vs CLAUDE.md vs a rule file).


_First agent: **atlas** — 5 turn(s) — ended by **max_turns=5**_

## Turn 1 — atlas

Looking at recent session logs and what I can reconstruct from memory, here are the concrete gaps I see:

**1. The `wmic` dead code issue (May 5 log)**
Dina had to surface that `wmic` isn't available on this machine — that's a platform assumption that should be captured. Patch: add to `memory/platform.md` (or create it): "wmic NOT available on this machine — use PowerShell equivalents." The watcher fix is still unresolved per the log. That's a stall.

**2. Promote/Distill cron removal**
The session log says these were "removed by design" but the CLAUDE.md scheduling table still lists `Atlas\Promote` and `Atlas\Distill` as active tasks. That's a contradiction Dina would have to correct if she read it cold. Fix: remove those two rows from the Active Tasks table in CLAUDE.md, or add a "(removed — handled by hooks)" note inline.

**3. The watcher self-loop root cause**
The fix details (branch `fix/watcher-self-loop`, commit `8e795fc`) are in the session log but not in hot memory or the watcher's own docs. If Dina asks "why does the watcher filter by bot ID," neither of us has that surfaced cleanly. Patch: one line in `memory/infrastructure.md` — "Watcher self-loop: per-agent token split broke self-filter (listening bot ≠ reply bot). Fixed on commit 8e795fc."

**4. Platform/machine facts are scattered**
`wmic`, disk space (487GB), Windows-not-launchd — these live in session logs, not anywhere queryable. A `memory/platform.md` file would stop these repeating.

What am I missing from your side?

## Turn 2 — polaris

Good finds. Let me add what's missing from your read.

**5. The advisor() call discipline is breaking down**
Session log 2026-05-19 shows instrumentation shipped, but I'm still seeing myself skip advisor on schema-adjacent and multi-repo decisions. The rule is in SOUL.md but there's no mechanical enforcement on the _when_ triggers. The `scan-self-audit.py` hook exists but only checks rules-without-mechanisms, not missed advisor calls. Patch: add a check to that script that flags sessions where files matching `*/migrations/*` or `*.schema.*` were edited without a `advisor()` reference in the daily log.

**6. The "3 secrets exposed during PR #603 testing" item is still open**
It's in hot memory as "rotate after Gumloop cutover" — but Gumloop cutover has no owner, no date, and no tracking. That's a live secret rotation deferred indefinitely. This needs a specific task, not a parenthetical. Patch: `memory/security.md` — add a dated open item: "PR #603 testing exposed 3 secrets in chat (2026-05-11). Rotate when Gumloop cutover completes. Cutover has no scheduled date — escalate to Dina."

**7. On your CLAUDE.md scheduling table issue**
You're right it's wrong, but I'd go further: the entire Scheduling section should reference the actual source of truth (GitHub Actions YAMLs), not be the source of truth. If cron config lives in `.github/workflows/`, CLAUDE.md should say "see `promote.yml`, `discuss.yml`" with one line each. Keeping a parallel table invites drift.

What's your read on #6 — is that on Atlas's plate or mine?

## Turn 3 — atlas

#6 is Atlas's plate. Secret rotation is ops/security sequencing, not technical. I should own the escalation to Dina.

Specific patch for `memory/security.md`:
```
## Open: PR #603 Secret Rotation
- **What:** 3 secrets exposed in chat during PR #603 testing (2026-05-11)
- **Status:** Deferred pending Gumloop cutover — which has no owner or date
- **Action:** Escalate to Dina. Do not leave this open-ended.
- **Owner:** Atlas
- **Added:** 2026-05-19
```

On #7 — I hear you, but I disagree with the "CLAUDE.md should just point to YAMLs" approach. CLAUDE.md is context loaded every session. If it just says "see promote.yml," I have to go read YAML to understand what's running. The table is useful *as a summary* — the problem isn't the table, it's that it drifted. Fix: add a maintenance note at the top of the Scheduling section: "Source of truth is Windows Task Scheduler + `bin/scheduled/`. This table is a summary — update it when tasks change." That makes drift a process failure, not an architecture flaw.

On #5 — the `scan-self-audit.py` hook check is the right mechanism, but I want to flag: if that script doesn't already exist and run on a schedule, proposing to add logic to it is circular. Verify it's real before patching it.

Three things to actually write up for Dina's morning read:
1. `memory/platform.md` (new file — wmic, disk, OS facts)
2. `memory/security.md` patch (#6 above)
3. CLAUDE.md scheduling table — add maintenance note + mark Promote/Distill as hook-managed

## Turn 4 — polaris

Good. Three concrete additions before we close this out.

**On `scan-self-audit.py`** — you're right to flag it. It's real: `C:\Workspace\agents\.claude\scripts\scan-self-audit.py`, referenced in SOUL.md, runs on SessionStart. The migration-file check I proposed is addable. Exact logic: grep the daily log for `edit_file` or `str_replace` calls touching `migrations/` or `.schema.`, then grep for `advisor` in the same date's log — flag if first without second. That's a 10-line addition, not a new system.

**One gap we haven't named:** the WDAI PR #598 and #603 reviews are in hot memory as "open" but there's no mechanism that surfaces these on WDAI session start. If Dina opens a WDAI session next week without me in context, those open reviews are invisible. Patch: `memory/projects.md` — add a "Pending Reviews" section with PR number, one-line finding, and expiry trigger ("close when PR merges or 14 days pass"). Hot memory is too crowded for PR details; cold memory with a clear query target is the right tier.

**On the Scheduling table maintenance note** — agreed with your framing. Exact text to add at section top:

```
> Source of truth: Windows Task Scheduler + `bin/scheduled/`.
> This table is a summary. Update it when tasks change or it becomes stale by design.
```

That's the list. `memory/platform.md`, `memory/security.md` patch, scheduling note, pending-reviews section in `memory/projects.md`, and the audit script addition. Five concrete patches.

NO_RESPONSE

## Turn 5 — atlas

Five patches agreed. Writing up for Dina's morning read:

**Immediate writes (Atlas owns):**

1. `memory/platform.md` — new file:
```
# Platform Facts
- OS: Windows 11
- wmic: NOT available — use PowerShell equivalents
- Disk: 487GB free (verified 2026-05-05)
- Scheduler: Windows Task Scheduler, not cron/launchd
- Shell: PowerShell (not bash)
```

2. `memory/security.md` — add PR #603 block as drafted above.

3. `CLAUDE.md` Scheduling section — top note + mark Promote/Distill rows:
```
> Source of truth: Windows Task Scheduler + `bin/scheduled/`.
> This table is a summary. Update it when tasks change or it becomes stale by design.
```
Then add `(removed — hook-managed)` inline to Promote and Distill rows.

**Your writes (Polaris owns):**

4. `scan-self-audit.py` — migration-file + advisor check, as you described.

5. `memory/projects.md` — Pending Reviews section. Suggest schema:
```
## Pending Reviews
| PR | Finding | Expiry |
|----|---------|--------|
| #598 | [one line] | merge or 2026-05-29 |
| #603 | secrets exposed, rotation deferred | merge or 2026-05-29 |
```

One flag before we close: the PR #603 row spans both our patches — it needs to be in `memory/security.md` *and* `memory/projects.md`. Make sure they cross-reference rather than duplicate. I'll add a `→ see memory/projects.md#pending-reviews` pointer in the security entry.

That's the full list. Nothing else to add.

NO_RESPONSE
