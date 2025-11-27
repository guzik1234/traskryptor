"""
Manualny test transkrypcji z symulowanym audio
"""
import numpy as np
import sys

print("="*70)
print("TEST MANUALNY TRANSKRYPCJI")
print("="*70)

# 1. Test AudioHandler
print("\n[KROK 1] Testowanie AudioHandler...")
try:
    from audio_handler import AudioHandler
    
    audio = AudioHandler(rate=16000)
    print("✓ AudioHandler utworzony (rate=16000)")
    
    # Symuluj dane audio (1 sekunda ciszy)
    test_data = np.zeros((16000, 1), dtype=np.int16)
    frames = [test_data[i:i+1024] for i in range(0, len(test_data), 1024)]
    
    processed = audio.process_audio(frames)
    print(f"✓ Przetwarzanie działa")
    print(f"  Input: {len(frames)} frames x {frames[0].shape}")
    print(f"  Output: shape={processed.shape}, dtype={processed.dtype}")
    print(f"  Zakres wartości: [{processed.min():.3f}, {processed.max():.3f}]")
    
except Exception as e:
    print(f"✗ BŁĄD AudioHandler: {e}")
    sys.exit(1)

# 2. Test WordHandler
print("\n[KROK 2] Testowanie WordHandler...")
word_available = False
try:
    from word_handler import WordHandler
    
    word = WordHandler()
    print("✓ WordHandler utworzony")
    
    if word.connect():
        print("✓ Połączono z Word!")
        word_available = True
        
        # Informacje o dokumencie
        try:
            doc_name = word.doc.Name
            print(f"  Dokument: {doc_name}")
        except:
            print("  Dokument: <otwarty>")
            
        # Test wstawienia
        print("\n  Testuję wstawienie tekstu...")
        word.insert_text("[TEST AUTOMATYCZNY]")
        print("  ✓ Tekst wstawiony - sprawdź dokument Word")
        
    else:
        print("⚠ Word NIE jest otwarty")
        print("  MUSISZ otworzyć dokument Word przed uruchomieniem transkrypcji!")
        
except Exception as e:
    print(f"✗ BŁĄD WordHandler: {e}")
    import traceback
    traceback.print_exc()

# 3. Test modelu transkrypcji (Polski)
print("\n[KROK 3] Testowanie modelu transkrypcji (Polski - Small)...")
print("UWAGA: Pierwsze uruchomienie pobierze model (~500MB) - może potrwać kilka minut")
try:
    from transcription_model import TranscriptionModel
    
    print("\nŁadowanie modelu polskiego...")
    model = TranscriptionModel("polski", "1")
    print("✓ Model załadowany")
    print(f"  Urządzenie: {model.device}")
    print(f"  Faster Whisper: {model.use_faster_whisper}")
    
    # Test na cichym audio (powinno zwrócić pusty string lub krótki wynik)
    print("\nTest transkrypcji na cichym audio (1 sek)...")
    silent_audio = np.zeros(16000, dtype=np.float32)
    
    result = model.transcribe(silent_audio, 16000)
    print(f"✓ Transkrypcja wykonana: '{result}'")
    
    if not result or not result.strip():
        print("  ✓ Poprawnie - cisza nie dała tekstu")
    else:
        print(f"  ⚠ Nieoczekiwany wynik: '{result}'")
    
except Exception as e:
    print(f"✗ BŁĄD modelu: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# 4. Test tłumaczenia
print("\n[KROK 4] Testowanie tłumaczenia...")
try:
    import argostranslate.package
    import argostranslate.translate
    
    print("✓ argostranslate zaimportowany")
    
    # Sprawdź zainstalowane języki
    installed = argostranslate.translate.get_installed_languages()
    print(f"  Zainstalowanych języków: {len(installed)}")
    
    if len(installed) == 0:
        print("\n  ⚠⚠⚠ BRAK ZAINSTALOWANYCH PAKIETÓW JĘZYKOWYCH!")
        print("  Tłumaczenie NIE będzie działać!")
        print("\n  Aby zainstalować pakiety językowe:")
        print("    python install_languages.py")
    else:
        print("\n  Dostępne języki:")
        for lang in installed:
            translations = [t.code for t in lang.translations_from]
            print(f"    - {lang.code} ({lang.name}) → {translations}")
        
        # Test tłumaczenia PL→EN
        print("\n  Test tłumaczenia PL→EN...")
        test_text = "To jest test transkrypcji"
        
        try:
            translated = argostranslate.translate.translate(test_text, "pl", "en")
            print(f"  ✓ '{test_text}'")
            print(f"    → '{translated}'")
        except Exception as e:
            print(f"  ⚠ Błąd tłumaczenia: {e}")
            
except Exception as e:
    print(f"⚠ Tłumaczenie niedostępne: {e}")

# Podsumowanie
print("\n" + "="*70)
print("PODSUMOWANIE TESTÓW")
print("="*70)

if word_available:
    print("\n✓✓✓ WSZYSTKO GOTOWE DO DZIAŁANIA! ✓✓✓")
    print("\nJak używać:")
    print("1. python main.py")
    print("2. Wybierz język (Polski lub Angielski)")
    print("3. Opcjonalnie włącz tłumaczenie automatyczne")
    print("4. Naciśnij START")
    print("5. Trzymaj LEWY SHIFT i mów do mikrofonu")
    print("6. Tekst pojawi się w Word")
else:
    print("\n⚠⚠⚠ WYMAGANE: Otwórz dokument Word!")
    print("\nPo otwarciu Word:")
    print("1. python main.py")
    print("2. Wybierz język i naciśnij START")

print("\nPierwsze uruchomienie pobierze modele AI (może potrwać)")
print("="*70)
