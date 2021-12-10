from selenium.webdriver.common.by import By
from .base_page import Page


class CartPage(Page):
    EMPTY_TEXT = (By.CSS_SELECTOR, 'p.cart-empty.woocommerce-info')
    partial_url = 'cart/'

    def open_me(self):
        self.open_page(self.partial_url)

    def verify_is_empty(self):
        self.verify_text('Your cart is currently empty.', self.EMPTY_TEXT)
