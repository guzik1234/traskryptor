import pyaudio
import win32com.client
import numpy as np
import keyboard
from transformers import AutoProcessor, AutoModelForSpeechSeq2Seq
import torch
import time


def choose_model():
    print("Wybierz model do transkrypcji:")
    print("1 — Small (szybszy, mniej dokładny)")
    print("2 — Medium (wolniejszy, dokładniejszy)")
    while True:
        choice = input("Podaj 1 lub 2: ").strip()
        if choice == "1":
            return "bardsai/whisper-small-pl"
        elif choice == "2":
            return "bardsai/whisper-medium-pl-v2"
        else:
            print("Niepoprawny wybór, spróbuj ponownie.")


def main():
    print("Initializing...")

    torch.set_num_threads(12)

    model_id = choose_model()
    print(f"Ładowanie modelu '{model_id}'...")

    try:
        device = "cuda" if torch.cuda.is_available() else "cpu"
        processor = AutoProcessor.from_pretrained(model_id)
        model = AutoModelForSpeechSeq2Seq.from_pretrained(model_id).to(device)
    except Exception as e:
        print("Błąd ładowania modelu:", e)
        return

    # --- Mikrofon ---
    p = pyaudio.PyAudio()
    RATE = 16000
    CHUNK = 1024

    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    # --- Word ---
    try:
        word = win32com.client.GetActiveObject("Word.Application")
        doc = word.ActiveDocument
    except:
        print("Otwórz Worda przed uruchomieniem skryptu.")
        stream.stop_stream()
        stream.close()
        p.terminate()
        return

    print("READY — wciśnij i trzymaj Lewy Shift, by nagrywać.")

    while True:
        keyboard.wait("left shift")
        print("Nagrywanie... (puść Lewy Shift, by zakończyć)")

        frames = []
        while keyboard.is_pressed("left shift"):
            data = stream.read(CHUNK, exception_on_overflow=False)
            frames.append(data)

        print("Przetwarzanie nagrania...")

        if not frames:
            print("Nie przechwycono dźwięku.")
            continue

        # --- Audio processing ---
        audio_bytes = b"".join(frames)
        audio_np = np.frombuffer(audio_bytes, dtype=np.int16).astype(np.float32)
        BOOST = 1.8
        audio_np *= BOOST
        audio_np = np.clip(audio_np, -32768, 32767)
        audio_np /= 32768.0

        # --- Transcription ---
        try:
            inputs = processor(audio_np, sampling_rate=RATE, return_tensors="pt").to(device)

            gen_cfg = model.generation_config
            gen_cfg.suppress_tokens = []
            gen_cfg.begin_suppress_tokens = [220, 50257]
            gen_cfg.forced_decoder_ids = None
            gen_cfg.forced_bos_token_id = None
            gen_cfg.forced_eos_token_id = None
            gen_cfg.pad_token_id = processor.tokenizer.eos_token_id

            inputs["attention_mask"] = torch.ones(
                (inputs["input_features"].shape[0], inputs["input_features"].shape[2]),
                dtype=torch.long
            ).to(device)

            generated_ids = model.generate(
                **inputs,
                generation_config=gen_cfg,
                max_new_tokens=256
            )

            text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0].strip()
            print("Transkrypcja:", text)

        except Exception as e:
            print("Błąd transkrypcji: ", e)
            text = ""

        if text:
            word.Selection.InsertAfter(text)
            word.Selection.MoveRight()

        time.sleep(0.1)


if __name__ == "__main__":
    main()
