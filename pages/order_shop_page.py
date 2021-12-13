from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC

from .base_page import Page


class _OrderSelection(Page):
    SELECT_ELEM = (By.CSS_SELECTOR, 'select.orderby')
    options = {
        "menu_order": "Default sorting",
        "popularity": "Sort by popularity",
        "rating": "Sort by average rating",
        "date": "Sort by latest",
        "price": "Sort by price: low to high",
        "price-desc": "Sort by price: high to low"
    }

    @property
    def _selector(self):
        return Select(self._driver.find_element(*self.SELECT_ELEM))

    def sort_by(self, visible_text):
        with self.wait_for_changed():
            self._selector.select_by_visible_text(visible_text)

    def selected_by(self, visible_text) -> bool:
        return self._selector.first_selected_option.text == visible_text

    def sort_by_latest(self):
        self.sort_by('Sort by latest')

    def latest_is_sorted(self):
        self.selected_by('Sort by latest')

    def sort_by_default(self):
        self.sort_by('Default sorting')

    def default_is_sorted(self):
        self.selected_by('Default sorting')


class _Pagination(Page):
    NAV_LINK = (By.CSS_SELECTOR, 'ul.page-numbers')
    PAGE_CURRENT = (By.CSS_SELECTOR, 'span.page-number.current')
    PAGE_1 = (By.XPATH, '//a[@class="page-number" and text()="1"]')
    PAGE_2 = (By.XPATH, '//a[@class="page-number" and text()="2"]')
    PREV_PAGE = (By.CSS_SELECTOR, 'a.prev.page-number')
    NEXT_PAGE = (By.CSS_SELECTOR, 'a.next.page-number')

    def __init__(self, driver):
        super(_Pagination, self).__init__(driver)

    def find_rel_element(self, *locator):
        nav_elem = self.find_element(*self.NAV_LINK)
        self.action_chain().move_to_element(nav_elem).perform()
        return nav_elem.find_element(*locator)

    def verify_current_page_number(self, number):
        number_current_elem = self.find_rel_element(*self.PAGE_CURRENT)
        actual_number = number_current_elem.text
        assert actual_number == number, \
            f'Error! Actual page number "{actual_number}" does not match expected "{number}"'

    def click_on_page_number(self, number):
        if number == "1":
            self.find_rel_element(*self.PAGE_1).click()
        elif number == "2":
            self.find_rel_element(*self.PAGE_2).click()

    def click_on_go_icon(self, go_icon):
        if go_icon == '>':
            self.find_rel_element(*self.NEXT_PAGE).click()
        elif go_icon == '<':
            self.find_rel_element(*self.PREV_PAGE).click()


class ShopPage(Page):
    ORDER_DATE_URL = 'shop/?orderby=date'
    ORDER_DATE_2_URL = 'shop/page/2/?orderby=date'

    def __init__(self, driver):
        super(ShopPage, self).__init__(driver)
        self.selector = _OrderSelection(self.driver)
        self.nav_pagination = _Pagination(self.driver)

    def open_me(self):
        self.open_page('shop/')

    def open_order_date_page(self, page_number='1'):
        if page_number == '1':
            self.open_page(self.ORDER_DATE_URL)
        elif page_number == '2':
            self.open_page(self.ORDER_DATE_2_URL)

    def query_date_opened(self):
        self.verify_url_contains_query('?orderby=date')



