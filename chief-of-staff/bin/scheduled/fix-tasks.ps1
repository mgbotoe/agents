$tasks = @('Promote','SelfImprove','IndexLogs','Distill','ScanSlackWed','ScanSlackFri','MorningBrief','MiddayCheck','EveningWrapup','FridayWrap','WeeklyReview','MeetingPrep')

foreach ($name in $tasks) {
    $path = "Atlas\$name"
    try {
        $task = Get-ScheduledTask -TaskPath "\Atlas\" -TaskName $name -ErrorAction Stop
        $settings = $task.Settings
        $settings.WakeToRun = $true
        $settings.StartWhenAvailable = $true
        $settings.DisallowStartIfOnBatteries = $false
        $settings.StopIfGoingOnBatteries = $false
        Set-ScheduledTask -TaskPath "\Atlas\" -TaskName $name -Settings $settings | Out-Null
        Write-Host "Fixed: $name (wake=true, battery=ok, start-if-missed=true)"
    } catch {
        Write-Host "Skip: $name (not found)"
    }
}
