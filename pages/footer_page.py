from typing import Tuple, List, Optional, Any
from operator import itemgetter

from selenium.webdriver.common.by import By
from .base_page import Page


class Footer(Page):
    FOOTER = (By.ID, 'footer')

    # FOOTER 1
    PRODUCT_GROUPS = dict(
        BEST_SELLING=(By.ID, 'woocommerce_products-11'),
        LATEST=(By.ID, 'woocommerce_products-12'),
        TOP_RATED=(By.ID, 'woocommerce_top_rated_products-3')
    )
    TITLE = (By.CSS_SELECTOR, 'span.widget-title')
    PROD_LIST = (By.CSS_SELECTOR, 'ul li')
    PROD_NAME = (By.CSS_SELECTOR, 'a span.product-title')
    INS_PRICE = (By.CSS_SELECTOR, 'ins span.woocommerce-Price-amount')
    DEL_PRICE = (By.CSS_SELECTOR, 'del span.woocommerce-Price-amount')
    INI_PRICE = (By.CSS_SELECTOR, 'span.woocommerce-Price-amount')
    RATING = (By.CSS_SELECTOR, 'div.star-rating')
    # FOOTER 2
    FOOTER_MENU = (By.ID, 'menu-main-1')
    CATEGORY_LI = (By.CSS_SELECTOR, 'li')
    COPYRIGHT_FOOTER = (By.CSS_SELECTOR, 'div.copyright-footer')

    def _get_market_category(self, category_name, *required) -> Tuple[str, List[dict]]:
        """
        :param category_name: [BEST_SELLING, LATEST, TOP_RATED]
        :return: title, [{
            name,
            price,
            old_price,
            rating
        }]
        """
        locator = self.find_element(*self.PRODUCT_GROUPS[category_name])
        ele = self.move_to_element_for_see(locator)
        title = ele.find_element(By.CSS_SELECTOR, 'span.widget-title').text

        if not required:
            return title, []

        product_infos = []
        for li in ele.find_elements(*self.PROD_LIST):
            _elems = li.find_elements(*self.PROD_NAME) or [None] if "name" in required else [None]
            name_ele = _elems[0]

            if "price" in required:
                _elems = li.find_elements(*self.INS_PRICE) or li.find_elements(*self.INI_PRICE) or [None]
                price_ele = _elems[0]

                _elems = li.find_elements(*self.DEL_PRICE) or [None]
                old_price_ele = _elems[0]
            else:
                price_ele = old_price_ele = None

            _elems = li.find_elements(*self.RATING) or [None] if "star-rating" in required else [None]
            rating_ele = _elems[0]
            # if rating_elems:
            #     aria_label = rating_elems[0].get_attribute('aria-label')
            #     rate = int(aria_label.split()[1].split('.')[0])
            #     rating = rate, aria_label

            product_infos.append({
                'name': name_ele,
                'price': price_ele,
                'old_price': old_price_ele,
                'rating': rating_ele
            })
        return title, product_infos

    def get_best_selling(self):
        return self._get_market_category('BEST_SELLING')

    def get_latest(self):
        return self._get_market_category('LATEST')

    def get_top_rated(self):
        return self._get_market_category('TOP_RATED')

    def verify_attributes_all_product(self):
        for grp in self.PRODUCT_GROUPS:
            grp_name, product_infos = self._get_market_category(grp, "price", "name")
            none_name_i = [str(i) for i, d in enumerate(product_infos) if d.setdefault('name', None) is None]
            none_name_i = ", ".join(none_name_i)
            assert len(none_name_i) == 0, \
                f'Expected "name" in "{grp_name}", got None in id_th product[{none_name_i}]'

            none_price_prod = [d['name'] for d in product_infos if d.setdefault('price', None) is None]
            none_price_prod = ", ".join(none_price_prod)
            assert len(none_price_prod) == 0, \
                f'Expected "price" in "{grp_name}", got None in product {none_price_prod}'

    def verify_rate_any_product(self):
        for grp in self.PRODUCT_GROUPS:
            grp_name, product_infos = self._get_market_category(grp, "star-rating")
            assert any(map(itemgetter('rating'), product_infos)), \
                f'Expected star-rating in "{grp_name}", not get any star rate in products'

    def verify_groups_are_shown(self, group_names: list):
        ss = set(self._get_market_category(grp)[0].lower() for grp in self.PRODUCT_GROUPS)

        shortage = set(x.lower() for x in group_names) - ss
        assert shortage == set(), f'Error! Expected footer shows these {", ".join(shortage)} categories'

    def verify_shown_copyright(self, text):
        self.verify_contain_text(text, self.COPYRIGHT_FOOTER)

    def get_categories(self) -> dict:
        footer_list_ele = self.move_to_element_for_see(self.FOOTER_MENU)
        working_links = dict(
            (li.text.strip(), li.find_element(By.CSS_SELECTOR, 'a').get_attribute('href'))
            for li in footer_list_ele.find_elements(*self.CATEGORY_LI)
        )
        return working_links

    def verify_categories_have_link(self, table):
        root = "https://gettop.us/product-category/"
        result = self.get_categories()
        # print(table)
        for a, l in result.items():
            actual = f'{root}{table[a]}'
            assert l == actual, f'"{l}" vs "{actual}"'
