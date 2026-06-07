# PowerShell Script to add StratumWeb Backend to Startup
$batPath = Join-Path $PSScriptRoot "run_backend.bat"
$startupPath = [System.IO.Path]::Combine([Environment]::GetFolderPath("Startup"), "StratumWebBackend.lnk")

if (Test-Path $batPath) {
    $WshShell = New-Object -ComObject WScript.Shell
    $Shortcut = $WshShell.CreateShortcut($startupPath)
    $Shortcut.TargetPath = "wscript.exe"
    $Shortcut.Arguments = "`"$(Join-Path $PSScriptRoot "run_hidden.vbs")`""
    $Shortcut.WorkingDirectory = $PSScriptRoot
    $Shortcut.WindowStyle = 7 # Minimized/Hidden context
    $Shortcut.Save()
    
    Write-Host "Success! StratumWeb Backend is now set to run 'all the time' in the background." -ForegroundColor Green
    Write-Host "The shortcut was created at: $startupPath"
    
    # Run it now if it's not already running
    Start-Process "wscript.exe" -ArgumentList "`"$(Join-Path $PSScriptRoot "run_hidden.vbs")`"" -WorkingDirectory $PSScriptRoot
} else {
    Write-Host "Error: run_backend.bat not found." -ForegroundColor Red
}
