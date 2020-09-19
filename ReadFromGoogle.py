import pandas as pd
import gspread
from df2gspread import gspread2df as g2d
from oauth2client.service_account import ServiceAccountCredentials

from WriteToGoogle import write

scope = ['https://www.googleapis.com/auth/spreadsheets']

def readFromGoogle(SPREADSHEET_KEY, WORKSHEET_NAME):
	credentials = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
	gc = gspread.authorize(credentials)
	df = g2d.download(SPREADSHEET_KEY, WORKSHEET_NAME,credentials=credentials, col_names = True)
	print("Reading done")
	return df[['Ticker', 'Company', 'Financial Links', 'Search Key for Company', 'Press Release Links', 'Search Key for Press Release']]


# SPREADSHEET_KEY = '1PfDAquK5ioQuWAvK4ujhenN5aqlBBKTRJTOqRmneH_Q'
# WORKSHEET_NAME = 'Testing'

# df = readFromGoogle(SPREADSHEET_KEY, WORKSHEET_NAME)
# searckKeysFinancials = []
# searckKeysPress = []

# for company in df['Company'].to_list():
# 	searckKeysFinancials.append(company + " com quarter results")
# 	searckKeysPress.append(company + " com press release invertor relations")

# df['Search Key for Company'] = searckKeysFinancials
# df['Search Key for Press Release'] = searckKeysPress

# write(df, SPREADSHEET_KEY, WORKSHEET_NAME)