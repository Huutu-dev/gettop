from selenium.webdriver.support.expected_conditions import *
from selenium.webdriver.support.ui import Select

def url_be_changed(old_url):
    """An expectation for checking the current url.
    url is the expected url, which must be an exact match
    returns True if the url matches, false otherwise."""

    def _predicate(driver):
        return old_url != driver.current_url

    return _predicate
