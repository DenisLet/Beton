import requests
from bs4 import BeautifulSoup
import asyncio
from playwright.async_api import async_playwright
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




asyncio.run(main())
