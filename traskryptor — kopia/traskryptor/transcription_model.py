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
            inputs = self.processor(audio_np, sampling_rate=rate, return_tensors="pt").to(self.device)
            
            gen_cfg = self.model.generation_config
            gen_cfg.suppress_tokens = []
            gen_cfg.begin_suppress_tokens = [220, 50257]
            gen_cfg.forced_decoder_ids = None
            gen_cfg.forced_bos_token_id = None
            gen_cfg.forced_eos_token_id = None
            gen_cfg.pad_token_id = self.processor.tokenizer.eos_token_id
            
            inputs["attention_mask"] = torch.ones(
                (inputs["input_features"].shape[0], inputs["input_features"].shape[2]),
                dtype=torch.long
            ).to(self.device)
            
            generated_ids = self.model.generate(
                **inputs,
                generation_config=gen_cfg,
                max_new_tokens=256
            )
            
            text = self.processor.batch_decode(generated_ids, skip_special_tokens=True)[0].strip()
        
        return text
