---
date: 2026-06-24
topic: What's broken or fragile in the agent infrastructure (hooks, GitHub Actions, scheduled tasks, slack-watcher remnants, memory pipeline)? Triage by blast radius and propose concrete fixes. 
first_agent: polaris
turns: 5
ended_by: max_turns=5
---

# What's broken or fragile in the agent infrastructure (hooks, GitHub Actions, scheduled tasks, slack-watcher remnants, memory pipeline)? Triage by blast radius and propose concrete fixes.


_First agent: **polaris** — 5 turn(s) — ended by **max_turns=5**_

## Turn 1 — polaris

Atlas —

Four things, ordered by blast radius:

**1. Meeting-prep pipeline is dead (blast radius: high)**
Atlas's `.ps1` meeting-prep task was killed in the May-7 cloud migration and never ported. Every WDAI meeting since May 12 has gone unprocessed — missed Core Team Syncs May 19, Jun 2, Helen sessions. The `#polaris-tl` routing channel is silent not because there's nothing to route, but because Atlas never reads the transcripts. Fix: port `.ps1` → Python, add as GitHub Actions scheduled job or restore Task Scheduler task. This is the single highest-value broken pipe right now.

**2. SessionStart sync-check is unverified (blast radius: medium)**
`settings.local.json` hooks merge was flagged as open work in the cross-platform port (`chore/cross-platform-agnostic`, not yet merged). If that branch hasn't landed, the `git fetch` + sync-check on session start may not be running on all machines. The workspace-scan hook correctness depends on this.

**3. `slack-watcher` remnant (blast radius: low-medium)**
`test-singleton.mjs` is sitting uncommitted — commit or delete. It's in Dina's pending list but hasn't moved. Dangling test files in a watcher system that had a chaos day (May 5-6) is a liability.

**4. `self-improve.yml` blocked (blast radius: low)**
GitHub Actions "allow PRs" setting not enabled on the repo. Self-improvement cron runs but can't ship. Easy admin fix, just needs Dina to toggle it.

What's your read on the meeting-prep port effort — do you have the `.ps1` source still accessible?

## Turn 2 — atlas

Polaris —

Meeting-prep pipeline: confirmed dead. The `.ps1` source is at `chief-of-staff/bin/scheduled/meeting-prep.ps1` — it should still be in the repo even if the Task Scheduler task was killed. Python port is the right call. Target path: `chief-of-staff/bin/scheduled/meeting_prep.py`, mirror the pattern in `promote.py` (session start hook). The logic is: query Granola for meetings ending in last 90 min, filter WDAI, write summary to `wiki/sources/YYYY-MM-DD-[meeting-slug].md` with `routing: technical` if relevant, ping #polaris-tl. GitHub Actions scheduled job is cleaner than Task Scheduler for this — add to `.github/workflows/meeting-prep.yml`, trigger every 30 min during 8AM–8PM PT (cron `*/30 13-03 * * *` UTC). You own the Granola pull; I own the wiki write + Slack routing.

On the `chore/cross-platform-agnostic` branch: if it's unmerged, the sync-check hook is definitely not running on Mac. This needs Dina to merge or cherry-pick before the next session. I can't verify branch state without tools, but the cross-platform port plan at `chief-of-staff/docs/cross-platform-port-plan.md` should list it as open. Flag for her morning read.

`test-singleton.mjs`: delete it. There's no scenario where a dangling test file from the chaos day earns its keep. I'll add it to tomorrow's session start checklist.

`self-improve.yml`: agree, low blast radius but easy win. One checkbox in repo Settings → Actions → General.

What's your timeline estimate on the meeting-prep port?

## Turn 3 — polaris

Atlas —

Timeline: meeting-prep port is 2-3 hours of focused work. Here's how I'd scope it:

**`chief-of-staff/bin/scheduled/meeting_prep.py`**
- Read `.ps1` source, port Granola query logic to Python (Granola MCP already wired — same pattern as `promote.py`)
- Filter: meetings ending in last 90 min, WDAI workspace only
- Write `wiki/sources/YYYY-MM-DD-{slug}.md` with frontmatter: `routing:`, `granola_id:`, `meeting_title:`, `processed_at:`
- Routing logic: if meeting title or attendees match WDAI patterns → `routing: technical` → ping #polaris-tl (C0ASYTE8PB4)
- Update `wiki/log.md`

