from abc import ABCMeta
from contextlib import contextmanager
from typing import Optional, Union, Tuple

from selenium.common import exceptions as selenium_error
from selenium.webdriver.remote.webdriver import WebDriver, WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains


class Page(metaclass=ABCMeta):
    def __init__(self, driver: WebDriver):
        self._driver = driver
        self._base_url = 'https://gettop.us/'

    @property
    def driver(self):
        return self._driver

    def open_page(self, page_address=''):
        if page_address.startswith(self._base_url):
            self.driver.get(page_address)
        else:
            self.driver.get(f'{self._base_url}{page_address}')

    def find_element(self, *locator):
        return self.driver.find_element(*locator)

    def find_elements(self, *locator):
        return self.driver.find_elements(*locator)

    def action_chain(self) -> ActionChains:
        return ActionChains(self.driver)

    def clear_input(self, *locator):
        self.driver.find_element(*locator).clear()

    def wait_for_opening(self, partial_url):
        return self.driver.wait.until(EC.url_contains(partial_url))

    def input_text(self, text, *locator, clean=False):
        elem = self.driver.find_element(*locator)
        if clean:
            elem.clear()
        elem.send_keys(text)

    def click(self, *locator):
        self.driver.find_element(*locator).click()

    def click_wait_page_changed(self, mark):
        old_url = self._driver.current_url
        if isinstance(mark, WebElement):
            mark.click()
        else:
            self.click(*mark)
        self.driver.wait.until(EC.url_changes(old_url))

    def wait_for_element_appear(self, locator) -> WebElement:
        return self.driver.wait.until(EC.presence_of_element_located(locator))

    def wait_for_element_displayed(self, locator):
        self.driver.wait.until(EC.visibility_of_element_located(locator))

    @staticmethod
    def wait_for_sub_element_displayed(element: WebElement, locator):
        def _predicate(_):
            try:
                sub_element = element.find_element(*locator)
                return sub_element if sub_element.is_displayed() else False
            except selenium_error.InvalidSelectorException as e:
                raise e
            except selenium_error.StaleElementReferenceException:
                return False

        driver = element.parent
        return driver.wait.until(_predicate)

    def wait_for_element_click(self, mark, message=''):
        e = self.driver.wait.until(EC.element_to_be_clickable(mark), message=message)
        e.click()

    def wait_for_renew(self, locator):
        element = self.find_element(*locator)
        self.driver.wait.until(EC.staleness_of(element))
        self.wait_for_element_appear(locator)

    def wait_staleness_of(self, element: WebElement):
        self.driver.wait.until(EC.staleness_of(element))

    def verify_text(self, expected_text, locator):
        e = self.driver.wait.until(EC.visibility_of_element_located(locator))
        actual_text = e.text
        assert actual_text == expected_text, \
            f'Error! Actual text "{actual_text}" does not match expected "{expected_text}"'

    def verify_contain_text(self, expected_text, locator):
        e = self.driver.wait.until(EC.visibility_of_element_located(locator))
        actual_text = e.text
        assert expected_text in actual_text, \
            f'Error! Actual text "{actual_text}" does not contain expected "{expected_text}"'

    def verify_url_contains_query(self, query):
        assert query in self.driver.current_url, f'{query} not in {self.driver.current_url}'

    def is_visible_in_viewport(self, element: WebElement) -> bool:
        def _predicate(_):
            try:
                return element if element.is_displayed() else False
            except selenium_error.InvalidSelectorException as e:
                raise e
            except selenium_error.StaleElementReferenceException:
                return False

        self.driver.wait.until(_predicate)

        source_js = """let elem = arguments[0];
        let box = elem.getBoundingClientRect();
        let cx = box.left + box.width / 2, 
            cy = box.top + box.height / 2;
        let e = document.elementFromPoint(cx, cy);
        for(; e; e = e.parentElement) {
            if(e === elem)
                return true;
        }
        return false;
        """
        return self.driver.execute_script(source_js, element)

    def move_to_element_for_see(self, mark: Union[WebElement, Tuple]):
        element = mark if isinstance(mark, WebElement) else self.find_element(*mark)
        if not self.is_visible_in_viewport(element):
            self.action_chain().move_to_element(element).perform()
        return element

    @contextmanager
    def wait_for_changed(self, an_element: Optional[WebElement] = None):
        an_element = an_element or self.find_element(By.TAG_NAME, 'html')
        yield
        self.driver.wait.until(EC.staleness_of(an_element))
