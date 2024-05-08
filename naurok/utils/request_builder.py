import requests

from .helpers import headers

class builder:
	session = requests.Session()
	api = "naurok.com.ua"


	def request(self, method: str, endpoint: str, data: dict = None, json: dict = None, content_type: str = None) -> requests.Response:
		result = self.session.request(method, url=f"https://{self.api}{endpoint}", data=data, headers=headers(
			self.api, f"https://{self.api}{endpoint}", len(data) if data else None, content_type)
		)
		return result