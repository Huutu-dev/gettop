from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

from .base_page import Page


class MainPage(Page):
    HEADER_SEARCH = (By.CSS_SELECTOR, "div#masthead li.header-search")
    SEARCH_FIELD = (By.ID, "woocommerce-product-search-field-0")
    SEARCH_BTN = (By.CSS_SELECTOR, "button.ux-search-submit")
    SEARCH_NAV = (By.CSS_SELECTOR, "nav.woocommerce-breadcrumb.breadcrumbs.uppercase")

    def drop_search(self):
        m = self.find_element(*self.HEADER_SEARCH)
        a = self.create_action_chain()
        a.move_to_element(m).perform()

    def input_search(self, search_word):
        self.input_text(search_word, *self.SEARCH_FIELD)

    def click_search(self):
        self.click(*self.SEARCH_BTN)

    def search_result(self):
        search_result_elem = self.find_element(*self.SEARCH_NAV)
        return search_result_elem.text
