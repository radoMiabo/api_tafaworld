from transformers import WhisperProcessor, WhisperForConditionalGeneration
import librosa
from speech_recognition import Recognizer, UnknownValueError, RequestError, AudioFile
import os
# import timess

class ASRModel:
    def __init__(self):
        # Initialisation du modèle
        model_path = "models/whisper_tiny_mg"
        
        self.processor = WhisperProcessor.from_pretrained(model_path)
        self.model = WhisperForConditionalGeneration.from_pretrained(model_path)
        self.forced_decoder_ids = self.processor.get_decoder_prompt_ids(language="mg", task="transcribe")
        self.model.config.forced_decoder_ids = self.forced_decoder_ids
        self.recognizer = Recognizer()

    def recognize(self,audio_path, lang: str):
        if lang== "mg": #pour l'ASR en malgache
            sample,sr = librosa.load(audio_path, sr=16000)
            input_features = self.processor(sample, sampling_rate=sr, return_tensors="pt").input_features
            predicted_ids = self.model.generate(input_features)
            transcription = self.processor.batch_decode(predicted_ids, skip_special_tokens=False)
            transcription = self.processor.batch_decode(predicted_ids, skip_special_tokens=True)
            return transcription[0].strip()
        else: #pour les autres langues
            with AudioFile(audio_path) as source:
                audio = self.recognizer.record(source)
            # time.sleep(0.2)
            try:
                texte = self.recognizer.recognize_google(audio_data= audio, language= lang)
                return texte
            except RequestError:
                return -1
            except UnknownValueError:
                return "Je n'ai pas compris"
