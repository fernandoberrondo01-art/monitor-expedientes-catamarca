import os
import requests
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")


def enviar_mensaje(texto):

    print("BOT_TOKEN cargado:", BOT_TOKEN is not None)
    print("CHAT_ID:", CHAT_ID)

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    respuesta = requests.post(
        url,
        data={
            "chat_id": CHAT_ID,
            "text": texto
        },
        timeout=30
    )

    print("Código HTTP:", respuesta.status_code)
    print("Respuesta Telegram:", respuesta.text)

    return respuesta.status_code == 200