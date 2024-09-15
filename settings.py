from dotenv import load_dotenv

import os


BASE_URL = 'https://www.saucedemo.com/'
PASSWORD = 'secret_sauce'
STANDARD_USER = 'standard_user'
LOCKED_OUT_USER = 'locked_out_user'
PROBLEM_USER = 'problem_user'

API_URL = 'https://api.github.com'


def get_project_root() -> str:
    """Задача функции - вернуть абсолютный путь к корню проекта. Поиск будет осуществляться ориентируясь на README.md"""
    current_path = os.path.abspath(__file__)
    while not os.path.exists(os.path.join(current_path, 'README.md')):
        current_path = os.path.dirname(current_path)

    return current_path


def get_right_path(root_path: str, *args) -> str:
    """В случае запуска на разных ОС функция обеспечит корректные пути для перемещения по папкам.
    Принимает путь до корня проекта и неограниченное необязательных аргументов - имена папок - хлебные крошки.
    Задача функции сформировать строку с правильным итоговым путем до папки назначения в соответствии с ОС"""
    if os.name == 'posix':
        path_to_folder = root_path + '/' + '/'.join(args) + '/'
    else:
        path_to_folder = root_path + '\\' + '\\'.join(args) + '\\'

    return path_to_folder


PATH_TO_ROOT = get_project_root()

load_dotenv(f'{PATH_TO_ROOT}/.env')

USER_NAME = os.getenv('USER_NAME')
REPO_NAME = os.getenv('REPO_NAME')
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
