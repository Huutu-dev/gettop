import os.path as osp
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as MozillaService
from selenium.webdriver.support.wait import WebDriverWait

from app.application import Application

from behave import fixture, use_fixture
_root = osp.dirname(__file__)
_chromedriver95 = osp.join(_root, r"..\..\bin\Chrome95\chromedriver.exe")
_geckodriver30 = osp.join(_root, r"..\..\bin\geckodriver-v0.30.0-win64\geckodriver.exe")


@fixture
def chrome_browser_init(context):
    if context.browser == 'Chrome':
        context.driver = webdriver.Chrome(service=ChromeService(_chromedriver95))
    elif context.browser == 'Firefox':
        context.driver = webdriver.Firefox(service=MozillaService(executable_path=_geckodriver30))
    elif context.browser == 'ChromeHeadless':
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--window-size=1920,1080')
        context.driver = webdriver.Chrome(chrome_options=options, service=ChromeService(_chromedriver95))

    context.driver.maximize_window()
    # context.driver.implicitly_wait(4)
    context.driver.wait = WebDriverWait(context.driver, 4)
    context.app = Application(context.driver)

    yield context.driver

    # -- CLEANUP-FIXTURE PART:
    print('Close all')
    context.driver.delete_all_cookies()
    context.driver.quit()


def before_feature(context, feature):
    for tag in feature.tags:
        platform, browser, browserVersion = tag.split('_')
        context.browser = browser
        break
    else:
        context.browser = 'Chrome'

    # print('\n<< Feature')
    use_fixture(chrome_browser_init, context)
    # print('---feature')


def before_scenario(context, scenario):
    print('\nStarted scenario: ', scenario.name)
    # browser_init(context)


def before_step(context, step):
    print('\nStarted step: ', step)


def after_step(context, step):
    if step.status == 'failed':
        print('\nStep failed: ', step)


def after_scenario(context, scenario):
    # context.driver.delete_all_cookies()
    # context.driver.quit()
    print('\nAfter Scenario.')


def after_feature(context, feature):
    # print('\nAfter feature')
    # time.sleep(3)
    pass


def after_all(context):
    # print('\nAfter ALL')
    pass