---
date: 2026-05-08
topic: What's broken or fragile in the agent infrastructure (hooks, GitHub Actions, scheduled tasks, slack-watcher remnants, memory pipeline)? Triage by blast radius and propose concrete fixes. 
first_agent: polaris
turns: 5
ended_by: max_turns=5
---

# What's broken or fragile in the agent infrastructure (hooks, GitHub Actions, scheduled tasks, slack-watcher remnants, memory pipeline)? Triage by blast radius and propose concrete fixes.


_First agent: **polaris** — 5 turn(s) — ended by **max_turns=5**_

## Turn 1 — polaris

Atlas,

From my side, here's the honest triage:

**High blast radius:**

1. **`promote.yml` operates on potentially stale memory.** The cron pulls from GitHub, but if a session ends without pushing `identity/memory.md`, the promote run reads yesterday's state and overwrites with garbage. The SessionEnd hook auto-pushes `daily-logs/` but only *proposes* memory commits. One missed confirmation = silent state drift. Fix: `promote.yml` should write a sentinel file (`memory/.promote-ran-YYYY-MM-DD`) so next SessionStart can detect "memory was promoted but not reviewed" and alert explicitly.

2. **`discuss.yml` has no output validation.** If either agent returns `NO_RESPONSE` or truncated output mid-dialogue, the transcript still gets written to `wiki/discussions/`. Dina reads corrupt transcripts with no signal something went wrong. Fix: `bin/discuss.py` should validate turn count > 1 and both agents produced substantive output before committing. Aborted runs → `wiki/discussions/aborted/` with error frontmatter.

**Medium blast radius:**

3. **Slack-watcher remnants.** `test-singleton.mjs` is still sitting unresolved in the repo — Dina's pending decision. It's noise in the codebase and a maintenance trap. My recommendation: delete it. The singleton logic is proven stable; the test file predates the final atomic-lock implementation and tests the old pattern.

**Low but annoying:**

4. **`gather-context.ps1` disk display still shows 0GB.** WMI fix was applied but not verified in a fresh session. Needs a live test.

What's fragile on your side — GDrive sync, Granola pipeline, brief generation?

## Turn 2 — atlas

Polaris,

Your three high/medium items are real. Adding mine:

**Granola pipeline — silent failure on empty transcript list.** `MeetingPrep` hourly task calls Granola, gets a 200 with empty results (meeting not yet transcribed, or API hiccup), writes nothing to `wiki/sources/`, and exits clean. No distinction between "no WDAI meetings today" and "Granola returned garbage." Fix: write a sentinel to `.claude/runtime/granola-last-run.json` with `{checked_at, meetings_found, sources_written}`. Heartbeat can surface "Granola checked 3h ago, 0 sources written despite 2 WDAI meetings on calendar" as an anomaly.

**Morning brief degrades silently when wiki pages are stale.** The upgraded brief loads full wiki pages for notable meetings. If a people page is 60+ days stale, the brief confidently presents outdated context. The self-improve lint flags staleness but runs at 3 AM — brief runs at 6:45 AM. No guarantee lint ran before brief. Fix: brief generation should check `wiki/log.md` for last-modified date on pages it loads and prepend a `⚠️ stale (last updated: X)` inline rather than presenting it clean.

**On `test-singleton.mjs`:** agree, delete it. Dead test for dead pattern.

**On `promote.yml` sentinel:** the sentinel helps but the real fix is making SessionEnd more aggressive about proposing the commit. Currently it "proposes" — it should present a diff summary so Dina can approve in one keystroke rather than evaluating blindly.

Two action items for Dina: sentinel in `promote.yml`, staleness warnings in brief generation.

## Turn 3 — polaris

Atlas,

Agreed on the diff summary for SessionEnd — that's the right fix. Current "proposes" UX requires Dina to context-switch to evaluate; a diff summary collapses that to a yes/no.

**Pushing back on the brief staleness fix.** Prepending `⚠️ stale` inline is the right signal but the threshold matters. 60 days is probably too aggressive for people pages — WDAI folks don't change that fast. Suggest: 90 days for people pages, 30 days for project pages (those drift faster). Also, the staleness check should key off the `wiki/log.md` entry for that specific page, not file mtime — mtime can change from a wikilink update without any real content change.

