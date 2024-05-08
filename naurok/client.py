from faker import Faker
from bs4 import BeautifulSoup
from typing import Union, List
from .exception import *



from .req import req, start_headers


class Client(req):

	def __init__(self, names_lang: str = 'ru_RU', proxy: str = None):
		req.__init__(self)
		self.faker = Faker(names_lang)

	def start_test(self, testLink: str, nick: str = None, json: str = False) -> str:
		soup = BeautifulSoup(self.session.request("GET", testLink).text, 'html.parser')
		form = soup.find('form', {'id': 'participate-form-code'})
		url = form['action'] if form else None
		data = {
			'SessionForm[firstname]': nick if nick else self.faker.name()
		}
		for input_tag in form.find_all('input'):
			if input_tag.get('name') and input_tag.get('value'):
				data[input_tag['name']] = input_tag['value']
		
		if url is None: raise LinkError(testLink)
		result = self.session.post(f"{self.url}{url}", data=data, allow_redirects=True, headers=start_headers(url=url))
		if result.status_code != 302: raise NotForwarded(testLink)
		if result.history:
			return result.history


	def end_test(self, sessionId: int, answer_id: Union[str, List[str]] = None, question_id: str = None, points: str = "5", homeworkType = False, homework = False):
		return self.request("PUT", f"/api2/test/sessions/end/{sessionId}", {
			"session_id":{sessionId},
			"answer":answer_id if isinstance(answer_id, list) else [answer_id],
			"question_id": question_id,
			"show_answer": 0,
			"type":"quiz",
			"point": points,
			"homeworkType":homeworkType,
			"homework": homework

		})


	def get_session_info(self, sessionId: int) -> dict:
		return self.request("GET", f"/api2/test/sessions/{sessionId}")
	
	def make_answer(self, sessionId: int, answer_id: Union[str, List[str]], question_id: str, points: str = "5", homeworkType = False, homework = False):
		return self.request("PUT", f"/api2/test/responses/answer", {
			"session_id":sessionId,
			"answer":answer_id if isinstance(answer_id, list) else [answer_id],
			"question_id": question_id,
			"show_answer":0,
			"type":"quiz",
			"point":points,
			"homeworkType":homeworkType,
			"homework":homework

		})

	def get_session_id(self, uuid: str) -> int:
		result = self.session.request("GET", f"{self.url}/test/testing/{uuid}").text
		soup = BeautifulSoup(result, 'html.parser')
		div_element = soup.find('div', attrs={'ng-app': 'testik'})
		if div_element:
			ng_init_attr = div_element.get('ng-init')
			init_values = ng_init_attr.split(',')
			target_value = init_values[1] if len(init_values) > 1 else None
			return int(target_value)
		else:
			return None