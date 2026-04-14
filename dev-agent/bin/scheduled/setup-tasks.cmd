@echo off
REM Create Polaris scheduled tasks in Windows Task Scheduler

set SCRIPT_PATH=C:\Workspace\agents\dev-agent\bin\scheduled\run-task.cmd

echo Creating \Polaris\Promote (daily 11:00 PM)...
schtasks /create /tn "\Polaris\Promote" /tr "\"%SCRIPT_PATH%\" promote" /sc daily /st 23:00 /f

echo Creating \Polaris\Distill (every 2 hours)...
schtasks /create /tn "\Polaris\Distill" /tr "\"%SCRIPT_PATH%\" distill-session" /sc minute /mo 120 /f

echo Creating \Polaris\SelfImprove (daily 3:00 AM)...
schtasks /create /tn "\Polaris\SelfImprove" /tr "\"%SCRIPT_PATH%\" self-improve" /sc daily /st 03:00 /f

echo Creating \Polaris\IndexLogs (daily 11:30 PM)...
schtasks /create /tn "\Polaris\IndexLogs" /tr "\"%SCRIPT_PATH%\" index-logs" /sc daily /st 23:30 /f

echo.
echo Verifying tasks...
schtasks /query /fo TABLE /tn "\Polaris\Promote"
schtasks /query /fo TABLE /tn "\Polaris\Distill"
schtasks /query /fo TABLE /tn "\Polaris\SelfImprove"
schtasks /query /fo TABLE /tn "\Polaris\IndexLogs"

echo Done.
