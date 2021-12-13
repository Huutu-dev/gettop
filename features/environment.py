import os.path as osp
import platform
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


def _register_browserstack(desired_cap):
    """ Register for BrowserStack, then grab it from https://www.browserstack.com/accounts/settings
        My fake name is Karim Lenin, dkarim.xs5z@mobii.site
            http://kevabba_1ovqjp.browserstack.com
    """
    bs_user = 'karimlenin_B4Adbi'
    bs_pw = 'EwpXxCCiVxpg67xV7Vs2'
    browser, browser_version = desired_cap['browser']
    if not browser_version:
        raise ValueError(f'Error @tag on Gherkin feature file, '
                         f'browser version needs be given for BrowserStack mode')

    os, os_version = desired_cap['platform']
    if not os_version:
        raise ValueError(f'Error @tag on Gherkin feature file, '
                         f'OS version needs be given for BrowserStack mode')
    desired_capabilities = {
        'browser': browser,
        'browser_version': browser_version,
        'os': os,
        'os_version': os_version,
        'name': desired_cap['name']
    }
    url = f'https://{bs_user}:{bs_pw}@hub-cloud.browserstack.com/wd/hub'
    return webdriver.Remote(url, desired_capabilities=desired_capabilities)


def _register_headless(options):
    options.add_argument('--headless')
    options.add_argument('--window-size=1920,1080')


@fixture
def browser_init(context):
    _desired_cap = context.desired_cap
    if 'BrowserStack' in _desired_cap['mode']:
        context.driver = _register_browserstack(_desired_cap)
    else:
        _browser_version = _desired_cap['browser']
        if 'Chrome' in _browser_version:
            browser = webdriver.Chrome
            options = webdriver.ChromeOptions()
            service = ChromeService(_chromedriver95)
        elif 'Firefox' in _browser_version:
            browser = webdriver.Firefox
            options = webdriver.FirefoxOptions()
            service = MozillaService(executable_path=_geckodriver30)
        else:
            raise ValueError(f'Error @tag on Gherkin feature file, {"_".join(_browser_version)} does not supported')

        if 'headless' in _desired_cap['mode']:
            _register_headless(options)
        context.driver = browser(options=options, service=service)

    context.driver.maximize_window()
    # context.driver.implicitly_wait(4)
    context.driver.wait = WebDriverWait(context.driver, 4)
    context.app = Application(context.driver)
    # -- END-INIT-BROWSER

    yield context.driver

    # -- CLEANUP-FIXTURE PART:
    print('Close all')
    context.driver.delete_all_cookies()
    context.driver.quit()


def _parse_tags(tags):
    desired_cap = (tag.split(':') for tag in tags)
    desired_cap = dict((x.lower(), y.replace('&', ' ').split('_')) for x, y in desired_cap)

    if 'platform' not in desired_cap:
        desired_cap['platform'] = [platform.system(), platform.release()]
    if 'browser' not in desired_cap:
        desired_cap['browser'] = ['Chrome']
    if 'mode' not in desired_cap:
        desired_cap['mode'] = ['default']
    return desired_cap


def before_feature(context, feature):
    """tags eg:
    @platform:Windows_10
    @browser:Chrome_96.0
    @mode:headless
    """
    desired_cap = _parse_tags(feature.tags)
    desired_cap['name'] = feature.name

    context.desired_cap = desired_cap
    # print('\n<< Feature')
    use_fixture(browser_init, context)
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
    time.sleep(3)
    pass


def after_all(context):
    # print('\nAfter ALL')
    pass