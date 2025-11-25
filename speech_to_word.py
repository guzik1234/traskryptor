import pyaudio
import win32com.client
import sys
import select
import numpy as np
import webrtcvad
import collections
from transformers import AutoProcessor, AutoModelForSpeechSeq2Seq
import torch

# Make sure you have transformers and torch installed:
# pip install transformers torch accelerate pyaudio webrtcvad numpy pywin32 collections

def main():
    print("Initializing...")

    # --- Configure PyTorch CPU Threads ---
    # This can potentially increase CPU utilization during model inference
    # Set this to the number of CPU cores you want PyTorch to use.
    # You can find this in Windows Task Manager under the Performance tab -> CPU.
    # Look for "Logical processors" or "Cores". Start with the number of Cores.
    num_cpu_threads = 12 # Example: replace with your number of cores/logical processors
    torch.set_num_threads(num_cpu_threads)
    print(f"Set PyTorch CPU threads to: {torch.get_num_threads()}")


    # Load Whisper model using Hugging Face transformers
    model_id = "bardsai/whisper-small-pl"
    print(f"Loading model '{model_id}' using Hugging Face Transformers...")

    try:
        # Check if a CUDA-enabled GPU is available and use it, otherwise use CPU
        device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"Using device: {device}")

        # Load the processor and the model from Hugging Face Hub
        # Consider adding torch_dtype=torch.float16 here for potential speedup if on a suitable device
        model = AutoModelForSpeechSeq2Seq.from_pretrained(model_id).to(device)
        processor = AutoProcessor.from_pretrained(model_id)


        print("Model loaded successfully using Transformers.")

        # --- Set up forced_decoder_ids for Polish transcription ---
        # ... (This section remains the same as the last working version) ...
        tokenizer = processor.tokenizer
        start_of_text_token_id = tokenizer.convert_tokens_to_ids("<|startoftext|>")
        pl_token_id = tokenizer.convert_tokens_to_ids("<|pl|>")
        transcribe_token_id = tokenizer.convert_tokens_to_ids("<|transcribe|>")
        no_timestamps_token_id = tokenizer.convert_tokens_to_ids("<|notimestamps|>")

        forced_decoder_ids = [
            (start_of_text_token_id, None),
            (pl_token_id, None),
            (transcribe_token_id, None),
            (no_timestamps_token_id, None)
        ]


    except Exception as e:
        print(f"Error loading model or setting up generation config: {e}")
        print("Please ensure libraries are correctly installed and you have internet access.")
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
        print("Error: Could not connect to Word. Make sure a document is open.")
        stream.stop_stream()
        stream.close()
        p.terminate()
        return

    print("Speak now...")

    # --- VAD Setup ---
    vad = webrtcvad.Vad(3)
    SAMPLE_RATE = 16000
    FRAME_DURATION_MS = 30
    FRAME_SIZE = int(SAMPLE_RATE * FRAME_DURATION_MS / 1000)
    BYTES_PER_FRAME = FRAME_SIZE * 2

    SILENCE_TIMEOUT_MS = 3000
    MIN_SPEECH_DURATION_MS = 450

    frames_buffer = collections.deque()
    speech_frames = []
    silence_frames_after_speech = 0
    triggered = False

    print("Listening...")
    while True:
        data = stream.read(1024, exception_on_overflow=False)
        frames_buffer.append(data)

        while len(b''.join(frames_buffer)) >= BYTES_PER_FRAME:
            full_buffer = b''.join(frames_buffer)
            vad_frame = full_buffer[:BYTES_PER_FRAME]
            frames_buffer.clear()
            frames_buffer.append(full_buffer[BYTES_PER_FRAME:])

            try:
                is_speech = vad.is_speech(vad_frame, SAMPLE_RATE)
            except Exception as e:
                print(f"VAD Error: {e}")
                is_speech = False

            if triggered:
                speech_frames.append(vad_frame)
                if not is_speech:
                    silence_frames_after_speech += 1
                    num_silence_frames_needed = SILENCE_TIMEOUT_MS // FRAME_DURATION_MS
                    if silence_frames_after_speech > num_silence_frames_needed:
                        phrase_bytes = b''.join(speech_frames)
                        speech_duration_ms = len(phrase_bytes) / (SAMPLE_RATE * 2) * 1000

                        triggered = False
                        speech_frames = []
                        silence_frames_after_speech = 0

                        if speech_duration_ms >= MIN_SPEECH_DURATION_MS:
                            print(f"End of phrase detected ({speech_duration_ms:.0f} ms), transcribing...")
                            audio_np = np.frombuffer(phrase_bytes, dtype=np.int16).astype(np.float32) / 32768.0

                            try:
                                inputs = processor(audio_np, sampling_rate=SAMPLE_RATE, return_tensors="pt").to(device)

                                generated_ids = model.generate(
                                    **inputs,
                                    forced_decoder_ids=forced_decoder_ids,
                                    max_new_tokens=128
                                )

                                text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
                                text = text.strip()
                                print(f"Transcription result: '{text}'")

                            except Exception as e:
                                print(f"Error during transcription with Transformers: {e}")
                                text = ""

                            if text:
                                print(f"Inserting text into Word: '{text}'")
                                word.Selection.InsertAfter(text + " ")
                                word.Selection.MoveRight()
                            else:
                                print("Transcription result was empty, not inserting.")
                        else:
                           print(f"Detected phrase too short ({speech_duration_ms:.0f} ms), ignoring.")

                else:
                    silence_frames_after_speech = 0

            elif is_speech:
                print("Speech detected...")
                triggered = True
                speech_frames.append(vad_frame)
                silence_frames_after_speech = 0

        if sys.stdin.isatty():
            try:
                ready, _, _ = select.select([sys.stdin], [], [], 0)
                if ready:
                    user_input = sys.stdin.readline().strip()
                    if user_input.lower() == "exit":
                        break
            except:
                pass

    print("Exiting...")
    stream.stop_stream()
    stream.close()
    p.terminate()


if __name__ == "__main__":
    main()