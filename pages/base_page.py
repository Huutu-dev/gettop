from abc import ABCMeta, abstractmethod

from selenium.webdriver.common.action_chains import ActionChains


class Page(metaclass=ABCMeta):
    def __init__(self, driver):
        self._driver = driver
        self._base_url = 'https://gettop.us/'

    @property
    def driver(self):
        return self._driver

    def open_page(self, page_address=''):
        self.driver.get(f'{self._base_url}{page_address}')

    def find_element(self, *locator):
        return self.driver.find_element(*locator)

    def create_action_chain(self) -> ActionChains:
        return ActionChains(self.driver)

    def clear_input(self, *locator):
        self.driver.find_element(*locator).clear()

    def input_text(self, text, *locator, clean=False):
        elem = self._driver.find_element(*locator)
        if clean:
            elem.clear()
        elem.send_keys(text)

    def click(self, *locator):
        self.driver.find_element(*locator).click()

    def verify_text(self, expected_text, *locator):
        actual_text = self.driver.find_element(*locator).text
        assert actual_text == expected_text, \
            f'Error! Actual text "{actual_text}" does not match expected "{expected_text}"'

