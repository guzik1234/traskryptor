# Automatyczna Instalacja Traskryptor

## Co robi ten instalator:

1. **Kopiuje wszystkie pliki** - Python + biblioteki do folderu Program Files
2. **Tworzy skróty** - Na pulpicie i w menu Start
3. **Konfiguruje pywin32** - Aby działał z Microsoft Word
4. **Gotowe!** - Aplikacja działa od razu po instalacji

---

## Jak stworzyć instalator:

### Opcja 1: Inno Setup (Zalecane)

1. **Pobierz Inno Setup:**
   - https://jrsoftware.org/isdl.php
   - Pobierz wersję z QuickStart Pack

2. **Utwórz instalator:**
   - Otwórz `Traskryptor_Installer.iss`
   - Kliknij: Build → Compile
   - Poczekaj 5-10 minut (kompresja 1.9 GB)

3. **Gotowy instalator:**
   - `Traskryptor_Installer.exe` (~250-300 MB skompresowane)
   - Użytkownicy uruchamiają i wszystko jest zainstalowane

---

### Opcja 2: Paczka ZIP (Jak jest teraz)

**Problem:** Hardcoded paths w bibliotekach nie działają na innych komputerach

**Rozwiązanie:**
- Instalator kopiuje pliki do stałej lokalizacji (Program Files)
- Wszystkie ścieżki są względne do tej lokalizacji
- Działa na każdym komputerze Windows

---

## Alternatywa: Portable (bez instalatora)

Jeśli nie chcesz używać instalatora, możemy:

1. **Użyć WinPython** - prawdziwie portable Python
2. **Lub Anaconda** - ma własny system pakietów
3. **Lub Docker Desktop** - kontener z wszystkim

---

## Zalecenie:

**INNO SETUP INSTALATOR** - najbardziej niezawodne rozwiązanie:
- ✅ Działa na każdym Windows
- ✅ Profesjonalny wygląd
- ✅ Łatwa instalacja dla użytkowników
- ✅ Automatyczna deinstalacja
- ✅ Bez problemów z PATH/DLL

---

## Co dalej?

Wybierz:
1. **Instalator** - Pobierz Inno Setup i skompiluj `Traskryptor_Installer.iss`
2. **Portable** - Spróbujmy WinPython (600 MB, prawdziwie portable)
3. **Docker** - Kontener który działa wszędzie

Która opcja?