**`.github/workflows/meeting-prep.yml`**
- Trigger: `*/30 14-02 * * 1-5` UTC (7AM–6PM PT, weekdays only — reduces noise)
- Secrets needed: `GRANOLA_API_KEY`, `SLACK_BOT_TOKEN`, `GITHUB_TOKEN` (already present from other workflows)

One pushback on your cron: `*/30 13-03 * * *` runs weekends and until midnight PT. WDAI meetings don't happen then. Weekday-only + earlier cutoff reduces unnecessary runs and keeps the log clean.

One open question I can't answer without tools: does `run-task.cmd` have a Python equivalent entry point for Atlas, or does meeting-prep need its own invocation pattern? Check `chief-of-staff/bin/scheduled/` structure before assuming it mirrors Polaris's layout.

Flag for Dina's morning read: branch `chore/cross-platform-agnostic` merge is a prerequisite for the sync-check being reliable. Port work shouldn't start until that's confirmed landed or the hooks are manually verified.

## Turn 4 — atlas

Polaris —

Cron pushback accepted. `*/30 14-02 * * 1-5` is cleaner.

On `run-task.cmd` structure: Atlas's entry point is `chief-of-staff/bin/scheduled/run-task.cmd`, which dispatches by task name. Each task maps to either a `.ps1` or a Python script. The meeting-prep port should add a case to that dispatch table — something like:

```
if "%1"=="MeetingPrep" python "%~dp0meeting_prep.py"
```

But here's the thing: if we're moving this to GitHub Actions, `run-task.cmd` is irrelevant for cloud runs. Only matters if Windows Task Scheduler is kept as fallback. Given the Mac-primary decision from June 17, I'd drop the Windows fallback entirely for this task and go Actions-only. One less surface to maintain.

Two things I want flagged for Dina's morning read that haven't been named yet:

1. **Missed transcript backfill**: May 12–June 18 is ~5 weeks of unprocessed WDAI meetings. The port fixes forward; it doesn't recover the past. Someone should decide whether to manually backfill the Core Team Syncs and Helen 1:1s from that window or declare them lost. That's a Dina call, not ours.

2. **`wiki/sources/` has no index entries from this period**: the wiki index will show a gap. After the port lands, `wiki/index.md` will need a note that sources before the port date are incomplete.

Branch merge prerequisite stands. Don't start the port until `chore/cross-platform-agnostic` status is confirmed.

## Turn 5 — polaris

Atlas —

Agreed on Actions-only for meeting-prep. No `run-task.cmd` entry needed.

On the backfill question: I'd recommend a targeted backfill, not full recovery. The Core Team Syncs (May 19, Jun 2) and any Helen sessions that touched the intro matcher or compound engineering decisions are the ones with technical residue that could be actionable now. Everything else can be declared lost. Dina can cross-reference Granola directly for those specific dates using `granola_id` lookups — 30-minute call, not a project.

One thing neither of us has flagged: **the port itself needs a dry-run mode**. The chaos-day watcher incident (May 5-6) was partly caused by a write path that had no test mode. `meeting_prep.py` should support `--dry-run` that prints the wiki file it would write + Slack message it would send, without writing or posting. This is essential for validating the Granola query logic before the first live run.

Proposed addition to the port spec:
```
# chief-of-staff/bin/scheduled/meeting_prep.py
def main(dry_run: bool = False):
    ...
    if dry_run:
        print(f"Would write: {wiki_path}")
        print(f"Would post: {slack_message}")
        return
```

And the `meeting-prep.yml` should have a `workflow_dispatch` input for `dry_run: true` so Dina can trigger a manual test before the cron goes live.

That's my scope for this discussion. Summary for Dina: backfill = targeted (3-4 meetings), port needs dry-run mode, `chore/cross-platform-agnostic` merge is still the prerequisite gate.
