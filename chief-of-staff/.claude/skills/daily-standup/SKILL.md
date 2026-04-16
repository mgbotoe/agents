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
5. **Wiki** — Check `C:\Workspace\agents\wiki\` for any people/project pages relevant to today's meetings.
6. **Overcommitment check** — Count only Danaher/work meetings. 6+ = heavy day. No breaks between work meetings = danger zone. Flag it.
7. **Meeting prep** — For each notable meeting today (skip routine recurring internals with no open threads):
   - Check Granola for the last occurrence — pull key outcomes, open action items, unresolved threads
   - Check wiki for attendee/project pages
   - Check gmail for recent email threads with key attendees (last 7 days)
   - Keep each prep to 2-3 lines max: who, last time context, open threads
   - Only prep meetings with external attendees OR Granola context worth surfacing. Skip the rest.
8. **Priorities** — Recommend the top 1-2 things to focus on today, factoring in energy (deep work mornings, lighter afternoons).
9. **Ask** — "Anything else on your mind?" — one line, end of brief.

Keep the whole brief concise. Lead with fires, then strategic, then operational. No filler.
