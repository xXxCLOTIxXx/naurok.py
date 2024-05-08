from faker import Faker
from bs4 import BeautifulSoup
from typing import Union, List

from .utils.request_builder import builder
from .objects.quizt import (
	QuizType
)
from .utils.exception import LinkError
from .utils.helpers import headers

class Client(builder):

	def __init__(self, names_lang: str = 'ru_RU', proxy: str = None):
		builder.__init__(self)
		self.faker = Faker(names_lang)

	def start_test(self, testLink: str, nick: str = None) -> str:
		#TODO

		soup = BeautifulSoup(self.session.request("GET", testLink).text, 'html.parser')
		form = soup.find('form', {'id': 'participate-form-code'})
		url = form['action'] if form else None
		if url is None: raise LinkError(testLink)
		data = {
			'SessionForm[firstname]': nick if nick else self.faker.name()
		}
		for input_tag in form.find_all('input'):
			if input_tag.get('name') and input_tag.get('value'):
				data[input_tag['name']] = input_tag['value']
		
		return self.session.request("POST", testLink, data=data, headers=headers(
			self.api, testLink, len(data), "application/x-www-form-urlencoded"
		), allow_redirects=True).status_code


	def end_test(self, sessionId: int, answer_id: Union[str, List[str]] = None, question_id: str = None, quiz_type: str = QuizType.QUIZ, points: str = "1", homeworkType = False, homework = False):
		return self.request("PUT", f"/api2/test/sessions/end/{sessionId}", {
			"session_id":{sessionId},
			"answer":answer_id if isinstance(answer_id, list) else [answer_id],
			"question_id": question_id,
			"show_answer": 1,
			"type": quiz_type,
			"point": points,
			"homeworkType":homeworkType,
			"homework": homework

		})


	def get_session_id(self, uuid: str) -> int:
		soup = BeautifulSoup(
			self.request("GET", f"/test/testing/{uuid}").text,
			'html.parser'
		)
		div_element = soup.find('div', attrs={'ng-app': 'testik'})
		if div_element:
			ng_init_attr = div_element.get('ng-init')
			init_values = ng_init_attr.split(',')
			return int(init_values[1]) if len(init_values) > 1 else None
		else:return None


	def get_session_info(self, sessionId: int) -> dict:
		return self.request("GET", f"/api2/test/sessions/{sessionId}")
	
	def make_answer(self, sessionId: int, answer_id: Union[str, List[str]], question_id: str, quiz_type: str = QuizType.QUIZ, points: str = "1", homeworkType = False, homework = False):

		return self.request("PUT", f"/api2/test/responses/answer", {
			"session_id":sessionId,
			"answer":answer_id if isinstance(answer_id, list) else [answer_id],
			"question_id": question_id,
			"show_answer":1,
			"type": quiz_type,
			"point":points,
			"homeworkType":homeworkType,
			"homework":homework

		}, content_type="application/x-www-form-urlencoded").json()