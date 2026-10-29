@echo off
setlocal
title SysAdmin Toolbox - Menu
:menu
cls
echo ==========================================
echo        SYSADMIN TOOLBOX - MENU
echo ==========================================
echo.
echo  [1] Windows HealthCheck
echo  [2] Security Baseline Checker
echo  [3] AD Bulk User Creation (SIMULATION)
echo  [4] Network Doctor (Python 3)
echo  [5] Linux HealthCheck (WSL)
echo  [Q] Quitter / Exit
echo.
choice /C 12345Q /N /M "Votre choix / Your choice: "
if errorlevel 6 goto finish
if errorlevel 5 call "%~dp0Bash\Lancer-Linux-HealthCheck.cmd" & goto menu
if errorlevel 4 call "%~dp0Python\Lancer-Network-Doctor.cmd" & goto menu
if errorlevel 3 call "%~dp0PowerShell\Lancer-AD-BulkUserCreation.cmd" & goto menu
if errorlevel 2 call "%~dp0PowerShell\Lancer-Security-BaselineChecker.cmd" & goto menu
if errorlevel 1 call "%~dp0PowerShell\Lancer-Windows-HealthCheck.cmd" & goto menu
:finish
exit /b 0
