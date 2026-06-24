@echo off
REM ============================================================
REM  Intonare - Play Store release bump
REM  Run this ONLY when prepping a build to upload to Google Play.
REM  Do NOT run it for everyday device testing (that's go.bat).
REM
REM  What it does:
REM    1. Reads the last versionCode from version.txt (starts at 1)
REM    2. Increments it (+1) so every Play upload is unique and higher
REM    3. Patches versionCode AND versionName into android\app\build.gradle
REM       AFTER cap sync has regenerated it (so the bump survives)
REM    4. Saves the new number back to version.txt
REM
REM  USAGE on an upload day:
REM    1. Run go.bat first (does the normal build + restores)
REM    2. Then run release.bat (bumps the version)
REM    3. Then build the signed AAB in Android Studio and upload
REM ============================================================

setlocal enabledelayedexpansion

REM --- read current versionCode (default 1 if file missing) ---
set "VCODE=1"
if exist version.txt (
    set /p VCODE=<version.txt
)

REM --- increment ---
set /a NEWCODE=VCODE+1

REM --- versionName mirrors the code as 1.0.N so the store shows movement ---
set "VNAME=1.0.%NEWCODE%"

echo ============================================================
echo  Bumping Intonare release version
echo    versionCode : %VCODE%  ^-^>  %NEWCODE%
echo    versionName : %VNAME%
echo ============================================================

REM --- patch android\app\build.gradle (runs AFTER go.bat / cap sync) ---
REM  Write the PowerShell script to a temp file and run it, so the pipe
REM  inside the pipeline is never seen by cmd (the old inline -Command
REM  let cmd eat the | and split the line, which broke Set-Content).
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

REM --- save the new number for next time ---
echo %NEWCODE%> version.txt

echo.
echo  Done. android\app\build.gradle now at versionCode %NEWCODE% / versionName %VNAME%.
echo  Verify: open android\app\build.gradle and check the versionCode line.
echo  Next: build the signed AAB in Android Studio and upload to Play.
echo ============================================================
pause
endlocal
