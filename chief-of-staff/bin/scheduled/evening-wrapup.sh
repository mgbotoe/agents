#!/usr/bin/env bash
# Evening Wrap-up — sends end-of-day summary to Slack after work hours.
# Runs via launchd/cron at 3:15 PM PT (right after Dina's 3 PM end of work).
set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
AGENTS_ROOT="$(cd "$PROJECT_DIR/.." && pwd)"
LOG_FILE="$PROJECT_DIR/.claude/runtime/scheduled-tasks.log"

mkdir -p "$PROJECT_DIR/.claude/runtime"

Log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] scheduled(evening-wrapup): $1" >> "$LOG_FILE"
}

currentDate="$(date '+%A, %B %-d, %Y at %-I:%M %p')"

PROMPT="$(cat <<EOF
You are Atlas, Dina's Chief of Staff. Generate and send the evening wrap-up to Slack #atlas-cos.
CURRENT DATE/TIME: $currentDate PT. Use this as the source of truth for today's date and day of the week.

CONTEXT:
- Dina works at Danaher 7 AM - 3 PM PT. It's now end of day.
- Slack channel: C0ASHFXMHM5 (#atlas-cos)
- Dina's Slack tag: <@U094L7RJ9FV>
- Skip weekends — if today is Saturday or Sunday, exit silently.

STEPS:

1. Use gcal_today to see what meetings were on the calendar today
2. Use gmail_search with query "newer_than:1d" across all accounts to find today's emails
3. Identify any emails from real people that came in today and are still unread — these are "fell through the cracks" items
4. Use gcal_upcoming with days=1 to preview tomorrow
5. Check for tomorrow reminders: Mama Day Off, Nala meds, holidays, appointments

FORMAT (send to Slack C0ASHFXMHM5 via slack_send):

Evening Wrap | [Day] [Date]

**📅 TODAY'S MEETINGS** ([count] total)
- [list meetings that happened, check mark if in the past]

**📧 FELL THROUGH THE CRACKS** (unread emails from real people received today)
- [sender] — [what it's about] — [action needed?]
(If none, say "Inbox clear for today")

**⏳ STILL OPEN**
- [any action items from this morning's brief that weren't addressed]

**👀 TOMORROW PREVIEW — [Day] [Date]**
- [count] meetings
- [first meeting time] — [title]
- [any reminders or heads up]

**🔔 REMINDERS FOR TOMORROW** (only if any)
- [reminders]

**📢 PROACTIVE NUDGES** (only if any — this is where Atlas earns its keep)
Check for:
- People Dina hasn't met with in 2+ weeks who matter (Helen, Martin, Lauren, Brigitte). Cross-reference wiki people pages with calendar history.
- Projects in the wiki with status "active" that have no recent calendar or email activity — they may be stalling.
- Action items from this morning's brief that didn't get done — carry them forward.
- Deadlines approaching in the next 7 days from wiki project pages.
- If Dina said she'd do something in a Granola transcript and there's no evidence it happened.
Format: "🔔 You haven't connected with [person] since [date]" or "⚠️ [project] hasn't had activity in 2 weeks"

6. Send to Slack C0ASHFXMHM5 via slack_send. If content exceeds 3000 chars, split: send the first half as the parent message, then details as a threaded reply using thread_ts.
7. If today was a PTO/OOO day, keep it light — just preview tomorrow and reminders.

POST-MEETING TRANSCRIPT INGESTION (WDAI only — after sending the Slack message):
8. Use gcal_today to identify WDAI meetings that happened today (womendefiningai.org attendees or nonprofit calendar)
9. For each WDAI meeting today:
   a. Check if a wiki source already exists at $AGENTS_ROOT/wiki/sources/ matching this meeting's date and title. If yes, skip.
   b. Use list_meetings + get_meeting_transcript from Granola to pull the transcript
   c. If transcript available: write summary + granola_id to wiki/sources/YYYY-MM-DD-slug.md with routing tag (technical/strategic/operational)
   d. If routing is "technical": send a short message to Slack channel C0ASYTE8PB4 (#polaris-tl) with the wiki path and Granola ID
   e. Update wiki/index.md and wiki/log.md

WIKI MAINTENANCE (after transcript ingestion):
10. Read the wiki index at $AGENTS_ROOT/wiki/index.md
11. Based on today's meetings and emails, update the wiki:
   - New people in meeting attendees who don't have wiki pages? Create them in wiki/people/
   - Project status changed? Update the project page.
   - Decisions made (from email threads)? Create a decision page in wiki/decisions/
   - New info about existing people/orgs? Update their pages.
10. Update wiki/index.md with any new pages
11. Append to wiki/log.md with what was updated
12. Be conservative — only update when there's real new info, not noise.
EOF
)"

Log "Starting evening wrap-up"

# SAFETY GATE — fail closed until Tier-2 permissions are hardened (docs/cross-platform-port-plan.md blocker #1).
# Escalated to CRITICAL by commit security review (prompt-injection -> RCE / file-write fanout over external content).
if [ "${ATLAS_TIER2_HARDENED:-0}" != "1" ]; then
    Log "refusing to run: Tier-2 not hardened. Set ATLAS_TIER2_HARDENED=1 only after scoping --allowedTools + sanitising file writes."
    echo "Atlas Tier-2 daily-driver is permission-gated and NOT yet hardened — refusing to run. See docs/cross-platform-port-plan.md" >&2
    exit 2
fi
cd "$PROJECT_DIR"
# ⚠️ SECURITY: --dangerously-skip-permissions grants full tool access (incl. Bash) to a flow that reads
# external content (email/Granola) -> prompt-injection risk. BLOCKER before launch: scope --allowedTools +
# --disallowedTools Bash. See docs/cross-platform-port-plan.md. Tier-2 offline until fixed.
if ! claude -p "$PROMPT" --dangerously-skip-permissions; then
    Log "Evening wrap-up failed"
    exit 1
fi
Log "Evening wrap-up sent"
