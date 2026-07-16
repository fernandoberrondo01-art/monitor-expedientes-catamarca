import requests
from config import API_URL


def consultar_expediente(anio, numero, codigo):

    params = {
        "year": anio,
        "number": numero,
        "user_repartition_code": codigo
    }

    r = requests.get(API_URL, params=params, timeout=30)

    if r.status_code != 200:
        return None

    respuesta = r.json()

    if not respuesta["data"]:
        return None

    return respuesta["data"][0]