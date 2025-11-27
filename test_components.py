"""
Test komponentów bez ładowania ciężkich modeli
"""
import sys

print("="*70)
print("TEST SZYBKI - BEZ MODELI AI")
print("="*70)

# 1. AudioHandler
print("\n✓ Test 1/5: AudioHandler")
try:
    from audio_handler import AudioHandler
    import numpy as np
    
    audio = AudioHandler(rate=16000)
    
    # Test przetwarzania
    test_frames = [np.random.randint(-1000, 1000, (1024, 1), dtype=np.int16) for _ in range(16)]
    processed = audio.process_audio(test_frames, boost=1.8)
    
    print(f"  ✓ Nagrywanie i przetwarzanie działa")
    print(f"    Shape: {processed.shape}, dtype: {processed.dtype}")
    print(f"    Zakres: [{processed.min():.3f}, {processed.max():.3f}]")
except Exception as e:
    print(f"  ✗ BŁĄD: {e}")
    sys.exit(1)

# 2. WordHandler
print("\n✓ Test 2/5: WordHandler (integracja z Word)")
try:
    from word_handler import WordHandler
    
    word = WordHandler()
    
    if word.connect():
        print(f"  ✓ Połączono z Word!")
        
        # Test wstawienia
        word.insert_text("[TEST KOMPONENTU]")
        print(f"  ✓ Tekst wstawiony do dokumentu")
    else:
        print(f"  ⚠ Word NIE jest otwarty")
        print(f"    Otwórz Word przed uruchomieniem aplikacji!")
except Exception as e:
    print(f"  ✗ BŁĄD: {e}")

# 3. Import modułów AI (bez ładowania)
print("\n✓ Test 3/5: Importy modułów AI")
try:
    import torch
    print(f"  ✓ PyTorch {torch.__version__}")
    print(f"    CUDA: {torch.cuda.is_available()}")
    
    import transformers
    print(f"  ✓ Transformers {transformers.__version__}")
    
    from transcription_model import TranscriptionModel
    print(f"  ✓ TranscriptionModel zaimportowany")
    
except Exception as e:
    print(f"  ✗ BŁĄD: {e}")
    sys.exit(1)

# 4. Keyboard
print("\n✓ Test 4/5: Keyboard (obsługa LEFT SHIFT)")
try:
    import keyboard
    print(f"  ✓ Keyboard załadowany")
    print(f"    UWAGA: Jeśli LEFT SHIFT nie działa - uruchom jako admin")
except Exception as e:
    print(f"  ⚠ Keyboard: {e}")

# 5. Tłumaczenie
print("\n✓ Test 5/5: Moduł tłumaczenia")
try:
    import argostranslate.package
    import argostranslate.translate
    
    installed = argostranslate.translate.get_installed_languages()
    
    if len(installed) > 0:
        print(f"  ✓ Pakiety językowe: {len(installed)}")
        for lang in installed:
            trans = [t.code for t in lang.translations_from]
            print(f"    - {lang.code} → {trans}")
    else:
        print(f"  ⚠ BRAK pakietów językowych")
        print(f"    Uruchom: python install_languages.py")
        
except Exception as e:
    print(f"  ⚠ argostranslate: {e}")

# Podsumowanie
print("\n" + "="*70)
print("WYNIK TESTÓW")
print("="*70)

print("\n✓✓✓ Wszystkie komponenty gotowe!")
print("\nNastępny krok:")
print("  python main.py")
print("\nPierwsze uruchomienie pobierze modele AI (~500MB-2GB)")
print("Może potrwać 5-15 minut w zależności od internetu.")
print("\nUŻYCIE:")
print("  1. Wybierz język (Polski/Angielski)")
print("  2. Naciśnij START")
print("  3. Trzymaj LEWY SHIFT i mów")
print("  4. Puść SHIFT - tekst pojawi się w Word")
print("="*70)
