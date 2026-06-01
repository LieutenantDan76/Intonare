@echo off
REM ============================================================
REM  Intonare — one-shot deploy
REM  Downloads -> GitHub -> Capacitor -> Android assets
REM ============================================================

echo [1/5] Copying latest Intonare.html from Downloads...
copy /Y C:\Users\citti\Downloads\Intonare.html Intonare.html
if errorlevel 1 (
  echo  ^>^> No Intonare.html found in Downloads. Aborting.
  goto :end
)

echo [2/5] Committing and pushing to GitHub...
git add -A
git commit -m "Update Intonare.html"
git push

echo [3/5] Copying Intonare.html to www...
if not exist www mkdir www
copy /Y Intonare.html www\index.html

echo [4/5] Syncing Capacitor...
call npx cap sync

REM Restore AndroidManifest.xml after cap sync overwrites it
echo [4b] Restoring AndroidManifest.xml with microphone permissions...
copy /Y AndroidManifest.xml android\app\src\main\AndroidManifest.xml

echo [5/5] Copying to Android assets + verifying...
copy /Y www\index.html android\app\src\main\assets\public\index.html
findstr "cueSelect_correct" android\app\src\main\assets\public\index.html

echo.
echo ============================================================
echo  DONE. Hit Run in Android Studio, then clear cache on phone.
echo ============================================================

:end
pause
