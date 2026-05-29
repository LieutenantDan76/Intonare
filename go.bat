@echo off
REM ============================================================
REM  Intonare — one-shot deploy
REM  Downloads -> GitHub -> build -> Capacitor -> Android assets
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

echo [3/6] Building JS bundle...
call npm run build
if errorlevel 1 (
  echo  ^>^> npm build failed. Aborting.
  goto :end
)

echo [4/6] Copying Intonare.html to www...
del /F www\index.html
copy /Y Intonare.html www\index.html

echo [5/6] Syncing Capacitor...
call npx cap sync

echo [6/6] Copying to Android assets + verifying...
copy /Y www\index.html android\app\src\main\assets\public\index.html
findstr "cueSelect_correct" android\app\src\main\assets\public\index.html

echo.
echo ============================================================
echo  DONE. Hit Run in Android Studio, then clear cache on phone.
echo ============================================================

:end
pause
