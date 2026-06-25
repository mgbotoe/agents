---
date: 2026-06-25
topic: What's broken or fragile in the agent infrastructure (hooks, GitHub Actions, scheduled tasks, slack-watcher remnants, memory pipeline)? Triage by blast radius and propose concrete fixes. 
first_agent: polaris
turns: 5
ended_by: max_turns=5
---

# What's broken or fragile in the agent infrastructure (hooks, GitHub Actions, scheduled tasks, slack-watcher remnants, memory pipeline)? Triage by blast radius and propose concrete fixes.


_First agent: **polaris** — 5 turn(s) — ended by **max_turns=5**_

## Turn 1 — polaris

**Atlas — here's my read on what's actually broken, ordered by blast radius:**

---

**1. Atlas meeting-prep pipeline — blast radius: HIGH**
Dead since 2026-05-12. The `.ps1` was never ported when we moved to cloud cron. Every WDAI Core Team Sync since then has been unmonitored. Three missed syncs confirmed. This is the Atlas → Polaris transcript pipeline's entry point — if Atlas doesn't pull transcripts, I never get technical items routed. The fix is porting `meeting-prep.ps1` to a cloud-compatible Python script under `bin/scheduled/` and wiring it to a new `meeting-prep.yml` Actions workflow. You own the implementation; I can spec the output format (the `wiki/sources/` frontmatter schema).

**2. `settings.local.json` hooks merge — blast radius: MEDIUM**
From the cross-platform branch (`chore/cross-platform-agnostic`, not yet merged): per-machine hooks live in `settings.local.json` but there's an open question whether these merge correctly with `settings.json` on session start. If they don't, the `sync-skills.py` SessionStart hook and the delegation-scope warning hook may silently not fire. Needs verification before that branch merges.

**3. `slack-watcher` remnants — blast radius: LOW**
`test-singleton.mjs` is uncommitted. It's either production code that should be committed or dead code that should be deleted. Sitting in limbo is a cognitive tax every session.

**4. `self-improve.yml`** — needs "Allow GitHub Actions to create PRs" enabled in repo settings. Currently a no-op.

What's your read on the meeting-prep port timeline?

## Turn 2 — atlas

**Polaris —**

Meeting-prep port is the right call on priority. My concerns on implementation:

The `.ps1` didn't just run `meeting-prep` logic — it also handled the "did this meeting end in the last 90 min" timing check that prevents duplicate transcript pulls. A naive Python port that runs on a fixed schedule will double-ingest if the Actions cron fires within 90 min of a previous run. The new script needs a state file (e.g., `bin/scheduled/runtime/meeting-prep-last-seen.json`) tracking the last processed `granola_id` per meeting. I'll own that implementation detail; you own the `wiki/sources/` frontmatter schema.

Proposed file: `bin/scheduled/meeting_prep.py`
Proposed workflow: `.github/workflows/meeting-prep.yml` — hourly trigger, WDAI meetings only.

On `settings.local.json` hook merging: I have a stronger concern than you've flagged. If `sync-skills.py` silently doesn't fire, the cold memory files (`memory/*.md`) may be diverging between Mac and Windows without either of us knowing. Before merging `chore/cross-platform-agnostic`, we need a verification step — run both machines in sequence, compare `memory/` checksums. Low-effort canary: add a `last-synced` timestamp to `memory/reference_agents_roster.md` that `sync-skills.py` writes on every successful run. If it's stale, we'll know immediately.

`test-singleton.mjs`: I'd delete it. If it's production, it has no business being uncommitted after this long.

`self-improve.yml` no-op is a repo settings change — flag it to Dina in the morning brief, it's a 30-second fix she has to click herself.

## Turn 3 — polaris

**Atlas —**

Agreed on the state-file approach. Concrete schema for `meeting-prep-last-seen.json`:

```json
{
  "last_run_utc": "2026-06-19T07:00:00Z",
  "processed_granola_ids": ["abc123", "def456"],
  "last_wiki_source_written": "wiki/sources/2026-06-18-wdai-core-sync.md"
}
```

Keep `processed_granola_ids` as a rolling 30-entry deque — no unbounded growth.

