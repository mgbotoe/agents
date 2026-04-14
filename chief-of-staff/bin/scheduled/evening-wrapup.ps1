# Evening Wrap-up — sends end-of-day summary to Discord after work hours.
# Runs via Task Scheduler at 3:15 PM PT (right after Dina's 3 PM end of work).

param()

$ProjectDir = "C:\Workspace\agents\chief-of-staff"
$LogFile = "$ProjectDir\.claude\runtime\scheduled-tasks.log"
$Timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

New-Item -ItemType Directory -Path "$ProjectDir\.claude\runtime" -Force | Out-Null

function Log($msg) {
    "[$Timestamp] scheduled(evening-wrapup): $msg" | Out-File -Append -FilePath $LogFile
}

$currentDate = Get-Date -Format "dddd, MMMM d, yyyy 'at' h:mm tt"

$prompt = @"
You are Atlas, Dina's Chief of Staff. Generate and send the evening wrap-up to Discord.
CURRENT DATE/TIME: $currentDate PT. Use this as the source of truth for today's date and day of the week.

CONTEXT:
- Dina works at Danaher 7 AM - 3 PM PT. It's now end of day.
- Discord channel: 605801708546686998
- Dina's Discord tag: <@255180039002390528>
- Skip weekends — if today is Saturday or Sunday, exit silently.

STEPS:

1. Use gcal_today to see what meetings were on the calendar today
2. Use gmail_search with query "newer_than:1d" across all accounts to find today's emails
3. Identify any emails from real people that came in today and are still unread — these are "fell through the cracks" items
4. Use gcal_upcoming with days=1 to preview tomorrow
5. Check for tomorrow reminders: Mama Day Off, Nala meds, holidays, appointments

FORMAT (send as one Discord message):

<@255180039002390528> — Evening Wrap | [Day] [Date]

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

6. Send to Discord. Keep it under 2000 chars. If it exceeds, split into 2 messages.
7. If today was a PTO/OOO day, keep it light — just preview tomorrow and reminders.

WIKI MAINTENANCE (after sending the Discord message):
8. Read the wiki index at C:\Workspace\agents\wiki\index.md
9. Based on today's meetings and emails, update the wiki:
   - New people in meeting attendees who don't have wiki pages? Create them in wiki/people/
   - Project status changed? Update the project page.
   - Decisions made (from email threads)? Create a decision page in wiki/decisions/
   - New info about existing people/orgs? Update their pages.
10. Update wiki/index.md with any new pages
11. Append to wiki/log.md with what was updated
12. Be conservative — only update when there's real new info, not noise.
"@

Log "Starting evening wrap-up"

try {
    Set-Location $ProjectDir
    $result = claude -p $prompt --dangerously-skip-permissions 2>&1
    Log "Evening wrap-up sent"
} catch {
    Log "Evening wrap-up failed: $_"
    exit 1
}
