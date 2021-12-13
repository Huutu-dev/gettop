from selenium.webdriver.remote.webdriver import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common import exceptions as selenium_error

from .base_page import Page
from .product_page import ProductPage
from .cart_page import CartPage
from .checkout_page import CheckoutPage


class HeaderNav(Page):
    def __init__(self, driver):
        super(HeaderNav, self).__init__(driver)
        self.cart_nav = CartNav(self)

    def get_header_elem(self):
        return self.find_element(By.ID, 'header')


class CartNav(Page):
    RIGHT_ELEMENTS = (By.CSS_SELECTOR, 'div.flex-col.hide-for-medium.flex-right')
    MOBILE_RIGHT_ELEMENTS = (By.CSS_SELECTOR, 'div.flex-col.show-for-medium.flex-right')
    _RIGHT_CART_PRICE = (By.CSS_SELECTOR, 'span.woocommerce-Price-amount')
    _RIGHT_CART_ICON = (By.CSS_SELECTOR, 'span.cart-icon')
    DROP_DOWN = (By.CSS_SELECTOR, 'li.cart-item.has-dropdown')
    EMPTY_MSG = (By.CSS_SELECTOR, 'li.cart-item.has-dropdown p.woocommerce-mini-cart__empty-message')
    UL_PRODUCT = (By.CSS_SELECTOR, 'li.cart-item.has-dropdown ul.woocommerce-mini-cart.cart_list.product_list_widget')
    _CART_ITEMS = (By.CSS_SELECTOR, 'li.mini_cart_item')
    SUBTOTAL = (By.CSS_SELECTOR, 'li.cart-item.has-dropdown p.total')
    WC_FORWARD = (By.CSS_SELECTOR, 'li.cart-item.has-dropdown a.button.wc-forward')

    def __init__(self, header: HeaderNav):
        super(CartNav, self).__init__(header.driver)
        self._header = header
        self._storage = {}

    def get_cart_amount(self):
        price_elem = self.find_element(*self.RIGHT_ELEMENTS).find_element(*self._RIGHT_CART_PRICE)
        return float(price_elem.text.replace('$', '').replace(',', ''))

    def get_number_prods(self):
        icon_elem = self.find_element(*self.RIGHT_ELEMENTS).find_element(*self._RIGHT_CART_ICON)
        return int(icon_elem.text.replace(',', ''))

    def get_view_card_element(self):
        return next(e for e in self.find_elements(*self.WC_FORWARD) if 'checkout' not in e.get_attribute('class'))

    def get_checkout_element(self):
        return next(e for e in self.find_elements(*self.WC_FORWARD) if 'checkout' in e.get_attribute('class'))

    def wait_cart_presence(self):
        self.wait_for_renew(self.RIGHT_ELEMENTS)

    def verify_amount_price(self, product_price):
        old_amount = self._storage['cart_amount']
        expected_amount = old_amount + product_price
        new_amount = self.get_cart_amount()
        assert new_amount == expected_amount, f'Expected ${expected_amount} amount, but got ${new_amount}'

    def verify_count_products(self, expected_count=None):
        if expected_count is None:
            expected_count = self._storage['number_prods'] + 1
        new_count = self.get_number_prods()
        assert new_count == expected_count, f'Expected ${expected_count} product(s), but got {new_count}'

    def add_product(self, product_page: ProductPage):
        self._storage['number_prods'] = self.get_number_prods()
        self._storage['cart_amount'] = self.get_cart_amount()
        self._storage['product_obj'] = product_page
        right_ele = self.find_element(*self.RIGHT_ELEMENTS)
        add_locator = product_page.add_cart_button_locator
        self.wait_for_element_click(add_locator)
        self.wait_staleness_of(right_ele)

    def click_to_open_cart_page(self):
        icon_elem = self.find_element(*self.RIGHT_ELEMENTS).find_element(*self._RIGHT_CART_ICON)
        icon_elem.click()
        self.wait_for_opening(CartPage.partial_url)

    def capture_hover_icon(self):
        icon_elem = self.find_element(*self.RIGHT_ELEMENTS).find_element(*self._RIGHT_CART_ICON)
        action = self.action_chain()
        action.move_to_element(icon_elem).perform()
        self.wait_for_element_appear(self.EMPTY_MSG)
        self._storage['drop_message'] = self.find_element(*self.EMPTY_MSG).text

    def verify_store_message(self, expected_text):
        actual_text = self._storage['drop_message']
        assert actual_text == expected_text, \
            f'Error! Actual text "{actual_text}" does not match expected "{expected_text}"'

    def hover_icon(self):
        icon_elem = self.find_element(*self.RIGHT_ELEMENTS).find_element(*self._RIGHT_CART_ICON)
        self.action_chain().move_to_element(icon_elem).perform()

    def verify_drop_message(self, expected_text):
        self.wait_for_element_displayed(self.EMPTY_MSG)
        self.verify_text(expected_text, self.EMPTY_MSG)

    def _parse_mini_cart_text(self):
        cart_items = {}
        for ele in self.find_element(*self.RIGHT_ELEMENTS).find_elements(*self._CART_ITEMS):
            info = [x.strip() for x in ele.text.split('\n') if x.strip()]  # ['×', 'iPhone SE', '1 × $379.00']
            try:
                _, prod_name, s_amount = info
            except ValueError as ex:
                print(info)
                raise ex

            number, _, price = s_amount.split()
            number = int(number)
            price = float(price.replace('$', '').replace(',', ''))
            cart_items[prod_name] = {'number': number, 'price': price}

        return cart_items

    def remove_latest_product(self):
        product_obj = self._storage['product_obj']
        product_name = product_obj.product_name

        action = self.action_chain()
        ul_product_ele = self.find_element(*self.UL_PRODUCT)
        action.move_to_element(ul_product_ele).perform()
        for ele in ul_product_ele.find_elements(*self._CART_ITEMS):
            self.driver.execute_script("arguments[0].scrollIntoView();", ele)
            if not any(x.strip() for x in ele.text.split('\n') if x.strip() == product_name):
                continue

            # remove_ele = self.wait_for_sub_element_displayed(ele, (By.CSS_SELECTOR, 'a.remove_from_cart_button'))
            self.wait_for_element_click(ele.find_element(By.CSS_SELECTOR, 'a.remove_from_cart_button'))
            # remove_ele = ele.find_element(By.CSS_SELECTOR, 'a.remove_from_cart_button')
            # self.action_chain().move_to_element(remove_ele).click(remove_ele).perform()
            self.wait_staleness_of(ele)
            break
        else:
            print(product_name)
            raise ValueError('No such element product in cart')

        # Now verify product has been deleted entirely
        # To make sure ul_product_ele is not stale
        try:
            ul_product_ele = self.find_element(*self.UL_PRODUCT)
        except selenium_error.NoSuchElementException:
            # Empty list
            return
        for ele in ul_product_ele.find_elements(*self._CART_ITEMS):
            cart_prod = ele.text.split('\n')[1]
            if cart_prod == product_name:
                print(cart_prod)
            assert cart_prod != product_name, \
                f'Error, could not remove product "{cart_prod}" from cart'

    def _verify_product(self, cart_items):
        product_obj = self._storage['product_obj']
        product_name = product_obj.product_name
        product_price = product_obj.price

        assert product_name in cart_items
        actual_price = cart_items[product_name]['price']
        assert product_price == actual_price, \
            f'Error! Actual price "{actual_price}" does not match expected "{product_price}" of product "{product_name}"'

    def _verify_subtotal(self, cart_items):
        subtotal_ele = self.find_element(*self.SUBTOTAL)  # Subtotal: $379.00
        subtotal_text = subtotal_ele.text
        subtotal = float(subtotal_text.split()[-1].replace('$', '').replace(',', ''))

        acc = 0
        for key, value in cart_items.items():
            price = value['price']
            number = value['number']
            acc += number * price

        assert subtotal == acc, f'Error, {subtotal_text} does not match expected ${acc}'

    def verify_products_subtotal(self):
        cart_items = self._parse_mini_cart_text()
        self._verify_product(cart_items)
        self._verify_subtotal(cart_items)

    def verify_click_view_cart(self):
        elem = self.get_view_card_element()
        self.click_wait_page_changed(elem)
        self.verify_url_contains_query(CartPage.partial_url)

    def verify_click_checkout(self):
        elem = self.get_checkout_element()
        self.click_wait_page_changed(elem)
        self.verify_url_contains_query(CheckoutPage.partial_url)
