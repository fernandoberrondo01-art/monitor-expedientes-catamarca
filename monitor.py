import requests
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
from telegram_utils import enviar_mensaje

# ==========================================
# CONFIGURACIÓN
# ==========================================

SPREADSHEET_ID = "17qm55yN3judZA37bcWoqOC7nR3qI_wXcdOYaSl-pdzk"
SHEET_NAME = "HOJA1"

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

API_URL = "https://api-intranet.catamarca.gob.ar/api/v1/gde/consulta-expediente-publica/"

creds = Credentials.from_service_account_file(
    "credentials.json",
    scopes=SCOPES
)

gc = gspread.authorize(creds)

worksheet = gc.open_by_key(SPREADSHEET_ID).worksheet(SHEET_NAME)

datos = worksheet.get_all_records()

for indice, fila in enumerate(datos, start=2):

    if str(fila["Activo"]).upper() != "SI":
        continue

    if fila["Número"] == "":
        continue

    print("=" * 60)
    print(f"Consultando: {fila['Descripción']}")

    params = {
        "year": fila["Año"],
        "number": fila["Número"],
        "user_repartition_code": fila["Código"]
    }

    try:

        r = requests.get(API_URL, params=params, timeout=30)

        if r.status_code != 200:
            print("Error HTTP:", r.status_code)
            continue

        respuesta = r.json()

        if not respuesta["data"]:
            print("No se encontró el expediente")
            continue

        exp = respuesta["data"][0]

        estado_anterior = str(fila["Estado"])
        motivo_anterior = str(fila["Motivo"])
        reparticion_anterior = str(fila["Repartición"])
        sector_anterior = str(fila["Sector"])

        hubo_cambios = (
            estado_anterior != exp["estado"] or
            motivo_anterior != exp["motivo_pase"] or
            reparticion_anterior != exp["nombre_reparticion"] or
            sector_anterior != exp["nombre_sector_interno"]
        )

        # Actualizar Google Sheets

        worksheet.update_cell(indice, 6, exp["estado"])
        worksheet.update_cell(indice, 7, exp["ultimo_pase"])
        worksheet.update_cell(indice, 8, exp["motivo_pase"])
        worksheet.update_cell(indice, 9, exp["nombre_reparticion"])
        worksheet.update_cell(indice, 10, exp["nombre_sector_interno"])

        ahora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        worksheet.update_cell(indice, 11, ahora)

        if hubo_cambios:

            worksheet.update_cell(indice, 12, ahora)

            mensaje = f"""
📢 EXPEDIENTE ACTUALIZADO

📌 {fila["Descripción"]}

📂 {exp["numero_expediente"]}

Estado
{estado_anterior}
⬇
{exp["estado"]}

Motivo
{motivo_anterior}
⬇
{exp["motivo_pase"]}

Repartición
{reparticion_anterior}
⬇
{exp["nombre_reparticion"]}

Sector
{sector_anterior}
⬇
{exp["nombre_sector_interno"]}

🕒 {ahora}
"""

            ok = enviar_mensaje(mensaje)

            if ok:
                print("📲 Telegram enviado")
            else:
                print("❌ Error enviando Telegram")

        else:
            print("Sin cambios")

        print("✅ Google Sheets actualizado")

    except Exception as e:
        print("ERROR:", e)