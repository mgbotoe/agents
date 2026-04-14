@echo off
REM Run a scheduled Polaris task via Claude Code.
REM Usage: run-task.cmd <task-name>
REM Example: run-task.cmd self-improve

setlocal
set TASK=%1
set PROJECT_DIR=%~dp0..\..
set LOG_FILE=%PROJECT_DIR%\.claude\runtime\scheduled-tasks.log

if "%TASK%"=="" (
    echo Usage: run-task.cmd ^<task-name^>
    exit /b 1
)

echo [%date% %time%] Running task: %TASK% >> "%LOG_FILE%"

cd /d "%PROJECT_DIR%"
claude --model opus -p "/%TASK%" 2>>"%LOG_FILE%"

echo [%date% %time%] Task completed: %TASK% >> "%LOG_FILE%"
endlocal
