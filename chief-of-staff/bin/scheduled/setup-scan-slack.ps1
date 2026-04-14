# Create twice-weekly scan-slack scheduled tasks
# Wednesday and Friday at 4:00 PM Pacific

$action = New-ScheduledTaskAction -Execute "C:\Workspace\agents\chief-of-staff\bin\scheduled\run-task.cmd" -Argument "scan-slack"

# Wednesday 4pm
$triggerWed = New-ScheduledTaskTrigger -Weekly -DaysOfWeek Wednesday -At "4:00PM"
Register-ScheduledTask -TaskName "Atlas\ScanSlackWed" -Action $action -Trigger $triggerWed -Description "WDAI Build Radar — Wednesday scan" -Force

# Friday 4pm
$triggerFri = New-ScheduledTaskTrigger -Weekly -DaysOfWeek Friday -At "4:00PM"
Register-ScheduledTask -TaskName "Atlas\ScanSlackFri" -Action $action -Trigger $triggerFri -Description "WDAI Build Radar — Friday scan" -Force

Write-Host "Done — scan-slack scheduled for Wed + Fri at 4pm"
Get-ScheduledTask -TaskPath "\Atlas\" | Where-Object {$_.TaskName -like "ScanSlack*"} | Format-Table TaskName, State, Description
