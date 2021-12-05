from behave import Given, When, Then


@Given("Open Shop page")
def open_shop_page(context):
    context.app.shop_page.open_me()


@Given("Open Sort by latest page")
def open_sort_page(context):
    context.app.shop_page.open_order_date_page()


@Given("Open Sort by latest on first page")
def open_sort_first_page(context):
    context.app.shop_page.open_order_date_page()


@Given("Open Sort by latest on second page")
def open_sort_second_page(context):
    context.app.shop_page.open_order_date_page('2')


@When('Select "{option}" on Order by drop box')
def select_option(context, option):
    context.app.shop_page.selector.sort_by(option)


@Then('Verify order by date page will open')
def verify_order_date_opened(context):
    context.app.shop_page.query_date_opened()


@Then('Verify that "{option}" will be selected')
def verify_option_selected(context, option):
    context.app.shop_page.selector.selected_by(option)


@Then('Verify that number {page_number} to be selected')
def is_number_selected(context, page_number):
    context.app.shop_page.nav_pagination.verify_current_page_number(page_number)


@When('Click on number {button_number} button')
def click_on_number(context, button_number):
    context.app.shop_page.nav_pagination.click_on_page_number(button_number)


@When('Click on "{go_icon}" button')
def click_on_go(context, go_icon):
    context.app.shop_page.nav_pagination.click_on_go_icon(go_icon)


