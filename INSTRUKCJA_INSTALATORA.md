# Instrukcja Tworzenia Instalatora Traskryptor

## ✅ Bundle został przygotowany pomyślnie!

Rozmiar: **~1.77 GB** - zawiera wszystkie potrzebne biblioteki i Python Embeddable

---

## Metoda 1: Instalator z Inno Setup (Zalecana)

### Instalacja Inno Setup

1. **Pobierz Inno Setup:**
   - Wejdź na: https://jrsoftware.org/isinfo.php
   - Pobierz najnowszą wersję (np. `innosetup-6.x.x.exe`)
   - Zainstaluj program

2. **Utwórz instalator:**
   - Otwórz plik: `traskryptor_installer.iss` (w tym katalogu)
   - W Inno Setup kliknij: **Build → Compile**
   - Poczekaj na zakończenie (może potrwać kilka minut)

3. **Gotowe!**
   - Instalator będzie w: `installer_output\Traskryptor_Setup.exe`
   - Rozmiar: ~600-800 MB (skompresowany)
   - Użytkownicy mogą po prostu uruchomić ten EXE aby zainstalować Traskryptor

---

## Metoda 2: Paczka ZIP (Bez instalatora)

Jeśli nie chcesz tworzyć instalatora EXE, możesz po prostu spakować bundle do ZIP:

### Za pomocą PowerShell:

```powershell
Compress-Archive -Path "installer_bundle\*" -DestinationPath "Traskryptor_Portable.zip"
```

### Lub ręcznie:

1. Wejdź do folderu `installer_bundle`
2. Zaznacz wszystko (Ctrl+A)
3. Prawy przycisk → "Wyślij do" → "Folder skompresowany (zip)"

**Użytkownicy będą musieli:**
1. Rozpakować ZIP
2. Uruchomić `Uruchom_Traskryptor.bat`

---

## Co zawiera bundle?

- ✅ **Python 3.11.9 Embeddable** - Nie wymaga instalacji Pythona
- ✅ **PyTorch 2.5.1 CPU** - Pełna biblioteka uczenia maszynowego  
- ✅ **OpenAI Whisper** - Model transkrypcji
- ✅ **Wszystkie zależności** - PyAudio, pywin32, argostranslate, etc.
- ✅ **Pliki aplikacji** - main.py, gui.py i wszystkie moduły

---

## Testowanie przed dystrybucją

Możesz przetestować bundle przed utworzeniem instalatora:

```bash
cd installer_bundle
Uruchom_Traskryptor.bat
```

Jeśli działa poprawnie, możesz tworzyć instalator.

---

## Dlaczego Inno Setup?

- ✅ **Kompresja** - Zmniejsza rozmiar z ~1.77 GB do ~600-800 MB
- ✅ **Profesjonalny wygląd** - Instalator z logo i opisem
- ✅ **Skróty** - Automatycznie tworzy ikony na pulpicie i w menu Start
- ✅ **Deinstalator** - Łatwe usuwanie aplikacji
- ✅ **Bezpieczeństwo** - Użytkownicy ufają EXE instalatorom

---

## Uwagi

- Bundle działa na Windows 64-bit
- Nie wymaga połączenia z internetem po instalacji
- Działa na komputerach **bez zainstalowanego Pythona**
- Zawiera wszystkie potrzebne DLL i biblioteki
