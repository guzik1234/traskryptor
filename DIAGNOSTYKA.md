# Diagnostyka i rozwiązywanie problemów transkrypcji

## Status testów

### ✓ Biblioteki zainstalowane pomyślnie:
- sounddevice - obsługa mikrofonu
- SpeechRecognition - rozpoznawanie mowy
- openai-whisper - model transkrypcji
- faster-whisper - szybszy model transkrypcji
- keyboard - obsługa klawiatury
- pywin32 - integracja z Windows/Word
- numpy, torch, transformers - AI/ML
- argostranslate - tłumaczenia offline
- PyMuPDF - obsługa PDF

### ✓ Moduły działają poprawnie:
- AudioHandler - nagrywanie i przetwarzanie audio ✓
- WordHandler - integracja z Microsoft Word ✓
- TranscriptionModel - modele transkrypcji (w trakcie ładowania)

## Jak przetestować transkrypcję

### Metoda 1: Test manualny (szybki)
```bash
python manual_test.py
```
Ten test sprawdzi:
- AudioHandler
- Połączenie z Word
- Załadowanie modelu transkrypcji
- Pakiety językowe do tłumaczenia

### Metoda 2: Pełna aplikacja
```bash
python main.py
```

## Instrukcja użycia

### 1. Przygotowanie
- Otwórz Microsoft Word (nowy lub istniejący dokument)
- Upewnij się że mikrofon działa

### 2. Uruchomienie
```bash
python main.py
```

### 3. Konfiguracja
- Wybierz język:
  - **Polski** - 2 modele do wyboru (Small - szybszy, Medium - dokładniejszy)
  - **Angielski** - model faster-whisper
- Opcjonalnie: włącz automatyczne tłumaczenie (PL→EN/RU/UK)

### 4. Użycie
- Naciśnij **START**
- Trzymaj **LEWY SHIFT** i mów do mikrofonu
- Puść **SHIFT** aby zakończyć nagrywanie
- Tekst pojawi się w Word automatycznie

### 5. Zatrzymanie
- Naciśnij **"Zakończ nasłuchiwanie"**

## Rozwiązywanie problemów

### Problem: "Otwórz Word przed uruchomieniem"
**Rozwiązanie:**
1. Otwórz Microsoft Word
2. Utwórz nowy dokument lub otwórz istniejący
3. Uruchom ponownie `python main.py`

### Problem: Brak tekstu w Word
**Możliwe przyczyny:**
1. **Mikrofon nie działa** - sprawdź w ustawieniach Windows
2. **Za cicho mówisz** - mów głośniej i bliżej mikrofonu
3. **Model pobiera się** - pierwsze uruchomienie wymaga czasu (~3-10 min)
4. **Zbyt krótkie nagranie** - mów dłużej (min. 2-3 sekundy)

**Diagnostyka:**
```bash
python quick_test.py
```

### Problem: Tłumaczenie nie działa
**Rozwiązanie:**
```bash
python install_languages.py
```
To zainstaluje pakiety językowe dla tłumaczeń offline (PL→EN/RU/UK)

### Problem: Model się nie ładuje / błędy PyTorch
**Rozwiązanie:**
1. Zaktualizuj biblioteki:
```bash
pip install --upgrade torch transformers faster-whisper
```

2. Jeśli Python 3.13+, może być problem z kompatybilnością:
```bash
pip uninstall torch -y
pip install torch --index-url https://download.pytorch.org/whl/cpu
```

### Problem: "KeyError" lub błędy importu
**Rozwiązanie:**
```bash
pip install -r requirements.txt --force-reinstall
```

## Pierwszy raz może być wolno!

### Pobieranie modeli (pierwsze uruchomienie):
- **Model Polski Small**: ~500 MB
- **Model Polski Medium**: ~1.5 GB
- **Model Angielski**: ~150 MB
- **Pakiety językowe**: ~50 MB każdy

