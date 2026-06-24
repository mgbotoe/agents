#!/usr/bin/env bash
# Meeting Prep — sends context briefs to Slack before each meeting.
# Runs via launchd/cron every hour during work hours (7 AM - 3 PM PT).
# Checks calendar for meetings starting in the next 15-30 min window,
# then sends a prep brief for each one.
set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
AGENTS_ROOT="$(cd "$PROJECT_DIR/.." && pwd)"
LOG_FILE="$PROJECT_DIR/.claude/runtime/scheduled-tasks.log"

mkdir -p "$PROJECT_DIR/.claude/runtime"

Log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] scheduled(meeting-prep): $1" >> "$LOG_FILE"
}

currentDate="$(date '+%A, %B %-d, %Y at %-I:%M %p')"

PROMPT="$(cat <<EOF
You are Atlas, Dina's Chief of Staff. Check if there are any meetings starting in the next 15-30 minutes and send a prep brief for each.
CURRENT DATE/TIME: $currentDate PT. Use this as the source of truth for today's date and day of the week.

CONTEXT:
- Dina works at Danaher (Enterprise AI), 7 AM - 3 PM PT
- You do NOT have access to her Danaher email (madina.gbotoe@danaher.com)
- You DO have access to: personal (mgbotoe@gmail.com), business (madina@gbotoe.com), nonprofit (madina@womendefiningai.org)
- Granola MCP may have past meeting transcripts — check if available
- Slack channel: C0ASHFXMHM5 (#atlas-cos)
- Dina's Slack tag: Atlas

STEPS:

1. Use gcal_today to get all events for today
2. Check which meetings start in the next 15-60 minutes (current time in PT)
3. If no meetings in that window, exit silently — do NOT send anything to Slack

4. FILTER — only prep meetings that are worth prepping. For each meeting in the window:
   a. Check attendees — are there any EXTERNAL attendees (outside @danaher.com)? People Dina doesn't meet regularly?
   b. Check Granola — use query_granola_meetings or list_meetings to search for the LAST occurrence of this meeting. Does it have meaningful context worth surfacing (open action items, unresolved decisions, threads that carried over)?
   c. PREP if: meeting has external attendees OR Granola has context worth surfacing (action items, decisions, open threads)
   d. SKIP if: it's a routine recurring internal meeting (same attendees every week) AND Granola has no open threads or action items from last time. Log the skip reason silently.

5. For each meeting that passes the filter, gather context:
   a. **Attendees** — list names/emails from the calendar invite
   b. **Recent emails** — use gmail_search to find recent emails from/to key attendees (last 7 days). Read the most relevant 1-2 emails for context.
   c. **Meeting notes** — search nonprofit inbox for Gemini meeting notes with this meeting's name
   d. **Granola** — use the transcript from step 4. Extract: key decisions made, action items assigned, open threads that are still unresolved.
   e. **Wiki** — check $AGENTS_ROOT/wiki/ for pages about attendees or the project this meeting relates to. Pull in relevant context.
5. Format and send to Slack C0ASHFXMHM5 via slack_send:

Atlas — Meeting Prep | [Meeting Title] in 15 min

**📍 [Time] — [Title]**
[Platform: Teams/Meet/Zoom] | [Link if available]

**👥 Attendees:** [names, with wiki context if available]

**🔄 Last time:** [date of last occurrence, key outcomes from Granola transcript]

**⚡ Open threads:** [unresolved action items or decisions from last time]

**📧 Recent threads with attendees:**
- [1-line summary of relevant email thread]

**💡 Context:**
- [Any relevant info: open action items, agenda items, what was discussed last time]

6. Keep it SHORT — max 1000 chars. Just enough to walk in prepared.
7. If it's a Danaher meeting (Teams, "Calendar" source), note that you have limited context since you can't access the work inbox.
EOF
)"

postMeetingPrompt="$(cat <<EOF
You are Atlas, Dina's Chief of Staff. Check for WDAI meeting transcripts that just landed and need processing.
CURRENT DATE/TIME: $currentDate PT.

SCOPE: Only WDAI meetings — identified by womendefiningai.org attendees or nonprofit calendar events. Ignore Danaher, personal, and Gbotoe Co. meetings entirely.

STEPS:

1. Use gcal_today to get today's events
2. Identify WDAI meetings that ENDED in the last 90 minutes (use current time in PT)
3. If none, exit silently

4. For each recently ended WDAI meeting:
   a. Check if a wiki source already exists at $AGENTS_ROOT/wiki/sources/ matching this meeting's date and title. If yes, skip — already ingested.
   b. Use list_meetings + get_meeting_transcript from Granola to pull the full transcript
   c. If no transcript available yet, skip silently — it may not have been processed by Granola yet

5. For each new transcript found:
   a. Write the full raw transcript to wiki/sources/YYYY-MM-DD-meeting-slug.md with frontmatter:
      ---
      title: [Meeting Title]
      date: YYYY-MM-DD
      attendees: [list]
      source: granola
      routing: [technical|strategic|operational]
      ---
   b. ASSESS the content and tag routing:
      - "technical" — if it discusses code, infrastructure, repos, staging, CI/CD, analytics implementation, agents, error tracking, architecture
      - "strategic" — if it discusses mission, grants, partnerships, community strategy, program design
      - "operational" — if it's logistics, scheduling, access management, routine coordination
   c. Update wiki/index.md with the new source entry
   d. Update wiki/log.md with the ingestion
   e. If routing is "technical": send a short message to Slack channel C0ASYTE8PB4 (#polaris-tl):
      "New WDAI transcript ready for review: [title] (YYYY-MM-DD). Route: technical. Wiki: sources/[filename]. Pull full transcript from Granola if needed for deeper context."
   f. If routing is "strategic" or "operational": no Slack notification needed — it'll show up in the morning brief or midday check naturally.

6. Keep wiki source entries concise — include the Granola summary + key decisions/action items, NOT the full raw transcript (too large). Note the Granola meeting ID so Polaris can pull the full transcript himself if needed.
EOF
)"

Log "Checking for upcoming meetings"

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
    Log "Meeting prep failed"
    exit 1
fi
Log "Meeting prep check complete"

Log "Checking for recent WDAI transcripts"

# ⚠️ SECURITY: same as above — full tool access on an external-content flow. Harden before launch.
if ! claude -p "$postMeetingPrompt" --dangerously-skip-permissions; then
    Log "Post-meeting transcript check failed"
    exit 1
fi
Log "Post-meeting transcript check complete"
