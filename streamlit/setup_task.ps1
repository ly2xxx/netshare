# setup_task.ps1
# This script registers 'keep_alive.ps1' in Windows Task Scheduler to run every 1 hour.

$TaskName = "StreamlitKeepAlive"
$ScriptPath = Join-Path -Path $PSScriptRoot -ChildPath "keep_alive.ps1"
$PythonPath = "powershell.exe"

Write-Host "Setting up Scheduled Task: $TaskName"
Write-Host "Script to run: $ScriptPath"

# Check if task exists and unregister it if so (to allow updating)
$TaskExists = Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue
if ($TaskExists) {
    Write-Host "Removing existing task..."
    Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false
}

# Define the Action (Run PowerShell with the script)
# -ExecutionPolicy Bypass allows the script to run even if policies are restrictive
# -WindowStyle Hidden keeps it from popping up a window every hour
$Action = New-ScheduledTaskAction -Execute "powershell.exe" -Argument "-NoProfile -WindowStyle Hidden -ExecutionPolicy Bypass -File `"$ScriptPath`""

# Define the Trigger
# Begins NOW, repeats every 1 hour, for an indefinite duration (represented as a very long time)
$Trigger = New-ScheduledTaskTrigger -Once -At (Get-Date) -RepetitionInterval (New-TimeSpan -Hours 1) 

# Create and Register the Task
# -Settings argument ensures the task can run properly
$Settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable

# Register execution
try {
    Register-ScheduledTask -Action $Action -Trigger $Trigger -TaskName $TaskName -Description "Keeps Streamlit App Alive by pinging it every hour." -Settings $Settings
    Write-Host -ForegroundColor Green "Success! Task '$TaskName' has been scheduled."
    Write-Host "It will run every 1 hour. You can view it in Windows Task Scheduler."
    Write-Host "Logs will be saved to: $(Join-Path -Path $PSScriptRoot -ChildPath 'keep_alive_log.txt')"
}
catch {
    Write-Host -ForegroundColor Red "Error registering task. You might need to run this script as Administrator."
    Write-Host "Error Details: $_"
}
