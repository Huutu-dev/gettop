from behave import given, when, then


@given('Open My Account Gettop')
def open_my_account(context):
    context.app.my_account.open_me()


@when('Clean email text input')
def clean_email(context):
    context.app.my_account.clean_email_field()


@when('Clean password text input')
def clean_password(context):
    context.app.my_account.clean_password_field()


@when('Click on LOG IN')
def click_on_login(context):
    context.app.my_account.click_login()


@when('Input {value} into password text input')
def input_password(context, value):
    context.app.my_account.input_password_field(value)


@when('Input {value} into username text input')
def input_password(context, value):
    context.app.my_account.input_email_field(value)


@then('Verify the message is "{msg}"')
def verify_error(context, msg):
    context.app.my_account.verify_error(msg)
