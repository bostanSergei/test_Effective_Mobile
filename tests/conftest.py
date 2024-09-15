import allure
import pytest

from playwright.async_api import Page, async_playwright

from datetime import datetime

from settings import get_right_path, PATH_TO_ROOT
from pages.base_page import BasePage
from api.repository import Repository


HEADLESS = False

# START_PARAMS - список кортежей с параметрами запуска, где первый параметр - движок, второй - устройство запуска.
# Если второй параметр - None - инициализируем десктопный браузер с параметрами 'width': 1440, 'height': 1000
START_PARAMS = [
    # ('chromium', None),
    ('firefox', None),
    # ('webkit', None),
    # ('chromium', "Galaxy S5"),
    # ('webkit', "iPhone 14 Pro Max"),
]


@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):
    allure_directory = getattr(config.option, "allure_report_dir", None)
    if not allure_directory:
        report_folder_name = f'report_day_{datetime.now().strftime("%d-%m-%y")}'
        setattr(
            config.option,
            "allure_report_dir",
            f"{get_right_path(PATH_TO_ROOT, 'reports', 'allure_report')}{report_folder_name}"
        )


@pytest.fixture
async def playwright_context_manager():
    with allure.step('Инициализируем контекстный менеджер'):
        async with async_playwright() as playwright_context_manager:
            yield playwright_context_manager

    await playwright_context_manager.stop()


@pytest.fixture(scope='function', params=START_PARAMS)
async def browser_page(playwright_context_manager, request) -> Page:
    launch_dt: str = datetime.now().strftime('%d_%m__%H_%M_%S')

    browser_name, device_name = request.param
    if device_name is not None:
        device_info = playwright_context_manager.devices[device_name]
        browser = await getattr(playwright_context_manager, browser_name).launch(headless=HEADLESS)
        context = await browser.new_context(**device_info)
    else:
        browser = await getattr(playwright_context_manager, browser_name).launch(headless=HEADLESS)
        context = await browser.new_context(
            viewport={'width': 1440, 'height': 1000},
        )

    await context.tracing.start(screenshots=True, snapshots=True, sources=True)

    page = await context.new_page()

    yield page

    trace_file = f'{get_right_path(PATH_TO_ROOT, "reports", "playwright_trace")}trace_{launch_dt}.zip'
    await context.tracing.stop(path=trace_file)
    allure.attach.file(trace_file)

    await browser.close()


@pytest.fixture(scope='function')
def test_page(browser_page: Page) -> BasePage:
    return BasePage(browser_page)


@pytest.fixture(scope='function')
def repository() -> Repository:
    yield Repository()
