import urllib.request
import json
from json import JSONDecodeError
urllib.error.URLError

def findnth(haystack, needle, n):
	parts= haystack.split(needle, n+1)
	if len(parts)<=n+1:
		return -1
	return len(haystack)-len(parts[-1])-len(needle)

def findInURL(link):
	name = link[0:findnth(link, "/", 2)]
	url = name +"/feed/PressRelease.svc/GetPressReleaseList?pressReleaseDateFilter=3"
	hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'}
	data = {}
	try:
		req = urllib.request.Request(url, headers = hdr)
		data = (urllib.request.urlopen(req)).read()
	except urllib.error.URLError:
		return {}

	if data:
		try:
			my_json = data.decode('utf8').replace("'", '"').replace("\\/", "/")
			data = json.loads(my_json)
		except (JSONDecodeError, AttributeError) as e:
			my_json = data.decode('utf8').replace("\\/", "/")
			data = json.loads(my_json)

	try:
		for n in range(len(data['GetPressReleaseListResult'])):
		    data['GetPressReleaseListResult'][n]['Body'] = None
		    data['GetPressReleaseListResult'][n]['ShortBody'] = None
	except:
		pass
	return data