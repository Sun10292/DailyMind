# DailyMind Windows 定时任务安装脚本
# 以管理员身份运行此脚本

$TaskName = "DailyMind"
$ScriptPath = "$PSScriptRoot\main.py"
$PythonPath = (Get-Command python).Source

if (-not $PythonPath) {
    $PythonPath = (Get-Command python3).Source
}

if (-not $PythonPath) {
    Write-Host "ERROR: Cannot find Python, please make sure Python is installed and added to PATH" -ForegroundColor Red
    exit 1
}

Write-Host "Found Python: $PythonPath" -ForegroundColor Cyan
Write-Host "Script path: $ScriptPath" -ForegroundColor Cyan

if (-not (Test-Path $ScriptPath)) {
    Write-Host "ERROR: Cannot find main.py" -ForegroundColor Red
    exit 1
}

$Action = New-ScheduledTaskAction -Execute $PythonPath -Argument "`"$ScriptPath`"" -WorkingDirectory "$PSScriptRoot"
$Trigger = New-ScheduledTaskTrigger -Daily -At "20:00"
$Principal = New-ScheduledTaskPrincipal -UserId "INTERACTIVE" -LogonType Interactive -RunLevel Limited

try {
    Register-ScheduledTask -TaskName $TaskName -Action $Action -Trigger $Trigger -Principal $Principal -Force
    Write-Host "SUCCESS: Scheduled task created! Runs daily at 20:00." -ForegroundColor Green
    Write-Host ""
    Write-Host "Task info:" -ForegroundColor Cyan
    Write-Host "  Name: $TaskName"
    Write-Host "  Time: 20:00 every day"
    Write-Host "  Script: $ScriptPath"
    Write-Host ""
    Write-Host "Commands:" -ForegroundColor Yellow
    Write-Host "  View task: Get-ScheduledTask -TaskName '$TaskName' | fl"
    Write-Host "  Run now: Start-ScheduledTask -TaskName '$TaskName'"
    Write-Host "  Delete: Unregister-ScheduledTask -TaskName '$TaskName' -Confirm:`$false"
}
catch {
    Write-Host "ERROR: Failed to create scheduled task: $_" -ForegroundColor Red
    Write-Host ""
    Write-Host "TIP: Run PowerShell as Administrator, then try again"
}