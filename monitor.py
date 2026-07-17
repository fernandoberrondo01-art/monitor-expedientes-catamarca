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

    try:

        if str(fila["Activo"]).upper() != "SI":
            continue

        if str(fila["Número"]).strip() == "":
            continue

        print("=" * 60)
        print(f"📄 Consultando: {fila['Descripción']}")

        params = {
            "year": fila["Año"],
            "number": fila["Número"],
            "user_repartition_code": fila["Código"]
        }

        r = requests.get(API_URL, params=params, timeout=30)

        if r.status_code != 200:
            print(f"❌ Error HTTP: {r.status_code}")
            continue

        respuesta = r.json()

        if not respuesta["data"]:
            print("⚠️ No se encontró el expediente")
            continue

        exp = respuesta["data"][0]

        # Normalizar valores nulos
        estado = str(exp.get("estado") or "").strip()
        motivo = str(exp.get("motivo_pase") or "").strip()
        reparticion = str(exp.get("nombre_reparticion") or "").strip()
        sector = str(exp.get("nombre_sector_interno") or "").strip()
        ultimo_pase = str(exp.get("ultimo_pase") or "").strip()

        estado_anterior = str(fila["Estado"] or "").strip()
        motivo_anterior = str(fila["Motivo"] or "").strip()
        reparticion_anterior = str(fila["Repartición"] or "").strip()
        sector_anterior = str(fila["Sector"] or "").strip()
        
        print("--------------------------------")
        print(f"Expediente: {fila['Descripción']}")
        print(f"Estado Sheet : '{estado_anterior}'")
        print(f"Estado API   : '{estado}'")
        print(f"Motivo Sheet : '{motivo_anterior}'")
        print(f"Motivo API   : '{motivo}'")
        print(f"Repartición Sheet : '{reparticion_anterior}'")
        print(f"Repartición API   : '{reparticion}'")
        print(f"Sector Sheet : '{sector_anterior}'")
        print(f"Sector API   : '{sector}'")
        print("--------------------------------")
        hubo_cambios = (
            estado_anterior != estado or
            motivo_anterior != motivo or
            reparticion_anterior != reparticion or
            sector_anterior != sector
        )

        # Actualizar Google Sheets

        worksheet.update_cell(indice, 6, estado)
        worksheet.update_cell(indice, 7, ultimo_pase)
        worksheet.update_cell(indice, 8, motivo)
        worksheet.update_cell(indice, 9, reparticion)
        worksheet.update_cell(indice, 10, sector)

        ahora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        worksheet.update_cell(indice, 11, ahora)

        if hubo_cambios:

            worksheet.update_cell(indice, 12, ahora)

            mensaje = f"""
📢 EXPEDIENTE ACTUALIZADO

📌 {fila["Descripción"]}

📂 {exp["numero_expediente"]}

🏢 Repartición
{reparticion if reparticion else "Sin datos"}

📍 Sector
{sector if sector else "Sin datos"}

🕒 Último Pase
{ultimo_pase}
"""

            ok = enviar_mensaje(mensaje)

            if ok:
                print("📲 Telegram enviado")
            else:
                print("❌ Error enviando Telegram")

        else:
            print("✔ Sin cambios")

    except Exception as e:
        descripcion = fila.get("Descripción", "Sin descripción")
        print(f"❌ Error procesando '{descripcion}': {e}")

print("=" * 60)
print("✅ Proceso finalizado.")