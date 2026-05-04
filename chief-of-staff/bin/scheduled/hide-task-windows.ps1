# Re-points all \Atlas\* scheduled tasks to use the hidden VBScript launcher.
# Backs up current XML to bin/scheduled/backups/ before changing anything.
# Reversible: run restore-from-backup if anything goes sideways.

$ErrorActionPreference = 'Stop'
$repoRoot = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$vbs      = Join-Path $PSScriptRoot 'run-hidden.vbs'
$backupDir = Join-Path $PSScriptRoot 'backups'
New-Item -ItemType Directory -Force -Path $backupDir | Out-Null

# Map each task to its argument (the task-name slug passed to run-task.cmd).
$tasks = @{
    'MorningBrief'      = 'morning-brief'
    'MiddayCheck'       = 'midday-check'
    'EveningWrapup'     = 'evening-wrapup'
    'FridayWrap'        = 'friday-wrap'
    'WeeklyReview'      = 'weekly-review'
    'GranolaIngest'     = 'granola-ingest'
    'Promote'           = 'promote'
    'Distill'           = 'distill'
    'IndexLogs'         = 'index-logs'
    'SelfImprove'       = 'self-improve'
    'ScanSlackWed'      = 'scan-slack'
    'ScanSlackFri'      = 'scan-slack'
    'ScanHeartbeatWed'  = 'scan-heartbeat'
    'ScanHeartbeatFri'  = 'scan-heartbeat'
    'MeetingPrep'       = 'meeting-prep'
}

$results = @()

foreach ($entry in $tasks.GetEnumerator()) {
    $taskName = $entry.Key
    $arg      = $entry.Value
    $fullPath = "\Atlas\$taskName"

    # Skip if task doesn't exist
    $existing = Get-ScheduledTask -TaskName $taskName -TaskPath '\Atlas\' -ErrorAction SilentlyContinue
    if (-not $existing) {
        $results += [pscustomobject]@{Task=$taskName; Status='skipped (not found)'}
        continue
    }

    # Backup current XML
    $backupFile = Join-Path $backupDir "$taskName.xml"
    schtasks /query /tn $fullPath /xml | Out-File -FilePath $backupFile -Encoding utf8

    # Build new hidden action
    $newAction = New-ScheduledTaskAction -Execute 'wscript' -Argument "`"$vbs`" $arg"

    try {
        Set-ScheduledTask -TaskName $taskName -TaskPath '\Atlas\' -Action $newAction | Out-Null
        $results += [pscustomobject]@{Task=$taskName; Status='updated'}
    } catch {
        $results += [pscustomobject]@{Task=$taskName; Status="FAILED: $($_.Exception.Message)"}
    }
}

$results | Format-Table -AutoSize
Write-Host ""
Write-Host "Backups saved to: $backupDir"
