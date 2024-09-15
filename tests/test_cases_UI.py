import allure
import pytest

from random import choice

from settings import BASE_URL, STANDARD_USER, LOCKED_OUT_USER, PROBLEM_USER
from pages.base_page import BasePage

from components.button import Button


@allure.feature(f'Тесты на UI на saucedemo.com')
class TestPages:
    # Один из тестов уйдет в FAILED на этапе заполнения заявки (PROBLEM_USER - неадекватно заполняется поле "контактов")
    @pytest.mark.parametrize('user', [STANDARD_USER, PROBLEM_USER])
    @allure.story('Тест по маршруту: user - выбор товара - корзина - "оплата".')
    async def test_first_route(self, test_page: BasePage, user):
        await test_page.visit(BASE_URL, waiting_flag=True)

        await test_page.log_in_system(user)

        with allure.step(f'Ожидаем загрузки товаров с максимальной задержкой в 3 секунды'):
            try:
                await test_page.page.wait_for_selector('div.inventory_list', timeout=3_000)
            except TimeoutError:
                raise Exception('Страница была загружена некорректно!')

        count_items_in_cart_before_adding = await test_page.get_count_goods_in_cart()

        with allure.step(f'Получим все товары со страницы с товарами'):
            items = await test_page.page.locator('div.inventory_list > div.inventory_item:visible').all()

        random_item = choice(items)
        title_item = (await random_item.locator('div.inventory_item_name').text_content()).strip()
        with (allure.step(f'Random товар "{title_item}" добавляем в корзину')):
            await random_item.locator('button.btn_inventory').click()

        count_items_in_cart_after_adding = await test_page.get_count_goods_in_cart()
        with allure.step(f"""Проверяем, что количество товаров в корзине изменилось.
                Было: '{count_items_in_cart_before_adding}'. Стало: '{count_items_in_cart_after_adding}'"""):
            assert count_items_in_cart_before_adding < count_items_in_cart_after_adding, 'Error!'

        with allure.step(f'Переходим в корзину с товарами.'):
            await test_page.page.locator('div#shopping_cart_container').click()

        with allure.step(f'Ожидаем перехода на страницу и появления списка товаров'):
            await test_page.page.wait_for_selector('div#cart_contents_container > div > div.cart_list', timeout=3_000)

        with allure.step(f'Проверяем количество товаров в списке. Их должно быть 1'):
            all_items = await test_page.page.locator('div.cart_item').all()
            assert len(all_items) == 1, 'Количество товаров в списке не соответствует ожидаемому!'

        with allure.step(f'Проверяем соответствует ли товар тому, что был добавлен в корзину'):
            current_item = await all_items[0].locator('div.inventory_item_name').text_content()
            assert current_item.strip() == title_item, 'Товар в корзине НЕ соответствует тому, что было добавлено'

        await Button(test_page.page, 'button#checkout', 'Checkout').click()

        with allure.step(f'Ожидаем перехода на страницу с информацией для отправки заказа'):
            await test_page.page.wait_for_selector('form > div.checkout_info', timeout=3_000)

        await test_page.fill_and_check_post_info()

        await Button(test_page.page, 'input#continue', 'Continue').click()
        with allure.step(f'Ожидаем перехода на финальную страницу'):
            await test_page.page.wait_for_selector('button#finish', timeout=2_500)
        await Button(test_page.page, 'button#finish', 'Finish').click()

        with allure.step(f'Ожидаем сообщения "Thank you for your order!"'):
            await test_page.page.wait_for_selector(
                'h2.complete-header:has-text("Thank you for your order!")', timeout=2_500
            )
        await Button(test_page.page, 'button#back-to-products', 'Back Home').click()

    @allure.story('Тест по маршруту: locked_out_user - Пользователь заблокирован')
    async def test_second_route(self, test_page: BasePage):
        await test_page.visit(BASE_URL, waiting_flag=True)

        await test_page.log_in_system(LOCKED_OUT_USER)
        with allure.step(f'Ожидаем сообщения о блокировке пользователя'):
            await test_page.page.wait_for_selector('h3:has-text("Epic sadface: Sorry, this user has been locked out.")')
