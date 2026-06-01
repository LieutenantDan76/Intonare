@echo off
REM ============================================================
REM  Intonare — one-shot deploy
REM  Downloads -> GitHub -> Capacitor -> Android assets
REM ============================================================

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

REM Restore files that cap sync overwrites
echo [4b] Restoring AndroidManifest.xml...
copy /Y AndroidManifest.xml android\app\src\main\AndroidManifest.xml

echo [4c] Restoring MainActivity.java...
copy /Y MainActivity.java android\app\src\main\java\com\lieutenantdan\intonare\MainActivity.java

echo [4d] Restoring styles.xml...
copy /Y styles.xml android\app\src\main\res\values\styles.xml

echo [4e] Restoring colors.xml...
copy /Y colors.xml android\app\src\main\res\values\colors.xml

echo [5/6] Copying to Android assets + verifying...
copy /Y www\index.html android\app\src\main\assets\public\index.html
findstr "cueSelect_correct" android\app\src\main\assets\public\index.html

echo.
echo ============================================================
echo  DONE. Hit Run in Android Studio, then clear cache on phone.
echo ============================================================

:end
pause
