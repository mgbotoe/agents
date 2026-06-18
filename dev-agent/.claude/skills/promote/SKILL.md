---
name: promote
description: Extract key learnings from daily logs and promote them to identity/memory.md. Run automatically via scheduler once per day, or manually after a productive day.
---

Daily log promotion — extract signal from raw conversation logs into long-term memory.

## Hot/Cold Memory Architecture

- **Hot:** `identity/memory.md` — always in context, kept under 2500 tokens. Only the essentials.
- **Cold:** `memory/*.md` — topic files searched on-demand. Detailed context lives here.
  - `memory/projects.md` — project details, architecture, status
  - `memory/preferences.md` — recurring patterns, style choices
  - `memory/decisions.md` — key decisions with reasoning (and ADRs)
  - `memory/archive-YYYY-MM.md` — older entries rotated out of hot memory

## Steps

1. Read the last 3 days of `daily-logs/` files
2. Read current `identity/memory.md` (hot) and relevant `memory/*.md` files (cold)
3. **Curation pass on `identity/memory.md`** (do this BEFORE appending new entries):
   - Scan `## Session Log` for runs of same-day, near-identical entries (typical case: scheduled-task ghost sessions that all report "no movement").
   - Collapse a run into a single entry with a count and time range.
     - Example bad: 6 separate `[2026-04-23] Ghost distill #30..#35. No inbox movement; short-circuit guard pending Dina.` lines.
     - Example collapsed: `[2026-04-23] Ghost distills #30–35 (11:12–23:12). No inbox movement; short-circuit guard pending Dina.`
   - If two entries on different days say the same thing, keep the most recent and drop the older — Session Log is a log of *changes*, not a heartbeat.
   - Don't collapse across distinct facts. "Ghost distill, nothing happened" is one fact; "shipped X" is another.
4. Extract and route:
   - **Key decisions** (with rationale) → `identity/memory.md` Current State + `memory/decisions.md`
   - **Lessons learned** → `memory/decisions.md`
   - **New preferences** → `memory/preferences.md`
   - **Project context** → `memory/projects.md`
   - **Active work / open threads** → `identity/memory.md` Active Work
5. For `identity/memory.md` (hot layer):
   - Only promote things needed in every conversation
   - Update `## Current State` and `## Active Work`
   - Add one-liner to `## Session Log`
   - Keep under 2500 tokens — push detail to cold files
6. For `memory/*.md` (cold layer):
   - Add detailed entries with datestamps: `<!-- promoted YYYY-MM-DD -->`
   - Don't duplicate — consolidate with existing entries
   - Remove stale entries that are clearly no longer relevant
7. If `identity/memory.md` is over 2500 tokens, archive oldest entries to `memory/archive-YYYY-MM.md`
8. Report what was promoted, where it went, what was skipped, and what got collapsed during curation.
9. Write current Unix timestamp to `.claude/runtime/promote-last-run.ts`:
   ```bash
   date +%s > .claude/runtime/promote-last-run.ts
   ```

## Decay (separate concern)

Raw `daily-logs/*.md` decay is handled by the weekly `decay.yml` GitHub Actions cron (`.github/workflows/decay.yml` → `.claude/scripts/decay-memory.py`, matrix over both agents). Don't manually move daily logs from this skill.
