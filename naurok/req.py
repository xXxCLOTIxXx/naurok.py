import requests


class req:
	session = requests.Session()
	url = "https://naurok.com.ua"


	def request(self, method: str, endpoint: str, data: dict = None, json: bool = True) -> requests.Response:
		result = self.session.request(method, url=f"{self.url}{endpoint}", data=data)
		if json:
			try:result.json()
			except: raise Exception(f"Decoding error: {result.text}")
			return result.json()
		return result


def start_headers(url):
	return {
		'Host': 'naurok.com.ua',
		'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0',
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
		'Accept-Language': 'en-US,en;q=0.5',
		'Accept-Encoding': 'gzip, deflate, br',
		'Content-Type': 'application/x-www-form-urlencoded',
		'Referer': f'https://naurok.com.ua{url}',
		'Origin': 'https://naurok.com.ua',
		'Upgrade-Insecure-Requests': '1',
		'Sec-Fetch-Dest': 'document',
		'Sec-Fetch-Mode': 'navigate',
		'Sec-Fetch-Site': 'same-origin',
		'Sec-Fetch-User': '?1',
		'Connection': 'keep-alive',
	}