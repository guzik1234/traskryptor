@echo off
chcp 65001 >nul
echo ================================================
echo          TRASKRYPTOR - Uruchamianie
echo ================================================
echo.
cd /d "%~dp0"
set PYTHONIOENCODING=utf-8
set KMP_DUPLICATE_LIB_OK=TRUE

echo [*] Sprawdzanie srodowiska...
if not exist ".venv\Scripts\python.exe" (
    echo [BLAD] Nie znaleziono Pythona w pakiecie!
    echo Upewnij sie ze caly folder zostal rozpakowany.
    pause
    exit /b 1
)

echo [*] Uruchamianie aplikacji...
echo.
".venv\Scripts\python.exe" main.py
if errorlevel 1 (
    echo.
    echo [BLAD] Aplikacja zakonczyla sie bledem!
    pause
)
