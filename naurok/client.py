from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from faker import Faker
from bs4 import BeautifulSoup
from typing import Union, List



from .req import req


class Client(req):

	def __init__(self, names_lang: str = 'ru_RU'):
		req.__init__(self)
		self.faker = Faker(names_lang)


	def start_test(self, testId: str, nick: str = None) -> str:
		self.browser.get(f'{self.url}/test/join?gamecode={testId}')
		WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.NAME, 'JoinForm[name]')))
		username_input = self.browser.find_element("name",'JoinForm[name]')
		username_input.clear()
		username_input.send_keys(nick if nick else self.fake.name())
		curent = self.browser.current_url
		username_input.send_keys(Keys.ENTER)
		id = None
		WebDriverWait(self.browser, 10).until(EC.url_changes(self.browser.current_url))
		if curent != self.browser.current_url:id = self.browser.current_url.split("/")[-1]
		return id


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