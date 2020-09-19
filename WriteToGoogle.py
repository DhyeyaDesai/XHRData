import pandas as pd
import gspread
from df2gspread import df2gspread as d2g
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/drive',
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive.file']

def write(df, SPREADSHEET_KEY, WORKSHEET_NAME):
    credentials = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
    gc = gspread.authorize(credentials)
    d2g.upload(df, SPREADSHEET_KEY, WORKSHEET_NAME, credentials=credentials, row_names=True)
    print("Written")