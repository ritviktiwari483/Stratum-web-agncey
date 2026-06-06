# PowerShell Script to add StratumWeb Backend to Startup
$vbsPath = Join-Path $PSScriptRoot "run_hidden.vbs"
$startupPath = [System.IO.Path]::Combine([Environment]::GetFolderPath("Startup"), "StratumWebBackend.vbs")

if (Test-Path $vbsPath) {
    Copy-Item -Path $vbsPath -Destination $startupPath -Force
    Write-Host "Success! StratumWeb Backend will now run automatically on startup." -ForegroundColor Green
    Write-Host "You can find the shortcut here: $startupPath"
} else {
    Write-Host "Error: run_hidden.vbs not found in the current directory." -ForegroundColor Red
}
