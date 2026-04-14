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
    "[$Timestamp] scheduled($Task): $msg" | Out-File -Append -FilePath $LogFile
}

$prompts = @{
    "promote" = "Run /promote — extract key learnings from recent daily logs into identity/memory.md. Be conservative, only promote genuinely useful insights. ALSO check if any daily log entries contain new info about people, projects, or decisions that should be reflected in the wiki at C:\Workspace\agents\wiki\. Update relevant wiki pages, index.md, and log.md."
    "distill" = "Run /distill-session — summarize any recent work into today's daily log at daily-logs/$(Get-Date -Format 'yyyy-MM-dd').md. If nothing meaningful happened, skip."
    "self-improve" = "Run /self-improve — review your own skills, rules, and scripts for improvements based on recent usage. Be conservative with changes. ALSO do two wiki maintenance tasks: (1) LINT the wiki at C:\Workspace\agents\wiki\: check for contradictions, stale info, orphan pages, missing cross-references, and gaps. Fix what you can, log what needs Dina's input. (2) INGEST GRANOLA: Read C:\Workspace\agents\wiki\SCHEMA.md for the classify-before-extract ingest workflow. Use list_meetings to find the 10 oldest meetings that do NOT already have a source page in wiki/sources/. For each: CLASSIFY the meeting type first (1:1, team-sync, strategy, demo, voc, external, wdai-program, personal), then use get_meetings to read the transcript, then extract using the type-specific template from the schema. REFLECT before writing — check if new info contradicts existing wiki pages. Create source page, update entity pages, create decision pages if decisions were made. Update wiki/index.md and wiki/log.md."
    "index-logs" = "Run the daily log indexer: python3 .claude/scripts/index-daily-logs.py"
    "scan-slack" = "Run /scan-slack — this is a scheduled run (4-day window). Follow the skill instructions exactly. Be strict with qualification rules. Output to Discord #product-radar (1493333553143091240). Stay silent if nothing found. Log results to daily-logs."
    "scan-heartbeat" = "Check if today's Build Radar scan ran. Read today's daily log at daily-logs/$(Get-Date -Format 'yyyy-MM-dd').md and look for 'Build Radar' or 'Product Signal Scan'. If found, do nothing. If NOT found, send a message to Discord #atlas (1493062124975685864) saying: 'Build Radar scan did not run today. Check Task Scheduler for Atlas\ScanSlackWed or Atlas\ScanSlackFri.' Then log the missed scan to the daily log."
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
