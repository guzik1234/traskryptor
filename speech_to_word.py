import pyaudio
import win32com.client
import sys
import select
import numpy as np
import webrtcvad
import collections
from transformers import AutoProcessor, AutoModelForSpeechSeq2Seq
import torch


def main():
    print("Initializing...")

    # --- Configure PyTorch CPU Threads ---
    torch.set_num_threads(12)
    print(f"Set PyTorch CPU threads to: {torch.get_num_threads()}")

    # Load Whisper model
    model_id = "bardsai/whisper-small-pl"
    print(f"Loading model '{model_id}' ...")

    try:
        device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"Using device: {device}")

        processor = AutoProcessor.from_pretrained(model_id)
        model = AutoModelForSpeechSeq2Seq.from_pretrained(model_id).to(device)

    except Exception as e:
        print(f"Error loading model: {e}")
        return

    # Initialize PyAudio
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=16000,
                    input=True,
                    frames_per_buffer=1024)

    # Connect to Word
    try:
        word = win32com.client.GetActiveObject("Word.Application")
        doc = word.ActiveDocument
    except:
        print("Error: Word not found.")
        stream.stop_stream()
        stream.close()
        p.terminate()
        return

    print("Speak now...")

    # --- VAD Setup ---
    vad = webrtcvad.Vad(3)
    SAMPLE_RATE = 16000
    FRAME_MS = 30
    FRAME_SIZE = int(SAMPLE_RATE * FRAME_MS / 1000)
    BYTES_PER_FRAME = FRAME_SIZE * 2

    SILENCE_TIMEOUT_MS = 1200
    MIN_SPEECH_MS = 400

    frames_buffer = collections.deque()
    speech_frames = []
    silence_after_speech = 0
    triggered = False

    while True:
        data = stream.read(1024, exception_on_overflow=False)
        frames_buffer.append(data)

        # Build full 30 ms frame for VAD
        while len(b''.join(frames_buffer)) >= BYTES_PER_FRAME:
            buf = b''.join(frames_buffer)
            frame = buf[:BYTES_PER_FRAME]
            rest = buf[BYTES_PER_FRAME:]
            frames_buffer.clear()
            frames_buffer.append(rest)

            try:
                is_speech = vad.is_speech(frame, SAMPLE_RATE)
            except Exception:
                is_speech = False

            if triggered:
                speech_frames.append(frame)

                if not is_speech:
                    silence_after_speech += 1
                    if silence_after_speech * FRAME_MS > SILENCE_TIMEOUT_MS:
                        # End of phrase
                        audio = b''.join(speech_frames)
                        duration_ms = len(audio) / (SAMPLE_RATE * 2) * 1000

                        triggered = False
                        speech_frames = []
                        silence_after_speech = 0

                        if duration_ms >= MIN_SPEECH_MS:
                            print(f"Transcribing ({duration_ms:.0f} ms)...")
                            audio_np = np.frombuffer(audio, dtype=np.int16).astype(np.float32) / 32768.0

                            try:
                                inputs = processor(audio_np, sampling_rate=SAMPLE_RATE,
                                                   return_tensors="pt").to(device)

                                generated_ids = model.generate(
                                    **inputs,
                                    max_new_tokens=128
                                )

                                text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0].strip()
                                print("Result:", text)

                            except Exception as e:
                                print("Transcription error:", e)
                                text = ""

                            if text:
                                word.Selection.InsertAfter(text + " ")
                                word.Selection.MoveRight()

                else:
                    silence_after_speech = 0

            else:
                if is_speech:
                    print("Speech detected.")
                    triggered = True
                    speech_frames.append(frame)

        # Allow exit via console
        if sys.stdin.isatty():
            try:
                ready, _, _ = select.select([sys.stdin], [], [], 0)
                if ready:
                    if sys.stdin.readline().strip().lower() == "exit":
                        break
            except:
                pass

    print("Exiting...")
    stream.stop_stream()
    stream.close()
    p.terminate()


if __name__ == "__main__":
    main()
