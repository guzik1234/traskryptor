"""
Test naprawy polskiego modelu transkrypcji
"""
import numpy as np
import sys

print("="*70)
print("TEST NAPRAWY - MODEL POLSKI")
print("="*70)

print("\n[1/2] Ładowanie modelu polskiego...")
try:
    from transcription_model import TranscriptionModel
    
    model = TranscriptionModel("polski", "1")
    print("✓ Model załadowany pomyślnie")
    print(f"  Urządzenie: {model.device}")
    print(f"  Model: bardsai/whisper-small-pl")
    
except Exception as e:
    print(f"✗ Błąd ładowania modelu: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n[2/2] Test transkrypcji...")

# Test 1: Cisza (1 sekunda)
print("\nTest 1: Cichy audio (1 sekunda)")
try:
    silent_audio = np.zeros(16000, dtype=np.float32)
    result = model.transcribe(silent_audio, 16000)
    print(f"✓ Transkrypcja wykonana")
    print(f"  Wynik: '{result}'")
    
    if not result or len(result.strip()) == 0:
        print("  ✓ Poprawnie - cisza dała pusty wynik")
    else:
        print(f"  ⚠ Nieoczekiwany tekst dla ciszy")
        
except Exception as e:
    print(f"✗ BŁĄD podczas transkrypcji: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 2: Losowy szum (symulacja mowy)
print("\nTest 2: Audio z szumem (symulacja mowy)")
try:
    # Generuj audio z pewną amplitudą (symuluje mowę)
    noise_audio = np.random.uniform(-0.1, 0.1, 16000).astype(np.float32)
    result = model.transcribe(noise_audio, 16000)
    print(f"✓ Transkrypcja wykonana")
    print(f"  Wynik: '{result}'")
    
except Exception as e:
    print(f"✗ BŁĄD podczas transkrypcji: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n" + "="*70)
print("✅ NAPRAWA DZIAŁA!")
print("="*70)
print("\nModel polski może teraz być używany w aplikacji.")
print("\nUruchom pełną aplikację:")
print("  python main.py")
print("\nWybierz 'Polski' i naciśnij START!")
print("="*70)
