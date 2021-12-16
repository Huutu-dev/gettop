import os
import os.path as osp
import platform
import time
import json
from functools import partial
from collections import defaultdict
from behave import fixture, use_fixture

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as MozillaService
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.events import EventFiringWebDriver

from support.logger import logger, MyListener
from app.application import Application


_root = osp.dirname(__file__)
_chromedriver95 = osp.join(_root, r"..\..\bin\Chrome95\chromedriver.exe")
_geckodriver30 = osp.join(_root, r"..\..\bin\geckodriver-v0.30.0-win64\geckodriver.exe")


def _register_browserstack(desired_cap, emulation=None):
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

    os_, os_version = desired_cap['platform']
    if not os_version:
        raise ValueError(f'Error @tag on Gherkin feature file, '
                         f'OS version needs be given for BrowserStack mode')
    desired_capabilities = {
        'browser': browser,
        'browser_version': browser_version,
        'os': os_,
        'os_version': os_version,
        'name': desired_cap['name']
    }
    url = f'https://{bs_user}:{bs_pw}@hub-cloud.browserstack.com/wd/hub'
    return partial(webdriver.Remote, url, desired_capabilities=desired_capabilities)
    # return webdriver.Remote(url, desired_capabilities=desired_capabilities)


def _register_headless(options):
    options.add_argument('--headless')
    options.add_argument('--window-size=1920,1080')


def _launch_event_firing(browser, **kwargs):
    return EventFiringWebDriver(browser(**kwargs), MyListener())


def _register_mobile_emulation(options, configs):
    config_json = configs[0]
    if not osp.isabs(config_json):
        config_json = osp.join('support', config_json)
    with open(config_json) as fp:
        mobile_emulation = json.load(fp)
        options.add_experimental_option(name="mobileEmulation", value=mobile_emulation)


@fixture
def browser_init(context):
    _desired_cap = context.desired_cap
    _browser_version = _desired_cap['browser']
    if 'Chrome' in _browser_version:
        options = webdriver.ChromeOptions()
        service = ChromeService(_chromedriver95)
        browser = partial(webdriver.Chrome, service=service)
    elif 'Firefox' in _browser_version:
        options = webdriver.FirefoxOptions()
        service = MozillaService(executable_path=_geckodriver30)
        browser = partial(webdriver.Firefox, service=service)
    else:
        raise ValueError(f'Error @tag on Gherkin feature file, {"_".join(_browser_version)} does not supported')

    if "emulation" in _desired_cap:
        _register_mobile_emulation(options, _desired_cap["emulation"])
    if 'headless' in _desired_cap['mode']:
        _register_headless(options)
    if 'BrowserStack' in _desired_cap['mode']:
        browser = _register_browserstack(_desired_cap)
    if "EventFiring" in _desired_cap['mode']:
        context.driver = _launch_event_firing(browser, options=options)
    else:
        context.driver = browser(options=options)

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
    iter_tags = (tag.split(':') for tag in tags if tag.strip())
    iter_tags = ((x.lower(), y.replace('&', ' ').split('_')) for x, y in iter_tags)

    configs = defaultdict(list)
    for tag, values in iter_tags:
        key = tag.lower()
        configs[key].extend(values)

    if 'platform' not in configs:
        configs['platform'] = [platform.system(), platform.release()]
    if 'browser' not in configs:
        configs['browser'] = ['Chrome']
    if 'mode' not in configs:
        configs['mode'] = ['default']
    return configs


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
    # print('\nStarted scenario: ', scenario.name)
    logger.info(f'Started scenario: {scenario.name}')


def before_step(context, step):
    # print('\nStarted step: ', step)
    logger.info(f'Started step: {step}')


def after_step(context, step):
    if step.status != 'failed':
        return
    # print('\nStep failed: ', step)
    logger.error(f'Step failed: {step}')

    # Mark test case as FAILED on BrowserStack:

    if 'BrowserStack' in context.desired_cap['mode']:
        context.driver.execute_script(
            'browserstack_executor: '
            '{"action": "setSessionStatus", "arguments": {"status":"failed", "reason": "Step failed"}}'
        )


def after_scenario(context, scenario):
    # context.driver.delete_all_cookies()
    # context.driver.quit()
    # print('\nAfter Scenario.')
    logger.info(f'After Scenario.')


def after_feature(context, feature):
    # print('\nAfter feature')
    time.sleep(1)
    pass


def after_all(context):
    # print('\nAfter ALL')
    pass
