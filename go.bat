@echo off
setlocal enabledelayedexpansion
REM ============================================================
REM  Intonare deploy
REM  Project folder -> GitHub -> Capacitor -> Android assets
REM ============================================================
REM
REM  Native sources live in native_src\, laid out like the Android tree.
REM  cap sync overwrites the generated project, so this script copies them
REM  back in on every run.
REM
REM  NATIVE_CHANGED records whether any native file changed this run. If one
REM  did, the script runs `gradlew clean` at the end. cap sync does not force
REM  a recompile, and Gradle would reuse the old compiled classes.
REM  Web-only deploys skip the clean and stay fast.
set NATIVE_CHANGED=0

echo [1/6] Verifying Intonare.html is present...
if not exist Intonare.html (
  echo  ^>^> No Intonare.html found in project folder. Aborting.
  goto :end
)

echo [2/6] Committing and pushing to GitHub...
git add -A
set "MSG="
set /p "MSG=Commit message (Enter for the default): "
if not defined MSG set "MSG=Update Intonare"
git commit -m "!MSG!"
git push

echo [3/6] Copying Intonare.html to www...
if not exist www mkdir www
copy /Y Intonare.html www\index.html

echo [4/6] Installing packages and syncing Capacitor...
call npm install

REM Build main.iife.js, the Capacitor haptics bridge, from main.js with Vite.
REM www\ is not in git, so this must run on every deploy. Without the file,
REM haptics stop working and nothing reports an error. Vite's emptyOutDir is
REM false, so the index.html copied in step 3 is kept.
echo [4a] Building main.iife.js (haptics bridge)...
call npm run build

call npx cap sync

REM Restore the files that cap sync overwrites. Sources are in native_src\.
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

echo [4c3] Restoring FileSaverPlugin.java...
REM Every native file must live in native_src and be restored here. A file
REM placed straight into android\ is lost, because step 4c restores
REM MainActivity.java and its registerPlugin lines on every run.
fc /b native_src\java\com\lieutenantdan\intonare\FileSaverPlugin.java android\app\src\main\java\com\lieutenantdan\intonare\FileSaverPlugin.java >nul 2>&1
if errorlevel 1 set NATIVE_CHANGED=1
copy /Y native_src\java\com\lieutenantdan\intonare\FileSaverPlugin.java android\app\src\main\java\com\lieutenantdan\intonare\FileSaverPlugin.java

echo [4c4] Restoring IntonareHapticsPlugin.java...
fc /b native_src\java\com\lieutenantdan\intonare\IntonareHapticsPlugin.java android\app\src\main\java\com\lieutenantdan\intonare\IntonareHapticsPlugin.java >nul 2>&1
if errorlevel 1 set NATIVE_CHANGED=1
copy /Y native_src\java\com\lieutenantdan\intonare\IntonareHapticsPlugin.java android\app\src\main\java\com\lieutenantdan\intonare\IntonareHapticsPlugin.java

echo [4d] Restoring styles.xml...
copy /Y native_src\res\values\styles.xml android\app\src\main\res\values\styles.xml

echo [4d2] Restoring home screen shortcuts...
REM shortcuts.xml and its labels. The manifest points at @xml/shortcuts, so if these
REM are not copied in, the build fails with a missing resource, not a quiet no-op.
if not exist android\app\src\main\res\xml mkdir android\app\src\main\res\xml
if not exist android\app\src\main\res\values-it mkdir android\app\src\main\res\values-it
copy /Y native_src\res\xml\shortcuts.xml android\app\src\main\res\xml\shortcuts.xml
copy /Y native_src\res\values\shortcut_strings.xml android\app\src\main\res\values\shortcut_strings.xml
copy /Y native_src\res\values-it\shortcut_strings.xml android\app\src\main\res\values-it\shortcut_strings.xml

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

REM Loose files in the audio_assets root. Step 4g uses `for /D`, which only
REM walks folders, so single files such as intonare_whip.mp3 need their own copy.
REM They are copied on every run so that a replaced file reaches the build.
if exist audio_assets (
    if not exist android\app\src\main\assets\public\audio mkdir android\app\src\main\assets\public\audio
    for %%f in (audio_assets\*.*) do (
        echo   Copying loose file %%~nxf...
        copy /Y "%%f" "android\app\src\main\assets\public\audio\%%~nxf" >nul
    )
)

echo [4i] Restoring splash launch sound...
if not exist android\app\src\main\res\raw mkdir android\app\src\main\res\raw
copy /Y native_src\res\raw\intonare_splash.ogg android\app\src\main\res\raw\intonare_splash.ogg
echo [4j] Restoring R8 rules and resource keep list...
copy /Y native_src\proguard-rules.pro android\app\proguard-rules.pro
copy /Y native_src\res\raw\keep.xml android\app\src\main\res\raw\keep.xml

echo [4h] Patching build.gradle proguard reference...
powershell -Command "(Get-Content android\app\build.gradle) -replace 'proguard-android\.txt', 'proguard-android-optimize.txt' | Set-Content android\app\build.gradle"

echo [5/6] Copying to Android assets + verifying...
copy /Y www\index.html android\app\src\main\assets\public\index.html
findstr "cueSelect_correct" android\app\src\main\assets\public\index.html

echo [5b] Native-change check...
REM gradlew needs a JDK. Use the one bundled with Android Studio if JAVA_HOME
REM is not set, so a forced clean cannot fail for that reason. This sits
REM outside the if-block to avoid nested-parenthesis expansion problems.
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
echo  DONE.
echo.
echo  This script does NOT build the APK. Hit Run in Android Studio,
echo  then clear cache on the phone.
echo.
echo  Native changes (manifest, .java) only reach the phone via that
echo  Run -- testing against the APK already installed will show the
echo  OLD native behaviour with the NEW web code, which looks like a
echo  half-broken feature rather than an unbuilt one.
echo ============================================================

endlocal
:end
pause
