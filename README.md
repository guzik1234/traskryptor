# Transkrypcja i Tłumaczenie

Aplikacja do transkrypcji mowy na tekst oraz tłumaczenia dokumentów.

## Funkcje

### 1. Transkrypcja z pliku audio
- Transkrypcja plików audio (MP3, WAV, M4A, FLAC, OGG) do DOCX i PDF
- Wsparcie dla języka polskiego i angielskiego
- Automatyczny eksport do dokumentów Word i PDF
- **Działa offline** po pobraniu modeli

### 2. Transkrypcja na żywo
- Transkrypcja na żywo z mikrofonu do Microsoft Word
- Wsparcie dla języka polskiego i angielskiego
- Opcjonalne automatyczne tłumaczenie (na angielski, rosyjski, ukraiński)
- Aktywacja nagrywania przez Lewy Shift
- **Działa offline** po pobraniu modeli (tłumaczenie wymaga internetu)

### 3. Tłumaczenie dokumentów Word/ODT
- Tłumaczenie z polskiego na angielski, rosyjski lub ukraiński
- **Obsługa formatów:** DOCX, ODT
- Zachowanie formatowania, układu i czcionek
- Eksport do DOCX + PDF
- **Wymaga:** Microsoft Word (używa automatyzacji COM)
- **Wymaga:** połączenie z internetem (ArgosTranslate)

## Struktura projektu

### Główne pliki
- **main.py** - Główne menu aplikacji

### Transkrypcja z pliku audio
- **audio_file_transcription.py** - GUI i logika transkrypcji z pliku
- **transcription_model.py** - Modele transkrypcji (polski/angielski)

### Transkrypcja na żywo
- **speech_to_word.py** - Logika transkrypcji na żywo
- **gui.py** - Interfejs graficzny transkrypcji na żywo
- **audio_handler.py** - Obsługa nagrywania z mikrofonu
- **word_handler.py** - Integracja z Microsoft Word

### Tłumaczenie
- **translation_gui.py** - Interfejs graficzny tłumaczenia
- **pdf_translator.py** - Logika tłumaczenia dokumentów

## Wymagania

```bash
pip install -r requirements.txt
```

**Biblioteki:**
- Python 3.8+ (testowane na 3.13)
- sounddevice (nagrywanie audio)
- SpeechRecognition (rozpoznawanie mowy)
- NumPy (przetwarzanie danych)
- Keyboard (obsługa klawiatury)
- Transformers (modele AI)
- PyTorch (backend AI)
- openai-whisper (transkrypcja)
- faster-whisper (transkrypcja angielska)
- pywin32 (integracja z Word, automatyzacja COM)
- librosa (wczytywanie plików audio)
- python-docx (tworzenie dokumentów Word)
- docx2pdf (konwersja DOCX do PDF)
- argostranslate (tłumaczenie OFFLINE)
- seInstalacja
```bash
# Utwórz środowisko wirtualne
python -m venv .venv
.venv\Scripts\activate  # Windows

# Zainstaluj zależności
pip install -r requirements.txt
```

### Główne menu (wszystkie funkcje)
```bash
python main.py
```

### 1. Transkrypcja z pliku audio
1. Z menu głównego wybierz "Transkrypcja z pliku audio"
2. Kliknij "Wybierz plik audio" i wskaż plik (MP3, WAV, M4A, FLAC, OGG)
3. Wybierz język (Polski/Angielski)
4. Kliknij "Rozpocznij transkrypcję"
5. Poczekaj na zakończenie
6. Pliki DOCX i PDF zostaną zapisane obok pliku źródłowego

### 2. Transkrypcja na żywo
1. Z menu głównego wybierz "Transkrypcja na żywo"
2. Instalacja pakietów językowych dla tłumaczenia (offline)

Aby tłumaczenie działało offline, pobierz pakiety językowe:

```bash
python install_languages.py
```

Ten skrypt pobierze pakiety dla:
- Polski → Angielski
- Polski → Rosyjski
- Polski → Ukraiński

Po pobraniu wszystko działa **w pełni offline**.

## Rozwiązywanie problemów

### Brak modułu (ModuleNotFoundError)
```bash
pip install -r requirements.txt
```

### Transkrypcja nie działa
1. Sprawdź czy mikrofon działa
2. Sprawdź czy Microsoft Word jest otwarty (dla transkrypcji na żywo)
3. Upewnij się że modele zostały pobrane (pierwsze uruchomienie wymaga internetu)

### Tłumaczenie się zawiesza
1. Sprawdź czy Microsoft Word jest zainstalowany
2. Zamknij wszystkie okna Word przed uruchomieniem
3. Przy pierwszym użyciu języka sprawdź połączenie z internetem
4. Zobacz plik `ROZWIAZANIE_PROBLEMU.md` dla szczegółów

### Brak pakietów językowych ArgosTranslate
Uruchom:
```bash
python install_languages.py
```

## Licencja

Projekt edukacyjny - użyj na własną odpowiedzialność.waga:** Tłumaczenie wymaga zainstalowanego Microsoft Word. Przy pierwszym użyciu języka wymaga internetu (pobiera pakiety ArgosTranslate)
7. Tekst pojawi się w Wordzie
8. Kliknij "Zakończ nasłuchiwanie" aby zatrzymać

### Tylko tłumaczenie dokumentów
1. Uruchom: `python main.py` → wybierz "Tłumaczenie dokumentów"
2. Kliknij "Wybierz plik" i wskaż dokument (.docx, .odt lub .pdf)
3. Wybierz język docelowy (English / Русский)
4. Kliknij "Rozpocznij tłumaczenie"
5. Poczekaj na zakończenie (progres wyświetlany na dole okna)
6. Przetłumaczone pliki DOCX i PDF zostaną zapisane obok oryginału z sufiksem `_en` lub `_ru`

**Uwaga:** Tłumaczenie wymaga połączenia z internetem i zainstalowanego Microsoft Word.

## Rozwiązywanie problemów

### Tłumaczenie się zawiesza
1. Sprawdź czy Microsoft Word jest zainstalowany
2. Zamknij wszystkie okna Word
3. Sprawdź połączenie z internetem
4. Zobacz plik `ROZWIAZANIE_PROBLEMU.md` dla szczegółów

### Błąd "constants" przy tłumaczeniu
To zostało naprawione - program używa wartości numerycznych zamiast stałych Word.

### Testowanie
Uruchom diagnostykę:
```bash
python test_mini_translate.py   # Test tłumaczenia 3 akapitów
python test_word_visible.py     # Test Word COM z widocznym oknem
```