Modele pobierają się automatycznie z HuggingFace.
**Czas pobierania:** 3-15 minut (zależnie od internetu)

Po pobraniu modele są zapisane lokalnie i kolejne uruchomienia są szybkie!

## Testowanie komponetów osobno

### 1. Test tylko audio
```python
from audio_handler import AudioHandler
import numpy as np

audio = AudioHandler()
audio.start()

# Nagraj 2 sekundy
import time
frames = []
for _ in range(32):  # 2 sekundy
    data = audio.read()
    frames.append(data)
    time.sleep(0.0625)

audio.stop()

# Przetwórz
processed = audio.process_audio(frames)
print(f"Nagrano: {processed.shape} próbek")
```

### 2. Test tylko Word
```python
from word_handler import WordHandler

word = WordHandler()
if word.connect():
    word.insert_text("Test!")
    print("Tekst wstawiony")
else:
    print("Word nie jest otwarty")
```

### 3. Test tylko model transkrypcji
```python
from transcription_model import TranscriptionModel
import numpy as np

# Załaduj model (to może chwilę potrwać)
model = TranscriptionModel("polski", "1")

# Przygotuj audio (np. 1 sekunda ciszy)
audio = np.zeros(16000, dtype=np.float32)

# Transkrybuj
text = model.transcribe(audio, 16000)
print(f"Wynik: {text}")
```

## Wydajność

### Polecane ustawienia:
- **CPU (bez GPU)**: Model Polski Small
- **GPU NVIDIA**: Model Polski Medium
- **Słabe PC**: Model Angielski (faster-whisper)

### Czasy przetwarzania (przykładowo):
- 5 sekund mowy → 2-10 sekund transkrypcji (CPU)
- 5 sekund mowy → 1-3 sekundy transkrypcji (GPU)

## Problemy znane

### 1. Python 3.13 i PyTorch
PyTorch może mieć problemy z Python 3.13. Jeśli występują błędy:
- Użyj Python 3.11 lub 3.12
- LUB zainstaluj nightly build PyTorch

### 2. Windows Defender
Może blokować keyboard hook. Jeśli LEFT SHIFT nie działa:
- Dodaj Python do wyjątków Windows Defender
- Uruchom jako administrator

### 3. Mikrofon nie działa
W Windows 10/11:
1. Ustawienia → Prywatność → Mikrofon
2. Włącz "Zezwalaj aplikacjom na dostęp do mikrofonu"
3. Sprawdź czy Python ma uprawnienia

## Logi i debugging

Wszystkie operacje wyświetlają logi w konsoli:
- `Nagrywanie...` - LEFT SHIFT wciśnięty
- `Przetwarzanie...` - analizuje audio
- `Transkrypcja: <tekst>` - wynik transkrypcji

Jeśli nie widzisz tych logów, coś jest nie tak z:
- Obsługą klawiatury (keyboard)
- Modelem AI (transformers/whisper)
- AudioHandler (sounddevice)

## Kontakt i wsparcie

W razie problemów:
1. Uruchom `python manual_test.py` - pokaże gdzie jest problem
2. Sprawdź logi w konsoli
3. Sprawdź czy Word jest otwarty
4. Sprawdź czy mikrofon działa w innych aplikacjach

## Szybki checklist przed uruchomieniem

- [ ] Microsoft Word otwarty
- [ ] Mikrofon podłączony i działa
- [ ] Python 3.11+ zainstalowany
- [ ] Biblioteki zainstalowane (`pip install -r requirements.txt`)
- [ ] Internet połączony (pierwsze uruchomienie)
- [ ] Windows Defender nie blokuje Python
- [ ] Pierwszy raz? Poczekaj 5-10 minut na pobranie modeli

## Gotowe!

Jeśli wszystkie testy przeszły ✓, możesz używać aplikacji:
```bash
python main.py
```

**Trzymaj LEWY SHIFT i mów - tekst pojawi się w Word!**
