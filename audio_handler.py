import pyaudio
import numpy as np


class AudioHandler:
    """Obsługuje nagrywanie audio z mikrofonu"""
    
    def __init__(self, rate=16000, chunk=1024):
        self.rate = rate
        self.chunk = chunk
        self.p = None
        self.stream = None
    
    def start(self):
        """Inicjalizuje i uruchamia strumień audio"""
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=self.rate,
            input=True,
            frames_per_buffer=self.chunk
        )
    
    def read(self):
        """Czyta chunk danych audio"""
        return self.stream.read(self.chunk, exception_on_overflow=False)
    
    def process_audio(self, frames, boost=1.8):
        """Przetwarza surowe dane audio do formatu numpy"""
        audio_bytes = b"".join(frames)
        audio_np = np.frombuffer(audio_bytes, dtype=np.int16).astype(np.float32)
        audio_np *= boost
        audio_np = np.clip(audio_np, -32768, 32767)
        audio_np /= 32768.0
        return audio_np
    
    def stop(self):
        """Zatrzymuje i zamyka strumień audio"""
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
        if self.p:
            self.p.terminate()

