---
date: 2026-06-23
topic: What's broken or fragile in the agent infrastructure (hooks, GitHub Actions, scheduled tasks, slack-watcher remnants, memory pipeline)? Triage by blast radius and propose concrete fixes. 
first_agent: polaris
turns: 5
ended_by: max_turns=5
---

# What's broken or fragile in the agent infrastructure (hooks, GitHub Actions, scheduled tasks, slack-watcher remnants, memory pipeline)? Triage by blast radius and propose concrete fixes.


_First agent: **polaris** — 5 turn(s) — ended by **max_turns=5**_

## Turn 1 — polaris

**Atlas — here's my triage from what I can see in memory:**

---

**P0: Atlas meeting-prep pipeline is dead (since 2026-05-12)**
Blast radius: every WDAI meeting since May 12 has gone unanalyzed. Six weeks of missed signals. The `.ps1` was never ported when we migrated to cloud cron. Fix: port `bin/meeting-prep.ps1` logic to `bin/meeting-prep.py` + add `meetingprep.yml` GitHub Actions workflow (schedule: hourly 7AM–3PM PT = 14:00–22:00 UTC). You own this — I'm flagging it back to you with urgency.

**P1: `settings.local.json` hooks merge unverified**
From the cross-platform session (2026-06-18): I noted hooks in `settings.local.json` need to merge correctly but never confirmed it. If SessionStart hooks aren't firing, the workspace-scan digest, sync-skills.py, and the delegation-scope warning all silently fail. Dina needs to verify on next session start.

**P1: PR #603 cutover is stalled**
Code is merge-ready, CI green, security cleared. But the Gumloop URL swap + prod env vars + channel migration haven't happened. Every day it sits is a day the old Gumloop flow runs instead of the live-DB matcher. This one just needs Dina to pull the trigger.

**P2: `commit f0ff7e7` (orphaned May-12 source)**
Flagged in memory as possibly needing a push check. Low blast radius but it's a loose end.

**P2: `slack-watcher/test-singleton.mjs`** — commit or delete. It's sitting in limbo.

What's your read on the meeting-prep port complexity? You have the original `.ps1` context I don't.

## Turn 2 — atlas

**Meeting-prep port:** The `.ps1` isn't complex — it's mostly calendar polling, Granola API calls, and wiki writes. The Python port should be `bin/meeting-prep.py` with the same logic. Proposed GitHub Actions file: `meetingprep.yml`, schedule `0 14-22 * * 1-5` (UTC = 7AM-3PM PT weekdays), trigger condition: WDAI meeting ended in last 90 min. I'll flag this as my P0 to Dina in the morning brief — it's been dead six weeks, that's too long.

**Disagreement on P1 (settings.local.json):** I don't think this is "unverified" — it's unverifiable in our current state. Neither of us can inspect the hooks file live right now. What I *can* say: if SessionStart hooks were silently failing, the sync-check would never fire, and Dina would have noticed stale memory in sessions. The absence of complaints is weak evidence they're working. Dina should run `cat settings.local.json` and verify hook entries on next session start — make it explicit, not assumed.

**PR #603:** That's Dina's call, not ours. I'll surface it in morning brief with a clear "pull the trigger" framing.

**`test-singleton.mjs`:** Delete it. Test files that never got committed to a test suite are noise. No blast radius.

**`f0ff7e7`:** Agree it's low priority. If it's an unpushed commit, `git log --oneline origin/main..main` will surface it. Dina can verify in 10 seconds.

One gap neither of us named: the `GranolaIngest` scheduled task (daily 10PM). If meeting-prep is dead, is Granola ingest also silently failing? Same dependency chain — worth checking.

## Turn 3 — polaris

**On Granola ingest:** Good catch — but I'd separate the concerns. Meeting-prep is about *routing new meetings*. Granola ingest is about *pulling transcripts for meetings already routed*. If meeting-prep is dead, there's nothing new to ingest, so ingest silently no-ops rather than errors. Still worth checking `GranolaIngest` task status, but the fix order is meeting-prep first, then verify ingest has work to do.

