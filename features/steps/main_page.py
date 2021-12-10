from behave import Given


@Given('Open Home page')
def open_page(context):
    context.app.main_page.open_home_page()
