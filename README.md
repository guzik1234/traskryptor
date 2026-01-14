# 🎤 Traskryptor - Transkrypcja i Tłumaczenie Offline

Uniwersalna aplikacja do transkrypcji mowy na tekst oraz tłumaczenia dokumentów **całkowicie offline**.

## 🌟 Główne cechy

- ✅ **100% Offline** - brak wymagań internetu po pobraniu modeli
- ✅ **Trzy funkcje:** transkrypcja pliku, transkrypcja na żywo, tłumaczenie dokumentów
- ✅ **Tłumaczenie offline** - translate library (bez PyTorch, bez zależności od sieci)
- ✅ **Przenośny bundle** - Python 3.13 + wszystkie zależności (1 GB, kompresja 366 MB)
- ✅ **Wielojęzyczność** - PL, EN, RU, UK

---

## 📦 Szybki start

### Opcja 1: Bundle (REKOMENDOWANE) ⭐

**Najłatwiej!** Pobierz gotowy bundle ze wszystkim wbudowanym:

1. Pobierz: [Traskryptor_WinPython_v1.1.zip (366 MB)](https://github.com/guzik1234/traskryptor/releases)
2. Rozpakuj folder
3. Uruchom `Traskryptor.exe`
4. Gotowe! 🎉 Działa 100% offline

### Opcja 2: Instalacja ręczna

```bash
# Utwórz środowisko
python -m venv .venv
.venv\Scripts\activate

# Zainstaluj zależności
pip install -r requirements.txt

# Uruchom aplikację
python main.py
```

---

## 📋 Funkcje

### 1️⃣ Transkrypcja z pliku audio

Konwertuj audio na tekst w kilka sekund.

- **Formaty:** MP3, WAV, M4A, FLAC, OGG
- **Języki:** Polski, Angielski
- **Wyjście:** DOCX + PDF
- **Czy offline?** ✅ Tak

**Jak użyć:**
1. Wybierz "Transkrypcja z pliku audio"
2. Zaznacz plik audio
3. Wybierz język
4. Kliknij "Start"
5. Czekaj na wynik (DOCX + PDF)

---

### 2️⃣ Transkrypcja na żywo

Nagrywaj i transkrybuj mowę w Microsoft Word w czasie rzeczywistym.

- **Języki:** Polski, Angielski
- **Integracja:** Microsoft Word
- **🆕 Tłumaczenie:** Opcjonalne tłumaczenie PL→EN
- **Czy offline?** ✅ Tak (transkrypcja + tłumaczenie)
- **Aktywacja:** Lewy Shift (do włączenia/wyłączenia nagrywania)

**Jak użyć:**
1. Otwórz Microsoft Word
2. Wybierz "Transkrypcja na żywo"
3. Kliknij "Włącz tłumaczenie PL→EN" (opcjonalnie)
4. Wciśnij **Lewy Shift** by zacząć nagrywać
5. Mów do mikrofonu
6. Tekst pojawia się w Wordzie

---

### 3️⃣ Tłumaczenie dokumentów

Przetłumacz całe dokumenty z zachowaniem formatowania.

- **Formaty wejścia:** DOCX, PDF
- **Formaty wyjścia:** DOCX + PDF
- **Języki:** Polski→ Angielski / Rosyjski / Ukraiński
- **Czy offline?** ✅ Tak (translate library)
- **Dodatkowe:** Wsparcie Microsoft Word (COM automation)

**Jak użyć:**
1. Wybierz "Tłumaczenie dokumentów"
2. Zaznacz dokument
3. Wybierz język docelowy
4. Kliknij "Start tłumaczenia"
5. Czekaj (progress na dole okna)
6. Pobierz przetłumaczony dokument (sufiks: `_en`, `_ru`, `_uk`)

---

## 🏗️ Struktura projektu

```
traskryptor/
├── main.py                      # Główne menu
├── gui.py                       # GUI transkrypcji na żywo
├── audio_file_transcription.py # Transkrypcja z pliku
├── speech_to_word.py           # Transkrypcja na żywo
├── transcription_model.py      # Modele AI
├── translation_gui.py          # GUI tłumaczenia
├── pdf_translator.py           # Logika tłumaczenia (translate library)
├── audio_handler.py            # Obsługa mikrofonu
├── word_handler.py             # Integracja Word (COM)
├── requirements.txt            # Zależności Python
└── Traskryptor_WinPython/      # Bundle (1 GB)
    ├── python/                 # Python 3.13 + pakiety
    ├── app/                    # Kod aplikacji
    └── Traskryptor.exe         # Launcher
```

---

## ⚙️ Wymagania

### Bundle (opcja rekomendowana)
- Windows 7+
- 366 MB na dysku (po rozpakowaniu ~1 GB)
- Mikrofon (dla transkrypcji na żywo)
- Microsoft Word (opcjonalnie, dla transkrypcji na żywo)

### Instalacja ręczna
- Python 3.8+ (testowane na 3.13)
- sounddevice, numpy, librosa, keyboard
- faster-whisper (transkrypcja)
- **translate 3.8.0** (tłumaczenie offline - NIE PyTorch)
- python-docx, pymupdf (dokumenty)
- pywin32 (integracja Word)

**Wszystkie biblioteki są DARMOWE i OPEN SOURCE** ✅

---

## 🚀 Instalacja zaawansowana

### Pobierz pakiety językowe (tłumaczenie)
Aby tłumaczenie było szybsze, pobierz pakiety offline:

```bash
python install_languages.py
```

Pobierze modele dla:
- 🇵🇱 Polski → 🇬🇧 Angielski
- 🇵🇱 Polski → 🇷🇺 Rosyjski  
- 🇵🇱 Polski → 🇺🇦 Ukraiński

Po pobraniu wszystko działa **bez internetu**.

---

## 🐛 Rozwiązywanie problemów

### "ModuleNotFoundError"
```bash
pip install -r requirements.txt
```

### Transkrypcja nie działa
- Sprawdź czy mikrofon działa
- Sprawdź czy Microsoft Word jest otwarty (transkrypcja na żywo)
- Pierwsze uruchomienie pobiera modele (wymaga internetu)

### Tłumaczenie zawiesza się
- Upewnij się że Microsoft Word jest zainstalowany
- Zamknij wszystkie okna Word przed uruchomieniem
- Sprawdź plik `ROZWIAZANIE_PROBLEMU.md`

### Brak pakietów tłumaczenia
```bash
python install_languages.py
```

---

## 📄 Dokumentacja

- [ROZWIAZANIE_PROBLEMU.md](ROZWIAZANIE_PROBLEMU.md) - Szczegółowe rozwiązania
- [LICENSES.md](LICENSES.md) - Informacje o licencjach
- [OFFLINE_MODE.md](OFFLINE_MODE.md) - Tryb offline

---

## 📜 Licencja

Wszystkie zależności są open source z licencjami permisywnymi:
- **MIT, Apache 2.0, BSD, ISC, PSF**
- ✅ Użycie komercyjne - DARMOWE
- ✅ Dystrybucja - DARMOWE
- ✅ Modyfikacja - DARMOWE

Szczegóły: [LICENSES.md](LICENSES.md)

---

## 🔧 Stack techniczny

| Komponent | Technologia | Licencja |
|-----------|------------|----------|
| **Transkrypcja** | faster-whisper (CTranslate2) | MIT |
| **Tłumaczenie** | translate 3.8.0 | MIT |
| **Audio** | sounddevice + librosa | MIT/ISC |
| **Dokumenty** | python-docx + pymupdf | MIT |
| **Word integration** | pywin32 (COM) | PSF |

---

## 📞 Wsparcie

- 📧 Dokumentacja: `README.md`
- 🐛 Problemy: `ROZWIAZANIE_PROBLEMU.md`
- ⚖️ Licencje: `LICENSES.md`

---

## 📌 Notatki

- **Transkrypcja na żywo wymaga:** Microsoft Word (COM automation)
- **Tłumaczenie działa offline:** dzięki translate library (bez PyTorch)
- **Bundle to:** Python 3.13 + wszystkie pakiety + aplikacja (przenośny)
- **Pierwsze uruchomienie:** pobiera modele AI (~1 GB, wymaga internetu)

**Wersja:** 1.1 (z offline translation)  
**Ostatnia aktualizacja:** styczeń 2026
