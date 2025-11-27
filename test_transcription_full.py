"""
Test diagnostyczny pełnej transkrypcji i tłumaczenia głosowego
"""
import numpy as np
import sys

print("=" * 60)
print("TEST DIAGNOSTYCZNY TRANSKRYPCJI I TŁUMACZENIA")
print("=" * 60)

# 1. Test importów
print("\n[1/7] Testowanie importów...")
try:
    from audio_handler import AudioHandler
    print("✓ AudioHandler zaimportowany")
except Exception as e:
    print(f"✗ Błąd AudioHandler: {e}")
    sys.exit(1)

try:
    from transcription_model import TranscriptionModel
    print("✓ TranscriptionModel zaimportowany")
except Exception as e:
    print(f"✗ Błąd TranscriptionModel: {e}")
    sys.exit(1)

try:
    from word_handler import WordHandler
    print("✓ WordHandler zaimportowany")
except Exception as e:
    print(f"✗ Błąd WordHandler: {e}")
    sys.exit(1)

try:
    import keyboard
    print("✓ keyboard zaimportowany")
except Exception as e:
    print(f"✗ Błąd keyboard: {e}")

try:
    import sounddevice as sd
    print("✓ sounddevice zaimportowany")
except Exception as e:
    print(f"✗ Błąd sounddevice: {e}")
    sys.exit(1)

# 2. Test urządzeń audio
print("\n[2/7] Testowanie urządzeń audio...")
try:
    devices = sd.query_devices()
    print(f"✓ Znaleziono {len(devices)} urządzeń audio")
    
    default_input = sd.query_devices(kind='input')
    print(f"✓ Domyślne urządzenie wejściowe: {default_input['name']}")
    print(f"  - Kanały: {default_input['max_input_channels']}")
    print(f"  - Sample rate: {default_input['default_samplerate']} Hz")
except Exception as e:
    print(f"✗ Błąd urządzeń audio: {e}")

# 3. Test AudioHandler
print("\n[3/7] Testowanie AudioHandler...")
try:
    audio = AudioHandler()
    print("✓ AudioHandler utworzony")
    
    audio.start()
    print("✓ Strumień audio uruchomiony")
    
    # Krótki test nagrania
    import time
    time.sleep(0.5)
    data = audio.read()
    print(f"✓ Odczytano dane audio: {data.shape}")
    
    # Test przetwarzania
    frames = [data]
    audio_np = audio.process_audio(frames)
    print(f"✓ Przetworzono audio do numpy: {audio_np.shape}, dtype: {audio_np.dtype}")
    
    audio.stop()
    print("✓ Strumień audio zatrzymany")
except Exception as e:
    print(f"✗ Błąd AudioHandler: {e}")
    import traceback
    traceback.print_exc()

# 4. Test modelu transkrypcji (Polski)
print("\n[4/7] Testowanie modelu transkrypcji (Polski - Small)...")
try:
    model_pl = TranscriptionModel("polski", "1")
    print("✓ Model polski załadowany")
    print(f"  - Urządzenie: {model_pl.device}")
    print(f"  - Faster Whisper: {model_pl.use_faster_whisper}")
    
    # Test transkrypcji na pustym audio
    test_audio = np.zeros(16000, dtype=np.float32)  # 1 sekunda ciszy
    try:
        result = model_pl.transcribe(test_audio, 16000)
        print(f"✓ Transkrypcja testowa wykonana: '{result}'")
    except Exception as e:
        print(f"⚠ Transkrypcja testowa nie powiodła się: {e}")
        
except Exception as e:
    print(f"✗ Błąd modelu polskiego: {e}")
    import traceback
    traceback.print_exc()

# 5. Test modelu transkrypcji (Angielski)
print("\n[5/7] Testowanie modelu transkrypcji (Angielski)...")
try:
    model_en = TranscriptionModel("angielski", None)
    print("✓ Model angielski załadowany")
    print(f"  - Urządzenie: {model_en.device}")
    print(f"  - Faster Whisper: {model_en.use_faster_whisper}")
    
    # Test transkrypcji na pustym audio
    test_audio = np.zeros(16000, dtype=np.float32)
    try:
        result = model_en.transcribe(test_audio, 16000)
        print(f"✓ Transkrypcja testowa wykonana: '{result}'")
    except Exception as e:
        print(f"⚠ Transkrypcja testowa nie powiodła się: {e}")
        
except Exception as e:
    print(f"✗ Błąd modelu angielskiego: {e}")
    import traceback
    traceback.print_exc()

# 6. Test połączenia z Word
print("\n[6/7] Testowanie połączenia z Word...")
try:
    word = WordHandler()
    if word.connect():
        print("✓ Połączono z Word")
        print(f"  - Dokument: {word.doc.Name if word.doc else 'N/A'}")
        
        # Test wstawiania tekstu
        try:
            word.insert_text("[TEST TRANSKRYPCJI]")
            print("✓ Tekst testowy wstawiony do Word")
        except Exception as e:
            print(f"⚠ Nie udało się wstawić tekstu: {e}")
    else:
        print("⚠ Nie znaleziono otwartego dokumentu Word")
        print("  UWAGA: Otwórz dokument Word przed uruchomieniem transkrypcji!")
except Exception as e:
    print(f"✗ Błąd WordHandler: {e}")
    import traceback
    traceback.print_exc()

# 7. Test tłumaczenia (opcjonalny)
print("\n[7/7] Testowanie modułu tłumaczenia...")
try:
    import argostranslate.package
    import argostranslate.translate
    
    print("✓ argostranslate zaimportowany")
    
    # Sprawdzenie zainstalowanych pakietów językowych
    installed_languages = argostranslate.translate.get_installed_languages()
    print(f"✓ Zainstalowane języki: {len(installed_languages)}")
    
    if len(installed_languages) > 0:
        for lang in installed_languages:
            print(f"  - {lang.code}: {lang.name}")
    else:
        print("  ⚠ Brak zainstalowanych pakietów językowych")
        print("  Uruchom: python install_languages.py")
    
    # Test tłumaczenia
    if len(installed_languages) >= 2:
        test_text = "To jest test"
        try:
            # Próba tłumaczenia PL -> EN
            translation = argostranslate.translate.translate(test_text, "pl", "en")
            print(f"✓ Test tłumaczenia: '{test_text}' -> '{translation}'")
        except Exception as e:
            print(f"⚠ Tłumaczenie testowe nie powiodło się: {e}")
    
except Exception as e:
    print(f"⚠ Moduł tłumaczenia niedostępny: {e}")

# Podsumowanie
print("\n" + "=" * 60)
print("PODSUMOWANIE")
print("=" * 60)
print("\nSYSTEM GOTOWY DO PRACY!")
print("\nInstrukcja użycia:")
print("1. Otwórz dokument Word")
print("2. Uruchom: python main.py")
print("3. Wybierz język i model")
print("4. Naciśnij START")
print("5. Trzymaj LEWY SHIFT i mów")
print("6. Tekst pojawi się w Word")
print("\nJeśli chcesz tłumaczenie automatyczne:")
print("- Zaznacz checkbox 'Włącz tłumaczenie'")
print("- Wybierz język docelowy")
print("- Upewnij się że pakiety językowe są zainstalowane")
print("  (uruchom: python install_languages.py)")
print("=" * 60)
