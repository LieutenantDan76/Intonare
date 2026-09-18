@echo off
REM Intonare ship check — run from anywhere; resolves to repo root.
setlocal EnableDelayedExpansion
cd /d "%~dp0.."
set PYTHONIOENCODING=utf-8

if not exist Intonare.html (
  echo FATAL: Intonare.html not found in %CD%
  exit /b 1
)

REM Prefer real installs over the Windows Store stub (python.exe in WindowsApps).
set "PY="
where py >nul 2>&1 && for /f "delims=" %%i in ('py -3 -c "import sys; print(sys.executable)" 2^>nul') do set "PY=%%i"
if not defined PY if exist "%LocalAppData%\Programs\Python\Python312\python.exe" set "PY=%LocalAppData%\Programs\Python\Python312\python.exe"
if not defined PY if exist "%LocalAppData%\Programs\Python\Python313\python.exe" set "PY=%LocalAppData%\Programs\Python\Python313\python.exe"
if not defined PY (
  for /f "delims=" %%i in ('where python 2^>nul') do (
    echo %%i | find /i "WindowsApps" >nul
    if errorlevel 1 if not defined PY set "PY=%%i"
  )
)
if not defined PY (
  echo FATAL: Python 3 not found.
  echo Install Python 3 and/or disable App execution aliases for python.exe
  echo Settings - Apps - Advanced app settings - App execution aliases
  exit /b 1
)

echo ============================================================
echo  INTONARE SHIP CHECK
echo  cwd: %CD%
echo  python: %PY%
echo ============================================================

echo.
echo [1/3] HTML integrity (size / shrink-vs-HEAD / end tag / braces)...
"%PY%" tools\audits\intonare_html_integrity.py Intonare.html
if errorlevel 1 (
  echo.
  echo FAILED: HTML integrity. Do not ship. Restore Intonare.html from git.
  exit /b 1
)

echo.
echo [2/3] Regression sentinel...
"%PY%" tools\audits\intonare_regression_sentinel.py Intonare.html
if errorlevel 1 (
  echo.
  echo FAILED: sentinel. Do not ship.
  exit /b 1
)

echo.
echo [3/3] Changelog gate...
"%PY%" tools\audits\intonare_changelog_gate.py Intonare.html CHANGELOG.md
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
