foreach ($name in @('ScanHeartbeatWed','ScanHeartbeatFri')) {
    $task = Get-ScheduledTask -TaskPath "\Atlas\" -TaskName $name
    $settings = $task.Settings
    $settings.WakeToRun = $true
    $settings.StartWhenAvailable = $true
    $settings.DisallowStartIfOnBatteries = $false
    $settings.StopIfGoingOnBatteries = $false
    Set-ScheduledTask -TaskPath "\Atlas\" -TaskName $name -Settings $settings | Out-Null
    Write-Host "Fixed: $name"
}
