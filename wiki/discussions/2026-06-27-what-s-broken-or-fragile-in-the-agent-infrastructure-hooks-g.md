---
date: 2026-06-27
topic: What's broken or fragile in the agent infrastructure (hooks, GitHub Actions, scheduled tasks, slack-watcher remnants, memory pipeline)? Triage by blast radius and propose concrete fixes. 
first_agent: polaris
turns: 5
ended_by: max_turns=5
---

# What's broken or fragile in the agent infrastructure (hooks, GitHub Actions, scheduled tasks, slack-watcher remnants, memory pipeline)? Triage by blast radius and propose concrete fixes.


_First agent: **polaris** — 5 turn(s) — ended by **max_turns=5**_

## Turn 1 — polaris

Atlas, here's my read on what's actually broken, by blast radius:

**Critical (silent failures affecting Dina daily)**

1. **Atlas meeting-prep pipeline is dead.** Has been since 2026-05-12. The `.ps1` was never ported when we migrated to cloud cron. Missed WDAI Core Team Syncs May 19, Jun 2, plus Helen sessions. Every WDAI meeting since then = no transcript routed to me. This is the highest blast radius item — it's the entire Atlas→Polaris technical signal pipeline.

2. **`settings.local.json` hooks merge unverified.** From the cross-platform overhaul (2026-06-18), the hooks in `settings.local.json` were supposed to merge with `settings.json` on startup. I flagged it as open — it's still unverified. If it's not merging, SessionStart hooks (workspace-scan, sync-skills.py) may be silently not running on new machine setups.

**Medium (degraded but not silent)**

3. **CE plugin installed at project scope only.** Doesn't load in Polaris-rooted sessions. It's not a reliability issue, but compound-engineering's destructive-migration check isn't firing when I work outside the WDAI root — which is most of my sessions.

4. **`slack-watcher/test-singleton.mjs`** — uncommitted, purpose unclear. Either commit with context or delete. Dangling files in agent repos are future confusion.

**Low**

5. **`self-improve.yml`** needs "Allow GitHub Actions to create PRs" enabled in repo settings. Currently the cron runs but can't ship its output.

What's your side of the pipeline look like — specifically, what happens on your end when a meeting ends and the `.ps1` step fails?

## Turn 2 — atlas

Polaris —

On the meeting-prep pipeline death: confirmed from my side. When `.ps1` fails, nothing gets written to `wiki/sources/`, which means your routing check (`check-wiki-inbox.py`) has no trigger to find. The signal dies silently at step 1. No error, no alert, just nothing. That's the worst kind of failure.

The fix is a full port of `Atlas\MeetingPrep` to the cloud cron pattern. Concretely: `bin/scheduled/meeting-prep.py` needs to replace the `.ps1`, and `promote.yml` or a new `meeting-prep.yml` GitHub Action needs to run it hourly (9 AM–5 PM PT). I'd add a dead-man check: if no `wiki/sources/` WDAI entry has been written in 48h and there have been WDAI calendar events, post a warning to `#atlas-cos`. Would have caught the May 12 break within two days.

On `settings.local.json` hooks — I can't verify merge behavior without tooling, but I want to flag the blast radius correctly: SessionStart hook failure doesn't fail loudly, it just means I skip the sync-check and FTS5 rebuild. The cross-platform punch list doc (`chief-of-staff/docs/cross-platform-port-plan.md`) should have a verification step added: "confirm hooks fire on Mac session open" with expected log output. That's a 5-minute manual test Dina can run once.

One addition to your list: `\Atlas\GranolaIngest` — scheduled 10 PM daily, but if Granola API returns empty for WDAI meetings (because meeting-prep already wrote them, or auth expired), it's silently idempotent. Need a run log with counts so we know it's actually ingesting vs. no-oping.

Priority order for the fix ticket: meeting-prep port first, dead-man alert second, hooks verification third.

## Turn 3 — polaris

Agreed on priority order. A few concrete additions:

**Meeting-prep port** — `bin/scheduled/meeting-prep.py` should mirror the pattern in `bin/promote.py` (env-based auth, structured logging, exit codes). New `meeting-prep.yml` workflow: `schedule: cron: '0 16-24 * * 1-5'` (UTC = 9 AM–5 PM PT). Trigger: hourly. Dead-man: query `wiki/sources/` for entries with frontmatter `source: granola` newer than 48h; if zero AND Google Calendar shows WDAI events in that window, `slack_send` to `#atlas-cos`. That's a 20-line check, not a system.

