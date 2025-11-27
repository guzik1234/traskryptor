"""Test modułów transkrypcji"""
print("Sprawdzam moduły transkrypcji...\n")

modules = [
    ("speech_recognition", "SpeechRecognition"),
    ("pyaudio", "PyAudio"),
    ("numpy", "NumPy"),
    ("whisper", "OpenAI Whisper"),
    ("torch", "PyTorch"),
    ("win32com.client", "pywin32"),
    ("keyboard", "keyboard"),
]

missing = []
for module, name in modules:
    try:
        __import__(module)
        print(f"✅ {name}")
    except ImportError as e:
        print(f"❌ {name} - BRAK")
        missing.append(name)

if missing:
    print(f"\n⚠ Brakujące moduły: {', '.join(missing)}")
    print("\nInstaluj:")
    for m in missing:
        if m == "SpeechRecognition":
            print("  pip install SpeechRecognition")
        elif m == "PyAudio":
            print("  pip install pipwin")
            print("  pipwin install pyaudio")
        elif m == "OpenAI Whisper":
            print("  pip install openai-whisper")
        elif m == "PyTorch":
            print("  pip install torch")
        else:
            print(f"  pip install {m.lower()}")
else:
    print("\n✅ Wszystkie moduły zainstalowane!")
