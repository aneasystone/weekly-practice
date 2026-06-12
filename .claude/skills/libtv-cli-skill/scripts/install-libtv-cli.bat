@echo off
setlocal EnableExtensions

set "SCRIPT_DIR=%~dp0"
set "LOCAL_PS1=%SCRIPT_DIR%install-libtv-cli.ps1"

if not exist "%LOCAL_PS1%" goto download_remote

powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%LOCAL_PS1%" %*
exit /b %ERRORLEVEL%

:download_remote

set "REMOTE_PS1=https://liblibai-web-static.liblib.cloud/cli/latest/install-libtv-cli.ps1"
set "TEMP_PS1=%TEMP%\install-libtv-cli-%RANDOM%%RANDOM%.ps1"

powershell.exe -NoProfile -ExecutionPolicy Bypass -Command "try { [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; Invoke-WebRequest -Uri $env:REMOTE_PS1 -UseBasicParsing -OutFile $env:TEMP_PS1; $text = [IO.File]::ReadAllText($env:TEMP_PS1, [Text.Encoding]::UTF8); [IO.File]::WriteAllText($env:TEMP_PS1, $text, [Text.Encoding]::UTF8) } catch { Write-Error $_; exit 1 }"
if errorlevel 1 exit /b %ERRORLEVEL%

powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%TEMP_PS1%" %*
set "EXIT_CODE=%ERRORLEVEL%"
del "%TEMP_PS1%" >nul 2>nul
exit /b %EXIT_CODE%
