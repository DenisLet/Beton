from playwright.sync_api import Playwright, sync_playwright
from time import sleep

class Sport:

    def __init__(self, url, duration, period_duration, number_of_periods):
        self.url = url
        self.duration = duration
        self.period_duration = period_duration
        self.number_of_periods = number_of_periods




Basketball = Sport('https://www.basketball24.com/', 40, 10, 4)
Soccer = Sport('https://www.soccer24.com/', 90, 45, 2)
Handball = Sport('https://www.handball24.com/', 60, 30, 2)
Hockey = Sport('https://www.icehockey24.com/', 60, 20, 3)

with sync_playwright() as pw:
    browser = pw.chromium.launch(headless=False)
    soccer_contex = browser.new_context()
    soccer_page = soccer_contex.new_page()
    soccer_page.goto(Soccer.url)
    soccer_page.locator('.filters__text--short').get_by_text('LIVE').click()
    basketball_context = browser.new_context()
    basketball_page = basketball_context.new_page()
    basketball_page.goto(Basketball.url)
    basketball_page.locator('.filters__text--short').get_by_text('LIVE').click()
    handball_context = browser.new_context()
    handball_page = handball_context.new_page()
    handball_page.goto(Handball.url)
    handball_page.locator('.filters__text--short').get_by_text('LIVE').click()
    sleep(10)
