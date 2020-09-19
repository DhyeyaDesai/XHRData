from seleniumwire import webdriver  
import pandas as pd
import json
import schedule
from time import sleep
import datetime
from json import JSONDecodeError
from ReadFromGoogle import readFromGoogle
from SearchOnGoogle import search
from UpdateData import update
from FindPressInURL import findInURL
from WriteToGoogle import write
from FindJSON import findJson

SPREADSHEET_KEY = '1PfDAquK5ioQuWAvK4ujhenN5aqlBBKTRJTOqRmneH_Q'
WORKSHEET_NAME = 'T2'
EXECUTABLE_PATH = "C:\\Python38\\geckodriver.exe"
#site:lifewire.com power search tricks
now = datetime.datetime.now()
current_year = now.year

def main():
	df = readFromGoogle(SPREADSHEET_KEY, WORKSHEET_NAME).head(5)

	search_keys_for_company = df['Search Key for Company'].to_list()
	financialLinks = df['Financial Links'].to_list()
	search_keys_for_press_release = df['Search Key for Press Release'].to_list()
	pressReleaseLinks = df['Press Release Links'].to_list()

	for index, link in enumerate(financialLinks):
		if link == "":
			financialLinks[index] = search(search_keys_for_company[index])

	for index, link in enumerate(pressReleaseLinks):
		if link == "":
			pressReleaseLinks[index] = search(search_keys_for_press_release[index])

	df['Financial Links'] = financialLinks
	df['Press Release Links'] = pressReleaseLinks

	write(df, SPREADSHEET_KEY, WORKSHEET_NAME)

	dataByScraper = []
	FinancialReportService = []
	PressReleaseService = []

	dx = {'Year': [],
	'Links': [],
	'LinkLabel': [],
	'LinkInfo': [] 
	}

	df1 = pd.DataFrame(dx)

	chrome_options = webdriver.ChromeOptions()
	chrome_options.headless = True
	driver = webdriver.Chrome(options=chrome_options, executable_path = EXECUTABLE_PATH)

	# firefox_options = webdriver.FirefoxOptions()
	# firefox_options.headless = True
	# driver = webdriver.Firefox(firefox_options=firefox_options, executable_path = EXECUTABLE_PATH)

	for link in df['Financial Links'].to_list():
		data = findJson(driver, link, "FinancialReport")
		new = []
		try:
			for n, d in enumerate(data["GetFinancialReportListResult"]):
				if d["ReportYear"] >= current_year-2:
					new.append(d)
			data["GetFinancialReportListResult"] = new
		except:
			pass
		FinancialReportService.append(data)

		data1 = findJson(driver, link, "PressRelease")
		new = []
		try:
			new = data1['GetPressReleaseListResult'][0:10]
			data1["GetPressReleaseListResult"] = new
		except:
			pass

		if not data:
			df1 = update(driver, df1, link, str(current_year))
			df1 = update(driver, df1, link, str(current_year - 1))
			df1 = update(driver, df1, link, str(current_year - 2))
			try:
				dataByScraper.append(df1[['Year', 'Links','LinkLabel', 'LinkInfo']].to_json(orient="records"))
			except KeyError:
				dataByScraper.append("")
			df1 = pd.DataFrame(dx)
		else:
			dataByScraper.append("")

		if data and not data1:
			data1 = findInURL(link)
			new = []
			try:
				new = data1['GetPressReleaseListResult'][0:10]
				data1["GetPressReleaseListResult"] = new
			except:
				pass
		PressReleaseService.append(data1)

	for n, link in enumerate(df['Press Release Links'].to_list()):
		if not PressReleaseService[n]:
			data1 = findJson(driver, link, "PressRelease")
			new = []
			try:
				new = data1['GetPressReleaseListResult'][0:10]
				data1["GetPressReleaseListResult"] = new
			except:
				pass
			PressReleaseService[n] = data1

	driver.quit()

	df['FinancialReportService'] = FinancialReportService
	df['PressReleaseService'] = PressReleaseService
	df['Scraped Data'] = dataByScraper

	newLinks = []
	for link in df['Scraped Data']:
		newLinks.append(link.replace('\\/', '/').replace('//', '/').replace('https:/', 'https://'))
	df['Scraped Data'] = newLinks
	write(df, SPREADSHEET_KEY, WORKSHEET_NAME)

main()

# IF YOU WANT TO TEST IT, COMMENT THE BELOW SECTION AND UNCOMMENT THE ABOVE MAIN() CALL

# schedule.every().day.do(main)
# while 1:
# 	schedule.run_pending()
# 	time.sleep(1)