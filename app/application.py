from pages.main_page import MainPage
from pages.account_page import MyAccount
from pages.order_shop_page import ShopPage


class Application:
    def __init__(self, driver):
        self.main_page = MainPage(driver)
        self.my_account = MyAccount(driver)
        self.shop_page = ShopPage(driver)
