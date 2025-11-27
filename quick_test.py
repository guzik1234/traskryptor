"""
Szybki test podstawowych funkcji transkrypcji
"""
import sys

print("="*60)
print("SZYBKI TEST TRANSKRYPCJI")
print("="*60)

# Test 1: Audio Handler
print("\n[1/4] Test AudioHandler...")
try:
    from audio_handler import AudioHandler
    import numpy as np
    
    audio = AudioHandler()
    print("✓ AudioHandler utworzony")
    
    # Test przetwarzania
    test_frames = [np.random.randint(-1000, 1000, (1024, 1), dtype=np.int16) for _ in range(10)]
    processed = audio.process_audio(test_frames)
    print(f"✓ Audio przetwarzanie działa: shape={processed.shape}, dtype={processed.dtype}")
    
except Exception as e:
    print(f"✗ AudioHandler BŁĄD: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 2: Word Handler
print("\n[2/4] Test WordHandler...")
try:
    from word_handler import WordHandler
    
    word = WordHandler()
    print("✓ WordHandler utworzony")
    
    if word.connect():
        print("✓ Połączono z Word!")
        print(f"  Dokument: {word.doc.Name if hasattr(word.doc, 'Name') else 'N/A'}")
        
        # Test wstawienia
        word.insert_text("[TEST - możesz usunąć]")
        print("✓ Test wstawienia tekstu zakończony")
    else:
        print("⚠ Word nie jest otwarty - otwórz dokument przed testowaniem transkrypcji")
        
except Exception as e:
    print(f"✗ WordHandler BŁĄD: {e}")
    import traceback
    traceback.print_exc()

# Test 3: Import modelu (bez ładowania)
print("\n[3/4] Test importu TranscriptionModel...")
try:
    from transcription_model import TranscriptionModel
    print("✓ TranscriptionModel zaimportowany")
    
    # Sprawdź czy torch działa
    import torch
    print(f"✓ PyTorch {torch.__version__}")
    print(f"  CUDA dostępna: {torch.cuda.is_available()}")
    
except Exception as e:
    print(f"✗ TranscriptionModel BŁĄD: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 4: Tłumaczenie
print("\n[4/4] Test modułu tłumaczenia...")
try:
    import argostranslate.package
    import argostranslate.translate
    
    print("✓ argostranslate zaimportowany")
    
    installed = argostranslate.translate.get_installed_languages()
    print(f"  Zainstalowane języki: {len(installed)}")
    
    if len(installed) > 0:
        for lang in installed:
            print(f"    - {lang.code}: {lang.name}")
            
        # Sprawdź dostępne pary
        pairs = []
        for src in installed:
            for trans in src.translations_from:
                pairs.append(f"{src.code}→{trans.code}")
        
        if pairs:
            print(f"  Dostępne pary tłumaczeń: {', '.join(pairs[:5])}")
    else:
        print("  ⚠ BRAK zainstalowanych pakietów językowych!")
        print("  Uruchom: python install_languages.py")
        
except Exception as e:
    print(f"⚠ Tłumaczenie: {e}")

# Podsumowanie
print("\n" + "="*60)
print("PODSUMOWANIE")
print("="*60)
print("\n✓ Podstawowe moduły działają poprawnie")
print("\nAby przetestować PEŁNĄ transkrypcję:")
print("1. Otwórz dokument Word")
print("2. Uruchom: python main.py")
print("3. Wybierz język (Polski lub Angielski)")
print("4. Naciśnij START")
print("5. Trzymaj LEWY SHIFT i mów do mikrofonu")
print("6. Tekst pojawi się w Word")
print("\nUWAGA: Pierwsze uruchomienie pobierze modele AI (~500MB-2GB)")
print("="*60)
