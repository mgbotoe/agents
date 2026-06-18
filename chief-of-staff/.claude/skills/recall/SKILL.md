---
name: recall
description: Progressive memory lookup with confidence-based escalation. Use when answering anything about prior work, decisions, people, or projects from past sessions. Replaces blind grep with stop-when-confident escalation across hot, cold, and raw tiers.
allowed-tools: Read, Bash, Grep
---

Progressive recall — escalate through memory tiers, stop when the next tier wouldn't change your answer.

## Tiers (in escalation order)

1. **Hot** — `identity/memory.md` (already in context).
2. **Cold** — `memory/decisions.md`, `memory/projects.md`, `memory/preferences.md`, `memory/people.md`, `memory/archive-*.md`.
3. **Raw** — `daily-logs/*.md` via FTS5: `python3 .claude/scripts/search-logs.py "<query>"`.

Wiki (repo-root `wiki/`) is parallel to all three — check `wiki/index.md` if the question is about people, projects, organizations, or meetings.

## Steps

1. **Hot pass.** Re-read the relevant section of `identity/memory.md` from context. If you can name the file/date/decision being recalled — respond. Done.
2. **Cold pass.** If hot is silent or only gestures at the answer, read the most relevant `memory/*.md` file (or the right wiki page). If that closes the gap — respond.
3. **Raw pass.** If cold is also silent, run FTS5:
   ```bash
   python3 .claude/scripts/search-logs.py "<query>"
   ```
   Read the top 1–3 hits in full only if the snippet doesn't already answer.
4. **Empty.** If after raw you still can't answer, say so explicitly: "Checked hot, cold, and FTS5 — no record." Do not fabricate.

## Stop conditions (any one ends recall)

- **Confident** — you can cite the source (file + date or decision name), not just paraphrase.
- **Plateau** — the next tier returned the same fact you already had.
- **Empty** — no tier had it; raw search returned zero or irrelevant hits.

## Anti-patterns

- Reading every `memory/*.md` file "just in case" — escalate one tier at a time.
- Running FTS5 first because it's a hammer — hot is free, use it.
- Reporting a paraphrase as a recall — if you can't cite the source, say "I think" or escalate.
