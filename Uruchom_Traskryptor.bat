@echo off
chcp 65001 >nul
cd /d "%~dp0"
set PYTHONIOENCODING=utf-8
set KMP_DUPLICATE_LIB_OK=TRUE
.\.venv\Scripts\python.exe main.py
if errorlevel 1 pause
