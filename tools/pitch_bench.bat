@echo off
setlocal
cd /d "%~dp0.."
echo [pitch] Generating synth corpus...
node tools\pitch\gen_corpus.mjs
if errorlevel 1 goto :fail
echo.
echo [pitch] Running bench...
node tools\pitch\run_bench.mjs %*
if errorlevel 1 goto :fail
echo.
echo [pitch] GREEN
goto :end
:fail
echo.
echo [pitch] FAILED
exit /b 1
:end
exit /b 0
