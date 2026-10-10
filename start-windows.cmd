@echo off
cd /d "%~dp0"
powershell.exe -NoProfile -File "%~dp0install-windows.ps1" -StartOnly -Open %*
set "install_result=%errorlevel%"
if not "%install_result%"=="0" pause
exit /b %install_result%
