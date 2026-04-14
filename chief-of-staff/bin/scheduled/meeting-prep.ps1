# Meeting Prep — sends context briefs to Discord 15 min before each meeting.
# Runs via Task Scheduler every 30 min during work hours (6:30 AM - 4 PM PT).
# Checks calendar for meetings starting in the next 15-30 min window,
# then sends a prep brief for each one.

param()

$ProjectDir = "C:\Workspace\agents\chief-of-staff"
$LogFile = "$ProjectDir\.claude\runtime\scheduled-tasks.log"
$Timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

New-Item -ItemType Directory -Path "$ProjectDir\.claude\runtime" -Force | Out-Null

function Log($msg) {
    "[$Timestamp] scheduled(meeting-prep): $msg" | Out-File -Append -FilePath $LogFile
}

$currentDate = Get-Date -Format "dddd, MMMM d, yyyy 'at' h:mm tt"

$prompt = @"
You are Atlas, Dina's Chief of Staff. Check if there are any meetings starting in the next 15-30 minutes and send a prep brief for each.
CURRENT DATE/TIME: $currentDate PT. Use this as the source of truth for today's date and day of the week.

CONTEXT:
- Dina works at Danaher (Enterprise AI), 7 AM - 3 PM PT
- You do NOT have access to her Danaher email (madina.gbotoe@danaher.com)
- You DO have access to: personal (mgbotoe@gmail.com), business (madina@gbotoe.com), nonprofit (madina@womendefiningai.org)
- Granola MCP may have past meeting transcripts — check if available
- Discord channel: 605801708546686998
- Dina's Discord tag: <@255180039002390528>

STEPS:

1. Use gcal_today to get all events for today
2. Check which meetings start in the next 15-30 minutes (current time in PT)
3. If no meetings in that window, exit silently — do NOT send anything to Discord
4. For each upcoming meeting, gather context:
   a. **Attendees** — list names/emails from the calendar invite
   b. **Recurring?** — is this a weekly/biweekly meeting or a one-off?
   c. **Recent emails** — use gmail_search to find recent emails from/to key attendees (last 7 days). Read the most relevant 1-2 emails for context.
   d. **Meeting notes** — search nonprofit inbox for Gemini meeting notes with this meeting's name
   e. **Granola** — use query_granola_meetings or list_meetings to search for the LAST occurrence of this meeting (same title or same key attendees). If found, use get_meetings to read the transcript. Extract: key decisions made, action items assigned, open threads that are still unresolved. This is the most valuable prep.
   f. **Wiki** — check C:\Workspace\agents\wiki\ for pages about attendees or the project this meeting relates to. Pull in relevant context.
5. Format and send to Discord:

<@255180039002390528> — Meeting Prep | [Meeting Title] in 15 min

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
"@

Log "Checking for upcoming meetings"

try {
    Set-Location $ProjectDir
    $result = claude -p $prompt --dangerously-skip-permissions 2>&1
    Log "Meeting prep check complete"
} catch {
    Log "Meeting prep failed: $_"
    exit 1
}
