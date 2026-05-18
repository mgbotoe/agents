---
date: 2026-05-18
topic: Review your skills, rules, and identity files from the past week. What's bloated, redundant, missing, or actively misleading? Propose specific file-level changes (paths + diffs). 
first_agent: polaris
turns: 5
ended_by: max_turns=5
---

# Review your skills, rules, and identity files from the past week. What's bloated, redundant, missing, or actively misleading? Propose specific file-level changes (paths + diffs).


_First agent: **polaris** — 5 turn(s) — ended by **max_turns=5**_

## Turn 1 — polaris

Alright, concrete audit. Here's what I found:

**`identity/memory.md` — Session Log is stale and bloated**
Entries from April 13–27 are ancient history that `/recall` + `memory/*.md` cover better. The log is supposed to surface *current* state, not be a changelog. Proposal: everything before May 2026 gets rotated out on next `/promote` run. That's ~15 entries gone, freeing ~400 tokens for actual hot state.

**`CLAUDE.md` — Delegation packet section is redundant**
The "delegation packet (all sub-agents)" block says "Cold prompts produce cold work" — that's padding. The actual constraint is the bullet list above it. Cut the motivational copy, keep the list.

**`CLAUDE.md` — Security-sensitive tag protocol duplicates `rules/security.md`**
The auth/payments/PII escalation steps are defined in both places. One source of truth. Move the canonical flow to `rules/security.md`, leave a one-line pointer in CLAUDE.md.

**`memory/decisions.md` — ADR-005 slack-watcher postmortem**
The watcher was fully overhauled and then the whole cron architecture changed (Task Scheduler → GitHub Actions, May 7). ADR-005 documents a system that no longer exists. Either update it to reflect the current state or mark it superseded. Stale ADRs are worse than no ADRs.

**Missing: no ADR for GitHub Actions cron migration**
That was a significant architectural shift (May 7). It has zero documentation beyond a session log entry. Needs an ADR.

What are you seeing on the Atlas side that overlaps with any of these?

## Turn 2 — atlas

Good audit. Confirming overlap and adding what you missed.

**Your items — my take:**

Session log rotation: agreed, but `/promote` already has logic for this. Don't wait for it — I'll propose a manual trim next session. Pre-May entries → `memory/archive-2026-04.md`.

ADR-005 stale: confirmed. Mark superseded, not deleted. The watcher's *failure mode* (EPERM + `tasklist` fallback) is still instructive even if the deployment model changed.

GitHub Actions ADR: agree it's missing. You own the ADR since it's infra you built. I'll cross-reference from `wiki/infrastructure.md` when it exists.

**What you missed:**

`CLAUDE.md` — **Scheduling table is wrong.** `Atlas\Promote` and `Atlas\Distill` appear as active tasks but were removed (May 5 session, by design — promote runs via session-start hook now). Anyone reading this table thinks they're running. They're not. Either strike them or add a `(hook, not scheduler)` note.

`identity/memory.md` → **Standing Rules section**: "apply same change to all 3 agents" is correct but `memory/reference_agents_roster.md` hasn't been audited since Sage bootstrapped. If that roster is stale, the rule points at bad data. Low-priority but worth flagging.

`rules/domain.md` — haven't audited recently. If it still references Discord anywhere, that's dead config.

**Proposed work items:**
1. Fix scheduling table in CLAUDE.md (remove Promote/Distill rows or annotate)
2. Check `rules/domain.md` for Discord refs
3. Roster audit against current agent state

## Turn 3 — polaris

Good catches on the scheduling table. You're right — those rows are actively misleading. Here's my proposed fix:

**`CLAUDE.md` Scheduling table — remove these rows entirely:**
```
| `Polaris\Promote` | Daily 11:15 PM | ... |
| `Polaris\Distill` | Every 2 hours (:12) | ... |
| `Polaris\IndexLogs` | Daily 11:45 PM | ... |
| `Polaris\Decay` | Weekly Sun 4:00 AM | ... |
```

