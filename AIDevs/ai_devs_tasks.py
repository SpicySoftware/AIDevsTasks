import json
import os
import requests

from enum import Enum
from pprint import pprint


class HTTPMethod(Enum):
    GET  = 'GET'
    POST = 'POST'


class AIDevsTasks:

    class WrongRequest(Exception):
        pass

    class ApiKeyMissing(Exception):
        pass

    class BaseUrlMissing(Exception):
        pass

    def __init__(self, task: str, debug: bool = True):
        self._task = task
        self._debug = debug

        self._load_env_vars()

        self._token = self._obtain_task_token(task)

    def _load_env_vars(self):
        self._api_key = os.getenv('AIDEVS_API_KEY')
        if not self._api_key:
            raise AIDevsTasks.ApiKeyMissing("API key is not defined in your environment variables, "
                                            "please define it first")

        self._base_url = os.getenv('AIDEVS_BASE_URL')
        if not self._base_url:
            raise AIDevsTasks.BaseUrlMissing("Base URL is not defined in your environment variables, "
                                             "please define it first")

    def _log(self, header: str, result):
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
        token_url = f"{self._base_url}/token/{task_name}"
        data = {
            'apikey': self._api_key
        }

        response = self._request(HTTPMethod.POST, url=token_url, data=json.dumps(data))

        return response['token']

    def task(self) -> dict:
        task_url = f"{self._base_url}/task/{self._token}"

        result = self._request(HTTPMethod.GET, url=task_url)

        if self._debug:
            self._log("TASK", result)

        return result

    def hint(self) -> dict:
        hint_url = f"{self._base_url}/hint/{self._task}"

        result = self._request(HTTPMethod.GET, url=hint_url)

        if self._debug:
            self._log("HINT", result)

        return result

    def send_answer(self, answer: dict) -> dict:
        answer_url = f"{self._base_url}/answer/{self._token}"

        result = self._request(HTTPMethod.POST, url=answer_url, data=json.dumps(answer))

        if self._debug:
            self._log("ANSWER", result)

        return result
