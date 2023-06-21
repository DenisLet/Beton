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

    async def get_data_from_page(self):
        all_matches = await self.page.query_selector_all(self.locator)
        return all_matches

    async def extract_link_and_scores(self):
        all_matches = await self.get_data_from_page()
        results = {}
        for match in all_matches:
            match_id = await match.get_attribute('id')
            current_link = f"{self.url}match/{match_id[4:]}"
            match_title = await match.inner_text()
            results[current_link] = match_title.split()
        # print(results)
        return results

    async def switch_to_live(self):
        await self.page.locator('.filters__text--short').get_by_text('LIVE').click()


class Soccer(Sport):
    def __init__(self):
        super().__init__('https://www.soccer24.com/', 90, 45, 2, 1)

    async def get_clear_results(self):
        results = []
        data = await self.extract_link_and_scores()
        print(data)
        for line in data.values():
            home_coef, draw_coef, away_coef = [float(i) if '.' in i else 0 for i in line[-3:]]
            print(line)
            try:
                team1_1half, team2_1half = re.findall(r'\(\d\)', ' '.join(line))
                mark = line.index(team1_1half)
                if 'After' not in line:
                    team1_all = int(line[mark - 2])
                    team2_all = int(line[mark - 1])
                else:
                    team1_all = int(line[mark + 2])
                    team2_all = int(line[mark + 3])

                team1_1half = int(team1_1half.strip('()'))
                team2_1half = int(team2_1half.strip('()'))

            except:
                team1_1half, team2_1half, team1_all, team2_all = -1, -1, -1, -1
            results.append((team1_1half, team2_1half, team1_all, team2_all))
            print(team1_1half, team2_1half, team1_all, team2_all)
        return results

    async def daily_scanning_1half_with_2half(self):





class Basketball(Sport):
    def __init__(self):
        super().__init__('https://www.basketball24.com/', 40, 10, 4, 3)


class Handball(Sport):
    def __init__(self):
        super().__init__('https://www.handball24.com/', 60, 30, 2, 7)


class Hockey(Sport):
    def __init__(self):
        super().__init__('https://www.icehockey24.com/', 60, 20, 3, 4)


async def main():
    hockey = Hockey()
    soccer = Soccer()
    basketball = Basketball()
    handball = Handball()

    # Запуск двух корутин одновременно
    await asyncio.gather(
        soccer.open_page(),
        basketball.open_page()
    )

    # await soccer.switch_to_live()
    # await basketball.switch_to_live()

    while True:
        r = await soccer.get_clear_results()
        print(r)
        await asyncio.sleep(3)

asyncio.run(main())