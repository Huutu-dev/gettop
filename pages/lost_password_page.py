from selenium.webdriver.common.by import By

from .base_page import Page


class LostPasswordPage(Page):
    USER_LOGIN = (By.ID, 'user_login')
    RESET_BTN = (By.CSS_SELECTOR, 'button.woocommerce-Button')
    MSG_CONTAINER = (By.CSS_SELECTOR, 'div.message-container')

    def open_me(self):
        self.open_page('my-account/lost-password/')

    def empty_username(self):
        self.clear_input(*self.USER_LOGIN)

    def click_reset_password(self):
        self.click(*self.RESET_BTN)

    def input_user_name(self, name):
        self.input_text(name, *self.USER_LOGIN, clean=True)

    def verify_error(self, msg):
        self.verify_text(msg, self.MSG_CONTAINER)