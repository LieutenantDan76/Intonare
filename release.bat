@echo off
REM ============================================================
REM  Intonare - Play Store release bump
REM  Run this ONLY when prepping a build to upload to Google Play.
REM  Do NOT run it for everyday device testing (that's go.bat).
REM
REM  USAGE on an upload day:
REM    1. Run go.bat first (does the normal build + restores)
REM    2. Then run release.bat (bumps the version)
REM    3. Then build the signed AAB in Android Studio and upload
REM ============================================================

setlocal enabledelayedexpansion

REM --- read current versionCode (default 1 if file missing or blank) ---
set "VCODE="
if exist version.txt set /p VCODE=<version.txt
if not defined VCODE set "VCODE=1"
set "VCODE=%VCODE: =%"
if "%VCODE%"=="" set "VCODE=1"

REM --- increment ---
set /a NEWCODE=VCODE+1

REM --- versionName mirrors the code as 1.0.N ---
set "VNAME=1.0.%NEWCODE%"

echo ============================================================
echo  Bumping Intonare release version
echo    versionCode : %VCODE%  ^-^>  %NEWCODE%
echo    versionName : %VNAME%
echo ============================================================

REM --- patch android\app\build.gradle (runs AFTER go.bat / cap sync) ---
set "PS1=%TEMP%\intonare_bump.ps1"
(
    echo $gradle = 'android\app\build.gradle'
    echo $c = Get-Content $gradle -Raw
    echo $c = $c -replace 'versionCode\s+\d+', 'versionCode %NEWCODE%'
    echo $c = $c -replace 'versionName\s+"[^"]*"', 'versionName "%VNAME%"'
    echo Set-Content -Path $gradle -Value $c -NoNewline
) > "%PS1%"

powershell -NoProfile -ExecutionPolicy Bypass -File "%PS1%"
del "%PS1%" >nul 2>&1

REM --- save the new number for next time (PowerShell write, never blanks) ---
powershell -NoProfile -Command "Set-Content -Path 'version.txt' -Value '%NEWCODE%' -NoNewline"

echo.
echo  Done. build.gradle now at versionCode %NEWCODE% / versionName %VNAME%.
echo  version.txt updated to %NEWCODE%.
echo  Verify: open android\app\build.gradle and check the versionCode line.
echo  Next: build the signed AAB in Android Studio and upload to Play.
echo ============================================================
pause
endlocal
