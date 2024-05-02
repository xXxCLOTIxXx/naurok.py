import requests
from selenium import webdriver
from selenium.webdriver.firefox.options import Options


class req:
	session = requests.Session()
	url = "https://naurok.com.ua"

	def __init__(self, proxy: str = None):
		opt = Options()
		opt.add_argument('--headless')
		if proxy:
			opt.add_argument('--proxy-server=%s' % proxy)
			self.session.proxies.update({
   				'http': proxy,
    			'https': proxy
			})
		self.browser = webdriver.Firefox(opt)



	def request(self, method: str, endpoint: str, data: dict = None, json: bool = True) -> requests.Response:
		result = self.session.request(method, url=f"{self.url}{endpoint}", data=data)
		if json:
			try:result.json()
			except: raise Exception(f"Decoding error: {result.text}")
			return result.json()
		return result