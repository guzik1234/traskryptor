from faster_whisper import WhisperModel


class TranscriptionModel:
    """Zarządza modelami transkrypcji (polski/angielski) - używa faster-whisper (CTranslate2)"""
    
    def __init__(self, language, model_choice=None):
        self.language = language
        self.model_choice = model_choice
        self.model = None
        
        self._load_model()
    
    def _load_model(self):
        """Ładuje odpowiedni model na podstawie języka"""
        if self.language == "polski":
            if self.model_choice == "1":
                # Mały model polski
                model_id = "Systran/faster-whisper-small"
                self.language_code = "pl"
            else:
                # Średni model polski
                model_id = "Systran/faster-whisper-medium"
                self.language_code = "pl"
        else:  # angielski
            model_id = "Systran/faster-whisper-base.en"
            self.language_code = "en"
        
        print(f"Ładowanie modelu '{model_id}' (faster-whisper)...")
        
        # Wszystkie języki używają faster-whisper
        self.model = WhisperModel(
            model_id,
            device="cpu",
            compute_type="int8",
            local_files_only=False
        )
    
    def transcribe(self, audio_np, rate=16000):
        """Transkrybuje audio do tekstu"""
        segments, info = self.model.transcribe(
            audio_np, 
            beam_size=5,
            language=self.language_code if hasattr(self, 'language_code') else None
        )
        text = " ".join([s.text for s in segments]).strip()
        return text
