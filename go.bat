@echo off
setlocal enabledelayedexpansion
REM ============================================================
REM  Intonare -- one-shot deploy
REM  Downloads -> GitHub -> Capacitor -> Android assets
REM ============================================================
REM
REM  NATIVE MASTERS now live under native_src\, mirroring the Android
REM  tree (native_src\java\... , native_src\res\... , etc). Run
REM  reorg_native.bat ONCE before the first run with this version.
REM  icon_res\ and audio_assets\ stayed in root (already folders).
REM
REM  NATIVE_CHANGED tracks whether any native source (.java / manifest /
REM  gradle-affecting file) actually changed bytes this run. If it did, we
REM  force `gradlew clean` at the end so the next Android Studio build can't
REM  ship stale native code. `cap sync` does NOT force a recompile, and
REM  Gradle's up-to-date cache will happily reuse old .class files + a stale
REM  plugin registry -- that's the trap that burned a whole Phase 0 session.
REM  Web-only deploys leave this flag at 0 and stay fast (no clean).
set NATIVE_CHANGED=0

echo [1/6] Copying latest Intonare.html from Downloads...
copy /Y C:\Users\citti\Downloads\Intonare.html Intonare.html
if errorlevel 1 (
  echo  ^>^> No Intonare.html found in Downloads. Aborting.
  goto :end
)

echo [2/6] Committing and pushing to GitHub...
git add -A
git commit -m "Update Intonare.html"
git push

echo [3/6] Copying Intonare.html to www...
if not exist www mkdir www
copy /Y Intonare.html www\index.html

echo [4/6] Installing packages and syncing Capacitor...
call npm install
call npx cap sync

REM Restore files that cap sync overwrites -- sources now under native_src\
echo [4b] Restoring AndroidManifest.xml...
fc /b native_src\AndroidManifest.xml android\app\src\main\AndroidManifest.xml >nul 2>&1
if errorlevel 1 set NATIVE_CHANGED=1
copy /Y native_src\AndroidManifest.xml android\app\src\main\AndroidManifest.xml

echo [4c] Restoring MainActivity.java...
fc /b native_src\java\com\lieutenantdan\intonare\MainActivity.java android\app\src\main\java\com\lieutenantdan\intonare\MainActivity.java >nul 2>&1
if errorlevel 1 set NATIVE_CHANGED=1
copy /Y native_src\java\com\lieutenantdan\intonare\MainActivity.java android\app\src\main\java\com\lieutenantdan\intonare\MainActivity.java

echo [4c2] Restoring IntonareMicPlugin.java...
fc /b native_src\java\com\lieutenantdan\intonare\IntonareMicPlugin.java android\app\src\main\java\com\lieutenantdan\intonare\IntonareMicPlugin.java >nul 2>&1
if errorlevel 1 set NATIVE_CHANGED=1
copy /Y native_src\java\com\lieutenantdan\intonare\IntonareMicPlugin.java android\app\src\main\java\com\lieutenantdan\intonare\IntonareMicPlugin.java

echo [4d] Restoring styles.xml...
copy /Y native_src\res\values\styles.xml android\app\src\main\res\values\styles.xml

echo [4e] Restoring colors.xml...
copy /Y native_src\res\values\colors.xml android\app\src\main\res\values\colors.xml

echo [4f] Restoring app icons...
xcopy /E /Y /I icon_res android\app\src\main\res

echo [4f2] Restoring notification icon...
xcopy /Y /I icon_res\notification\drawable-mdpi\ic_stat_intonare.png android\app\src\main\res\drawable-mdpi\
xcopy /Y /I icon_res\notification\drawable-hdpi\ic_stat_intonare.png android\app\src\main\res\drawable-hdpi\
xcopy /Y /I icon_res\notification\drawable-xhdpi\ic_stat_intonare.png android\app\src\main\res\drawable-xhdpi\
xcopy /Y /I icon_res\notification\drawable-xxhdpi\ic_stat_intonare.png android\app\src\main\res\drawable-xxhdpi\
xcopy /Y /I icon_res\notification\drawable-xxxhdpi\ic_stat_intonare.png android\app\src\main\res\drawable-xxxhdpi\

echo [4g] Restoring audio samples (skipping folders already present)...
if exist audio_assets (
    for /D %%i in (audio_assets\*) do (
        set "dest=android\app\src\main\assets\public\audio\%%~ni"
        if not exist "android\app\src\main\assets\public\audio\%%~ni" (
            echo   Copying %%~ni...
            xcopy /E /Y /I "%%i" "android\app\src\main\assets\public\audio\%%~ni"
        )
    )
)

echo [4i] Restoring splash launch sound...
if not exist android\app\src\main\res\raw mkdir android\app\src\main\res\raw
copy /Y native_src\res\raw\intonare_splash.ogg android\app\src\main\res\raw\intonare_splash.ogg

echo [4h] Patching build.gradle proguard reference...
powershell -Command "(Get-Content android\app\build.gradle) -replace 'proguard-android\.txt', 'proguard-android-optimize.txt' | Set-Content android\app\build.gradle"

echo [5/6] Copying to Android assets + verifying...
copy /Y www\index.html android\app\src\main\assets\public\index.html
findstr "cueSelect_correct" android\app\src\main\assets\public\index.html

echo [5b] Native-change check...
REM gradlew needs a JDK. Point JAVA_HOME at Android Studio's bundled one if
REM this shell doesn't already have it set, so a forced clean never silently
REM fails (a failed clean would put us right back into stale-build territory).
REM Done here, outside the if-block, to avoid nested-paren expansion quirks.
if not defined JAVA_HOME if exist "C:\Program Files\Android\Android Studio\jbr\bin\java.exe" set "JAVA_HOME=C:\Program Files\Android\Android Studio\jbr"
if "!NATIVE_CHANGED!"=="1" (
  echo   ^>^> Native source changed this run. Forcing gradlew clean so the
  echo      next build can't ship stale native code...
  pushd android
  call gradlew.bat clean
  if errorlevel 1 (
    echo   ^>^> ^*^* WARNING: gradlew clean FAILED. Native may still be stale.
    echo      Check JAVA_HOME, then run `gradlew clean` manually in \android.
  ) else (
    echo   ^>^> Clean done. The next Android Studio Run will fully recompile native.
  )
  popd
) else (
  echo   ^>^> No native changes detected. Skipping clean ^(fast web-only deploy^).
)

echo.
echo ============================================================
echo  DONE. Hit Run in Android Studio, then clear cache on phone.
echo ============================================================

endlocal
:end
pause
