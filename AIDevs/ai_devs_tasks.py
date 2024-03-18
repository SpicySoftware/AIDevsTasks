import json
import requests

from enum import Enum
from pprint import pprint


class HTTPMethod(Enum):
    GET  = 'GET'
    POST = 'POST'


class AIDevsTasks:

    class WrongRequest(Exception):
        pass

    BASE_URL = "AI_DEVS_ADDRESS"

    def __init__(self, api_key: str, task: str, debug: bool = True):
        self._api_key = api_key
        self._task = task
        self._debug = debug
        self._token = self._obtain_task_token(task)

    def log(self, header: str, result):
        print(f"=> {header}")
        pprint(result)
        print()

    def _request(self, method: HTTPMethod, **kwargs) -> dict:
        match method:
            case HTTPMethod.GET:
                response = requests.get(**kwargs)
            case HTTPMethod.POST:
                response = requests.post(**kwargs)

        response_json = response.json()

        if response.status_code not in (200, 201, 202, 204):
            raise AIDevsTasks.WrongRequest(f"Error, status_code={response.status_code}, response={response_json}")

        return response_json

    def _obtain_task_token(self, task_name: str) -> str:
        token_url = f"{AIDevsTasks.BASE_URL}/token/{task_name}"
        data = {
            'apikey': self._api_key
        }

        response = self._request(HTTPMethod.POST, url=token_url, data=json.dumps(data))

        return response['token']

    def task(self) -> dict:
        task_url = f"{AIDevsTasks.BASE_URL}/task/{self._token}"

        result = self._request(HTTPMethod.GET, url=task_url)

        if self._debug:
            self.log("TASK", result)

        return result

    def hint(self) -> dict:
        hint_url = f"{AIDevsTasks.BASE_URL}/hint/{self._task}"

        result = self._request(HTTPMethod.GET, url=hint_url)

        if self._debug:
            self.log("HINT", result)

        return result

    def send_answer(self, answer: dict) -> dict:
        answer_url = f"{AIDevsTasks.BASE_URL}/answer/{self._token}"

        result = self._request(HTTPMethod.POST, url=answer_url, data=json.dumps(answer))

        if self._debug:
            self.log("ANSWER", result)

        return result
