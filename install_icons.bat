@echo off
echo Installing Intonare icons...

set SRC=C:\Users\citti\Downloads
set RES=android\app\src\main\res

copy /Y "%SRC%\ic_launcher_mdpi.png"     "%RES%\mipmap-mdpi\ic_launcher.png"
copy /Y "%SRC%\ic_launcher_hdpi.png"     "%RES%\mipmap-hdpi\ic_launcher.png"
copy /Y "%SRC%\ic_launcher_xhdpi.png"    "%RES%\mipmap-xhdpi\ic_launcher.png"
copy /Y "%SRC%\ic_launcher_xxhdpi.png"   "%RES%\mipmap-xxhdpi\ic_launcher.png"
copy /Y "%SRC%\ic_launcher_xxxhdpi.png"  "%RES%\mipmap-xxxhdpi\ic_launcher.png"

copy /Y "%SRC%\ic_launcher_round_mdpi.png"     "%RES%\mipmap-mdpi\ic_launcher_round.png"
copy /Y "%SRC%\ic_launcher_round_hdpi.png"     "%RES%\mipmap-hdpi\ic_launcher_round.png"
copy /Y "%SRC%\ic_launcher_round_xhdpi.png"    "%RES%\mipmap-xhdpi\ic_launcher_round.png"
copy /Y "%SRC%\ic_launcher_round_xxhdpi.png"   "%RES%\mipmap-xxhdpi\ic_launcher_round.png"
copy /Y "%SRC%\ic_launcher_round_xxxhdpi.png"  "%RES%\mipmap-xxxhdpi\ic_launcher_round.png"

echo Done. Now run go.bat to deploy.
pause
