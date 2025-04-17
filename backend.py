
from googletrans import Translator
from tts_model import TTSModel
from asr_model import ASRModel

class Backend():
    def __init__(self):
        self.ttsModel = TTSModel() #Instance de la classe qui gère la synthèse de la parole
        self.ASRModel = ASRModel() #Instance de la classe qui gère la reconnaissance de la parole
        self.languagesKey = {
            "Malagasy": "mg",
            "Français": "fr",
            "Anglais": "en"
        }
        self.translator = Translator() #Instance de la classe qui gère la traduction
    
    async def translate(self, text, sourceLang, destLang):
        try:
            translatedText = await self.translator.translate(text= text, dest= destLang, src= sourceLang)
            return translatedText.text
        except Exception as e:
            return -1

appBackend = Backend()