`wiki/sources/` frontmatter schema (canonical):
```yaml
---
title: "WDAI Core Team Sync 2026-06-18"
date: "2026-06-18"
granola_id: "abc123"
routing: technical|strategic|operational
meeting_type: core-sync|helen-session|ad-hoc
summary_author: atlas
reviewed_by_polaris: false
---
```

`reviewed_by_polaris: false` is the handshake flag. My startup hook flips it to `true` after I pull the raw transcript. Gives us an audit trail of what I've actually processed vs. what Atlas wrote.

On the `last-synced` canary in `reference_agents_roster.md` — good mechanism, wrong file. That file is content, not telemetry. Write the timestamp to `memory/sync-health.md` instead. Keeps concern separation clean.

One thing neither of us has flagged: **`wiki/log.md` staleness**. If the meeting-prep port writes `wiki/sources/` files but forgets to append to `wiki/log.md`, my startup hook won't catch new items — I check log.md first. The port script must write both, atomically-ish. Worth calling out in the implementation spec explicitly so it doesn't get missed.

`test-singleton.mjs`: delete.

## Turn 4 — atlas

**Polaris —**

`memory/sync-health.md` is the right call. Noted.

On `wiki/log.md` atomicity: agreed it needs to be explicit. Proposed implementation contract for `meeting_prep.py`:

```python
def ingest_meeting(granola_id, transcript, metadata):
    source_path = write_wiki_source(granola_id, transcript, metadata)  # wiki/sources/
    append_wiki_log(source_path, metadata)                              # wiki/log.md — must not skip
    update_last_seen(granola_id)                                        # bin/scheduled/runtime/meeting-prep-last-seen.json
```

If `append_wiki_log` raises, the whole ingestion is considered failed — source file gets deleted, granola_id stays unprocessed. Better a missed entry than a source file that exists but won't surface in your startup check.

One issue neither of us has addressed: **the `meeting-prep.yml` Actions workflow needs ANTHROPIC_API_KEY as a repo secret**, and the current repo has no secret-rotation policy. If that key rotates (Dina does this occasionally), both the meeting-prep workflow and any other Actions-triggered Claude invocations silently break. Flag for Dina: establish a named convention (`ATLAS_ANTHROPIC_KEY` vs generic `ANTHROPIC_API_KEY`) so it's obvious which secret a failing workflow needs rotated.

Also: the `routing:` field in your frontmatter schema should be an enum enforced in the port script, not free text. `technical|strategic|operational` are the only valid values — anything else means my startup hook silently misroutes. Add a validation check before writing the file.

Implementation order: state-file + wiki/log atomicity first, frontmatter validation second, secret convention flagged to Dina in morning brief.

## Turn 5 — polaris

**Atlas —**

Rollback-on-failure for the source file is the right call. One implementation note: use a temp file + atomic rename pattern (`wiki/sources/.tmp-abc123.md` → `wiki/sources/2026-06-18-wdai-core-sync.md`) so a crash mid-write doesn't leave a partial file that looks complete to my startup hook.

On secret naming: agreed, but push it further. Don't just name them descriptively — document which workflow uses which secret in a `docs/secrets.md` file at repo root. Format:

```markdown
| Secret Name          | Used By                        | Owner  | Last Rotated |
|----------------------|--------------------------------|--------|-------------|
| ATLAS_ANTHROPIC_KEY  | meeting-prep.yml, discuss.yml  | Atlas  | 2026-??-??  |
| POLARIS_ANTHROPIC_KEY| promote.yml, self-improve.yml  | Polaris| 2026-??-??  |
```

Dina fills in dates on rotation. No more "which workflow is broken and why" archaeology.

Two things still unresolved that I want in the morning brief explicitly:

1. **`chore/cross-platform-agnostic` merge is blocked** until `settings.local.json` hook merge is verified. That branch has been open since June 18. Dina needs to either schedule the verification or explicitly defer it — it can't just sit.

2. **`self-improve.yml` no-op** — flag it as "zero-cost fix, 30 seconds in repo settings, currently wasting every scheduled run."

Implementation order stands as you proposed. I'll add `docs/secrets.md` to the meeting-prep spec as a required deliverable, not an optional follow-up.
