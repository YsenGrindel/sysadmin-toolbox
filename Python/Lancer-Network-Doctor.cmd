@echo off
setlocal
title Network Doctor - Diagnostic reseau
echo === Network Doctor ===
echo Tests de connectivite IP, TCP et DNS.
echo.
where py.exe >nul 2>&1
if not errorlevel 1 goto with_py
where python.exe >nul 2>&1
if not errorlevel 1 goto with_python
echo Python 3 introuvable. Installer Python 3 puis relancer.
set "RESULT=2"
goto finished
:with_py
py -3 "%~dp0network_doctor.py" %*
set "RESULT=%ERRORLEVEL%"
goto finished
:with_python
python "%~dp0network_doctor.py" %*
set "RESULT=%ERRORLEVEL%"
:finished
echo.
echo Fin du diagnostic / Finished. Code: %RESULT%
echo Code 1 peut simplement indiquer un test reseau echoue.
echo Appuyez sur une touche pour fermer / Press any key to close.
pause >nul
exit /b %RESULT%
