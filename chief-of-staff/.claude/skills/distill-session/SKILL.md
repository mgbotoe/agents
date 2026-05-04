---
name: distill-session
description: Compress and save the key context from this session to the daily log. Run before ending a long session.
disable-model-invocation: true
---

**Short-circuit check (run FIRST):**

Before doing anything, assess: did this session contain real work?

Signals of a "ghost session" (skip distill):
- No user messages beyond automated startup hook output
- No file edits (Edit/Write/NotebookEdit calls = 0)
- No substantive tool calls — only inbox checks (slack_read), wiki reads, and a `git status`
- Session triggered by scheduler with no human interaction

If 3+ of those are true: do NOT append to daily log under a `Session Distill` heading, do NOT touch `identity/memory.md`.
Instead, append ONE line to `daily-logs/YYYY-MM-DD.md` under `## Ghost Distills`:
`- [HH:MM] no-op — scheduler spawn, no work to distill`
Create the section if missing. Then exit.

This prevents the every-2h scheduler from polluting daily logs and memory with 30+ identical "checked inbox, nothing to do" entries.

---

Session distillation — save this session's context to the daily log:

1. Summarize what was accomplished in this session (3-5 bullets)
2. List any open tasks or threads left unfinished
3. Extract any preferences or patterns Dina demonstrated
4. Append to `daily-logs/YYYY-MM-DD.md` (today's date) under a `## [HH:MM] Session Distill` heading
   - Create the file with a `# Daily Log — YYYY-MM-DD` header if it doesn't exist
5. Also append a one-liner to `identity/memory.md` under `## Session Log`:
   Format: `- [YYYY-MM-DD] <what was done, 1 line>`
6. Do not output any confirmation to the conversation. Write silently.

Token budget: keep the daily log entry under 200 words. Keep the identity/memory.md one-liner under 20 words.
