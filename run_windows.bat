@echo off
cd /d "%~dp0"
title SpecCheck AI

if exist ".venv\Scripts\python.exe" goto install
echo Setting up SpecCheck AI. The first run takes a few minutes...
py -3 -m venv .venv
if exist ".venv\Scripts\python.exe" goto install
python -m venv .venv
if exist ".venv\Scripts\python.exe" goto install
echo.
echo Python was not found. Install Python 3.11 or newer from python.org, then try again.
pause
exit /b 1

:install
".venv\Scripts\python.exe" -m pip install --quiet --disable-pip-version-check -r requirements.txt
if errorlevel 1 (
    echo.
    echo The install failed. Send the error message above for help.
    pause
    exit /b 1
)

echo Starting SpecCheck AI. Keep this window open while you use the app.
".venv\Scripts\python.exe" -m streamlit run app.py
pause
