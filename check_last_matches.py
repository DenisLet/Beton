from playwright.sync_api import sync_playwright, Page
from time import sleep
import re


class Sport:

    def __init__(self, url, duration, period_duration, number_of_periods, locator):
        self.url = url
        self.duration = duration
        self.period_duration = period_duration
        self.number_of_periods = number_of_periods
        self.locator = "[id^='g_{}']".format(locator)
        self.page = None
        self.context = None
        self.browser = None

    def open_page(self):
        pw = sync_playwright().start()
        self.browser = pw.chromium.launch(headless=False, args=["--mute-audio"])
        self.context = self.browser.new_context()
        self.page = self.context.new_page()
        self.page.goto(self.url)
        input('Choose date of matches: ')



    def close_page(self):
        self.page.close()
        self.context.close()
        self.browser.close()

    # def get_data_from_page(self):
    #     if self.page is None:
    #         raise Exception
    #     all_matches = self.page.query_selector_all(self.locator)
    #     for match in all_matches:
    #         match_title = match.inner_text().split()
    #         print(match_title)


class Soccer(Sport):
    def __init__(self):
        super().__init__('https://www.soccer24.com/', 90, 45, 2, 1)


    def get_data_from_page(self):
        if self.page is None:
            raise Exception
        all_matches = self.page.query_selector_all(self.locator)
        for match in all_matches:
            match_title = match.inner_text().split()
            print(match_title)


class Basketball(Sport):
    def __init__(self):
        super().__init__('https://www.basketball24.com/', 40, 10, 4, 3)

    def get_data_from_page(self):
        if self.page is None:
            raise Exception
        all_matches = self.page.query_selector_all(self.locator)
        for match in all_matches:
            match_title = match.inner_text().split()
            print(match_title)

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
soccer.get_data_from_page()
soccer.close_page()
sleep(5)
basketball.open_page()
basketball.get_data_from_page()
basketball.close_page()

# soccer.close_page()
