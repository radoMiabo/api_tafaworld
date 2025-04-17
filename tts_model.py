from transformers import VitsModel, AutoTokenizer
import torch
import torchaudio
import os
from gtts import gTTS, gTTSError


class TTSModel():
    def __init__(self):
        model_path = "models/tts_female"
        self.model = VitsModel.from_pretrained(model_path, local_files_only= True)
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        self.gtts_API = gTTS(" ", lang= "fr",slow= True)
    
    def synthesis(self, text: str, lang: str, audioPath: str ):
        if lang == "mg": #pour la TTS en Malgache
            inputs = self.tokenizer(text= text, return_tensors= "pt")
            with torch.inference_mode():
                output = self.model(**inputs).waveform
            torchaudio.save(audioPath, sample_rate= self.model.config.sampling_rate, src= output, format= "wav")
        else: #pour les autres langues
            self.gtts_API.lang = lang
            self.gtts_API.text = text
            try:
                self.gtts_API.save(audioPath)
            except gTTSError as e:
                return -1
        return 0