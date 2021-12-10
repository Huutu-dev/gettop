from selenium.webdriver.common.by import By

from .base_page import Page


class MyAccount(Page):
    ID_WRAPPER = (By.ID, 'wrapper')
    ID_USERNAME = (By.ID, 'username')
    ID_PASSWORD = (By.ID, 'password')
    WOO_SUBMIT = (By.CSS_SELECTOR, 'button.woocommerce-button')
    ALERT_DIV = (By.CSS_SELECTOR, 'div[id="wrapper"] div.message-container')

    def open_me(self):
        page_address = 'my-account'
        self.open_page(page_address)

    def clean_email_field(self):
        self.clear_input(*self.ID_USERNAME)

    def clean_password_field(self):
        self.clear_input(*self.ID_PASSWORD)

    def input_password_field(self, text):
        self.input_text(text, *self.ID_PASSWORD, clean=True)

    def input_email_field(self, text):
        self.input_text(text, *self.ID_USERNAME, clean=True)

    def click_login(self):
        self.click(*self.WOO_SUBMIT)

    def verify_error(self, msg):
        self.verify_text(msg, self.ALERT_DIV)
