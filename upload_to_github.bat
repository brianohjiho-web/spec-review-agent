@echo off
cd /d "%~dp0"
title Upload SpecCheck AI to GitHub

where git >nul 2>nul
if errorlevel 1 (
    echo Git was not found. Install it from https://git-scm.com/download/win, then try again.
    pause
    exit /b 1
)

echo First create an empty GitHub repo named spec-review-agent.
echo.
set /p GHUSER=Your GitHub username: 
set /p GHMAIL=Your GitHub email: 

if not exist ".git" git init
git config user.name "Brian Oh"
git config user.email "%GHMAIL%"
git add .

git ls-files --error-unmatch .env >nul 2>nul
if not errorlevel 1 (
    echo.
    echo STOPPED: your .env file was about to be uploaded. Nothing was pushed.
    pause
    exit /b 1
)

git diff --cached --quiet
if errorlevel 1 git commit -m "Add SpecCheck AI"

git branch -M main
git remote get-url origin >nul 2>nul
if errorlevel 1 git remote add origin https://github.com/%GHUSER%/spec-review-agent.git

git push -u origin main
if errorlevel 1 (
    echo.
    echo The upload failed. Send the message above for help.
    pause
    exit /b 1
)

echo.
echo Done: https://github.com/%GHUSER%/spec-review-agent
pause
