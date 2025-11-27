"""
Test transkrypcji na żywym audio (LIVE TEST)
Ten skrypt nagra 3 sekundy i przetranksrybuje
"""
import sys
import time
import numpy as np

print("="*70)
print("TEST LIVE - TRANSKRYPCJA MOWY")
print("="*70)

# Inicjalizacja
print("\n[1/4] Inicjalizacja audio...")
try:
    from audio_handler import AudioHandler
    
    audio = AudioHandler(rate=16000)
    audio.start()
    print("✓ Mikrofon gotowy")
    
except Exception as e:
    print(f"✗ Błąd audio: {e}")
    sys.exit(1)

# Ładowanie modelu
print("\n[2/4] Ładowanie modelu transkrypcji...")
print("UWAGA: Pierwsze uruchomienie pobierze model (~500MB)")
try:
    from transcription_model import TranscriptionModel
    
    # Możesz zmienić na "angielski" jeśli wolisz
    model = TranscriptionModel("polski", "1")
    print("✓ Model załadowany")
    
except Exception as e:
    print(f"✗ Błąd modelu: {e}")
    audio.stop()
    sys.exit(1)

# Nagranie
print("\n[3/4] Nagrywanie...")
print("\n" + "="*70)
print("🎤 MÓWI TERAZ PRZEZ 3 SEKUNDY!")
print("="*70)

frames = []
start_time = time.time()
duration = 3.0  # 3 sekundy

try:
    while time.time() - start_time < duration:
        data = audio.read()
        frames.append(data)
        
        elapsed = time.time() - start_time
        remaining = duration - elapsed
        print(f"\rNagrywanie: {elapsed:.1f}/{duration}s (pozostało: {remaining:.1f}s)", end='', flush=True)
        
    print("\n✓ Nagranie zakończone")
    
except KeyboardInterrupt:
    print("\n⚠ Przerwano przez użytkownika")
    audio.stop()
    sys.exit(0)

# Przetwarzanie i transkrypcja
print("\n[4/4] Transkrypcja...")
try:
    # Przetwórz audio
    audio_np = audio.process_audio(frames, boost=1.8)
    print(f"✓ Audio przetworzone: {len(audio_np)} próbek")
    
    # Transkrybuj
    print("⏳ Trwa transkrypcja... (może potrwać 5-20 sekund)")
    text = model.transcribe(audio_np, 16000)
    
    # Wynik
    print("\n" + "="*70)
    print("WYNIK TRANSKRYPCJI:")
    print("="*70)
    
    if text and text.strip():
        print(f"\n📝 \"{text}\"\n")
        print("✅ TRANSKRYPCJA DZIAŁA!")
    else:
        print("\n⚠ Brak tekstu (za cicho? za krótko?)")
        print("Spróbuj ponownie i mów głośniej przez całe 3 sekundy")
    
    print("="*70)
    
except Exception as e:
    print(f"✗ Błąd transkrypcji: {e}")
    import traceback
    traceback.print_exc()
    
finally:
    audio.stop()
    print("\n✓ Test zakończony")

print("\n" + "="*70)
print("Jeśli transkrypcja działa, możesz uruchomić pełną aplikację:")
print("  python main.py")
print("="*70)
