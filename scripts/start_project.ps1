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

function Wait-ForUrl([string]$Url, [string]$Name) {
    for ($attempt = 1; $attempt -le 40; $attempt++) {
        try {
            Invoke-WebRequest -Uri $Url -UseBasicParsing -TimeoutSec 2 | Out-Null
            return
        } catch {
            Start-Sleep -Milliseconds 500
        }
    }
    throw "$Name 启动后未能通过健康检查：$Url"
}

if (-not (Test-Path -LiteralPath $Python)) {
    throw "未找到当前项目虚拟环境：$Python"
}

foreach ($port in 8000, 8080) {
    $ownerPid = Get-ListeningPid $port
    if ($ownerPid) {
        throw "端口 $port 已被占用：$(Describe-Process $ownerPid)。请先运行 stop_project.ps1，或关闭占用程序后重试。"
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

    Wait-ForUrl "http://127.0.0.1:8000/" "后端"
    Wait-ForUrl "http://127.0.0.1:8080/" "前端"

    [PSCustomObject]@{
        projectRoot = $ProjectRoot
        backendPid = $backend.Id
        frontendPid = $frontend.Id
        startedAt = (Get-Date).ToString("o")
    } | ConvertTo-Json | Set-Content -LiteralPath $RuntimeFile -Encoding UTF8

    Write-Host "MedicalAgent 已从当前项目目录启动。" -ForegroundColor Green
    Write-Host "前端：http://127.0.0.1:8080/"
    Write-Host "接口文档：http://127.0.0.1:8000/docs"
} catch {
    if ($backend -and -not $backend.HasExited) { Stop-Process -Id $backend.Id -Force -ErrorAction SilentlyContinue }
    if ($frontend -and -not $frontend.HasExited) { Stop-Process -Id $frontend.Id -Force -ErrorAction SilentlyContinue }
    throw
}
