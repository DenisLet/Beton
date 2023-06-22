import asyncio
from playwright.async_api import async_playwright
import re
from sheet_with_possible_scores import soccer_first_half_often

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

    def stop_to_change_page(self):
        input('Change page and press Enter to continue:')


class Soccer(Sport):
    def __init__(self):
        super().__init__('https://www.soccer24.com/', 90, 45, 2, 1)

    async def get_clear_results(self):

        datablock = []
        data = await self.extract_link_and_scores()
        # print(data)
        for line in data.values():
            home_coef, draw_coef, away_coef = [float(i) if '.' in i else 0 for i in line[-3:]]
            # print(line)
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

            except Exception:
                continue
                team1_1half, team2_1half, team1_all, team2_all = -1, -1, -1, -1
            to_datablock = [(team1_1half, team2_1half, team1_all, team2_all),(home_coef, draw_coef, away_coef)]
            datablock.append(to_datablock)
            # print(team1_1half, team2_1half, team1_all, team2_all)
        return datablock

    async def daily_scanning_1half_with_2half(self):
        all_matches = await self.get_clear_results()

        while True:
            user_input = input("Enter scores in first half: ")
            try:
                if ' ' in user_input:
                    first_half_input = tuple([int(x) for x in user_input.split()])
                else:
                    first_half_input = tuple([int(x) for x in list(user_input)])
                break
            except ValueError:
                print("Format : 00 or 0 0")

        case_counter, half2_eval_1, half2_more_1, half2_eval_0 = 0, 0, 0, 0
        case_counter_favor, half2_eval_1_favor, half2_more_1_favor, half2_eval_0_favor = 0, 0, 0, 0
        for each_match in all_matches:
            half1 = tuple(each_match[0][:2])
            half2 = tuple(each_match[0][2:])
            real_half2 = sum(half2) -sum(half1)
            coefs = tuple(each_match[1])
            is_favorite = True if 1<coefs[0] < 1.5 or 1<coefs[2]<1.5 else False
            if half1 == first_half_input:
                case_counter += 1
                if is_favorite:
                    case_counter_favor += 1
                if real_half2 == 1:
                    print('case half2 == 1:',each_match[0],each_match[1])
                    half2_eval_1 += 1
                    if is_favorite:
                        print()
                        print('case half2 == 1:', each_match[0], each_match[1])
                        half2_eval_1_favor += 1
                elif real_half2 > 1:
                    print('case half2 >> 1:', each_match[0],each_match[1])
                    half2_more_1 += 1
                    if is_favorite:
                        print()
                        print('case half2 == 1:', each_match[0], each_match[1])
                        half2_more_1_favor += 1
                else:
                    print('case half2 == 0:', each_match[0],each_match[1])
                    half2_eval_0 += 1
                    if is_favorite:
                        print()
                        print('case half2 == 1:', each_match[0], each_match[1])
                        half2_eval_0_favor += 1
        print(f'Total matches with 1h score({first_half_input} : {case_counter} | 2half with 0: {half2_eval_0} | 2half with 1: {half2_eval_1} | 2 half with >2 {half2_more_1}')
        print(
            f'Total matches with 1h score with FAVORIT ({first_half_input} : {case_counter_favor} | 2half with 0: {half2_eval_0_favor} | 2half with 1: {half2_eval_1_favor} | 2 half with >2 {half2_more_1_favor}')
            # t1_score_1h = each_match[0][0]
            # t2_score_1h = each_match[0][1]
            # first_half = (t1_score_1h, t2_score_1h)
            # t1_score_ft = each_match[0][2]
            # t2_score_ft = each_match[0][3]
            # t1_coef = each_match[1][0]
            # t2_coef = each_match[1][2]
            # draw_coef = each_match[1][1]






    # while True:
    #     user_input = input("Enter scores in first half: ")
    #     try:
    #         if ' ' in user_input:
    #             first_half = [int(x) for x in user_input.split()]
    #         else:
    #             first_half = [int(x) for x in list(user_input)]
    #         break
    #     except ValueError:
    #         print("Format : 00 or 0 0")












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

    # await asyncio.gather(
    #     soccer.open_page(),
    #     basketball.open_page()
    # )
    await soccer.open_page()

    # await soccer.switch_to_live()
    # await basketball.switch_to_live()

    while True:
        soccer.stop_to_change_page()
        # r = await soccer.get_clear_results()
        await soccer.daily_scanning_1half_with_2half()
        await asyncio.sleep(3)

asyncio.run(main())