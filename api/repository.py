import allure
import requests

import json

from settings import USER_NAME, REPO_NAME, GITHUB_TOKEN, API_URL


class Repository:
    def __init__(self):
        self._user_name = USER_NAME
        self._repository_name = REPO_NAME
        self._header = {"Authorization": f"token {GITHUB_TOKEN}"}

        self.path_to_get_list_repo = f"{API_URL}/users/{self._user_name}/repos"
        self.path_to_create_repo = f"{API_URL}/user/repos"
        self.path_to_delete_repo = f"{API_URL}/repos/{self._user_name}/{self._repository_name}"

    def get_public_repo(self) -> tuple[int, dict]:
        with allure.step(f'GET запрос на url "{self.path_to_get_list_repo}" для получения списка репозиториев'):
            response = requests.get(self.path_to_get_list_repo)
            return response.status_code, response.json()

    def create_public_repo(self) -> tuple[int, dict]:
        with allure.step(f'POST запрос на url "{self.path_to_create_repo}" на создание публичного репозитория'):
            data_with_repo_info = {
                'name': self._repository_name,
                'description': 'create test repo for test task',
                'private': False,
            }
            response = requests.post(
                url=self.path_to_create_repo,
                headers=self._header,
                data=json.dumps(data_with_repo_info),
            )
            return response.status_code, response.json()

    def delete_repo(self) -> int:
        with allure.step(f'DELETE запрос на url "{self.path_to_delete_repo}" на удаление репозитория'):
            response = requests.delete(url=self.path_to_delete_repo, headers=self._header)
            return response.status_code

    def get_test_repo_name(self):
        return self._repository_name
