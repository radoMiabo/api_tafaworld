import requests
from backend import appBackend

url = "http://127.0.0.1:8000/synthesize"

data = {
    "text" : "bonjour tout le monde",
    "lang" : "fr"
}

response = requests.post(url= url, data= data)

if response.status_code == 200:
    with open("result.wav", "wb") as f:
        f.write(response.content)
    print("Fichier telecharge")
else:
    print(f"Errure {response.status_code}")

