import gspread
from google.oauth2.service_account import Credentials
from config import *

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

creds = Credentials.from_service_account_file(
    "credentials.json",
    scopes=SCOPES
)

gc = gspread.authorize(creds)

worksheet = gc.open_by_key(SPREADSHEET_ID).worksheet(SHEET_NAME)


def leer_expedientes():
    return worksheet.get_all_records()


def actualizar(indice, exp, fecha):

    worksheet.update_cell(indice, COL_ESTADO, exp["estado"])
    worksheet.update_cell(indice, COL_ULTIMO_PASE, exp["ultimo_pase"])
    worksheet.update_cell(indice, COL_MOTIVO, exp["motivo_pase"])
    worksheet.update_cell(indice, COL_REPARTICION, exp["nombre_reparticion"])
    worksheet.update_cell(indice, COL_SECTOR, exp["nombre_sector_interno"])
    worksheet.update_cell(indice, COL_ULTIMA_CONSULTA, fecha)


def actualizar_ultima_consulta(indice, fecha):
    worksheet.update_cell(indice, COL_ULTIMA_CONSULTA, fecha)


def actualizar_ultimo_cambio(indice, fecha):
    worksheet.update_cell(indice, COL_ULTIMO_CAMBIO, fecha)