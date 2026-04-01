@echo off
title Live Translator - Installer
color 0A

:check_python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ========================================
    echo     ERROR: Python is not installed!
    echo ========================================
    echo.
    echo Please install Python 3.10+ from:
    echo https://www.python.org/downloads/
    echo.
    echo Make sure to check "Add Python to PATH" during installation.
    echo.
    set /p install_now="Would you like to open the download page? (y/n): "
    if /i "%install_now%"=="y" start https://www.python.org/downloads/
    echo.
    echo After installing Python, run this script again.
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VER=%%i
echo     Python %PYTHON_VER% found

:check_node
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ========================================
    echo     ERROR: Node.js is not installed!
    echo ========================================
    echo.
    echo Please install Node.js 18+ from:
    echo https://nodejs.org/
    echo.
    set /p install_now="Would you like to open the download page? (y/n): "
    if /i "%install_now%"=="y" start https://nodejs.org/
    echo.
    echo After installing Node.js, run this script again.
    pause
    exit /b 1
)

for /f "tokens=1" %%i in ('node --version') do set NODE_VER=%%i
echo     Node.js %NODE_VER% found

:start_services
title Live Translator Launcher
color 0A

echo.
echo ========================================
echo     Live Translator - One Click Start
echo ========================================
echo.

echo [1/6] Node.js dependencies...
if not exist "node_modules" (
    echo     Installing npm packages...
    call npm install
    if %errorlevel% neq 0 (
        echo     ERROR: npm install failed!
        pause
        exit /b 1
    )
) else (
    echo     Already installed - skipping
)

echo.
echo [2/6] Python virtual environment...
if not exist "venv\Scripts\python.exe" (
    echo     Creating virtual environment...
    python -m venv venv
    if %errorlevel% neq 0 (
        echo     ERROR: Failed to create venv!
        pause
        exit /b 1
    )
) else (
    echo     Already exists - skipping
)

echo.
echo [3/6] Python packages...
call venv\Scripts\pip install -r requirements.txt --quiet --disable-pip-version-check
if %errorlevel% neq 0 (
    echo     ERROR: pip install failed!
    pause
    exit /b 1
)

echo.
echo [4/6] Verifying Python packages...
call venv\Scripts\python -c "import faster_whisper, sounddevice, socketio, numpy, scipy" 2>nul
if %errorlevel% neq 0 (
    echo     WARNING: Some packages may not be installed correctly.
    echo     Retrying installation...
    call venv\Scripts\pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo     ERROR: Package verification failed!
        pause
        exit /b 1
    )
) else (
    echo     All packages verified
)

echo.
echo [5/6] Whisper model...
call :choose_model
if %errorlevel% neq 0 (
    echo     ERROR: Model setup failed!
    pause
    exit /b 1
)

echo.
echo [6/6] Starting services...
goto :start_services_now

:choose_model
echo.
echo     Choose your Whisper model:
echo.
echo     [1] tiny      - 17 MB   (fastest, lower accuracy)
echo     [2] small     - 70 MB   (recommended - balance)  ^<^&lt; Pre-installed with repo
echo     [3] medium    - 300 MB  (slower, higher accuracy)
echo     [4] large-v2  - 1.5 GB  (slowest, highest accuracy)
echo     [5] large-v3  - 1.5 GB  (slowest, highest accuracy)
echo.
set /p choice="Enter choice (1-5) or press Enter for [2] small: "
if "%choice%"=="" set choice=2
if "%choice%"=="1" set "MODEL_SELECTED=tiny"
if "%choice%"=="2" set "MODEL_SELECTED=small"
if "%choice%"=="3" set "MODEL_SELECTED=medium"
if "%choice%"=="4" set "MODEL_SELECTED=large-v2"
if "%choice%"=="5" set "MODEL_SELECTED=large-v3"
if "%MODEL_SELECTED%"=="" set "MODEL_SELECTED=small"

if exist "models\%MODEL_SELECTED%\*" (
    echo.
    echo     Using pre-installed %MODEL_SELECTED% model (no download needed)
    exit /b 0
)

echo.
echo     Downloading %MODEL_SELECTED% model...
echo     (This may take several minutes on first run)
call venv\Scripts\python download_model.py %MODEL_SELECTED%
if %errorlevel% neq 0 (
    echo     ERROR: Model download failed!
    exit /b 1
)
echo     Model downloaded successfully!
exit /b 0

:start_services_now

echo.
echo ========================================
echo     All Checks Passed!
echo ========================================
echo.
echo [Bridge] Socket.io server on port 5050
echo [Web]    Overlay on port 8080
echo [Ear]    Speech recognition
echo.
echo ========================================
echo.
echo Starting services...
echo.
echo Add http://localhost:8080 as an OBS Browser Source
echo.

start "Live Translator - Bridge" cmd /k "title Bridge && npm start"
timeout /t 2 >nul
start "Live Translator - Ear" cmd /k "title Ear && venv\Scripts\python ear.py"

pause
