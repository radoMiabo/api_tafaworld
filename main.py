from backend import appBackend
from fastapi import FastAPI, Form, File, UploadFile
from fastapi.responses import FileResponse, Response
from fastapi.middleware.cors import CORSMiddleware
import os
from uuid import uuid4
import tempfile

app = FastAPI()

app.add_middleware(CORSMiddleware,
                    allow_origins = ["*"],
                    allow_credentials = True,
                    allow_methods = ["*"],
                    allow_headers = ["*"])

temp_dir = tempfile.gettempdir()
@app.get("/")
def root():
    return {"message": "Bienvenue sur l'API de synthese vocale"}

@app.post("/synthesize")
def synthesize(text: str = Form(...), lang: str = Form(...)):
    # audio_id = str(uuid4)  
    audio_path = os.path.join(temp_dir, f"{str(uuid4())}.wav")
    if appBackend.ttsModel.synthesis(text= text, lang= lang, audioPath= audio_path) == 0:
        return FileResponse(path = audio_path, media_type= "audio/wav", filename= f"{str(uuid4())}.wav")
    else:
        return {"error": "Erreur de synthese"}

@app.post("/recognize")
async def recognize(audio : UploadFile = File(...), lang: str = Form(...)):
    with tempfile.NamedTemporaryFile(delete= False, suffix= ".aac") as tmp:
        tmp.write(await audio.read())
        tmp_path = tmp.name
    recognizedText = appBackend.ASRModel.recognize(audio_path= tmp_path, lang= lang)
    return {"text" : f"{recognizedText}"}

@app.post("/translate")
async def translate(text: str = Form(...), sourceLang: str = Form(...), destLang: str = Form(...) ):
    translated = await appBackend.translate(text= text, sourceLang= sourceLang, destLang= destLang)
    if translated == -1:
        return Response(status_code= 404)
    else:
        return {"text" : translated}