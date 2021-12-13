from behave import Given, Then, When


@Given('a "{product}" page "{url}"')
def work_on(context, product, url):
    # print(f'Working on "{product}" with "{url}"')
    context.app.product_page.open_me(url, product)


@Then('verify that product is in stock')
def verify_in_stock(context):
    if context.app.product_page.out_of_stock:
        print(context.app.product_page.warning_stock())


@When('add to cart')
def add_to_cart(context):
    if context.app.product_page.out_of_stock:
        return

    context.app.header_nav.cart_nav.add_product(context.app.product_page)


@Then('verify user can remove a product')
def remove_product(context):
    context.app.header_nav.cart_nav.remove_latest_product()


@Then('verify user can click on "View Cart" and is taken to cart page')
def click_view_cart(context):
    context.app.header_nav.cart_nav.verify_click_view_cart()


@Then('verify user can click on "Checkout" and is taken to checkout page')
def click_checkout(context):
    context.app.header_nav.cart_nav.verify_click_checkout()

