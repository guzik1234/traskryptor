import sounddevice as sd
import numpy as np
import queue


class AudioHandler:
    """Obsługuje nagrywanie audio z mikrofonu"""
    
    def __init__(self, rate=16000, chunk=1024):
        self.rate = rate
        self.chunk = chunk
        self.stream = None
        self.audio_queue = queue.Queue()
    
    def start(self):
        """Inicjalizuje i uruchamia strumień audio"""
        def callback(indata, frames, time, status):
            if status:
                print(f"Audio status: {status}")
            self.audio_queue.put(indata.copy())
        
        self.stream = sd.InputStream(
            samplerate=self.rate,
            channels=1,
            dtype=np.int16,
            blocksize=self.chunk,
            callback=callback
        )
        self.stream.start()
    
    def read(self):
        """Czyta chunk danych audio"""
        try:
            return self.audio_queue.get(timeout=1.0)
        except queue.Empty:
            return np.zeros((self.chunk, 1), dtype=np.int16)
    
    def process_audio(self, frames, boost=1.8):
        """Przetwarza surowe dane audio do formatu numpy"""
        # frames to lista numpy arrays - konkatenujemy
        audio_np = np.concatenate(frames).flatten().astype(np.float32)
        audio_np *= boost
        audio_np = np.clip(audio_np, -32768, 32767)
        audio_np /= 32768.0
        return audio_np
    
    def stop(self):
        """Zatrzymuje i zamyka strumień audio"""
        if self.stream:
            self.stream.stop()
            self.stream.close()
            self.stream = None
