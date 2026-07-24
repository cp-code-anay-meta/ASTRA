@echo off
setlocal EnableExtensions

title ASTRA COMPLETE SETUP

cd /d "%~dp0"

echo.
echo ==========================================
echo          ASTRA COMPLETE SETUP
echo ==========================================
echo.

REM ==========================================
REM 1. FIND PYTHON 3.11
REM ==========================================

echo [1/7] Checking Python 3.11...

set "PYTHON_EXE=%LocalAppData%\Programs\Python\Python311\python.exe"

if not exist "%PYTHON_EXE%" (
    echo Python 3.11 was not found.
    echo Downloading Python 3.11.9...

    powershell -NoProfile -ExecutionPolicy Bypass -Command "Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.11.9/python-3.11.9-amd64.exe' -OutFile '%TEMP%\python311.exe'"

    if not exist "%TEMP%\python311.exe" (
        echo ERROR: Python download failed.
        pause
        exit /b 1
    )

    echo Installing Python 3.11.9...

    "%TEMP%\python311.exe" /quiet InstallAllUsers=0 PrependPath=1 Include_test=0 Include_launcher=1

    if errorlevel 1 (
        echo ERROR: Python installation failed.
        pause
        exit /b 1
    )
)

if not exist "%PYTHON_EXE%" (
    echo ERROR: Python 3.11 was not found.
    pause
    exit /b 1
)

echo Python found:

"%PYTHON_EXE%" --version


REM ==========================================
REM 2. DELETE OLD BROKEN VENV
REM ==========================================

echo.
echo [2/7] Removing old virtual environment if needed...

if exist "%~dp0.venv" (
    echo Removing old .venv...
    rmdir /s /q "%~dp0.venv"
)

echo Old environment removed.


REM ==========================================
REM 3. CREATE NEW VENV
REM ==========================================

echo.
echo [3/7] Creating fresh virtual environment...

"%PYTHON_EXE%" -m venv "%~dp0.venv"

if errorlevel 1 (
    echo ERROR: Virtual environment creation failed.
    pause
    exit /b 1
)

set "VENV_PYTHON=%~dp0.venv\Scripts\python.exe"

if not exist "%VENV_PYTHON%" (
    echo ERROR: Virtual environment Python was not created.
    pause
    exit /b 1
)

echo Virtual environment created.

"%VENV_PYTHON%" --version


REM ==========================================
REM 4. INSTALL PIP USING PYTHON DIRECTLY
REM ==========================================

echo.
echo [4/7] Preparing pip...

"%VENV_PYTHON%" -m ensurepip --upgrade

if errorlevel 1 (
    echo ERROR: ensurepip failed.
    pause
    exit /b 1
)

"%VENV_PYTHON%" -m pip install --upgrade pip setuptools wheel

if errorlevel 1 (
    echo ERROR: pip setup failed.
    pause
    exit /b 1
)


REM ==========================================
REM 5. INSTALL DEPENDENCIES
REM ==========================================

echo.
echo [5/7] Installing Astra dependencies...

if not exist "%~dp0requirements.txt" (
    echo ERROR: requirements.txt is missing.
    pause
    exit /b 1
)

"%VENV_PYTHON%" -m pip install -r "%~dp0requirements.txt"

if errorlevel 1 (
    echo ERROR: Dependency installation failed.
    pause
    exit /b 1
)


REM ==========================================
REM 6. INSTALL OLLAMA
REM ==========================================

echo.
echo [6/7] Checking Ollama...

where ollama >nul 2>&1

if errorlevel 1 (
    echo Ollama not found.
    echo Please install Ollama separately from the official installer.
    echo.
    echo After installing Ollama, run this setup again.
    pause
    exit /b 1
)

echo Ollama found.

echo.
echo Downloading Gemma 3 1B...

ollama pull gemma3:1b

if errorlevel 1 (
    echo ERROR: Gemma download failed.
    pause
    exit /b 1
)


REM ==========================================
REM 7. TEST
REM ==========================================

echo.
echo [7/7] Testing Astra...

"%VENV_PYTHON%" -c "import streamlit; print('Streamlit OK')"

if errorlevel 1 exit /b 1

"%VENV_PYTHON%" -c "import ollama; print('Ollama Python OK')"

if errorlevel 1 exit /b 1

"%VENV_PYTHON%" -c "from kokoro import KPipeline; print('Kokoro OK')"

if errorlevel 1 exit /b 1

"%VENV_PYTHON%" -c "import soundfile; print('SoundFile OK')"

if errorlevel 1 exit /b 1

"%VENV_PYTHON%" -c "import sounddevice; print('SoundDevice OK')"

if errorlevel 1 exit /b 1

echo.
echo ==========================================
echo          ASTRA IS READY!
echo ==========================================
echo.

pause