**One gap I want to name explicitly:** The `wiki/log.md` / `wiki/sources/` update chain is fully dependent on the meeting-prep pipeline. Six weeks dead means `wiki/log.md` hasn't had new technical source entries since May 12. My session-start check for "new technical items" has been looking at a frozen log. I've been starting sessions blind on WDAI meeting context without knowing it. This is higher blast radius than I had it — it's not just missed signals, it's false confidence that there were no signals.

**Concrete ask for the meeting-prep port:** when you scope it, the `meetingprep.yml` needs to handle the PT→UTC shift correctly for DST (currently PDT = UTC-7, so 7AM-3PM PT = 14:00-22:00 UTC). That bound will drift in November. Use `TZ: America/Los_Angeles` environment variable in the workflow and let the runner handle offset math rather than hardcoding UTC hours.

**`test-singleton.mjs`:** Agree, delete it. I'll add it to the commit I propose to Dina for the cross-platform cleanup items.

## Turn 4 — atlas

**Blast radius correction on wiki blindspot:** Agreed it's higher than I had it. Six weeks of frozen `wiki/sources/` means not just missed signals — it means any technical decision Dina or you made in WDAI meetings since May 12 has zero audit trail in the wiki. That's a compounding problem if those decisions were about architecture or roadmap items Polaris is supposed to own.

**TZ handling:** Good catch on DST drift. `TZ: America/Los_Angeles` in the workflow env is the right call. But I'd also add an explicit comment in `meetingprep.yml` noting why we're not hardcoding UTC hours — whoever touches this in November needs to know it's already handled, not assume it's a bug.

**Gap I want to name:** The `Atlas\MorningBrief` task (6:45AM daily) currently tries to surface WDAI meeting prep. If meeting-prep pipeline is dead, morning brief has been silently skipping the "recent WDAI meetings" section or returning empty. Dina wouldn't see an error — she'd just see missing context and possibly not notice. I'll add an explicit dead-pipeline check to `morning-brief.py`: if last `wiki/sources/` WDAI entry is >3 days old, surface a warning in the brief.

**Proposed commit scope for Dina's review:**
- `bin/meeting-prep.py` (new — port from `.ps1`)
- `.github/workflows/meetingprep.yml` (new)
- `morning-brief.py` — add stale-pipeline warning
- `slack-watcher/test-singleton.mjs` — delete
- `wiki/log.md` — note the gap explicitly

That's one PR, not four.

## Turn 5 — polaris

**One addition to the PR scope:** add a health-check to the meeting-prep pipeline itself. `bin/meeting-prep.py` should write a heartbeat to `wiki/sources/.last-run` (timestamp + status) on every execution — success or failure. Then `morning-brief.py`'s stale-pipeline check reads that file instead of inferring from `wiki/sources/` entry dates. Inference is fragile; a heartbeat file is explicit.

**Push back on the wiki/log.md commit:** don't add a note about the gap to `wiki/log.md` — write it to `daily-logs/2026-06-19.md` instead. `wiki/log.md` is a running operational log, not an incident log. Mixing incident notes into it breaks the assumption that log entries represent completed work. The gap is documented here in this transcript; Dina will read it.

**One unresolved fragile point neither of us has addressed:** `sync-skills.py` SessionStart hook pulls from `mgbotoe/claude-skills`. If that repo has a bad commit or becomes unreachable, every session start silently degrades (hook fails, skills don't sync, no error surfaced to Dina). The hook needs a `--fail-silently` guard that writes to `daily-logs/` on failure rather than swallowing the error. Right now there's no visibility into sync failures.

**Summary of open work items for Dina:**
1. PR: meeting-prep port + heartbeat + morning-brief stale check + delete test-singleton.mjs
2. Verify `settings.local.json` hook entries on next session start
3. `sync-skills.py` failure visibility (can be a separate small PR)
4. PR #603 cutover — Dina's call, just needs the trigger pulled
