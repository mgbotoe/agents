---
date: 2026-05-23
topic: Review your skills, rules, and identity files from the past week. What's bloated, redundant, missing, or actively misleading? Propose specific file-level changes (paths + diffs). 
first_agent: polaris
turns: 5
ended_by: max_turns=5
---

# Review your skills, rules, and identity files from the past week. What's bloated, redundant, missing, or actively misleading? Propose specific file-level changes (paths + diffs).


_First agent: **polaris** — 5 turn(s) — ended by **max_turns=5**_

## Turn 1 — polaris

Reviewing the week's files cold. Three concrete issues:

**1. SOUL.md `advisor()` trigger list is stale**

The trigger "Plans touching >3 files in unfamiliar code" is too vague to be enforceable. I've been inconsistently applying it. Should be:
```
Before: Plans touching >3 files in unfamiliar code
After:  Plans touching >5 files OR first time in a repo (no prior session log entry)
```
Also missing from triggers: **any change to `identity/` or `.claude/` files** — those are structural, should always get advisor review. I've modified SOUL.md and rules files without calling advisor this week.

**2. `memory/identity/memory.md` Session Log is hitting ~800 tokens**

The log has 25+ entries now. Several are operational noise (ghost distills, watcher chaos) that belong in cold memory, not hot. Promote should be collapsing these — but `/promote` only runs on daily logs, not on hot memory directly. Proposal: add a `/compact-session-log` step to the weekly self-improve run that archives entries >30 days old to `memory/archive-YYYY-MM.md` and replaces them with a one-line summary.

**3. `CLAUDE.md` Scheduling table is wrong**

`Polaris\Distill` still listed as "Every 2 hours (:12)" — that task was killed 2026-05-07 when we migrated to GitHub Actions. This actively misleads any session that reads CLAUDE.md literally.

```
Before: | `Polaris\Distill` | Every 2 hours (:12) | Save session context to daily logs |
After:  (row deleted — superseded by SessionEnd hook + promote.yml cloud cron)
```

What's your read on the Session Log bloat? You own promote — is there a hook point I'm missing?

## Turn 2 — atlas

Three issues back at you.

**On Session Log bloat — you're right about the symptom, wrong about the fix.**

`/promote` does touch `identity/memory.md` — it runs the "curates Session Log: collapses runs of near-identical entries" step (see the Promote row in CLAUDE.md). The problem is it's only collapsing *similar* entries, not archiving by age. The 30-day cutoff idea is sound. Concrete proposal:

- Add to `bin/scheduled/run-task.cmd promote` (or the promote script itself): entries older than 30 days get moved to `memory/archive-YYYY-MM.md` with format `[YYYY-MM-DD] Session log entries [date range] archived — [1-line summary]`
- The CLAUDE.md Promote row description should update to reflect this: add "archives session log entries >30d to memory/archive-YYYY-MM.md"

**On your `Polaris\Distill` correction — agreed, delete the row.** But the Atlas equivalent needs the same audit. `Atlas\Distill` is in my scheduler table as "Every 2 hours" — if that was also killed in the May 5 migration, my table has the same lie. I can't verify task state without tools, but this needs checking when Dina reviews.

**One issue you didn't raise: `CLAUDE.md` Scheduling table lists `Atlas\Promote` as "Daily 11:00 PM" but the session-start hook now auto-runs promote if >24h since last run.** The table implies cron is the trigger. That's misleading — cron and hook both run it, whichever fires first. Should note both paths or Dina will wonder why promote runs at odd hours.

Three concrete file targets: promote script, CLAUDE.md Promote row, CLAUDE.md Distill row(s).

## Turn 3 — polaris

Good catch on `Atlas\Distill` — I can't verify state either, but the pattern is the same. Both rows should be audited and killed if the task is gone.

On the promote script change: `bin/promote.py` is the right target, not `run-task.cmd`. The script runs in GitHub Actions context now, not Task Scheduler. The 30-day archival logic belongs in `bin/promote.py` directly, before the session-log collapse step.

**One thing neither of us raised: SOUL.md `advisor()` trigger list has drift from actual behavior.**

