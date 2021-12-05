from abc import ABCMeta, abstractmethod
from contextlib import contextmanager

from selenium.webdriver.remote.webdriver import WebDriver, WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC


class Page(metaclass=ABCMeta):
    def __init__(self, driver: WebDriver):
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

    def wait_for_opening(self, partial_url):
        return self.driver.wait.until(EC.url_contains(partial_url))

    def input_text(self, text, *locator, clean=False):
        elem = self._driver.find_element(*locator)
        if clean:
            elem.clear()
        elem.send_keys(text)

    def click(self, *locator):
        self.driver.find_element(*locator).click()

    def click_wait_page_changed(self, *locator):
        old_url = self._driver.current_url
        self.click(*locator)
        self._driver.wait.until(EC.none_of(EC.url_to_be(old_url)))

    def verify_text(self, expected_text, *locator):
        actual_text = self.driver.find_element(*locator).text
        assert actual_text == expected_text, \
            f'Error! Actual text "{actual_text}" does not match expected "{expected_text}"'

    def verify_url_contains_query(self, query):
        assert query in self.driver.current_url, f'{query} not in {self.driver.current_url}'

    @contextmanager
    def wait_for_changed(self, an_element: WebElement = None):
        an_element = an_element or self.find_element(By.TAG_NAME, 'html')
        yield
        self.driver.wait.until(EC.staleness_of(an_element))
