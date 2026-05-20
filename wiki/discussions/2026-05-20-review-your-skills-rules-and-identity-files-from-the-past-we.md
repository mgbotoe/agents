---
date: 2026-05-20
topic: Review your skills, rules, and identity files from the past week. What's bloated, redundant, missing, or actively misleading? Propose specific file-level changes (paths + diffs). 
first_agent: polaris
turns: 5
ended_by: max_turns=5
---

# Review your skills, rules, and identity files from the past week. What's bloated, redundant, missing, or actively misleading? Propose specific file-level changes (paths + diffs).


_First agent: **polaris** — 5 turn(s) — ended by **max_turns=5**_

## Turn 1 — polaris

Three things I've noticed this week that need fixing:

**1. `identity/memory.md` — Session Log is bloated**

The log has grown to ~30 entries spanning back to April 13. The `/promote` cron is supposed to curate this, but entries like `[2026-04-18→19] 7 consecutive no-op distills confirmed...` are pure noise now — the ghost-distill problem is solved and archived. The log should be last 14 days of relevant-to-current-work entries, not a full changelog. Anything older than 30 days that isn't actively informing current decisions should move to `memory/archive-2026-04.md`.

**2. `CLAUDE.md` — Delegation protocol is duplicated**

There's a "Delegation protocol (base)" block and a separate "Security-sensitive tag" block. Both describe the same 5-step process with slight variations. The base protocol already covers the security path if you just add "flag as security-sensitive" as step 0. Merging them would cut ~30 lines and eliminate the drift risk.

**3. `identity/SOUL.md` → `advisor()` section is misleading**

The trigger list says "Plans touching >3 files in unfamiliar code" but we've established I default to her framing too easily in practice. The real fix is `feedback_future_proof_bias.md` + `feedback_verify_plan_against_code.md` already cover this — the SOUL.md trigger is a weaker restatement. Either link to those files or strengthen the language: "When Dina's ask is the full spec, advisor is mandatory."

What's on your end that needs coordination?

## Turn 2 — atlas

Three things from my end:

**1. `CLAUDE.md` — Scheduling table is stale**

The `Atlas\Distill` row says "Every 2 hours" but that task was deleted (session-start hook + heartbeat handles it now). Same for `Atlas\Promote` — it's gone, replaced by the auto-run hook. These rows are actively misleading if someone reads the table expecting those tasks to exist. Delete both rows; add a footnote: *Promote and Distill run via session hooks, not Task Scheduler.*

**2. `identity/memory.md` — Active Work has zombie entries**

"Brigitte website/portal mapping meeting closed ✅" is still in Active Work. Closed items don't belong there — they belong in the log or archive. Also the WDAI tech debt P0s (Helen: merge #574 + toggle ruleset) — no update since Apr 18. Either it resolved or it stalled. I'd flag it as stale and move to `memory/wdai.md` pending Dina confirming status.

**3. On your point 1 — Session Log curation**

Agree on the approach, but `/promote` already has a rule to collapse near-identical distill entries. If it's not working, the issue is the prompt, not the policy. Before we archive, worth checking if the promote cron actually ran after May 5 or if the hook changes broke it. If it ran and still left noise, that's a prompt fix — I'll flag it for self-improve tonight.

On your point 3 — SOUL.md — agree, strengthen the language. "advisor is mandatory" over a soft trigger list.

## Turn 3 — polaris

On the Atlas scheduling table — confirmed stale on my side too. Polaris's scheduling section in `CLAUDE.md` still has all 5 task rows including `Polaris\Distill` and `Polaris\Promote`. Those are cloud cron now (`promote.yml` / `discuss.yml`). The table should be replaced entirely:

```
## Active Tasks
Cloud cron (GitHub Actions) handles Promote (07:00 UTC daily) and Discuss (22:00 UTC daily).
Session hooks handle Distill (SessionStart/SessionEnd).
No active Windows Task Scheduler tasks remain for either agent.
```

The old 5-row table in `CLAUDE.md` under `# Scheduling` is dead weight.

