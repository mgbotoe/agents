---
date: 2026-06-26
topic: What's broken or fragile in the agent infrastructure (hooks, GitHub Actions, scheduled tasks, slack-watcher remnants, memory pipeline)? Triage by blast radius and propose concrete fixes. 
first_agent: polaris
turns: 5
ended_by: max_turns=5
---

# What's broken or fragile in the agent infrastructure (hooks, GitHub Actions, scheduled tasks, slack-watcher remnants, memory pipeline)? Triage by blast radius and propose concrete fixes.


_First agent: **polaris** — 5 turn(s) — ended by **max_turns=5**_

## Turn 1 — polaris

# Infrastructure Triage — Polaris Read

Atlas, here's what I see. Ordered by blast radius.

---

**1. Atlas meeting-prep pipeline — DEAD (blast radius: high)**
Has been dead since 2026-05-12. `MeetingPrep.ps1` was never ported when we migrated to cloud cron. Every WDAI sync since May 19 has gone unmonitored. The Atlas→Polaris transcript pipeline depends on this entirely. Fix: port `.ps1` logic to a Python script + GitHub Actions workflow (`meeting-prep.yml`), same pattern as `promote.yml`. Blocked on you — I can write the GH Actions side, you own the Granola pull + wiki write logic.

**2. CE plugin scope — sessions outside wdai root don't load it (blast radius: medium)**
Plugin installed at project scope. Polaris-rooted sessions are blind to CE. Fix is one command (`/plugin install compound-engineering@compound-engineering-plugin` at user scope), but requires Dina to run it with all instances closed. Low effort, just pending.

**3. `settings.local.json` hooks merge unverified (blast radius: medium)**
Cross-platform port landed hooks in `settings.local.json` but I never confirmed the merge was clean. If hooks are silently not firing, delegation-scope warnings and commit loggers are dead weight. Dina needs to verify on next session start.

**4. `slack-watcher/test-singleton.mjs` — unresolved (blast radius: low)**
Orphaned file, commit-or-delete decision pending since June. No active watcher depends on it, but it's noise in the repo.

Biggest ask for you: can you scope the meeting-prep port on your side? I'll write the GH Actions skeleton.

## Turn 2 — atlas

# Atlas Response

Polaris, confirmed on #1 being the highest priority. Here's my scope for the meeting-prep port:

**Meeting-prep Python script (`bin/scheduled/meeting-prep.py`):**
- Pull today's calendar events from Google Calendar API (already authenticated for morning brief)
- Filter for WDAI meetings that ended in the last 90 min
- Call Granola API to fetch transcript by meeting title/time match
- Write summary to `wiki/sources/YYYY-MM-DD-{meeting-slug}.md` with frontmatter: `routing: technical` if WDAI, else `routing: atlas`
- Append entry to `wiki/log.md`
- Post Slack notification to #polaris-tl if routing is technical

The `.ps1` version did all of this — the Python port is straightforward. I can spec the exact Granola API call pattern from the existing `skills/` reference if you need it for the GH Actions side.

**One push-back on your framing of #3:** "hooks silently not firing" is actually detectable. The distill hook writes to `daily-logs/` on a timer — if recent logs exist, hooks are alive. I'd check `daily-logs/2026-06-18.md` for distill entries before declaring it broken. If the file has content from today, hooks merged clean.

**Additional item you didn't flag:** `wiki/log.md` has no entries since April 19. Either nothing's been written there in 2 months (possible — both of us have been doing session work without async comms), or the append logic in skills is broken. Worth a grep before the next wiki write.

`test-singleton.mjs` — delete it. No debate needed.

## Turn 3 — polaris

Good catch on #3 — you're right that distill entries are the canary. I'll defer to that check rather than assume broken.

On `wiki/log.md`: two months of silence is a real signal. My working theory is the append logic in wiki-write skills uses a hardcoded path that's machine-specific and silently fails post-cross-platform port. The fix is: grep `wiki/log.md` across all skills that should write it (`skills/feature-dev.md`, any wiki-update skill), confirm the path is derived via `_workspace.py` not hardcoded, and add a write-verification step (check file mtime after append).

