$ErrorActionPreference = "Stop"
$ProjectRoot = [System.IO.Path]::GetFullPath((Join-Path $PSScriptRoot ".."))
$Python = Join-Path $ProjectRoot ".venv\Scripts\python.exe"
$RuntimeDir = Join-Path $ProjectRoot ".runtime"
$LogDir = Join-Path $ProjectRoot "logs"
$RuntimeFile = Join-Path $RuntimeDir "services.json"

function Get-ListeningPid([int]$Port) {
    $pattern = ":$Port\s+\S+\s+LISTENING\s+(\d+)\s*$"
    foreach ($line in (& netstat.exe -ano -p tcp)) {
        if ($line -match $pattern) { return [int]$Matches[1] }
    }
    return $null
}

function Describe-Process([int]$ProcessId) {
    try {
        $process = Get-CimInstance Win32_Process -Filter "ProcessId=$ProcessId"
        return "$($process.Name) $($process.CommandLine)"
    } catch {
        return "PID $ProcessId"
    }
}

function Test-ManagedService([int]$ProcessId, [string]$ServiceName) {
    try {
        $process = Get-CimInstance Win32_Process -Filter "ProcessId=$ProcessId" -ErrorAction Stop
        $commandLine = ([string]$process.CommandLine).ToLowerInvariant()
        if ([string]$process.Name -ne "python.exe") { return $false }
        if ($ServiceName -eq "backend") {
            return $commandLine.Contains("backend.app:app") -and $commandLine.Contains("--port 8000")
        }
        $frontendPath = (Join-Path $ProjectRoot "frontend").ToLowerInvariant()
        return $commandLine.Contains("http.server 8080") -and $commandLine.Contains($frontendPath)
    } catch {
        return $false
    }
}

function Wait-ForUrl([string]$Url, [string]$Name) {
    for ($attempt = 1; $attempt -le 40; $attempt++) {
        try {
            Invoke-WebRequest -Uri $Url -UseBasicParsing -TimeoutSec 2 | Out-Null
            return
        } catch {
            Start-Sleep -Milliseconds 500
        }
    }
    throw "$Name failed its startup health check: $Url"
}

if (-not (Test-Path -LiteralPath $Python)) {
    throw "Project virtual environment not found: $Python"
}

$mysqlBootstrap = Join-Path $PSScriptRoot "ensure_mysql.ps1"
if (Test-Path -LiteralPath $mysqlBootstrap) {
    & $mysqlBootstrap
}

$backendOwnerPid = Get-ListeningPid 8000
$frontendOwnerPid = Get-ListeningPid 8080
if ($backendOwnerPid -and $frontendOwnerPid -and (Test-Path -LiteralPath $RuntimeFile)) {
    try {
        $runtime = Get-Content -LiteralPath $RuntimeFile -Raw -Encoding UTF8 | ConvertFrom-Json
        $runtimeRoot = [System.IO.Path]::GetFullPath([string]$runtime.projectRoot)
        $isCurrentProject = $runtimeRoot -eq $ProjectRoot `
            -and [int]$runtime.backendPid -eq $backendOwnerPid `
            -and [int]$runtime.frontendPid -eq $frontendOwnerPid `
            -and (Test-ManagedService $backendOwnerPid "backend") `
            -and (Test-ManagedService $frontendOwnerPid "frontend")
        if ($isCurrentProject) {
            Write-Host "MedicalAgent is already running." -ForegroundColor Green
            Write-Host "Frontend: http://127.0.0.1:8080/"
            Write-Host "API docs: http://127.0.0.1:8000/docs"
            exit 0
        }
    } catch {
        # A damaged runtime record must not take ownership of unknown processes.
    }
}

foreach ($port in 8000, 8080) {
    $ownerPid = Get-ListeningPid $port
    if ($ownerPid) {
        throw "Port $port is already in use by $(Describe-Process $ownerPid). Run stop_project.ps1 or close that process before retrying."
    }
}

New-Item -ItemType Directory -Path $RuntimeDir -Force | Out-Null
New-Item -ItemType Directory -Path $LogDir -Force | Out-Null

$backend = $null
$frontend = $null
try {
    $backendArgs = @("-m", "uvicorn", "backend.app:app", "--host", "127.0.0.1", "--port", "8000")
    $frontendArgs = @("-m", "http.server", "8080", "--bind", "127.0.0.1", "--directory", (Join-Path $ProjectRoot "frontend"))
    $backend = Start-Process -FilePath $Python `
        -ArgumentList $backendArgs `
        -WorkingDirectory $ProjectRoot -WindowStyle Hidden -PassThru `
        -RedirectStandardOutput (Join-Path $LogDir "backend.out.log") `
        -RedirectStandardError (Join-Path $LogDir "backend.err.log")

    $frontend = Start-Process -FilePath $Python `
        -ArgumentList $frontendArgs `
        -WorkingDirectory $ProjectRoot -WindowStyle Hidden -PassThru `
        -RedirectStandardOutput (Join-Path $LogDir "frontend.out.log") `
        -RedirectStandardError (Join-Path $LogDir "frontend.err.log")

    Wait-ForUrl "http://127.0.0.1:8000/" "Backend"
    Wait-ForUrl "http://127.0.0.1:8080/" "Frontend"

    $backendListenerPid = Get-ListeningPid 8000
    $frontendListenerPid = Get-ListeningPid 8080
    if (-not $backendListenerPid -or -not (Test-ManagedService $backendListenerPid "backend")) {
        throw "Backend responded, but its listening process could not be verified as part of this project."
    }
    if (-not $frontendListenerPid -or -not (Test-ManagedService $frontendListenerPid "frontend")) {
        throw "Frontend responded, but its listening process could not be verified as part of this project."
    }

    [PSCustomObject]@{
        projectRoot = $ProjectRoot
        backendPid = $backendListenerPid
        frontendPid = $frontendListenerPid
        startedAt = (Get-Date).ToString("o")
    } | ConvertTo-Json | Set-Content -LiteralPath $RuntimeFile -Encoding UTF8

    Write-Host "MedicalAgent started from the current project directory." -ForegroundColor Green
    Write-Host "Frontend: http://127.0.0.1:8080/"
    Write-Host "API docs: http://127.0.0.1:8000/docs"
} catch {
    $backendListenerPid = Get-ListeningPid 8000
    $frontendListenerPid = Get-ListeningPid 8080
    if ($backendListenerPid -and (Test-ManagedService $backendListenerPid "backend")) {
        & taskkill.exe /PID $backendListenerPid /T /F | Out-Null
    }
    if ($frontendListenerPid -and (Test-ManagedService $frontendListenerPid "frontend")) {
        & taskkill.exe /PID $frontendListenerPid /T /F | Out-Null
    }
    if ($backend -and -not $backend.HasExited) { Stop-Process -Id $backend.Id -Force -ErrorAction SilentlyContinue }
    if ($frontend -and -not $frontend.HasExited) { Stop-Process -Id $frontend.Id -Force -ErrorAction SilentlyContinue }
    throw
}
