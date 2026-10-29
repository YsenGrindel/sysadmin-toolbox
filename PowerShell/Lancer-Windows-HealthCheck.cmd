@echo off
setlocal
title Windows HealthCheck
cd /d "%~dp0.."
echo.
echo ==============================================
echo   Windows HealthCheck - Diagnostic Windows
echo ==============================================
echo.
powershell.exe -NoProfile -File "%~dp0Windows-HealthCheck.ps1" -Language fr %*
set "EXITCODE=%ERRORLEVEL%"
echo.
if not "%EXITCODE%"=="0" (
    echo [ERREUR] Le script s'est termine avec le code %EXITCODE%.
    echo Ouvrez PowerShell dans ce dossier pour examiner le message.
) else (
    echo Diagnostic termine / Diagnostics completed.
)
echo.
echo Appuyez sur une touche pour fermer / Press any key to close.
pause >nul
exit /b %EXITCODE%
