import allure
from playwright.async_api import Page

from random import randint

from components.input import Input
from components.button import Button

from settings import PASSWORD


class BasePage:
    def __init__(self, page: Page) -> None:
        self.time_for_timeout = 1_500, 2_500

        self.page = page
        self.username = Input(
            page=self.page,
            locator='div.form_group > input#user-name',
            name='Поле ввода "username"'
        )
        self.password = Input(
            page=self.page,
            locator='div.form_group > input#password',
            name='Поле ввода "password"'
        )
        self.enter_button = Button(
            page=self.page,
            locator='input#login-button',
            name='Кнопка "Login"'
        )

    def __await__(self):
        return self

    async def visit(self, url: str, waiting_flag: bool = True, waiting_timeout: tuple = None):
        if waiting_timeout is None:
            waiting_timeout = self.time_for_timeout
        with allure.step(f'Открываем страницу по ссылке: "{url}" c ожиданием полной загрузки'):
            await self.page.goto(url, wait_until='load')

        if waiting_flag:
            random_timeout = randint(*waiting_timeout)
            with allure.step(f'Задержка перед следующим шагом {random_timeout}'):
                await self.page.wait_for_timeout(random_timeout)

    async def reload(self):
        with allure.step(f'Перезагружаем страницу со следующей ссылкой: "{self.page.url}"'):
            return await self.page.reload()

    def check_url(self) -> str:
        with allure.step(f'Возвращаем ссылку текущей страницы'):
            return self.page.url

    async def wait_for_timeout(self, timeout) -> None:
        if isinstance(timeout, tuple):
            waiting_time = randint(*timeout)
        else:
            waiting_time = timeout

        with allure.step(f'Ожидаем {waiting_time}'):
            await self.page.wait_for_timeout(waiting_time)

    async def wait_for_selector(self, locator: str, name: str, waiting_flag: bool = False) -> None:
        with allure.step(f'Ожидаем появления элемента: {name}'):
            await self.page.wait_for_selector(locator)
            if waiting_flag:
                await self.wait_for_timeout(self.time_for_timeout)

    async def waiting_to_load_some_element(self, locator, description: str, has_text=None) -> None:
        with allure.step(f'Ожидание загрузки: "{description}"'):
            element = self.page.locator(locator, has_text=has_text)
            try:
                await element.wait_for(timeout=5_000)
                with allure.step(f'Элемент {description} найден'):
                    pass
            except TimeoutError:
                with allure.step(f'Элемент {description} НЕ был найден'):
                    raise Exception('Ошибка: Элемент не найден!')

    async def log_in_system(self, login):
        with allure.step(f'Пытаемся залогиниться в системе'):
            await self.username.fill(login)
            await self.password.fill(PASSWORD)
            await self.enter_button.click()

    async def get_count_goods_in_cart(self):
        text = await self.page.locator('div#shopping_cart_container').text_content()
        if (result := [symb for symb in text if symb.isdigit()]) == []:
            return 0
        return int(''.join(result))

    async def fill_and_check_post_info(self):
        test_info = ['my_first_name', 'my_last_name', '123456']
        tags = ['first-name', 'last-name', 'postal-code']

        with allure.step(f'Заполняем форму'):
            for index, tag_id in enumerate(tags):
                await Input(self.page, f'input#{tag_id}', tag_id).fill(test_info[index])

        with allure.step(f'Проверим, что форма была заполнена корректно'):
            for index, tag_id in enumerate(tags):
                actual_value = await self.page.locator(f'input#{tag_id}').input_value()
                assert actual_value == test_info[index], f'{actual_value =} != {test_info[index] =}'
