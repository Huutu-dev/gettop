from selenium.webdriver.common.by import By
from .base_page import Page


class ProductPage(Page):
    PROD_TITLE = (By.CSS_SELECTOR, 'h1.product-title.entry-title')
    OUT_OF_STOCK = (By.CSS_SELECTOR, 'p.out-of-stock')
    ADD_CART_BUTTON = (By.CSS_SELECTOR, 'button.single_add_to_cart_button')
    PROD_PRICE_AMOUNT = (By.CSS_SELECTOR, 'div.product-main p.product-page-price span.woocommerce-Price-amount')

    _storage = {}

    @classmethod
    def get_storage(cls, reset=False):
        if reset:
            cls._storage.clear()
        return cls._storage

    def __init__(self, driver):
        super(ProductPage, self).__init__(driver)
        self._price = None
        self._out_of_stock = None
        self._prod_name = None

    def open_me(self, prod_address: str, product_name=None):
        """eg 'https://gettop.us/product/airpods-pro/"""
        if 'product' not in prod_address:
            prod_address = f'product/{prod_address}'
        self.open_page(prod_address)
        self.pre_load(prod_address)
        if product_name:
            self.verify_prod_name(product_name)

    def verify_prod_name(self, prod_name):
        assert self.product_name == prod_name, \
            f'Expected "{self.product_name}", but got {prod_name}'
        # print('Working on', prod_name)

    @property
    def product_name(self) -> str:
        return self._prod_name

    @property
    def price(self) -> float:
        return self._price

    @property
    def out_of_stock(self) -> bool:
        return self._out_of_stock

    def pre_load(self, url):
        self.wait_for_opening(url)
        # price
        elements = self.find_elements(*self.PROD_PRICE_AMOUNT)
        if len(elements) == 1:
            ele = elements[0]
        else:
            for ele in elements:
                parent_node = ele.find_element(By.XPATH, '..')
                if parent_node.tag_name.lower() != 'del':
                    break
            else:
                assert False, 'Product Price could not found'
        self._price = float(ele.text.strip().replace('$', '').replace(',', ''))

        # check stock
        self._out_of_stock = len(self.find_elements(*self.OUT_OF_STOCK)) > 0

        # product name
        ele = self.find_element(*self.PROD_TITLE)
        self._prod_name = ele.text.strip()

    def warning_stock(self) -> str:
        if self.out_of_stock:
            return f'{self.product_name} is out of stock!'
        return "In STOCK"

    def add_to_cart(self):
        """Obsolete, using CartNav.add_product(self.ADD_CART_BUTTON)"""
        self.wait_for_element_click(self.ADD_CART_BUTTON)

    @property
    def add_cart_button_locator(self):
        return self.ADD_CART_BUTTON