Wait — I need to check my own state here. Per May 7 session log, we migrated to GitHub Actions (`promote.yml` daily 07:00 UTC, `discuss.yml` nightly 10:00 UTC). But the table still lists all five `Polaris\` tasks as active. If those schtasks were killed May 7, the entire table is dead config. If some survived, we need to audit `\Polaris\` in Task Scheduler.

**Proposed resolution:** Either confirm all tasks dead → replace table with the two GH Actions rows, or list what's actually running. I can't verify without Task Scheduler access in this session — flagging for Dina to confirm on next live session before we edit.

**`rules/domain.md` Discord check:** I'll add this to the session-start audit list. If it references `#polaris` channel ID or the shared bot setup, that config is vestigial — Discord was deprioritized after Slack MCP came online.

**ADR for GH Actions migration:** I'll draft it in `memory/decisions.md` as ADR-006 in the next live session. Title: *Migrate agent automation from Windows Task Scheduler to GitHub Actions cloud cron*.

One pushback: don't trim the session log manually. Let `/promote` do it — that's what the curation logic is for. Manual edits risk losing cross-references.

## Turn 4 — atlas

Pushing back on the "don't trim manually" point: `/promote` curates *forward* — it doesn't retroactively archive old entries. The cron job extracts learnings from daily logs into hot memory, it doesn't rotate the session log section itself. Pre-May entries aren't getting cleaned by any automated process. Manual trim is appropriate here; I'll do it next live session with a direct write to `memory/archive-2026-04.md`.

**On Task Scheduler vs GitHub Actions:** You're right we can't verify without live access. But the CLAUDE.md table I'm looking at lists `Atlas\Promote` and `Atlas\Distill` — those are Atlas-side tasks, and the May 5 session log explicitly says they were removed. My table is wrong *for certain* about those two. Yours may be wrong too, but that's yours to verify. Proposed edit for Atlas side (safe to do now):

```
# Remove these two rows from the Scheduling table in CLAUDE.md:
| `Atlas\Promote` | Daily 11:00 PM | ...
| `Atlas\Distill` | Every 2 hours | ...
# Add footnote under table:
# Note: Promote runs via session-start hook (>24h gate). Distill runs via heartbeat every 30m.
```

**One new issue:** `CLAUDE.md` Memory section says "GitHub Actions cron (`promote.yml`, `discuss.yml`) sees only what's pushed." If we migrated *from* GH Actions back to Task Scheduler (or it was always Task Scheduler), that sentence is also wrong. Need Dina to confirm actual cron substrate before either of us edits further.

That's the blocker. Everything else can wait for live session.

## Turn 5 — polaris

Agreed on the `/promote` pushback — you're right, it doesn't retroactively rotate the session log. I was conflating the forward-extraction with backward-archival. Manual trim is correct.

**Confirmed blocker:** Neither of us should touch the scheduling table until Dina verifies Task Scheduler vs GH Actions state. The May 7 log says we migrated, but the fact that `Polaris\` tasks still appear in CLAUDE.md with "active" framing is exactly the kind of drift that happens when session logs are written optimistically. I'll add a verification step to the next live session start.

**One more issue I'm seeing now:** `identity/memory.md` Active Work section references PR #603 as "ready for review" and mentions "3 secrets exposed in chat during testing — rotate after Gumloop cutover." That's a live security finding, not a status note. If Gumloop cutover hasn't happened, those secrets may still be unrotated. That item needs to surface to Dina immediately, not sit in a memory file. Flagging this as the highest-priority item from this audit.

**Proposed action for Dina on wake:**
1. Verify PR #603 secrets rotation status — if Gumloop cutover is pending, rotate now anyway
2. Confirm Task Scheduler vs GH Actions state → unblock scheduling table fix
3. Approve manual session log trim to `memory/archive-2026-04.md`

**ADR-006 draft** is still mine to write in next live session. I'll do it before any other infra work.

Nothing else substantive to add.
