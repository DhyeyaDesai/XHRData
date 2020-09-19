import selenium
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

def findnth(haystack, needle, n):
	parts= haystack.split(needle, n+1)
	if len(parts)<=n+1:
		return -1
	return len(haystack)-len(parts[-1])-len(needle)


def update(driver, df, url, year):
	all_links = driver.find_elements_by_css_selector('a')
	for a in all_links:
		UncleanedData = ""
		Links = ""
		LinkLabel = ""
		LinkInfo = ""
		try:
			if year in a.get_attribute('href'):
				link = a.get_attribute('href')
				if ".com" not in link:
					link = url + "/" + link
				link.replace("//", "/").replace("https:/", "https://").replace("http:/", "http://")
				Links = link
				LinkInfo = link[link.rfind('/')+1: len(link)]
				LinkLabel = a.text
				row = {'Year': year, 
					'Links': Links, 
					'LinkLabel': LinkLabel, 
					'LinkInfo': LinkInfo}
				df = df.append(row, ignore_index=True)
		except TypeError:
			continue
		except:
			continue
	return df


