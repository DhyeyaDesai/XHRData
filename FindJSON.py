import urllib.request
from seleniumwire import webdriver
import json
from json import JSONDecodeError
from time import sleep

def findJson(driver, url, keyword):
	hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'}
	data = {}
	reqs = []
	try:
		if not ((url in driver.current_url) or (driver.current_url in url)):
			del driver.requests
			driver.get(url)
			sleep(1)
			
		for r in driver.requests:
			if r.headers.get('X-Requested-With'):
				driver.wait_for_request(r.path)
				try:
					if(keyword in str(r).split("?")[0]):
						reqs.append(r)
						data = r.response.body
				except:
					pass
	except:
		pass

	if data:
		try:
			my_json = data.decode('utf8').replace("'", '"').replace("\\/", "/")
			data = json.loads(my_json)
		except (JSONDecodeError, AttributeError) as e:
			my_json = data.decode('utf8').replace("\\/", "/")
			data = json.loads(my_json)

	if keyword == "FinancialReport":
		try:
			x = data['GetFinancialReportListResult'][0]['CoverImagePath']
		except KeyError:
			for r in reqs:
				try:
					req = urllib.request.Request(r, headers = hdr)
					s = (urllib.request.urlopen(req)).read()
					if len(data) < len(s) and type(s) is bytes:
						data = s
				except:
					pass

	if keyword == "PressRelease":
		try:
			x = data['GetPressReleaseListResult'][0]['Attachments']
		except KeyError:
			for r in reqs:
				try:
					req = urllib.request.Request(r, headers = hdr)
					s = (urllib.request.urlopen(req)).read()
					if len(data) < len(s) and type(s) is bytes:
						data = s
				except:
					pass
		try:
			for n in range(len(data['GetPressReleaseListResult'])):
			    data['GetPressReleaseListResult'][n]['Body'] = None
			    data['GetPressReleaseListResult'][n]['ShortBody'] = None

		except:
			pass

	try:
		if data:	
			try:
				my_json = data.decode('utf8').replace("'", '"').replace("\\/", "/")
				data = json.loads(my_json)
				# jsonData[0] = json.dumps(data, indent=4, sort_keys=True)
			except (JSONDecodeError, AttributeError) as e:
				my_json = data.decode('utf8').replace("\\/", "/")
				data = json.loads(my_json)
				# jsonData[0] = json.dumps(data, indent=4, sort_keys=True)
	except AttributeError:
		pass
	return data