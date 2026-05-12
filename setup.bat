@echo off
REM hooliGAN-harness Quick Setup Script for Windows
REM Uses uv for fast Python dependency management

setlocal enabledelayedexpansion

echo.
echo ╔══════════════════════════════════════════════╗
echo ║        hooliGAN-harness Installer           ║
echo ║              Version 1.3.0                  ║
echo ╚══════════════════════════════════════════════╝
echo.

REM Check for Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python 3 is required but not installed.
    echo Please install Python 3.8 or higher from python.org
    pause
    exit /b 1
)

echo ✓ Python detected

REM Check for uv
where uv >nul 2>&1
if errorlevel 1 (
    echo 📦 Installing uv (fast Python package manager)...
    powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

    REM Check if uv was installed
    where uv >nul 2>&1
    if errorlevel 1 (
        echo ❌ Failed to install uv
        echo Please install manually from: https://github.com/astral-sh/uv
        pause
        exit /b 1
    )
)

echo ✓ uv is installed

REM Create virtual environment
echo 🔧 Setting up virtual environment...
uv venv .venv --python python

REM Activate virtual environment
if exist ".venv\Scripts\activate.bat" (
    call .venv\Scripts\activate.bat
) else (
    echo ❌ Failed to create virtual environment
    pause
    exit /b 1
)

REM Install dependencies
echo 📦 Installing dependencies with uv...
uv pip install rich

REM Run the installer
echo 🚀 Launching hooliGAN-harness installer...
echo.
python install.py

REM Deactivate virtual environment
call deactivate

echo.
echo ✨ Setup complete!
echo To reinstall or uninstall later, run: setup.bat
pause