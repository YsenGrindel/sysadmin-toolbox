@echo off
setlocal
title Security Baseline Checker
echo === Security Baseline Checker / Controle de securite ===
echo Lecture seule - indicateurs non exhaustifs.
echo.
powershell.exe -NoProfile -File "%~dp0Security-BaselineChecker.ps1"
set "RESULT=%ERRORLEVEL%"
echo.
echo Termine, code de retour: %RESULT%
if not "%RESULT%"=="0" echo Le script a signale une erreur; verifier les lignes ci-dessus.
echo Appuyez sur une touche pour fermer / Press any key to close.
pause >nul
exit /b %RESULT%
