import os
import requests
from dotenv import load_dotenv

# Cargar variables del archivo .env
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")


def enviar_mensaje(texto):

    print("=" * 50)
    print("DIAGNÓSTICO TELEGRAM")
    print("=" * 50)

    print("BOT_TOKEN existe:", BOT_TOKEN is not None)
    print("CHAT_ID:", CHAT_ID)

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    try:

        respuesta = requests.post(
            url,
            data={
                "chat_id": CHAT_ID,
                "text": texto
            },
            timeout=30
        )

        print("Código HTTP:", respuesta.status_code)
        print("Respuesta Telegram:")
        print(respuesta.text)

        if respuesta.status_code == 200:
            print("✅ Mensaje enviado correctamente")
            return True
        else:
            print("❌ Error enviando mensaje")
            return False

    except Exception as e:
        print("❌ EXCEPCIÓN TELEGRAM")
        print(e)
        return False