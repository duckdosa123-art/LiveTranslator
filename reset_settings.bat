@echo off
title Live Translator - Reset Settings
color 0A

echo ========================================
echo     Live Translator - Reset Settings
echo ========================================
echo.

if not exist "ear_settings.json" (
    echo     No settings file found.
    echo     Nothing to reset.
    echo.
    pause
    exit /b 0
)

echo     Current settings:
    type ear_settings.json
echo.
echo ========================================
echo.

set /p confirm="Are you sure you want to reset all settings? (y/n): "
if /i "%confirm%" neq "y" (
    echo.
    echo     Reset cancelled.
    pause
    exit /b 0
)

del ear_settings.json

echo.
echo ========================================
echo     Settings reset successfully!
echo ========================================
echo.
echo     Next time you run ear.py, it will ask for:
echo     - Model selection (if multiple models exist)
echo     - Audio device selection
echo     - Channel selection
echo.
echo     Run start.bat to launch the application.
echo.
pause
