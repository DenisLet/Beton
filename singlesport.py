import asyncio
from playwright.async_api import async_playwright, TimeoutError


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
        self.league_name = None
        self.number_of_seasons = None

    async def open_page(self):
        pw = await async_playwright().start()
        self.browser = await pw.chromium.launch(headless=False, args=["--mute-audio"])
        self.context = await self.browser.new_context()
        self.page = await self.context.new_page()
        await self.page.goto(self.url)
        return self.page

    async def close_page(self):
        await self.page.close()
        await self.context.close()
        await self.browser.close()

    async def stop_to_change_page(self):
        self.number_of_seasons = int(
            input('Смените страницу, введите количество сезонов для сканирования и нажмите Enter для продолжения: '))

    async def get_seasons_links(self):
        seasons = await self.page.query_selector_all('.archive__season a')
        links = []
        for i, season in enumerate(seasons):
            if i == 0:
                continue
            try:
                season_link = await season.get_attribute('href')
                current_link = f"{self.url}{season_link}"
                links.append(current_link)
                if i == self.number_of_seasons:
                    break
            except Exception:
                continue
        print("Season links:")
        print(links)
        assert self.number_of_seasons == len(links), 'НЕВЕРНОЕ КОЛИЧЕСТВО СЕЗОНОВ'
        return links


class Soccer(Sport):
    def __init__(self):
        super().__init__('https://www.soccer24.com', 90, 45, 2, 1)

    async def process_links_to_matches(self, links_to_matches):
        for link, title_parts in links_to_matches.items():
            current_link = f"{self.url}/match/{link}"
            await self.page.goto(current_link)
            await self.page.wait_for_selector('.smv__verticalSections')
            await self.page.wait_for_selector('.oddsPlacement')
            data = await self.page.query_selector_all('.smv__verticalSections')
            all_data_list = []
            for i in data:
                text = await self.page.evaluate('(element) => element.innerText', i)
                text = text.split()
                all_data_list.append(text)

            odds_data = await self.page.query_selector_all('.oddsPlacement')
            for odds in odds_data:
                odds_text = await self.page.evaluate('(element) => element.innerText', odds)
                odds_text = odds_text.split()
                all_data_list.append(odds_text)


            print(all_data_list)


class ParsingPage:
    def __init__(self, urls, locator, soccer):
        self.urls = urls
        self.pages = []
        self.locator = locator
        self.soccer = soccer

    async def open_pages(self):
        pw = await async_playwright().start()
        browser = await pw.chromium.launch(headless=False, args=["--mute-audio"])
        context = await browser.new_context()

        for url in self.urls:
            page = await context.new_page()
            await page.goto(url)
            self.pages.append(page)

        self.soccer.page = self.pages[0]

    async def close_pages(self):
        for page in self.pages:
            await page.close()

        context = self.pages[0].context
        browser = context.browser
        await context.close()
        await browser.close()

    async def click_element_until_disappears(self):
        for page in self.pages:
            while True:
                try:
                    elements = await page.query_selector_all('.event__more.event__more--static')
                    if len(elements) == 0:
                        break
                    await elements[0].click()
                    await page.wait_for_load_state('networkidle', timeout=3000)
                except TimeoutError:
                    continue
                await asyncio.sleep(1)

    async def get_links_to_matches(self):
        results = {}
        for page, url in zip(self.pages, self.urls):
            all_matches = await page.query_selector_all(self.locator)
            champ = await page.locator('.heading__name').evaluate('(element) => element.textContent')
            year = await page.locator('.heading__info').evaluate('(element) => element.textContent')
            year = year.replace('/', '_')
            self.soccer.league_name = f'{champ} {year}'

            for match in all_matches:
                match_id = await match.get_attribute('id')
                current_link = match_id[4:]
                match_title = await match.inner_text()
                print(match_title.split())
                results[current_link] = match_title.split()

        return results


async def main():
    soccer = Soccer()
    page = await soccer.open_page()
    await soccer.stop_to_change_page()
    seasons_links = await soccer.get_seasons_links()

    parser = ParsingPage(seasons_links, soccer.locator, soccer)
    await parser.open_pages()
    # await parser.click_element_until_disappears()
    links_to_matches = await parser.get_links_to_matches()

    await soccer.process_links_to_matches(links_to_matches)

    await parser.close_pages()
    await soccer.close_page()


asyncio.run(main())
