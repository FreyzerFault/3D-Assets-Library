@echo off
setlocal
cd /d "%~dp0"
python run_autopilot_loop.py
if errorlevel 1 (
    echo.
    echo El bucle de autopilot ha fallado.
    pause
    exit /b %errorlevel%
)

echo.
echo Bucle de autopilot finalizado.
pause
