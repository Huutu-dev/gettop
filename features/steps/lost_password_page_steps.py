from behave import Given, When, Then

from pages.lost_password_page import LostPasswordPage


@Given('Open lost-password page')
def open_page(context):
    # Todo: as soon as attach lostpassword page into app and remove the line below
    context.app.lost_password_page = LostPasswordPage(context.driver)
    context.app.lost_password_page.open_me()


@When('Clean user_login')
def clean_user_login(context):
    context.app.lost_password_page.empty_username()


@When('Click on RESET PASSWORD')
def reset_password(context):
    context.app.lost_password_page.click_reset_password()


@When('Input "{name}" into user_login')
def input_user_name(context, name):
    context.app.lost_password_page.input_user_name(name)


@Then('Verify the message is "{msg}" on lost-password page')
def verify(context, msg):
    context.app.lost_password_page.verify_error(msg)
