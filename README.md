# Transkrypcja i Tłumaczenie

Aplikacja do transkrypcji mowy na tekst oraz tłumaczenia dokumentów PDF.

## Funkcje

### 1. Transkrypcja mowy do tekstu
- Transkrypcja na żywo z mikrofonu do Microsoft Word
- Wsparcie dla języka polskiego (2 modele) i angielskiego
- Aktywacja nagrywania przez Lewy Shift

### 2. Tłumaczenie dokumentów Word/ODT/PDF
- Tłumaczenie z polskiego na angielski lub rosyjski
- **Obsługa formatów:** DOCX, ODT (pełne zachowanie struktury), PDF (konwersja przez Word)
- Zachowanie formatowania, układu i czcionek
- Eksport do DOCX + PDF
- **Wymaga:** Microsoft Word (używa automatyzacji COM)
- **Wymaga:** połączenie z internetem (Google Translate API)

## Struktura projektu

### Transkrypcja
- **speech_to_word.py** - Logika transkrypcji
- **gui.py** - Interfejs graficzny transkrypcji
- **audio_handler.py** - Obsługa nagrywania audio
- **transcription_model.py** - Modele transkrypcji (polski/angielski)
- **word_handler.py** - Integracja z Microsoft Word

### Tłumaczenie
- **translation_gui.py** - Interfejs graficzny tłumaczenia
- **pdf_translator.py** - Logika tłumaczenia PDF
- **main.py** - Główne menu aplikacji

## Wymagania

### Instalacja zależności
```bash
pip install -r requirements.txt
```

**Biblioteki (kluczowe):**
- Python 3.8+ (testowane na 3.13)
- SoundDevice (nagrywanie audio, zamiennik PyAudio na Windows)
- NumPy
- Keyboard
- Faster Whisper / OpenAI Whisper (transkrypcja)
- PyTorch
- Transformers, SentencePiece, ArgosTranslate (tłumaczenie offline)
- pywin32 (Word COM)
- **Microsoft Word** (wymagane dla tłumaczenia dokumentów)

**Ważne:**
- Transkrypcja: modele pobierają się przy pierwszym użyciu (offline później)
- Na Windows zalecane: uruchom PowerShell jako administrator lub włącz Developer Mode (lepszy cache HF bez ostrzeżeń o symlinkach).
- Tłumaczenie dokumentów Word/PDF wymaga zainstalowanego Microsoft Word.

## Uruchomienie

### Główne menu (wszystkie funkcje)
```bash
python main.py
```

### Tylko transkrypcja
1. Otwórz Microsoft Word z dokumentem
2. Uruchom: `python speech_to_word.py`
3. Wybierz język (Polski/Angielski)
4. Dla polskiego wybierz model (1 - szybszy, 2 - dokładniejszy)
5. Kliknij "Start"
6. Przytrzymaj Lewy Shift aby nagrywać
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
