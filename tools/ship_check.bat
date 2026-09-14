@echo off
REM Intonare ship check — run from anywhere; resolves to repo root.
setlocal
cd /d "%~dp0.."
set PYTHONIOENCODING=utf-8

if not exist Intonare.html (
  echo FATAL: Intonare.html not found in %CD%
  exit /b 1
)

where python >nul 2>&1
if errorlevel 1 (
  echo FATAL: python not on PATH. Install Python 3 and reopen the terminal.
  exit /b 1
)

echo ============================================================
echo  INTONARE SHIP CHECK
echo  cwd: %CD%
echo ============================================================

echo.
echo [1/2] Regression sentinel...
python tools\audits\intonare_regression_sentinel.py Intonare.html
if errorlevel 1 (
  echo.
  echo FAILED: sentinel. Do not ship.
  exit /b 1
)

echo.
echo [2/2] Changelog gate...
python tools\audits\intonare_changelog_gate.py Intonare.html CHANGELOG.md
if errorlevel 1 (
  echo.
  echo FAILED: changelog gate. Do not ship.
  exit /b 1
)

echo.
echo ============================================================
echo  SHIP CHECK PASSED.
echo  Still do: on-device verify, then go.bat / Codemagic as needed.
echo ============================================================
endlocal
exit /b 0
