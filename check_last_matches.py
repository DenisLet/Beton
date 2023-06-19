from playwright.sync_api import sync_playwright
from time import sleep
import re


class Sport:
    def __init__(self, url, duration, period_duration, number_of_periods, locator):
        self.url = url
        self.duration = duration
        self.period_duration = period_duration
        self.number_of_periods = number_of_periods
        self.locator = "[id^='g_{}']".format(locator)

    def open_page(self):
        with sync_playwright() as pw:
            browser = pw.chromium.launch(headless=False, args=["--mute-audio"])
            context = browser.new_context()
            page = context.new_page()
            page.goto(self.url)
            input('Chose data of matches: ')

            sleep(3)  # Пример задержки
            self.get_data_from_page(page)  # Вызов метода get_data_from_page с передачей объекта страницы
            page.close()
            context.close()
            browser.close()

    def get_data_from_page(self, page):
        all_matches = page.query_selector_all(self.locator)
        for match in all_matches:

            match_title = match.inner_text().split()
            print(match_title)


class Soccer(Sport):
    def __init__(self):
        super().__init__('https://www.soccer24.com/', 90, 45, 2, 1)


class Basketball(Sport):
    def __init__(self):
        super().__init__('https://www.basketball24.com/', 40, 10, 4, 3)


class Handball(Sport):
    def __init__(self):
        super().__init__('https://www.handball24.com/', 60, 30, 2, 7)


class Hockey(Sport):
    def __init__(self):
        super().__init__('https://www.icehockey24.com/', 60, 20, 3, 4)


hockey = Hockey()
soccer = Soccer()
basketball = Basketball()
handball = Handball()

soccer.open_page()
