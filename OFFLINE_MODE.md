# Praca Offline - Analiza Bibliotek

## Podsumowanie
**Aplikacja może działać w pełni offline** po odpowiednim przygotowaniu.

## Status bibliotek

### ✅ Pełna praca offline
1. **sounddevice** - lokalna obsługa audio
2. **librosa** - lokalne przetwarzanie plików audio
3. **SpeechRecognition** - framework, działa lokalnie
4. **numpy** - obliczenia numeryczne, lokalne
5. **keyboard** - obsługa klawiatury, lokalne
6. **pywin32** - automatyzacja Windows, lokalne
7. **python-docx** - tworzenie dokumentów Word, lokalne
8. **docx2pdf** - konwersja dokumentów, lokalne (wymaga Word)

### ⚠️ Wymaga internetu tylko przy pierwszym użyciu
1. **openai-whisper** - pobiera modele przy pierwszym użyciu (~140MB dla small, ~460MB dla medium)
   - Po pobraniu: **100% offline**
   - Modele zapisywane w: `~/.cache/whisper/`

2. **faster-whisper** - pobiera modele przy pierwszym użyciu (~140MB dla base.en)
   - Po pobraniu: **100% offline**
   - Modele zapisywane w: `~/.cache/huggingface/`

3. **transformers** - pobiera modele przy pierwszym użyciu
   - Po pobraniu: **100% offline**
   - Modele zapisywane w: `~/.cache/huggingface/`

4. **torch** - pobiera przy instalacji, potem offline
   - Po instalacji: **100% offline**

5. **argostranslate** - framework offline, ale pakiety językowe wymagają pobrania
   - Po pobraniu pakietów: **100% offline**
   - Pakiety zapisywane w: `~/.local/share/argos-translate/packages/`

6. **sentencepiece** - tokenizacja, działa offline po instalacji
   - Po instalacji: **100% offline**

## Przygotowanie do pracy offline

### Krok 1: Instalacja pakietów Python
```bash
pip install -r requirements.txt
```
**Wymaga internetu** - jednorazowo

### Krok 2: Pobieranie modeli transkrypcji
Uruchom aplikację i użyj każdej funkcji raz:

```bash
# Transkrypcja polska - pobierze bardsai/whisper-small-pl (~140MB)
python main.py
# Wybierz "Transkrypcja na żywo" → Polski → Start → Zatrzymaj

# Transkrypcja angielska - pobierze faster-whisper-base.en (~140MB)
python main.py
# Wybierz "Transkrypcja na żywo" → Angielski → Start → Zatrzymaj
```

### Krok 3: Instalacja pakietów językowych dla tłumaczenia
```bash
python install_languages.py
```
Ten skrypt pobierze:
- `translate-pl_en` (~40MB) - Polski → Angielski
- `translate-pl_ru` (~40MB) - Polski → Rosyjski  
- `translate-pl_uk` (~40MB) - Polski → Ukraiński

**Łącznie:** ~120MB

## Całkowity rozmiar pobrań dla pełnej pracy offline

| Komponent | Rozmiar | Opis |
|-----------|---------|------|
| Pakiety Python | ~2-3GB | torch, transformers, etc. |
| Model polski small | ~140MB | bardsai/whisper-small-pl |
| Model angielski base | ~140MB | faster-whisper-base.en |
| Pakiety tłumaczenia | ~120MB | pl→en, pl→ru, pl→uk |
| **RAZEM** | **~2.4-3.4GB** | Jednorazowe pobranie |

## Po przygotowaniu

✅ **Transkrypcja z pliku audio** - 100% offline
✅ **Transkrypcja na żywo** - 100% offline
✅ **Tłumaczenie w transkrypcji** - 100% offline
✅ **Tłumaczenie dokumentów** - 100% offline

## Lokalizacje danych

### Windows
- Modele Whisper: `C:\Users\<user>\.cache\whisper\`
- Modele HuggingFace: `C:\Users\<user>\.cache\huggingface\`
- Pakiety ArgosTranslate: `C:\Users\<user>\.local\share\argos-translate\packages\`

### Backup dla pracy offline
Jeśli chcesz przenieść aplikację na komputer bez internetu:

1. Zainstaluj wszystko na komputerze Z internetem
2. Skopiuj foldery:
   - `.cache\whisper\`
   - `.cache\huggingface\`
   - `.local\share\argos-translate\`
3. Przenieś na komputer bez internetu do tych samych lokalizacji
4. Aplikacja będzie działać w pełni offline

## Weryfikacja pracy offline

Test 1: Transkrypcja
```bash
# Wyłącz internet
python main.py
# Użyj "Transkrypcja z pliku audio" lub "Transkrypcja na żywo"
# Powinno działać bez błędów
```

Test 2: Tłumaczenie
```bash
# Wyłącz internet (po pobraniu pakietów językowych!)
python main.py
# Użyj "Tłumaczenie dokumentów"
# Powinno działać bez błędów
```

## Uwagi
- Microsoft Word musi być zainstalowany (lokalne)
- Pierwsze użycie każdej funkcji wymaga internetu do pobrania modeli
- Po pobraniu wszystkich modeli: **pełna praca offline**
- ArgosTranslate to lokalna biblioteka tłumaczenia (nie Google Translate!)
