import os.path as osp

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.wait import WebDriverWait

from app.application import Application


_root = osp.dirname(__file__)
_chromedriver95 = osp.join(_root, r"..\..\bin\Chrome95\chromedriver.exe")


def browser_init(context):
    context.driver = webdriver.Chrome(service=ChromeService(_chromedriver95))
    context.driver.maximize_window()
    context.driver.implicitly_wait(4)
    context.driver.wait = WebDriverWait(context.driver, 4)
    context.app = Application(context.driver)


def before_scenario(context, scenario):
    print('\nStarted scenario: ', scenario.name)
    browser_init(context)


def before_step(context, step):
    print('\nStarted step: ', step)


def after_step(context, step):
    if step.status == 'failed':
        print('\nStep failed: ', step)


def after_scenario(context, feature):
    context.driver.delete_all_cookies()
    context.driver.quit()
    print('\nBehave DONE.')