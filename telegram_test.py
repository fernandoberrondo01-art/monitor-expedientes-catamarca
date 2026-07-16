import os
import requests
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

respuesta = requests.post(
    url,
    data={
        "chat_id": CHAT_ID,
        "text": "✅ Prueba exitosa desde el Monitor de Expedientes"
    }
)

print("Código HTTP:", respuesta.status_code)
print("Respuesta:", respuesta.text)