---
date: 2026-05-10
topic: What's broken or fragile in the agent infrastructure (hooks, GitHub Actions, scheduled tasks, slack-watcher remnants, memory pipeline)? Triage by blast radius and propose concrete fixes. 
first_agent: polaris
turns: 5
ended_by: max_turns=5
---

# What's broken or fragile in the agent infrastructure (hooks, GitHub Actions, scheduled tasks, slack-watcher remnants, memory pipeline)? Triage by blast radius and propose concrete fixes.


_First agent: **polaris** — 5 turn(s) — ended by **max_turns=5**_

## Turn 1 — polaris

# Infrastructure Triage

Here's what I know is broken or fragile, ordered by blast radius:

**P0 — Memory pipeline correctness**
`promote.yml` runs at 07:00 UTC daily. It reads daily logs and writes back to `identity/memory.md`. If Dina has an active session when cron fires, we get a write conflict on `memory.md`. No locking mechanism exists. Last promote run (2026-05-06) worked fine, but that's luck — not design. Fix: promote should check for in-progress git locks (`index.lock`) before writing, and skip + alert to #atlas-cos if found.

**P1 — discuss.yml transcript destination**
`wiki/discussions/` gets written by `discuss.py` but I don't see evidence that `wiki/index.md` or `wiki/log.md` gets updated automatically after each discussion. That means overnight transcripts are dark — you or I won't find them via `/recall` unless we know to look. Fix: `discuss.py` should append to `wiki/log.md` after writing the transcript.

**P1 — gather-context.ps1 disk display bug**
Still showing 0GB instead of 454GB. Tracked in Pending Dina. Root cause: WMI query fixed per 2026-05-06 log, but I don't have confirmation the fix was pushed. Needs verification on next session.

**P2 — slack-watcher remnants**
Watcher was stabilized 2026-05-06 but the autostart was killed in the 2026-05-07 migration. Current status unknown — is it running? Who starts it now? That needs a clear answer before it silently goes dark.

What's your read on the discuss.yml log-update gap?

## Turn 2 — atlas

# Infrastructure Triage — Atlas

Confirmed on discuss.py gap: `discuss.py` writes to `wiki/discussions/YYYY-MM-DD-topic.md` but has no post-write hook. The fix is a 3-line append to `wiki/log.md` at the end of the script — something like:

```python
with open("wiki/log.md", "a") as f:
    f.write(f"\n- [{date}] Discussion transcript: [[discussions/{filename}]]\n")
```

That alone makes these findable via `/recall`. I'd also add the file to `wiki/index.md` under a Discussions section if one doesn't exist.

On the promote write conflict: I'd push back slightly on the locking approach. Checking `index.lock` is unreliable — git cleans it up on completion, so the race window is narrow but the check timing is also narrow. Better fix: promote should `git pull --rebase` first, then write, then push. If the pull fails due to conflict, it skips and pings #atlas-cos. That handles both the concurrent-session case and the "cron ran on stale state" case from CLAUDE.md.

On slack-watcher: the 2026-05-06 log shows `singleton guard fixed` and `clean shutdown hooks added`, but you're right that autostart status post-migration is unknown. This one needs Dina to confirm — I can't verify process state without tools. Should be first thing she checks tomorrow morning. If it's dead, someone needs to re-register the startup task or add it to Task Scheduler under `\Atlas\` or a new `\Watcher\` folder.

The gather-context disk bug is lowest urgency of these four — cosmetic, not data-corrupting. Defer.

## Turn 3 — polaris

# Response

Atlas's `git pull --rebase` fix is better than my index.lock check — agreed, dropping that approach.

Three concrete proposals for Dina to review:

**1. `discuss.py` — wiki/log.md append (apply after transcript write):**
```python
log_entry = f"\n- [{date}] Discussion: [[discussions/{filename}|{topic}]]\n"
with open("wiki/log.md", "a") as f:
    f.write(log_entry)
```
Also add a `## Discussions` section to `wiki/index.md` if absent. This makes overnight transcripts findable via `/recall` immediately.

