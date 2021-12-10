from pages.main_page import MainPage
from pages.account_page import MyAccount
from pages.order_shop_page import ShopPage
from pages.product_page import ProductPage
from pages.header_page import HeaderNav
from pages.cart_page import CartPage


class Application:
    def __init__(self, driver):
        self.main_page = MainPage(driver)
        self.header_nav = HeaderNav(driver)
        self.my_account = MyAccount(driver)
        self.shop_page = ShopPage(driver)
        self.product_page = ProductPage(driver)
        self.cart_page = CartPage(driver)
