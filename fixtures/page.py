import pytest


import config
from config.playwright import *
# rom playwright.sync_api import Browser, BrowserContext, Page, sync_playwright
import pytest
from config.playwright import async_playwright

@pytest.fixture
def page():
    playwright = async_playwright().start()

    browser = None
    context = None
    page_data = None

    try:
        if config.playwright.BROWSER == 'firefox':
            browser = get_firefox_browser(playwright)
            context = get_context(browser)
            page_data = context.new_page()
        elif config.playwright.BROWSER == 'chrome':
            browser = get_chrome_browser(playwright)
            context = get_context(browser)
            page_data = context.new_page()
        else:
            browser = get_chrome_browser(playwright)
            context = get_context(browser)
            page_data = context.new_page()

        yield page_data
    finally:
        if page_data:
            await page_data.close()
        if context:
            await context.close()
        if browser:
            await browser.close()
        playwright.stop()

def get_firefox_browser(playwright) -> Browser:
    return playwright.firefox.launch(
        headless=config.playwright.IS_HEADLESS,
        slow_mo=config.playwright.SLOW_MO,
    )

def get_chrome_browser(playwright) -> Browser:
    return playwright.chromium.launch(
        headless=config.playwright.IS_HEADLESS,
        slow_mo=config.playwright.SLOW_MO
    )

def get_context(browser) -> BrowserContext:
    context = browser.new_context(
        viewport=config.playwright.PAGE_VIEWPORT_SIZE,
        locale=config.playwright.LOCALE
    )
    context.set_default_timeout(
        timeout=config.expectations.DEFAULT_TIMEOUT
    )
    return context
