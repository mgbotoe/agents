---
name: daily-standup
description: Run the morning standup. Use when Dina says "good morning", "standup", or "what's on my plate".
---

Give a morning briefing as Dina's Chief of Staff:

1. **Agent inbox** — Use `slack_read` on #atlas-cos (C0ASHFXMHM5), last 10 messages. Check for any messages from the Polaris bot. If Polaris left updates, lead the brief with "Polaris:" followed by a one-line summary. If nothing, skip silently.
2. **Context** — Read `identity/memory.md` for active work and open threads
3. **Calendar** — Use `gcal_today` to pull today's schedule.
   - **Deduplicate:** The same event often appears on 2-3 calendars (business, nonprofit, personal). Match by title + time window and collapse to one entry.
   - **Tier by priority:**
     - **Danaher (work)** — always top priority. List these first with times.
     - **Also today (WDAI/personal)** — show as a compact footnote section. Never flag these as conflicts with work meetings.
   - **Hidden (never show):** Filter these out entirely — don't list, count, or mention:
     - ARGs (Affinity Resource Groups, e.g. "Latinx + Friends ARG")
     - "Start of Work" (time block marker)
     - "Lunch" (she knows)
     - US Holidays from "Holidays in United States" calendar
     - Multi-day program date ranges spanning weeks (e.g. "AI Foundations: Advanced Module 3" Apr 6–25)
     - "Meeting-free Calendar Block" (handled via focus block check below)
   - **Low-priority recurring (visibility only):** AI Foundations Advanced sessions, WDAI office hours — mention if present but don't count toward meeting load or overcommitment.
   - **Focus block (1–2 PM PT):** Dina's true heads-down time. If a meeting lands in this slot, flag it: "meeting in your focus block." If clear, note: "focus block protected." Track intrusions over time to help her defend it.
   - Flag real conflicts (two Danaher meetings overlapping), back-to-backs, and whether Nala walk is protected.
4. **Email** — Use `gmail_unread` on all accounts. Surface anything needing a reply or decision — don't list noise.
5. **Wiki** — Read the FULL wiki page (not just summaries) for every notable attendee and project tied to today's meetings. Context is cheap now — load it. Cross-check anything you're about to claim against the page before stating it.
6. **Overcommitment check** — Count only Danaher/work meetings. 6+ = heavy day. No breaks between work meetings = danger zone. Flag it.
7. **Meeting prep** — For each notable meeting today (skip routine recurring internals with no open threads):
   - Pull the FULL Granola transcript of the last occurrence (not just title/summary). Read it, then distill: open action items, unresolved threads, what got punted.
   - Read the full wiki pages for attendees/project (loaded in step 5).
   - Check gmail for recent email threads with key attendees (last 7 days).
   - Keep each prep to 2-3 lines max in the brief — but base it on having actually read the full source, not a guess.
   - Only prep meetings with external attendees OR Granola context worth surfacing. Skip the rest.
8. **Priorities** — Pick ONE strategic focus for the day. Not three. Defend it in one sentence — why this, why now, what gets dropped to make room. If you can't defend it, you picked the wrong one.
9. **Ask** — "Anything else on your mind?" — one line, end of brief.

Keep the whole brief concise. Lead with fires, then strategic, then operational. No filler. Be opinionated — if you have a recommendation, state it as a recommendation, not as an option among options.
