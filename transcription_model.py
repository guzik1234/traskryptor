import torch
from transformers import AutoProcessor, AutoModelForSpeechSeq2Seq
from faster_whisper import WhisperModel


class TranscriptionModel:
    """Zarządza modelami transkrypcji (polski/angielski)"""
    
    def __init__(self, language, model_choice=None):
        self.language = language
        self.model_choice = model_choice
        self.model = None
        self.processor = None
        self.device = None
        self.use_faster_whisper = False
        
        torch.set_num_threads(12)
        self._load_model()
    
    def _load_model(self):
        """Ładuje odpowiedni model na podstawie języka"""
        if self.language == "polski":
            if self.model_choice == "1":
                model_id = "bardsai/whisper-small-pl"
            else:
                model_id = "bardsai/whisper-medium-pl-v2"
            self.use_faster_whisper = False
        else:  # angielski
            model_id = "guillaumekln/faster-whisper-base.en"
            self.use_faster_whisper = True
        
        print(f"Ładowanie modelu '{model_id}'...")
        
        if self.use_faster_whisper:
            # Angielski - faster-whisper
            self.model = WhisperModel(
                model_id,
                device="cpu",
                compute_type="int8",
                local_files_only=False
            )
            self.processor = None
            self.device = "cpu"
        else:
            # Polski - transformers
            self.device = "cuda" if torch.cuda.is_available() else "cpu"
            self.processor = AutoProcessor.from_pretrained(model_id)
            self.model = AutoModelForSpeechSeq2Seq.from_pretrained(model_id).to(self.device)
    
    def transcribe(self, audio_np, rate=16000):
        """Transkrybuje audio do tekstu"""
        if self.use_faster_whisper:
            # Angielski - faster-whisper
            segments, info = self.model.transcribe(audio_np, beam_size=5)
            text = " ".join([s.text for s in segments]).strip()
        else:
            # Polski - transformers
            # Przetwórz audio
            inputs = self.processor(
                audio_np, 
                sampling_rate=rate, 
                return_tensors="pt"
            ).to(self.device)
            
            # Przygotuj forced_decoder_ids dla polskiego
            forced_decoder_ids = self.processor.get_decoder_prompt_ids(
                language="polish", 
                task="transcribe"
            )
            
            # Napraw generation_config - usuń suppress_tokens który powoduje błąd
            gen_config = self.model.generation_config
            gen_config.suppress_tokens = None  # Wyłącz suppress_tokens
            
            # Generuj transkrypcję
            with torch.no_grad():
                generated_ids = self.model.generate(
                    inputs["input_features"],
                    generation_config=gen_config,
                    forced_decoder_ids=forced_decoder_ids,
                    max_length=448
                )
            
            # Dekoduj
            text = self.processor.batch_decode(
                generated_ids, 
                skip_special_tokens=True
            )[0].strip()
        
        return text
