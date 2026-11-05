@echo off
REM Pushes the local v1.0.4 tag to GitHub. Safe to run more than once.
cd /d "%~dp0.."
git push origin v1.0.4
echo.
pause
