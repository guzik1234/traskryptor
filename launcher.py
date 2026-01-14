"""
Launcher dla Traskryptor - uruchamia aplikację z portable bundle
"""
import os
import sys
import subprocess
from pathlib import Path


def main():
    # Pobierz ścieżkę do folderu z EXE
    if getattr(sys, 'frozen', False):
        # Uruchomione jako EXE
        exe_dir = Path(sys.executable).parent
    else:
        # Uruchomione jako skrypt
        exe_dir = Path(__file__).parent
    
    # Ścieżki do Python i aplikacji
    python_dir = exe_dir / "python"
    app_dir = exe_dir / "app"
    python_exe = python_dir / "python.exe"
    main_py = app_dir / "main.py"
    
    # Sprawdź czy struktura istnieje
    if not python_exe.exists():
        print(f"BŁĄD: Nie znaleziono Python.exe w {python_dir}")
        input("Naciśnij Enter aby zakończyć...")
        return 1
    
    if not main_py.exists():
        print(f"BŁĄD: Nie znaleziono main.py w {app_dir}")
        input("Naciśnij Enter aby zakończyć...")
        return 1
    
    # Ustaw zmienne środowiskowe
    env = os.environ.copy()
    env["PYTHONHOME"] = str(python_dir)
    env["PYTHONPATH"] = f"{python_dir};{python_dir / 'Lib'};{python_dir / 'Lib' / 'site-packages'}"
    env["TCL_LIBRARY"] = str(python_dir / "tcl" / "tcl8.6")
    env["TK_LIBRARY"] = str(python_dir / "tcl" / "tk8.6")
    
    # Uruchom aplikację
    try:
        subprocess.run(
            [str(python_exe), str(main_py)],
            cwd=str(app_dir),
            env=env
        )
        return 0
    except Exception as e:
        print(f"BŁĄD podczas uruchamiania aplikacji: {e}")
        input("Naciśnij Enter aby zakończyć...")
        return 1


if __name__ == "__main__":
    sys.exit(main())
