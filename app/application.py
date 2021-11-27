from pages.main_page import MainPage
from pages.account_page import MyAccount


class Application:
    def __init__(self, driver):
        self.main_page = MainPage(driver)
        self.my_account = MyAccount(driver)
