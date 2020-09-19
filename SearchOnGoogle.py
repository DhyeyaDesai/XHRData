from requests_html import HTMLSession

def search(keywords):
	url = "https://www.google.com/search?q=" + keywords.strip().replace(" ", "+")
	session = HTMLSession()
	r = session.get(url)
	r.html.render(sleep=1)
	try:
		resultSection = r.html.find("div.g")
		resultLink = resultSection[0].find("a", first = True).attrs['href']
		if "/search?q=" in resultLink:
			resultLink = resultSection[1].find("a", first = True).attrs['href']
		if "/search?q=" in resultLink:
			resultLink = resultSection[2].find("a", first = True).attrs['href']
	except:
		return ""
	return resultLink