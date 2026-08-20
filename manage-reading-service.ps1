# manage-reading-service.ps1
# 管理 ReadingService（运行 reading.py）的服务
# 用法: 右键 -> "以 PowerShell 运行"   （首次或改动后需"以管理员身份运行"）
#       .\manage-reading-service.ps1 install   # 安装/重新安装服务
#       .\manage-reading-service.ps1 start     # 启动服务
#       .\manage-reading-service.ps1 stop      # 停止服务
#       .\manage-reading-service.ps1 restart   # 重启服务
#       .\manage-reading-service.ps1 status    # 查看状态
#       .\manage-reading-service.ps1 logs      # 查看日志
#       .\manage-reading-service.ps1 remove    # 删除服务

param(
    [ValidateSet("install", "start", "stop", "restart", "status", "logs", "remove")]
    [string]$Action = "status"
)

$nssm = "C:\tools\nssm\nssm-2.24-101-g897c7ad\win64\nssm.exe"
$python = "C:\Users\Ray\Documents\Projects\prompts-skills\.venv\Scripts\python.exe"
$script = "C:\Users\Ray\Documents\Projects\prompts-skills\tools\reading.py"
$workDir = "C:\Users\Ray\Documents\Projects\prompts-skills"
$serviceName = "ReadingService"
$logDir = "$workDir\reading"
$stdoutLog = "$logDir\reading-service.log"
$stderrLog = "$logDir\reading-service-error.log"

# 确保日志目录存在
if (-not (Test-Path $logDir)) { New-Item -ItemType Directory -Path $logDir -Force | Out-Null }

switch ($Action) {
    "install" {
        Write-Host "=== 安装/重新安装 ReadingService ==="
        # 如果已存在，先删除
        $existing = & $nssm status $serviceName 2>$null
        if ($LASTEXITCODE -eq 0) {
            & $nssm stop $serviceName 2>$null
            & $nssm remove $serviceName confirm 2>$null
            Start-Sleep -Seconds 1
        }
        # 安装服务
        & $nssm install $serviceName $python $script
        if ($LASTEXITCODE -ne 0) { Write-Host "安装失败"; exit 1 }
        # 配置参数
        & $nssm set $serviceName AppDirectory $workDir
        & $nssm set $serviceName Description "Browser reading workflow HTTP server (reading.py)"
        & $nssm set $serviceName AppStdout $stdoutLog
        & $nssm set $serviceName AppStderr $stderrLog
        & $nssm set $serviceName AppRestartDelay 2000
        & $nssm set $serviceName AppExit Default Exit
        Write-Host "服务已安装。运行以下命令启动："
        Write-Host "  .\manage-reading-service.ps1 start"
    }
    "start" {
        Write-Host "=== 启动 ReadingService ==="
        & $nssm start $serviceName
        if ($LASTEXITCODE -eq 0) {
            Write-Host "服务已启动。访问 http://127.0.0.1:8009/"
        } else {
            Write-Host "启动失败，请检查是否有管理员权限"
        }
    }
    "stop" {
        Write-Host "=== 停止 ReadingService ==="
        & $nssm stop $serviceName
    }
    "restart" {
        Write-Host "=== 重启 ReadingService ==="
        & $nssm restart $serviceName
    }
    "status" {
        Write-Host "=== ReadingService 状态 ==="
        $status = & $nssm status $serviceName 2>$null
        if ($LASTEXITCODE -eq 0) {
            Write-Host "状态: $status"
        } else {
            Write-Host "服务未安装或无法访问（需要管理员权限）"
        }
        Get-Service $serviceName -ErrorAction SilentlyContinue | Format-Table Name, Status, StartType -AutoSize
        Write-Host "--- 当前指向 ---"
        Get-ItemProperty "HKLM:\SYSTEM\CurrentControlSet\Services\$serviceName\Parameters" -ErrorAction SilentlyContinue | Format-List Application, AppParameters
    }
    "logs" {
        Write-Host "=== 查看日志（最近 30 行）==="
        $logFile = $stdoutLog
        $errLog = $stderrLog
        if (Test-Path $logFile) {
            Write-Host "--- stdout ---"
            Get-Content $logFile -Tail 30
        } else {
            Write-Host "（无日志文件）"
        }
        if (Test-Path $errLog) {
            Write-Host "--- stderr ---"
            Get-Content $errLog -Tail 30
        }
    }
    "remove" {
        Write-Host "=== 删除 ReadingService ==="
        & $nssm stop $serviceName 2>$null
        Start-Sleep -Seconds 1
        & $nssm remove $serviceName confirm
    }
}