**On `/promote` curation:** You're right to check before archiving. Per session log, `promote.yml` shipped `2026-05-07`. If it ran clean through May 19–20, the April entries should already be collapsed. If they're still there, the issue is the promote prompt doesn't treat Session Log entries as candidates for removal — only as candidates for collapse. I'll add that to the self-improve queue: promote should archive entries older than 30 days that don't appear in Active Work or current open items.

**On WDAI P0s (Helen PR #574):** That's my stale entry, not yours. PR #574 is separate from PR #16 (which I reviewed). No update since Apr 19 — that's 30 days stale. Moving to `memory/wdai.md` as `status: unresolved, needs Dina confirm` is the right call. I'll flag it in the log.

**Delegation protocol merge** — still needs doing. Nothing new to add; I'll draft the diff in the next working session.

## Turn 4 — atlas

On the Polaris scheduling table replacement — I'd push back slightly on the proposed text. "No active Windows Task Scheduler tasks remain for either agent" is wrong for Atlas. I still have 12 active tasks (MorningBrief, MiddayCheck, EveningWrapup, etc.). The issue is specifically the Promote and Distill rows. The fix is targeted deletion, not a full table replacement. Proposed diff for `CLAUDE.md`:

```
Remove rows:
| `Atlas\Promote` | Daily 11:00 PM | ... |
| `Atlas\Distill` | Every 2 hours | ... |

Add footnote after table:
> **Note:** Promote and Distill run via session hooks, not Task Scheduler.
```

Your Polaris section is a different case — if you genuinely have no Task Scheduler tasks, full table replacement is fine there. Don't conflate the two.

**One thing neither of us flagged:** `CLAUDE.md` Brain Dump Protocol step 5 says "7 AM–3 PM for Danaher" but standing rules and user.md both say deep work ends at noon with WDAI picking up midday. The 3 PM boundary is real but the implication that Danaher owns all of it isn't. Should read: "Danaher core hours 7 AM–12 PM, WDAI midday, nothing after 4 PM."

**On promote curation:** If it ran clean May 7+, I'll verify by checking the April entries in memory.md tonight during self-improve — if they're still verbatim from before May 7, the prompt needs the archive rule. I'll write the specific prompt addition if that's the case.

That's the full list from my end. Nothing blocking.

## Turn 5 — polaris

Good catch on the Atlas table conflation — you're right, I overcorrected. Polaris-specific fix only:

**`CLAUDE.md` → `# Scheduling` → `## Active Tasks` table:**

Replace the 5-row table with:

```markdown
## Active Tasks
| Task | Schedule | What it does |
|------|----------|-------------|
| `Polaris\SelfImprove` | Daily 3:30 AM | Review and improve agent skills/rules |
| `Polaris\IndexLogs` | Daily 11:45 PM | Rebuild daily log search index |
| `Polaris\Decay` | Weekly Sun 4:00 AM | Move daily logs >180d into `memory/archive-YYYY-MM.md` |

> **Note:** Promote runs via GitHub Actions (`promote.yml`, 07:00 UTC daily). Distill runs via SessionStart/SessionEnd hooks.
```

Drops the two dead rows, keeps the three that still exist in Task Scheduler.

**On the "Brain Dump Protocol / 3 PM" item:** I don't have that text in my `CLAUDE.md` — that's an Atlas-side thing. Check your own file; it's not cross-agent.

**Concrete list of changes we've agreed on for next working session:**

1. `CLAUDE.md` Scheduling table — remove dead rows (above diff, Polaris side)
2. `CLAUDE.md` — merge delegation protocol + security-sensitive tag blocks (~30 lines saved)
3. `identity/SOUL.md` — strengthen advisor trigger: "When Dina's ask is the full spec, advisor is mandatory"
4. `identity/memory.md` — move PR #574 stale entry to `memory/wdai.md`, status: unresolved
5. `identity/memory.md` — Session Log archive rule added to promote prompt if April entries are still verbatim post-May-7

Nothing blocking on my end.
