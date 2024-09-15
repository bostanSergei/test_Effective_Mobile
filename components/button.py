import allure

from components.component import Component
from typing import Optional


class Button(Component):
    @property
    def type_of(self) -> str:
        return 'button'

    async def click(
            self,
            click_count: Optional[int] = None,
            timeout: Optional[int] = None,
            delay: Optional[float] = None,
            **kwargs
    ):
        with allure.step(f'Кликнуть на "{self.type_of}" с именем "{self.name}"'):
            locator = self.get_locator(**kwargs)
            await locator.click(
                click_count=click_count,
                timeout=timeout,
                delay=delay
            )
