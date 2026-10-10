# Windows PowerShell 5.1+. Never changes execution policy or disables security.
param([switch]$NoStart, [switch]$StartOnly, [switch]$Open, [int]$Port = 8767)
$ErrorActionPreference = 'Stop'
$env:PYTHONUTF8 = '1'
Set-Location -LiteralPath $PSScriptRoot
function Refresh-Path {
    $env:Path = [Environment]::GetEnvironmentVariable('Path', 'User') + ';' + [Environment]::GetEnvironmentVariable('Path', 'Machine') + ';' + $env:Path
}
function Find-Python {
    $candidates = @("$env:LOCALAPPDATA\Programs\Python\Python312\python.exe", "$env:ProgramFiles\Python312\python.exe")
    $launcher = Get-Command py.exe -ErrorAction SilentlyContinue
    if ($launcher) {
        $found = $null
        try { $found = & $launcher.Source -3.12 -c 'import sys; print(sys.executable)' 2>$null } catch { $found = $null }
        if ($LASTEXITCODE -eq 0 -and $found) { $candidates = @($found) + $candidates }
    }
    $command = Get-Command python.exe -ErrorAction SilentlyContinue
    if ($command -and $command.Source -notlike '*WindowsApps*') { $candidates += $command.Source }
    foreach ($candidate in $candidates) {
        if (Test-Path -LiteralPath $candidate) {
            & $candidate -c 'import sys,platform; sys.exit(not (sys.version_info[:2]==(3,12) and sys.maxsize>2**32 and platform.machine().lower() in (''amd64'',''x86_64'')))' 2>$null
            if ($LASTEXITCODE -eq 0) { return $candidate }
        }
    }
    return $null
}
function Test-Node {
    $node = Get-Command node.exe -ErrorAction SilentlyContinue
    if (-not $node) { return $false }
    & $node.Source -e 'process.exit(process.arch === ''x64'' && Number(process.versions.node.split(''.'')[0]) >= 22 ? 0 : 1)'
    return ($LASTEXITCODE -eq 0)
}
function Install-Package([string]$Id, [string[]]$ExtraArgs) {
    if (-not (Get-Command winget.exe -ErrorAction SilentlyContinue)) {
        throw '缺少 WinGet。下一步：按 README 手动安装官方 Python 3.12 64位和 Node.js LTS x64，然后重跑入口。'
    }
    & winget.exe install --id $Id --exact --source winget --architecture x64 --accept-source-agreements --accept-package-agreements @ExtraArgs
    if ($LASTEXITCODE -ne 0) { throw "WinGet 安装 $Id 未完成。请按上方错误处理或使用 README 官方安装包，再重跑；系统授权由本人完成。" }
    Refresh-Path
}
try {
    if ([Environment]::OSVersion.Platform -ne 'Win32NT' -or [Environment]::OSVersion.Version.Build -lt 17763 -or $env:PROCESSOR_ARCHITECTURE -ne 'AMD64') {
        throw '需要 Windows 11 x64（或 Windows Server 2019+） 和64位 PowerShell。Windows ARM、32位和 WSL 尚不支持。'
    }
    $osInfo = Get-CimInstance Win32_OperatingSystem
    if ($osInfo.ProductType -eq 1 -and [Environment]::OSVersion.Version.Build -lt 22000) {
        throw '需要 Windows 11 x64；当前 Playwright 不正式支持 Windows 10，不能承诺自动安装。'
    }
    Refresh-Path
    $python = Find-Python
    if (-not $python) { Install-Package 'Python.Python.3.12' @('--scope', 'user'); $python = Find-Python }
    if (-not $python) { throw '下一步：重新打开终端后重跑入口；仍失败时安装 README 中的 Python 3.12 64位官方包。' }
    if (-not (Test-Node)) { Install-Package 'OpenJS.NodeJS.LTS' @() }
    if (-not (Test-Node)) { throw '下一步：重新打开终端再重跑；仍失败时安装 Node.js 22+ LTS x64 官方包。' }
    $installArgs = @('install.py', '--port', "$Port")
    if ($NoStart) { $installArgs += '--no-start' }
    if ($StartOnly) { $installArgs += '--start-only' }
    if ($Open) { $installArgs += '--open' }
    & $python @installArgs
    exit $LASTEXITCODE
} catch {
    Write-Host "未完成：$_" -ForegroundColor Red
    exit 1
}
