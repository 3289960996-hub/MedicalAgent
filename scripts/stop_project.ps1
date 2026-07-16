$ErrorActionPreference = "Stop"
$ProjectRoot = [System.IO.Path]::GetFullPath((Join-Path $PSScriptRoot ".."))
$RuntimeFile = Join-Path $ProjectRoot ".runtime\services.json"

if (-not (Test-Path -LiteralPath $RuntimeFile)) {
    Write-Host "No services managed by this project were found."
    exit 0
}

$runtime = Get-Content -LiteralPath $RuntimeFile -Raw -Encoding UTF8 | ConvertFrom-Json
$runtimeRoot = [System.IO.Path]::GetFullPath([string]$runtime.projectRoot)
if ($runtimeRoot -ne $ProjectRoot) {
    throw "The runtime record belongs to another project. No process was stopped."
}

foreach ($service in @(
    @{ Name = "Backend"; Pid = [int]$runtime.backendPid; Tokens = @("backend.app:app", "--port 8000") },
    @{ Name = "Frontend"; Pid = [int]$runtime.frontendPid; Tokens = @("http.server 8080", (Join-Path $ProjectRoot "frontend")) }
)) {
    $process = Get-CimInstance Win32_Process -Filter "ProcessId=$($service.Pid)" -ErrorAction SilentlyContinue
    if (-not $process) { continue }
    $commandLine = ([string]$process.CommandLine).ToLowerInvariant()
    $hasExpectedCommand = [string]$process.Name -eq "python.exe"
    foreach ($token in $service.Tokens) {
        $hasExpectedCommand = $hasExpectedCommand -and $commandLine.Contains(([string]$token).ToLowerInvariant())
    }
    if (-not $hasExpectedCommand) {
        Write-Warning "$($service.Name) PID was reused by another process. It was not stopped."
        continue
    }
    & taskkill.exe /PID $service.Pid /T /F | Out-Null
    if ($LASTEXITCODE -ne 0) {
        Write-Warning "$($service.Name) process tree could not be stopped. Check PID $($service.Pid)."
        continue
    }
    Write-Host "$($service.Name) stopped."
}

Remove-Item -LiteralPath $RuntimeFile -Force -ErrorAction SilentlyContinue
