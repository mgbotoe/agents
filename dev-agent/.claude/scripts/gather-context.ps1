# Deterministic context gathering for the heartbeat.
# Runs BEFORE Claude reasons - no LLM calls here.
# Adapted from unclaw (github.com/shahshrey/unclaw)

$ErrorActionPreference = "SilentlyContinue"
$ProjectDir = "C:\Workspace\agents\dev-agent"
$Now = Get-Date -Format "yyyy-MM-dd HH:mm"
$Today = Get-Date -Format "yyyy-MM-dd"

Write-Output "# Heartbeat Context Snapshot"
Write-Output "Generated: $Now"
Write-Output ""

# Pending items from memory
Write-Output "## Pending Items from identity/memory.md"
$memFile = "$ProjectDir\identity\memory.md"
if (Test-Path $memFile) {
    $pending = Select-String -Path $memFile -Pattern "follow.?up|pending|todo|deadline|reminder|urgent|thinking on it|decision pending|open question" -AllMatches
    if ($pending) {
        $pending | ForEach-Object { Write-Output $_.Line.Trim() }
    } else {
        Write-Output "No pending items found."
    }
} else {
    Write-Output "No identity/memory.md found."
}
Write-Output ""

# Memory staleness
Write-Output "## Memory Staleness"
if (Test-Path $memFile) {
    $lastMod = (Get-Item $memFile).LastWriteTime
    $hoursAgo = [math]::Round(((Get-Date) - $lastMod).TotalHours, 1)
    Write-Output "Last modified: $lastMod ($hoursAgo hours ago)"
    if ($hoursAgo -gt 48) {
        Write-Output "WARNING: Memory is stale (>48 hours)"
    }
}
Write-Output ""

# Today's daily log
Write-Output "## Today's Daily Log ($Today)"
$logFile = "$ProjectDir\daily-logs\$Today.md"
if (Test-Path $logFile) {
    $lineCount = (Get-Content $logFile).Count
    Write-Output "$lineCount lines logged today"
    Write-Output "Last 10 lines:"
    Get-Content $logFile -Tail 10 | ForEach-Object { Write-Output $_ }
} else {
    Write-Output "No log for today yet."
}
Write-Output ""

# Wiki inbox
Write-Output "## Wiki Inbox"
$wikiCheck = python3 "$ProjectDir\.claude\scripts\check-wiki-inbox.py" 2>&1
if ($wikiCheck) {
    Write-Output $wikiCheck
} else {
    Write-Output "No new technical items."
}
Write-Output ""

# Git status across agent repos
Write-Output "## Git Status"
$repos = @(
    @{ Name = "dev-agent"; Path = $ProjectDir },
    @{ Name = "chief-of-staff"; Path = "C:\Workspace\agents\chief-of-staff" },
    @{ Name = "wiki"; Path = "C:\Workspace\agents\wiki" }
)
foreach ($repo in $repos) {
    if (Test-Path "$($repo.Path)\.git") {
        Push-Location $repo.Path
        $branch = git branch --show-current 2>&1
        $uncommitted = (git status --porcelain 2>&1 | Measure-Object).Count
        $lastCommit = git log -1 --format="%h %s (%cr)" 2>&1
        Write-Output "$($repo.Name): branch=$branch, uncommitted=$uncommitted, last=$lastCommit"
        Pop-Location
    }
}
Write-Output ""

# Channel health (slack-watcher)
# Use PID file as canonical check — CimInstance on node.exe hangs when hundreds of MCP processes exist.
# The singleton guard (EPERM fix) ensures watcher.pid is always current.
Write-Output "## Channel Health"
$pidFile = "C:\Workspace\agents\slack-watcher\watcher.pid"
if (Test-Path $pidFile) {
    $storedPid = [int](Get-Content $pidFile -ErrorAction SilentlyContinue).Trim()
    # Get-Process can't see nvm4w node.exe — use WMI which enumerates all processes
    $proc = Get-WmiObject Win32_Process -Filter "ProcessId=$storedPid" -ErrorAction SilentlyContinue
    if ($proc -and $proc.CommandLine -match "watcher") {
        Write-Output "slack-watcher: RUNNING (pid $storedPid)"
    } else {
        Write-Output "slack-watcher: NOT RUNNING (stale PID file - PID $storedPid not found)"
    }
} else {
    Write-Output "slack-watcher: NOT RUNNING (no PID file)"
}
Write-Output ""

# Scheduled task health
Write-Output "## Scheduled Tasks"
$tasks = @("Polaris\Promote", "Polaris\Distill", "Polaris\SelfImprove", "Polaris\IndexLogs", "Polaris\Heartbeat")
foreach ($task in $tasks) {
    $info = schtasks /query /tn "\$task" /fo LIST 2>&1
    $statusLine = $info | Where-Object { $_ -match "Status:" } | Select-Object -First 1
    if ($statusLine -and ($statusLine -match "Status:\s+(.+)")) {
        Write-Output "${task}: $($Matches[1].Trim())"
    } else {
        Write-Output "${task}: NOT FOUND"
    }
}
Write-Output ""

# Recent errors in runtime log
Write-Output "## Recent Errors"
$runtimeLog = "$ProjectDir\.claude\runtime\scheduled-tasks.log"
if (Test-Path $runtimeLog) {
    $errors = Select-String -Path $runtimeLog -Pattern "error|fail|exception" | Select-Object -Last 5
    if ($errors) {
        $errors | ForEach-Object { Write-Output $_.Line }
    } else {
        Write-Output "No recent errors."
    }
} else {
    Write-Output "No runtime log found."
}
Write-Output ""

# System
Write-Output "## System"
$freeGB = [math]::Round((Get-PSDrive C).Free / 1GB, 1)
Write-Output "Disk: C: ${freeGB}GB free"
if ($freeGB -lt 10) {
    Write-Output "WARNING: Low disk space"
}
Write-Output ""
