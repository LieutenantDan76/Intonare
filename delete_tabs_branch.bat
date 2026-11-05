@echo off
cd /d "%~dp0"
git push origin --delete tabs
git branch -D tabs 2>nul
del "%~f0"
