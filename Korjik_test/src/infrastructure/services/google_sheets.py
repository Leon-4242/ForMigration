import logging

from gspread import service_account

from config.google import AUTH_DIR, SHEET_ID
from models.sheet_types import SheetTypes


class GoogleService:
    def __init__(self):
        self.client = service_account(filename=str(AUTH_DIR))
        self.sheetId = SHEET_ID
        self.spreadsheet = self.client.open_by_key(self.sheetId)

        logging.info("Connection with GoogleSheet successfully established!")

    def get_from_table(self, sheetName: SheetTypes):
        data = self.spreadsheet.worksheet(sheetName).get_all_records()
        logging.info(f"Sheet {sheetName} successfully loaded!")
        return data

    def close(self):
        pass
