@echo off
setlocal
cd /d "%~dp0"
python run_automation.py
if errorlevel 1 (
    echo.
    echo La automatizacion ha fallado.
    pause
    exit /b %errorlevel%
)

echo.
echo Automatizacion completada correctamente.
pause
