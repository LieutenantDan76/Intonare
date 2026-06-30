@echo off
setlocal enabledelayedexpansion
REM ============================================================
REM  Intonare -- ONE-TIME native-source reorganization
REM  Moves the loose native master files out of the repo root and
REM  into native_src/, mirroring the Android tree so every go.bat
REM  restore line is just  native_src\<same path>  ->  android\...\<same path>.
REM
REM  Run this ONCE, from the repo root, BEFORE the new go.bat.
REM  It only MOVES files that exist and verifies each move, so a
REM  half-finished run fails loud instead of leaving you guessing.
REM
REM  It does NOT touch:
REM    - icon_res\        (already a self-contained folder)
REM    - audio_assets\    (already a self-contained folder)
REM    - the android\ tree itself
REM    - build.gradle / proguard (that's a patch, not a master file)
REM ============================================================

set FAIL=0

echo Creating native_src folder structure...
if not exist native_src\java\com\lieutenantdan\intonare mkdir native_src\java\com\lieutenantdan\intonare
if not exist native_src\res\values mkdir native_src\res\values
if not exist native_src\res\raw mkdir native_src\res\raw

REM ---- helper: move a file only if it exists, verify it landed ----
call :moveone "AndroidManifest.xml"                 "native_src\AndroidManifest.xml"
call :moveone "MainActivity.java"                   "native_src\java\com\lieutenantdan\intonare\MainActivity.java"
call :moveone "IntonareMicPlugin.java"              "native_src\java\com\lieutenantdan\intonare\IntonareMicPlugin.java"
call :moveone "styles.xml"                          "native_src\res\values\styles.xml"
call :moveone "colors.xml"                          "native_src\res\values\colors.xml"
call :moveone "intonare_splash.ogg"                 "native_src\res\raw\intonare_splash.ogg"

echo.
if "!FAIL!"=="1" (
  echo ============================================================
  echo  ^>^> REORG INCOMPLETE. One or more moves failed above.
  echo     Check the messages, fix, and re-run. Do NOT run the new
  echo     go.bat until this reports SUCCESS.
  echo ============================================================
) else (
  echo ============================================================
  echo  ^>^> REORG SUCCESS. All native masters now live under native_src\.
  echo     icon_res\ and audio_assets\ were left as-is ^(already folders^).
  echo     Next: swap in the new go.bat and do one full run to verify.
  echo ============================================================
)

endlocal
pause
goto :eof

REM ============================================================
REM  :moveone  <source>  <dest>
REM  Moves source->dest only if source exists. If source is already
REM  gone AND dest already exists, treats it as already-done (idempotent,
REM  so re-running after a partial reorg is safe). Sets FAIL on real trouble.
REM ============================================================
:moveone
set "SRC=%~1"
set "DST=%~2"
if exist "%SRC%" (
  echo Moving %SRC%  -^>  %DST%
  move /Y "%SRC%" "%DST%" >nul
  if exist "%DST%" (
    echo   OK
  ) else (
    echo   ^>^> FAILED to move %SRC%
    set FAIL=1
  )
) else (
  if exist "%DST%" (
    echo Skipping %SRC%  ^(already moved^)
  ) else (
    echo   ^>^> MISSING: %SRC% not in root and not at %DST%
    echo      If this file should exist, restore it before continuing.
    set FAIL=1
  )
)
goto :eof
