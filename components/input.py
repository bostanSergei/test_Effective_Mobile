import allure

from components.component import Component
from typing import Union, Optional


class Input(Component):
    @property
    def type_of(self) -> str:
        return 'input'

    async def fill(self, value: str, **kwargs) -> None:
        with allure.step(f'Заполнить {self.type_of} "{self.name}" значением "{value}"'):
            locator = self.get_locator(**kwargs)
            await locator.fill(value)