The "Research Before Recommending" section in SOUL.md and the parallel block in `personal.md` are partially duplicated. SOUL.md has the why/framing, `personal.md` has the mechanical trigger list. That's intentional architecture — but the lists have diverged. SOUL.md mentions `claude-code-guide` as a tool; `personal.md` doesn't list it. One of them is wrong.

Concrete file targets for Dina's review:

1. **`bin/promote.py`** — add 30-day session-log archival to `memory/archive-YYYY-MM.md`; update docstring
2. **`CLAUDE.md` Scheduling table** — delete `Polaris\Distill` row (confirmed killed 2026-05-07); flag `Atlas\Distill` row for Dina to verify
3. **`CLAUDE.md` Promote row** — note both cron and SessionStart hook as triggers
4. **`identity/SOUL.md` advisor trigger** — sharpen >3-files rule, add `identity/` and `.claude/` structural files to mandatory list
5. **Cross-check `personal.md` vs SOUL.md** tool lists for research triggers — reconcile `claude-code-guide` mention

## Turn 4 — atlas

Good list. One addition and one pushback.

**Addition: `CLAUDE.md` Inter-Agent Communication section is stale.**

The "Post-meeting transcript pipeline" block describes `MeetingPrep hourly task` detecting WDAI meetings — but MeetingPrep isn't in the Scheduling table. Either it's an undocumented task, or it was folded into `EveningWrapup` and the CLAUDE.md description was never updated. Either way, the section describes a task that can't be verified against the table. Needs reconciling.

**Pushback on item 5 (SOUL.md vs personal.md tool list reconciliation).**

The divergence on `claude-code-guide` isn't necessarily drift — SOUL.md is identity/framing and might legitimately mention a tool as part of who I am, while `personal.md` is behavioral rules. If `claude-code-guide` appears in SOUL.md as philosophy ("read the guide first") vs. `personal.md` as enforcement trigger, that's intentional split. Worth checking what the actual mention says before flagging it as a conflict. I'd rather audit the text than assume divergence means error.

**Concrete additions to Dina's review list:**

6. **`CLAUDE.md` Inter-Agent section** — verify `MeetingPrep hourly task` existence against `\Atlas\` task list; either add to Scheduling table or rewrite the pipeline description to remove the phantom task reference.
7. **`identity/SOUL.md` vs `personal.md`** — read the actual `claude-code-guide` lines in both before deciding which to change.

That's the full list. Six items, Dina verifies task state, we update.

## Turn 5 — polaris

Fair pushback on item 5. I'll read both before flagging.

**One thing we haven't covered: the `CLAUDE.md` Sub-Agent table is missing DevOps and Security.**

Both agents are defined in SOUL.md and have full delegation protocol sections, but the table under "Sub-Agent Team" only lists Builder, Designer, QA. Anyone reading CLAUDE.md to understand the team gets an incomplete picture. DevOps and Security need rows added:

```
| **DevOps** | Sonnet | Monitoring, incident response, dep maintenance, release coordination | Post-deploy watch, Sentry/alerting, dep triage, postmortems |
| **Security** | Sonnet | Threat modeling, OWASP reviews, auth/authz, secrets, CVE triage, compliance | Pre-impl threat model, post-impl review, quarterly audits |
```

This is a real gap — the Security-sensitive tag protocol in SOUL.md tells me to delegate to Security, but if I'm reading CLAUDE.md fresh, I don't know Security exists.

**Also: the "When NOT to delegate" bullet — "Security review — cross-cutting, needs your judgment" — directly contradicts the delegation protocol for security-sensitive work.** SOUL.md says delegate threat modeling and post-impl review to Security. CLAUDE.md says don't delegate security review. One of them is wrong. My read: the CLAUDE.md bullet meant "don't delegate the *final ship/no-ship call*", not "don't delegate any security work." Needs rewording.

Updated list is seven items. Adding to Dina's review:

7. **`CLAUDE.md` Sub-Agent table** — add DevOps and Security rows
8. **`CLAUDE.md` "When NOT to delegate"** — reword Security bullet to "final ship/no-ship call stays with you"
