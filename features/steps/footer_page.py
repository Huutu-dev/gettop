from behave import When, Then, Given
from pages.footer_page import Footer


@Given('Foreach footer categories')
def store_product_cats(context):
    table = context.app.product_page.get_storage(reset=True)
    for row in context.table:
        table[row['category']] = row['partial_url']


@Given('foreach footer groups')
def store_product_group(context):
    table = context.app.product_page.get_storage(reset=True)
    table['groups'] = [row['group'] for row in context.table]


@Then('verify that each group on the footer is shown')
def verify_groups_are_shown(context):
    footer = context.app.footer
    table = context.app.product_page.get_storage()
    footer.verify_groups_are_shown(table['groups'])


@Then('Verify that all products on the footer have price, name')
def verify_price_name(context):
    footer = context.app.footer
    footer.verify_attributes_all_product()


@Then('Verify that at least one product on the footer has star-rating')
def verify_star_rating(context):
    footer = context.app.footer
    footer.verify_rate_any_product()


@Then('Verify that each category on the footer has valid link')
def verify_work_link(context):
    table = context.app.product_page.get_storage()
    footer = context.app.footer
    footer.verify_categories_have_link(table)


@Then('verify that copyright contain "{text}"')
def verify_copyright(context, text):
    footer = context.app.footer
    footer.verify_shown_copyright(text)
