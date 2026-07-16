$ErrorActionPreference = "Stop"

function Ensure-OptionalMySqlService {
    try {
        $configuredName = [string]$env:MYSQL_SERVICE_NAME
        if ($configuredName) {
            $service = Get-Service -Name $configuredName -ErrorAction SilentlyContinue
            if (-not $service) {
                Write-Warning "Configured MySQL service '$configuredName' was not found. Project startup will continue with built-in data."
                return
            }
        } else {
            $candidates = @(Get-Service | Where-Object {
                $_.Name -match "(?i)mysql|mariadb" -or $_.DisplayName -match "(?i)mysql|mariadb"
            })

            if ($candidates.Count -eq 0) {
                Write-Host "MySQL service was not found. Project startup will continue with built-in data." -ForegroundColor Yellow
                return
            }

            $running = @($candidates | Where-Object Status -eq "Running")
            if ($running.Count -gt 0) {
                $service = $running | Sort-Object Name | Select-Object -First 1
            } elseif ($candidates.Count -eq 1) {
                $service = $candidates[0]
            } else {
                $names = ($candidates | Sort-Object Name | ForEach-Object Name) -join ", "
                Write-Warning "Multiple stopped MySQL services were found ($names). Set MYSQL_SERVICE_NAME to select one. Project startup will continue with built-in data."
                return
            }
        }

        if ($service.Status -eq "Running") {
            Write-Host "MySQL service '$($service.Name)' is already running." -ForegroundColor Green
            return
        }

        Write-Host "Starting optional MySQL service '$($service.Name)'..."
        Start-Service -Name $service.Name -ErrorAction Stop
        $service.WaitForStatus("Running", [TimeSpan]::FromSeconds(15))
        Write-Host "MySQL service '$($service.Name)' started." -ForegroundColor Green
    } catch {
        Write-Warning "MySQL could not be started automatically: $($_.Exception.Message) Project startup will continue with built-in data."
    }
}

Ensure-OptionalMySqlService
