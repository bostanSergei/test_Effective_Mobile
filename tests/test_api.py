import allure
from jsonschema import validate

from http import HTTPStatus

from api.repository import Repository
from models.github_schemas import CreateSchema


@allure.feature(f'Тесты на UI на saucedemo.com')
class TestPages:
    @allure.story("Создание нового репозитория")
    def test_create_repository(self, repository: Repository):
        status_code, json_response = repository.create_public_repo()

        with allure.step(f'Выполняем проверку status code ответа от GitHub'):
            assert status_code == HTTPStatus.CREATED

        with allure.step(f'Выполняем валидацию полученного ответа'):
            validate(json_response, CreateSchema.model_json_schema())

    @allure.story("Получение списка всех публичных репозиториев")
    def test_get_repo_list(self, repository: Repository):
        all_public_repository: list = []
        status_code, json_response = repository.get_public_repo()

        with allure.step(f'Выполняем проверку status code ответа от GitHub'):
            assert status_code == HTTPStatus.OK

        with allure.step(f'Выполняем валидацию полученного ответа'):
            assert isinstance(json_response, list) is True
            for repo in json_response:
                validate(repo, CreateSchema.model_json_schema())
                all_public_repository.append(repo['name'])

        with allure.step(f'Проверяем наличие ранее созданного репозитория в списке публичных репозиториев'):
            assert repository.get_test_repo_name() in all_public_repository

    @allure.story("Удаление тестового репозитория")
    def test_delete_repo(self, repository: Repository):
        status_code = repository.delete_repo()

        with allure.step(f'Выполняем проверку status code ответа от GitHub'):
            assert status_code == HTTPStatus.NO_CONTENT
