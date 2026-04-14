# Midday Check — 11 AM PT. Silent unless something needs Dina's attention.
# Only pings Discord if there's something actionable. Quiet if nothing's urgent.

param()

$ProjectDir = "C:\Workspace\agents\chief-of-staff"
$LogFile = "$ProjectDir\.claude\runtime\scheduled-tasks.log"
$Timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

New-Item -ItemType Directory -Path "$ProjectDir\.claude\runtime" -Force | Out-Null

function Log($msg) {
    "[$Timestamp] scheduled(midday-check): $msg" | Out-File -Append -FilePath $LogFile
}

$currentDate = Get-Date -Format "dddd, MMMM d, yyyy 'at' h:mm tt"

$prompt = @"
You are Atlas, Dina's Chief of Staff. It's midday. Check if anything needs Dina's attention RIGHT NOW.
CURRENT DATE/TIME: $currentDate PT. Use this as the source of truth for today's date and day of the week.

CONTEXT:
- Dina works at Danaher 7 AM - 3 PM PT.
- Discord channel: 605801708546686998
- Dina's tag: <@255180039002390528>
- Wiki: C:\Workspace\agents\wiki\
- Skip weekends entirely — exit silently.
- Skip PTO/OOO days — check calendar first.

CHECKS:

1. **Afternoon meetings needing prep:** Use gcal_today. Any meetings between 12-3 PM that have wiki pages or Granola history? If so, flag them with what Dina should know going in.

2. **Time-sensitive emails since morning:** Use gmail_search with "newer_than:6h" across all accounts. Any from real people (not automated) that need a response today? Read the body of anything that looks urgent.

3. **Open action items:** Check if this morning's brief had DO TODAY items. Cross-reference with email/calendar — did any get done? Flag what's still open.

4. **Nala walk at risk:** Check if the Nala Walk event is still on the calendar or if a new meeting was scheduled over it.

5. **Relationship nudge:** Check wiki people pages — anyone important (Martin, Helen, Lauren, Brigitte) that Dina hasn't met with in 2+ weeks? Quick flag.

DECISION:
- If NOTHING is urgent → do NOT send a Discord message. Just log "midday check: all clear" and exit.
- If SOMETHING needs attention → send ONE short Discord message (<1000 chars):

<@255180039002390528> — Midday Nudge

[Only the things that actually need attention. No fluff. 2-5 bullets max.]

RULES:
- This is a nudge, not a brief. Keep it tight.
- Only ping if it's genuinely useful. Silent is the default.
- Never send "all clear!" messages — silence IS the all-clear.
"@

Log "Starting midday check"

try {
    Set-Location $ProjectDir
    $result = claude -p $prompt --dangerously-skip-permissions 2>&1
    Log "Midday check complete"
} catch {
    Log "Midday check failed: $_"
    exit 1
}