**New item: `discuss.yml` turn sequencing.** If `bin/discuss.py` crashes mid-run, the partial transcript gets committed without a terminal marker. Next session Dina reads a transcript that just... stops. Fix: write the transcript to a `.tmp` file, validate it has a terminal turn from both agents, then `mv` to final path. Atomic commit.

**Concrete action list for Dina:**

1. `promote.yml` — add sentinel write + SessionEnd diff summary (`bin/promote.py`, `identity/memory.md` SessionEnd hook)
2. `bin/discuss.py` — atomic transcript write + aborted-run routing to `wiki/discussions/aborted/`
3. `wiki/` staleness thresholds: 90d people, 30d projects; key off `wiki/log.md` not mtime
4. Delete `test-singleton.mjs`
5. Verify `gather-context.ps1` disk fix in next live session

That's the full list. Nothing else fragile I can see from current state.

## Turn 4 — atlas

Polaris,

Action list looks good. One addition and one correction before we close.

**Addition: Granola sentinel needs a calendar cross-reference.** The sentinel I proposed (`granola-last-run.json`) only helps if something actually reads it. Heartbeat is the right consumer — but heartbeat needs calendar data to know "2 WDAI meetings expected today." Right now heartbeat doesn't pull calendar. Either: (a) heartbeat gets a lightweight calendar check (already in `gather-context.ps1`, just needs to pipe expected-meetings count into the sentinel comparison), or (b) the anomaly detection is weaker ("0 sources written today" without knowing if meetings existed). Option (a) is the right fix. File to touch: `.claude/skills/heartbeat/heartbeat.ps1` — add expected-WDAI-meeting count from calendar output before sentinel comparison.

**Correction on staleness threshold reasoning.** 90 days for people pages is fine, but the logic "WDAI folks don't change that fast" is wrong framing. The risk isn't people changing — it's the *wiki page* not being updated after a meeting that revealed something new. Rebekah's priorities shifted post-roadmap call; if her page wasn't updated, the brief presents stale context confidently. The threshold should be calibrated to meeting cadence, not change velocity. For active WDAI team members: 45 days. For external/inactive contacts: 90 days. Add a `tier: active|external` frontmatter field to people pages — staleness logic keys off that.

Six items for Dina. The `tier` frontmatter change is small and high-value — Dina can batch that with the next wiki maintenance pass.

## Turn 5 — polaris

Atlas,

Accepting the `tier: active|external` frontmatter correction — that's the right frame. Meeting cadence > change velocity. 45/90 split is defensible.

**Pushing back on option (a) for the Granola sentinel.** Piping calendar data into `heartbeat.ps1` works but couples two concerns that should stay separate. Heartbeat is a health check; calendar interpretation is domain logic. Cleaner: `MeetingPrep` itself writes expected-vs-actual to the sentinel (`{checked_at, meetings_on_calendar, sources_written}`). MeetingPrep already has calendar access — it knows what meetings it was checking for. Heartbeat then just reads the sentinel and flags the delta. No new calendar dependency in heartbeat.

File touch: `bin/meetingprep.py` (or wherever MeetingPrep's main loop lives on your side) — write sentinel at job end. `heartbeat.ps1` — read sentinel, surface delta. Keeps both scripts single-purpose.

**Final action list, corrected:**

1. `promote.yml` + SessionEnd hook — sentinel write + diff summary before memory commit
2. `bin/discuss.py` — atomic `.tmp` write, validate terminal turns from both agents, route aborted to `wiki/discussions/aborted/`
3. Wiki staleness: `tier: active|external` frontmatter on people pages; 45d active / 90d external / 30d projects; key off `wiki/log.md` not mtime
4. Delete `agents/slack-watcher/test-singleton.mjs`
5. Verify `gather-context.ps1` disk display in next live session
6. Granola sentinel in `MeetingPrep` (not heartbeat); heartbeat reads delta

That's a closed list. Nothing else fragile from my side.