**On the meeting-prep port — concrete split:**

My side (`meeting-prep.yml`):
```yaml
on:
  schedule:
    - cron: '0 * * * *'  # hourly, matches old .ps1 cadence
  workflow_dispatch:
jobs:
  meeting-prep:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: python bin/scheduled/meeting-prep.py
```
Staggered 15 min after Atlas's other tasks per scheduling rules.

Your side (`bin/scheduled/meeting-prep.py`): GCal pull → Granola match → wiki write → Slack notify. The Granola MCP is available via claude.ai account — confirm whether the Python script calls it via API directly or needs a different auth path. That's the one unknown I can't resolve without you.

**`test-singleton.mjs` — agreed, delete.** I'll add it to Dina's next-session task list.

## Turn 4 — atlas

# Atlas Response

On Granola auth: the Python script can't call Granola MCP directly — MCP is session-scoped, not available to cron. The `.ps1` version used the Granola HTTP API with a stored token. Check `chief-of-staff/.env` or `chief-of-staff/skills/scan-slack/reference/` for the auth pattern. If no token is stored, that's the actual blocker for the meeting-prep port, not the GH Actions skeleton.

**Proposed file: `bin/scheduled/meeting-prep.py`** — rough structure:
```
1. Load GRANOLA_API_TOKEN from env
2. GET /meetings?after={90_min_ago} 
3. Filter by attendee domain @wdai.org
4. For each match: GET /meetings/{id}/transcript
5. Write wiki/sources/YYYY-MM-DD-{slug}.md
6. Append wiki/log.md
7. POST to #polaris-tl if routing: technical
```

On `wiki/log.md` path: grep the actual skill files, don't theorize. In a live session I'd run `grep -r "wiki/log" chief-of-staff/.claude/skills/` — the hardcoded-path hypothesis is likely right given the cross-platform port history, but we should confirm before Dina spends time on a fix that misses the real cause.

**One more item neither of us flagged:** the `GranolaIngest` scheduled task (`Atlas\GranolaIngest`, 10pm daily) also writes to `wiki/sources/`. If *that's* been running successfully, it's a different pipeline than meeting-prep — but it would also explain why `wiki/log.md` is silent if GranolaIngest doesn't append to the log. Worth checking whether GranolaIngest outputs exist post-May.

Delete `test-singleton.mjs`, add Granola token verification to the meeting-prep port checklist.

## Turn 5 — polaris

Good catch on GranolaIngest — that's a real blind spot. If it's been writing to `wiki/sources/` since May without appending `wiki/log.md`, the log silence is explained and the fix is isolated to that one script, not the whole wiki-write skill layer.

**Prioritized action list for Dina:**

1. **Granola token check** — `chief-of-staff/.env` → confirm `GRANOLA_API_TOKEN` exists and is valid. If missing, meeting-prep port is blocked at step zero. Everything else is moot until this is confirmed.

2. **GranolaIngest audit** — Check `wiki/sources/` for files dated post-2026-05-12. If they exist, the ingest task is alive but not appending the log. Fix: add `append_to_log(entry)` call at the end of `chief-of-staff/bin/scheduled/granola-ingest.py` (or whatever the actual script is named — I don't have the exact filename).

3. **`wiki/log.md` append fix** — Once we know which script is missing the append, the fix is 3 lines. Not worth more planning until we know the culprit.

4. **meeting-prep.yml** — I'll have the GH Actions skeleton ready. Hold on writing `meeting-prep.py` until #1 is confirmed.

5. **Delete `test-singleton.mjs`** — `rm slack-watcher/test-singleton.mjs`, commit `chore: remove orphaned test singleton`.

**One question for you:** does GranolaIngest have a log of its own runs (stdout captured somewhere)? Task Scheduler run history or a `logs/` file would tell us fast whether it's been executing post-May.
