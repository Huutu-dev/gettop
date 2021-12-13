from behave import Given, Then, When


@Then('verify that amount of price is correct')
def verify_cart_amount_price(context):
    if context.app.product_page.out_of_stock:
        return

    product_price = context.app.product_page.price
    context.app.header_nav.cart_nav.verify_amount_price(product_price)


@Then('verify that amount of items are correct')
def verify_cart_amount_number(context):
    if context.app.product_page.out_of_stock:
        return
    context.app.header_nav.cart_nav.verify_count_products()


@Then('Verify if no products were added')
def without_product(context):
    context.app.header_nav.cart_nav.verify_count_products(0)


@When('Click on Cart')
def open_cart_page(context):
    context.app.header_nav.cart_nav.click_to_open_cart_page()


@Then('Verify that Empty Cart page opened')
def is_empty_cart(context):
    context.app.cart_page.verify_is_empty()


@When("Hover over Cart icon and capture message")
def capture_hover_icon(context):
    context.app.header_nav.cart_nav.capture_hover_icon()


@When("Hover over Cart icon")
def hover_cart_icon(context):
    context.app.header_nav.cart_nav.hover_icon()


@Then('Verify that message is "{expected_text}"')
def verify_drop_message(context, expected_text):
    context.app.header_nav.cart_nav.verify_drop_message(expected_text)


@Then('verify correct products and subtotal shown')
def verify_products_subtotal(context):
    context.app.header_nav.cart_nav.verify_products_subtotal()
