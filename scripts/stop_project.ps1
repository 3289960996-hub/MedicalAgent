$ErrorActionPreference = "Stop"
$ProjectRoot = [System.IO.Path]::GetFullPath((Join-Path $PSScriptRoot ".."))
$RuntimeFile = Join-Path $ProjectRoot ".runtime\services.json"
$ExpectedPython = (Join-Path $ProjectRoot ".venv\Scripts\python.exe").ToLowerInvariant()

if (-not (Test-Path -LiteralPath $RuntimeFile)) {
    Write-Host "没有找到由当前项目启动脚本管理的服务记录。"
    exit 0
}

$runtime = Get-Content -LiteralPath $RuntimeFile -Raw -Encoding UTF8 | ConvertFrom-Json
foreach ($service in @(
    @{ Name = "后端"; Pid = [int]$runtime.backendPid; Token = "uvicorn" },
    @{ Name = "前端"; Pid = [int]$runtime.frontendPid; Token = "http.server" }
)) {
    $process = Get-CimInstance Win32_Process -Filter "ProcessId=$($service.Pid)" -ErrorAction SilentlyContinue
    if (-not $process) { continue }
    $executable = [string]$process.ExecutablePath
    $commandLine = [string]$process.CommandLine
    if ($executable.ToLowerInvariant() -ne $ExpectedPython -or $commandLine -notlike "*$($service.Token)*") {
        Write-Warning "$($service.Name)记录的 PID 已被其他程序复用，未停止该进程。"
        continue
    }
    & taskkill.exe /PID $service.Pid /T /F | Out-Null
    if ($LASTEXITCODE -ne 0) {
        Write-Warning "$($service.Name)进程树停止失败，请检查PID $($service.Pid)。"
        continue
    }
    Write-Host "$($service.Name)已停止。"
}

Remove-Item -LiteralPath $RuntimeFile -Force -ErrorAction SilentlyContinue
