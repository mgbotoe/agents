@echo off
REM Run a scheduled Polaris task via Claude Code.
REM Usage: run-task.cmd <task-name>
REM Example: run-task.cmd self-improve
REM
REM After claude.exe exits, kills any orphaned MCP server children (node.exe)
REM that were spawned by the session but not cleaned up on exit.

setlocal
set TASK=%1
set PROJECT_DIR=%~dp0..\..
set LOG_FILE=%PROJECT_DIR%\.claude\runtime\scheduled-tasks.log
set CLAUDE=%USERPROFILE%\.local\bin\claude.exe

if "%TASK%"=="" (
    echo Usage: run-task.cmd ^<task-name^>
    exit /b 1
)

echo [%date% %time%] Running task: %TASK% >> "%LOG_FILE%"

cd /d "%PROJECT_DIR%"

REM Run claude.exe and kill its entire process tree after it exits.
REM -PassThru captures the PID; WaitForExit() blocks until done.
REM taskkill /T /F kills the named child and all its descendants.
powershell -NonInteractive -NoProfile -Command ^
    "$env:TASK = '%TASK%';" ^
    "$claude = $env:CLAUDE;" ^
    "$proc = Start-Process -FilePath $claude -ArgumentList ('--model opus -p /' + $env:TASK) -NoNewWindow -PassThru;" ^
    "$claudePid = $proc.Id;" ^
    "Write-Host ('[' + (Get-Date -Format 'HH:mm:ss') + '] claude.exe PID: ' + $claudePid);" ^
    "$proc.WaitForExit();" ^
    "$ec = $proc.ExitCode;" ^
    "$children = Get-CimInstance Win32_Process -Filter ('ParentProcessId=' + $claudePid) -ErrorAction SilentlyContinue;" ^
    "foreach ($child in $children) { & taskkill /T /F /PID $child.ProcessId 2>&1 | Out-Null };" ^
    "if ($children.Count -gt 0) { Write-Host ('[' + (Get-Date -Format 'HH:mm:ss') + '] Cleaned up ' + $children.Count + ' orphaned MCP children') };" ^
    "exit $ec"

echo [%date% %time%] Task completed: %TASK% (exit: %ERRORLEVEL%) >> "%LOG_FILE%"
endlocal