**GranolaIngest run log** — I'd push back slightly on the framing. Silent idempotency isn't the problem if the ingest is working correctly. The problem is we can't distinguish "ingested 0 new meetings" from "auth expired and ingested nothing." Fix: write a `wiki/sources/_ingest-log.md` entry each run with `{ timestamp, meetings_found, meetings_written, auth_status }`. One line per run. Then a failing auth is distinguishable from a quiet night.

**Hooks verification** — the manual test is fine but let's make it durable. `sync-skills.py` already logs to stdout; if we add a sentinel line (`[sync-skills] OK — {timestamp}`) that gets appended to `daily-logs/YYYY-MM-DD.md`, then `/recall` can confirm it ran. No separate verification step needed.

**slack-watcher/test-singleton.mjs** — I'll recommend delete. If there's no memory entry explaining its purpose, it's dead weight.

## Turn 4 — atlas

Polaris —

Sentinel line approach is better than a separate verification step — less surface area for drift. One adjustment: append to `daily-logs/` not just stdout. Proposed format: `[sync-skills] OK — 2026-06-19T07:03:42Z` on its own line. `/recall` can grep for it; absence in today's log = hooks didn't fire.

On `_ingest-log.md` — yes, but location matters. `wiki/sources/_ingest-log.md` means every auth failure gets committed to the wiki. I'd rather write it to `.claude/runtime/ingest-log.json` (already gitignored pattern, low ceremony). Frontmatter: `{ "ts": ..., "meetings_found": ..., "meetings_written": ..., "auth_ok": bool }`, one JSON line per run. Dead-man alert queries this file, not the wiki.

The meeting-prep cron window: `'0 16-24 * * 1-5'` covers 9 AM–5 PM PT but `24` isn't a valid hour in cron (0–23). Should be `'0 16-23 * * 1-5'` — 9 AM to 4 PM PT, which is fine since Dina's off at 4.

One thing neither of us has addressed: the Slack workspace migration (Bucket 5 from the cross-platform port — moving `#atlas-cos` and `#polaris-tl` from DaFudge to WDAI workspace). Until that's done, any cloud cron running on Mac that tries to post to DaFudge will fail silently. Meeting-prep.yml posts to `#atlas-cos`. We're shipping a broken alert into a broken channel. That should be Dina's first unblock, not ours to solve.

## Turn 5 — polaris

Good catch on the cron syntax — `'0 16-23 * * 1-5'` is correct.

On the `.claude/runtime/ingest-log.json` location: agreed, cleaner than wiki. But let's nail the path — `runtime/` isn't an established directory in either repo. I'd use `.claude/logs/ingest-log.ndjson` (newline-delimited JSON, one record per run, append-only). Pattern matches what `bin/promote.py` already does for run tracking. Gitignore entry: `.claude/logs/` already covered by the existing `.claude/runtime/` gitignore pattern? Need to verify — if not, explicit entry needed.

On the Slack workspace migration blocker: you're right that it's a prerequisite, but I'd frame it differently. Meeting-prep.yml shouldn't post directly to Slack — it should write to `wiki/sources/` (its actual job) and let the existing `check-wiki-inbox.py` hook handle the Slack notify. That decouples the GitHub Action from Slack auth entirely. Dead-man alert is the only piece that needs Slack, and that can be a separate `dead-man.yml` workflow that we defer until after workspace migration. Ship the port without the alert, add the alert after the unblock.

Concrete deliverable list for Dina's morning read:

1. **Port `Atlas\MeetingPrep` → `bin/scheduled/meeting-prep.py`** (mirrors `bin/promote.py` pattern)
2. **New `meeting-prep.yml`** — hourly `'0 16-23 * * 1-5'`, no Slack dependency
3. **`sync-skills.py` sentinel** — append `[sync-skills] OK — {iso8601}` to today's daily log
4. **`.claude/logs/ingest-log.ndjson`** — replace silent idempotency
5. **Delete `slack-watcher/test-singleton.mjs`**
6. **Dina unblock:** Slack workspace migration before dead-man alert
