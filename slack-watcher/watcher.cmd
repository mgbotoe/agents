@echo off
REM Supervisor loop — restart watcher if it exits for any reason.
REM Exit code 0 = intentional shutdown (SIGINT/SIGTERM), stop the loop.
REM Any other exit = crash, wait 10s and restart.

cd /d C:\Workspace\agents\slack-watcher

:loop
echo [%DATE% %TIME%] Starting watcher
node watcher.mjs
set EXITCODE=%ERRORLEVEL%
echo [%DATE% %TIME%] watcher exited with code %EXITCODE%

if "%EXITCODE%"=="0" (
  echo [%DATE% %TIME%] Clean exit, stopping supervisor.
  goto :eof
)

echo [%DATE% %TIME%] Restarting in 10s...
timeout /t 10 /nobreak >nul
goto loop
