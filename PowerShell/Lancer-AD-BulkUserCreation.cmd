@echo off
setlocal
title AD Bulk User Creation - SIMULATION
echo === Active Directory - simulation uniquement ===
echo Aucune creation de compte ne sera effectuee par ce lanceur.
echo.
set "CSV=%~dp0..\examples\ad-users.example.csv"
if not exist "%CSV%" set "CSV=%~dp0ad-users.example.csv"
if not exist "%CSV%" (
  echo Fichier CSV manquant. Laisser le .csv et le .cmd dans le meme dossier,
  echo ou telecharger tout le depot depuis GitHub.
  set "RESULT=2"
  goto end
)
powershell.exe -NoProfile -File "%~dp0AD-BulkUserCreation.ps1" -CsvPath "%CSV%"
set "RESULT=%ERRORLEVEL%"
:end
echo.
echo Simulation terminee / Simulation finished. Code: %RESULT%
echo Appuyez sur une touche pour fermer / Press any key to close.
pause >nul
exit /b %RESULT%
