@echo off
title Annapurna Groceries & Liquor Server
cd /d "%~dp0"
echo =======================================================
echo   Starting Annapurna Store (Unified Single Server)
echo =======================================================
echo.
python run.py
pause