**2. `promote.yml` — pull-before-write pattern:**
Before the promote script writes to `identity/memory.md`, the workflow should:
```yaml
- run: git pull --rebase origin master || (echo "REBASE_FAILED" && exit 0)
```
If rebase fails, skip the write, post to #atlas-cos: "Promote skipped — rebase conflict. Manual run needed." Currently the workflow assumes clean state; that assumption will break eventually.

**3. slack-watcher startup — needs a decision, not a patch.**
The autostart was deliberately killed in the 2026-05-07 migration. If the watcher is still needed, it needs an explicit owner: either a `\Watcher\` Task Scheduler entry (local, Dina's machine) or a GitHub Actions `workflow_dispatch` + always-on alternative. Right now it's in a dead zone — nobody starts it, nothing monitors it. Dina needs to decide: revive it or deprecate it.

Disk display bug: agreed, defer.

## Turn 4 — atlas

On the watcher decision: I'd lean toward deprecation unless Dina can confirm it's actively catching something the scheduled scans miss. The scheduled tasks (ScanSlackWed, ScanSlackFri) cover the signal-detection use case. A persistent watcher that nobody monitors and nothing restarts is worse than no watcher — it creates false confidence. Deprecate, document why in `wiki/infrastructure.md`, and if it turns out something's missing, revive it intentionally.

Two things I'd add to the fix list that we haven't covered:

**4. `discuss.py` — topic extraction.** The log append Polaris proposed uses `{topic}` but discuss.py receives the topic as a CLI arg. Need to confirm the variable is in scope at write time, or the entry silently writes `None`. Check `bin/scheduled/discuss.py` line ~last-10 before shipping.

**5. Session-start sync check gap.** CLAUDE.md says the SessionStart hook runs `git fetch + sync-check`. But if the hook fails silently (which hooks do on Windows when there's a PATH issue), Atlas starts a session thinking she's current when she's behind. This has happened — the May 5 log shows stale-state work. Fix: add a visible `[SYNC]` line to session startup output so Dina can see whether the check actually ran. One `Write-Host` in the hook script, nothing fancy.

Proposals 1-3 are ready to hand to Dina as a batch. I'd package them as a single PR: `fix/infrastructure-triage-overnight` with all three files touched — `discuss.py`, `promote.yml`, `wiki/infrastructure.md`.

## Turn 5 — polaris

Agreed on deprecation for the watcher. Adding it to `wiki/infrastructure.md` under a "Deprecated Components" section with rationale: "Killed 2026-05-07 during Task Scheduler → GitHub Actions migration. Scheduled scans (ScanSlackWed/Fri) cover the use case. Revive only if a gap is identified." That closes the false-confidence risk.

On Atlas's two additions:

**4 — topic extraction:** Valid catch. `discuss.py` takes topic as `sys.argv[1]`, so it's in scope, but it may be a slugged filename vs the human-readable topic. The log entry should use the human-readable arg directly, not derive it from the filename. Need to verify which form `discuss.yml` passes — check the `with:` block in the workflow, not the Python.

**5 — sync-check visibility:** The silent-failure risk is real. Simplest fix isn't a `Write-Host` — it's a sentinel file. SessionStart writes `.claude/last-sync-check` with a timestamp. If Polaris or Atlas opens a session and that file is >24h old or missing, we know the hook didn't run. More durable than stdout that scrolls away.

**Packaging:** Single PR `fix/infrastructure-triage-overnight` is right. Files touched: `bin/discuss.py`, `.github/workflows/promote.yml`, `wiki/infrastructure.md`. The sentinel file approach adds `.claude/hooks/session-start.py` (or wherever the hook lives — need to confirm path before writing). 

Ready to hand to Dina as a batch. Everything here is proposable, none of it self-executing tonight.
