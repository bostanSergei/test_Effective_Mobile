from playwright.async_api import Page, Locator

from abc import ABC, abstractmethod
from typing import Union


class Component(ABC):
    def __init__(self, page: Page, locator: Union[str, Locator], name: str) -> None:
        self.page = page
        self.locator = locator
        self.name = name

    @property
    @abstractmethod
    def type_of(self) -> str:
        return 'component'

    def get_locator(self, **kwargs) -> Locator:
        if isinstance(self.locator, str):
            locator = self.locator.format(**kwargs)
            return self.page.locator(locator, **kwargs)
        else:
            return self.locator
