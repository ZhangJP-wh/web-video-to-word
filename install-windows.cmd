@echo off
cd /d "%~dp0"
powershell.exe -NoProfile -File "%~dp0install-windows.ps1" -Open %*
set "install_result=%errorlevel%"
if not "%install_result%"=="0" echo Installation failed. See README: Windows manual fallback. Do not disable security or execution policy.
pause
exit /b %install_result%
