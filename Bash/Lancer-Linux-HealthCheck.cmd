@echo off
setlocal
title Linux HealthCheck (WSL)
echo === Linux HealthCheck ===
echo Le controle sera lance dans votre distribution WSL par defaut.
echo.
where wsl.exe >nul 2>&1
if errorlevel 1 (
  echo WSL absent. Installer WSL et une distribution Linux.
  set "RESULT=2"
  goto finished
)
wsl.exe --exec bash -s < "%~dp0linux-healthcheck.sh"
set "RESULT=%ERRORLEVEL%"
:finished
echo.
echo Fin du controle / Finished. Code: %RESULT%
echo Pour un Linux natif : bash linux-healthcheck.sh
echo Appuyez sur une touche pour fermer / Press any key to close.
pause >nul
exit /b %RESULT%
