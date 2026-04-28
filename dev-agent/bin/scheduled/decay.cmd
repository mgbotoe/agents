@echo off
REM Decay old daily logs into monthly archives. Schedule weekly.
setlocal
set PROJECT_DIR=%~dp0..\..
set LOG_FILE=%PROJECT_DIR%\.claude\runtime\scheduled-tasks.log

echo [%date% %time%] Running decay >> "%LOG_FILE%"
cd /d "%PROJECT_DIR%"
python .claude\scripts\decay-memory.py >> "%LOG_FILE%" 2>&1
echo [%date% %time%] Decay completed >> "%LOG_FILE%"
endlocal
