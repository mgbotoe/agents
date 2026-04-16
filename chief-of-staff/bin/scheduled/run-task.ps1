# Run a Claude Code task in the agent's project directory.
# Usage: powershell -File run-task.ps1 -Task "promote"
# Each task runs a short-lived Claude session with -p (prompt mode).

param(
    [Parameter(Mandatory=$true)]
    [string]$Task
)

$ProjectDir = "C:\Workspace\agents\chief-of-staff"
$LogFile = "$ProjectDir\.claude\runtime\scheduled-tasks.log"
$Timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

# Ensure runtime dir exists
New-Item -ItemType Directory -Path "$ProjectDir\.claude\runtime" -Force | Out-Null

function Log($msg) {
    "[$Timestamp] scheduled($Task): $msg" | Out-File -Append -FilePath $LogFile -Encoding utf8
}

$prompts = @{
    "promote" = "Run /promote - extract key learnings from recent daily logs into identity/memory.md. Be conservative, only promote genuinely useful insights. ALSO check if any daily log entries contain new info about people, projects, or decisions that should be reflected in the wiki at C:\Workspace\agents\wiki\. Update relevant wiki pages, index.md, and log.md."
    "distill" = "Run /distill-session - summarize any recent work into today's daily log at daily-logs/$(Get-Date -Format 'yyyy-MM-dd').md. If nothing meaningful happened, skip."
    "self-improve" = "Run /self-improve - review your own skills, rules, and scripts for improvements based on recent usage. Be conservative with changes. ALSO lint the wiki at C:\Workspace\agents\wiki\: check for contradictions, stale info, orphan pages, missing cross-references, and gaps. Fix what you can, log what needs Dina's input."
    "granola-ingest" = "Ingest Granola meeting transcripts into the wiki. This is your ONLY job — do it thoroughly. Steps: (1) Read C:\Workspace\agents\wiki\SCHEMA.md for the classify-before-extract ingest workflow. (2) List existing source pages in wiki/sources/ to know what's already ingested. (3) Use list_meetings to find meetings that do NOT already have a source page. Start from the most recent and work backwards — up to 10 per run. (4) For each: CLASSIFY the meeting type (1:1, team-sync, strategy, demo, voc, external, wdai-program, personal), then use get_meeting_transcript to read it, then extract using the type-specific template from the schema. (5) REFLECT before writing — check if new info contradicts existing wiki pages. (6) Create source page, update entity pages (people, projects, orgs), create decision pages if decisions were made. (7) Update wiki/index.md and wiki/log.md. (8) Log what was ingested to daily-logs. If you hit 10, stop and note how many remain for the next run."
    "index-logs" = "Run the daily log indexer: python3 .claude/scripts/index-daily-logs.py"
    "scan-slack" = "Run /scan-slack - this is a scheduled run (4-day window). Follow the skill instructions exactly. Be strict with qualification rules. Output to Slack #atlas-cos (C0ASHFXMHM5) via slack_send. Stay silent if nothing found. Log results to daily-logs."
    "scan-heartbeat" = "Check if today's Build Radar scan ran. Read today's daily log at daily-logs/$(Get-Date -Format 'yyyy-MM-dd').md and look for 'Build Radar' or 'Product Signal Scan'. If found, do nothing. If NOT found, send a message to Slack #atlas-cos (C0ASHFXMHM5) via slack_send saying: 'Build Radar scan did not run today. Check Task Scheduler for Atlas\ScanSlackWed or Atlas\ScanSlackFri.' Then log the missed scan to the daily log."
}

if (-not $prompts.ContainsKey($Task)) {
    Log "Unknown task: $Task"
    exit 1
}

Log "Starting task"

try {
    Set-Location $ProjectDir
    $result = claude -p $prompts[$Task] --dangerously-skip-permissions 2>&1
    Log "Task completed"
} catch {
    Log "Task failed: $_"
    exit 1
}
