import asyncio
from playwright.async_api import async_playwright
import re
from sheet_with_often_scores import soccer_first_half_often

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
            print(match_title.split())
            results[current_link] = match_title.split()
        # print(results)
        return results

    async def switch_to_live(self):
        await self.page.locator('.filters__text--short').get_by_text('LIVE').click()

    def stop_to_change_page(self):
        input('Change page and press Enter to continue:')



    async def check_league_results(self):
        all_links = await self.extract_link_and_scores()
        all_data_list = []
        for each in all_links:
            await self.page.goto(each)
            await self.page.wait_for_selector('.smv__verticalSections')
            await self.page.wait_for_selector('.oddsPlacement')
            data = await self.page.query_selector_all('.smv__verticalSections')
            to_list = []
            for i in data:
                text = await self.page.evaluate('(element) => element.innerText', i)
                text = text.split()
                # print(text)
                to_list.append(text)
                odds_data = await self.page.query_selector_all('.oddsPlacement')
                for odds in odds_data:
                    odds_text = await self.page.evaluate('(element) => element.innerText', odds)
                    odds_text = odds_text.split()
                    # print(odds_text)
                    to_list.append(odds_text)
            all_data_list.append(to_list)
        return all_data_list





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
                # team1_1half, team2_1half, team1_all, team2_all = -1, -1, -1, -1
            to_datablock = [(team1_1half, team2_1half, team1_all, team2_all),(home_coef, draw_coef, away_coef)]

            datablock.append(to_datablock)
            # print(team1_1half, team2_1half, team1_all, team2_all)
        return datablock



    async def compare_league_1half_vs_2half(self):
        data = await self.check_league_results()
        team1_1h_score = team2_1h_score = team1_2h_score = team2_2h_score  = None

        match_data  = []
        for match in data:
            for scores in range(len(match[0])):
                to_match_data = ()
                try:
                    k1, k2 = (float(match[1][3]), float(match[1][7]))
                except:
                    k1 = k2 = 1
                to_match_data+= (k1,k2)
                if match[0][scores] == '1ST' and match[0][scores+1] == 'HALF':
                    team1_1h_score, team2_1h_score = (int(match[0][scores+2]),int(match[0][scores+4]))
                to_match_data += (team1_1h_score, team2_1h_score)
                if match[0][scores] == '2ND' and match[0][scores+1] == 'HALF':
                    team1_2h_score, team2_2h_score = (int(match[0][scores+2]),int(match[0][scores+4]))
                    to_match_data += (team1_2h_score, team2_2h_score)
                    match_data.append(to_match_data)
                    break

        for i in match_data:
            print(i)

        return match_data


    async def get_league_results_all(self):
        import openpyxl
        all_matches =await self.compare_league_1half_vs_2half()
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        sheet.append(('HOME','TEAM','IS','FAVORITE','OR','EQUAL POWER'))
        print('FOR HOME TEAM FAVORITE AND EQUAL POWER TEAM')
        for score in soccer_first_half_often:
            ultra_cases = ultra_2h_0 = ultra_2h_1 = ultra_2h_2 = 0
            super_cases = super_2h_0 = super_2h_1 = super_2h_2 = 0
            huge_cases = huge_2h_0 = huge_2h_1 = huge_2h_2 = 0
            strong_cases = strong_2h_0 = strong_2h_1 = strong_2h_2 = 0
            lite_cases = lite_2h_0 = lite_2h_1 = lite_2h_2 = 0
            equal_cases = equal_2h_0 = equal_2h_1 = equal_2h_2 = 0
            for match in all_matches:
                half1_res = (match[2], match[3])
                half2_res = sum([match[4], match[5]])
                k1 = match[0]
                k2 = match[1]
                if 1 < k1 <= 1.1:
                    if score == half1_res:
                        ultra_cases += 1
                        if half2_res == 0:
                            ultra_2h_0 += 1
                        if half2_res == 1:
                            ultra_2h_1 += 1
                        if half2_res > 1:
                            ultra_2h_2 += 1
                if 1.1 < k1 <= 1.25:
                    if score == half1_res:
                        super_cases += 1
                        if half2_res == 0:
                            super_2h_0 += 1
                        if half2_res == 1:
                            super_2h_1 += 1
                        if half2_res > 1:
                            super_2h_2 += 1
                if 1.25 < k1 <= 1.5:
                    if score == half1_res:
                        huge_cases += 1
                        if half2_res == 0:
                            huge_2h_0 += 1
                        if half2_res == 1:
                            huge_2h_1 += 1
                        if half2_res > 1:
                            huge_2h_2 += 1
                if 1.5 < k1 <= 1.8:
                    if score == half1_res:
                        strong_cases += 1
                        if half2_res == 0:
                            strong_2h_0 += 1
                        if half2_res == 1:
                            strong_2h_1 += 1
                        if half2_res > 1:
                            strong_2h_2 += 1
                if 1.8 < k1 <= 2.2:
                    if score == half1_res:
                        lite_cases += 1
                        if half2_res == 0:
                            lite_2h_0 += 1
                        if half2_res == 1:
                            lite_2h_1 += 1
                        if half2_res > 1:
                            lite_2h_2 += 1
                if k1 > 2.2 and k1 <= k2:
                    if score == half1_res:
                        equal_cases += 1
                        if half2_res == 0:
                            equal_2h_0 += 1
                        if half2_res == 1:
                            equal_2h_1 += 1
                        if half2_res > 1:
                            equal_2h_2 += 1

            if any([ultra_cases, super_cases, huge_cases, strong_cases, lite_cases, equal_cases]):
                print('SCORE:', score)
                print("ULTRA", ultra_cases, ultra_2h_0, ultra_2h_1, ultra_2h_2)
                print('SUPER', super_cases, super_2h_0, super_2h_1, super_2h_2)
                print('HUGE', huge_cases, huge_2h_0, huge_2h_1, huge_2h_2)
                print('STRONG', strong_cases, strong_2h_0, strong_2h_1, strong_2h_2)
                print('LITE', lite_cases, lite_2h_0, lite_2h_1, lite_2h_2)
                print('EQUAL', equal_cases, equal_2h_0, equal_2h_1, equal_2h_2)
                print()
                row_data = [
                    ('SCORE', str(score)),
                    ("ULTRA", ultra_cases, ultra_2h_0, ultra_2h_1, ultra_2h_2),
                    ('SUPER', super_cases, super_2h_0, super_2h_1, super_2h_2),
                    ('HUGE', huge_cases, huge_2h_0, huge_2h_1, huge_2h_2),
                    ('STRONG', strong_cases, strong_2h_0, strong_2h_1, strong_2h_2),
                    ('LITE', lite_cases, lite_2h_0, lite_2h_1, lite_2h_2),
                    ('EQUAL', equal_cases, equal_2h_0, equal_2h_1, equal_2h_2),
                    (' ', ' ')

                ]
                for row in row_data:
                    sheet.append(row)

        sheet.append(("AWAY", "TEAM", "IS", "FAVORITE"))
        print('FOR AWAY TEAM FAVORITE')
        for score in soccer_first_half_often:
            ultra_cases = ultra_2h_0 = ultra_2h_1 = ultra_2h_2 = 0
            super_cases = super_2h_0 = super_2h_1 = super_2h_2 = 0
            huge_cases = huge_2h_0 = huge_2h_1 = huge_2h_2 = 0
            strong_cases = strong_2h_0 = strong_2h_1 = strong_2h_2 = 0
            lite_cases = lite_2h_0 = lite_2h_1 = lite_2h_2 = 0
            equal_cases = equal_2h_0 = equal_2h_1 = equal_2h_2 = 0
            for match in all_matches:
                half1_res = (match[2], match[3])
                half2_res = sum([match[4], match[5]])
                k1 = match[0]
                k2 = match[1]
                if 1 < k2 <= 1.1:
                    if score == half1_res:
                        ultra_cases += 1
                        if half2_res == 0:
                            ultra_2h_0 += 1
                        if half2_res == 1:
                            ultra_2h_1 += 1
                        if half2_res > 1:
                            ultra_2h_2 += 1
                if 1.1 < k2 <= 1.25:
                    if score == half1_res:
                        super_cases += 1
                        if half2_res == 0:
                            super_2h_0 += 1
                        if half2_res == 1:
                            super_2h_1 += 1
                        if half2_res > 1:
                            super_2h_2 += 1
                if 1.25 < k2 <= 1.5:
                    if score == half1_res:
                        huge_cases += 1
                        if half2_res == 0:
                            huge_2h_0 += 1
                        if half2_res == 1:
                            huge_2h_1 += 1
                        if half2_res > 1:
                            huge_2h_2 += 1
                if 1.5 < k2 <= 1.8:
                    if score == half1_res:
                        strong_cases += 1
                        if half2_res == 0:
                            strong_2h_0 += 1
                        if half2_res == 1:
                            strong_2h_1 += 1
                        if half2_res > 1:
                            strong_2h_2 += 1
                if 1.8 < k2 <= 2.2:
                    if score == half1_res:
                        lite_cases += 1
                        if half2_res == 0:
                            lite_2h_0 += 1
                        if half2_res == 1:
                            lite_2h_1 += 1
                        if half2_res > 1:
                            lite_2h_2 += 1
                if k2>2.2 and k2 < k1:
                    if score == half1_res:
                        equal_cases += 1
                        if half2_res == 0:
                            equal_2h_0 += 1
                        if half2_res == 1:
                            equal_2h_1 += 1
                        if half2_res > 1:
                            equal_2h_2 += 1

            if any([ultra_cases, super_cases, huge_cases, strong_cases, lite_cases, equal_cases]):
                print('SCORE:', score)
                print("ULTRA", ultra_cases, ultra_2h_0, ultra_2h_1, ultra_2h_2)
                print('SUPER', super_cases, super_2h_0, super_2h_1, super_2h_2)
                print('HUGE', huge_cases, huge_2h_0, huge_2h_1, huge_2h_2)
                print('STRONG', strong_cases, strong_2h_0, strong_2h_1, strong_2h_2)
                print('LITE', lite_cases, lite_2h_0, lite_2h_1, lite_2h_2)
                print('EQUAL', equal_cases, equal_2h_0, equal_2h_1, equal_2h_2)
                print()
                row_data = [
                    ('SCORE', str(score)),
                    ("ULTRA", ultra_cases, ultra_2h_0, ultra_2h_1, ultra_2h_2),
                    ('SUPER', super_cases, super_2h_0, super_2h_1, super_2h_2),
                    ('HUGE', huge_cases, huge_2h_0, huge_2h_1, huge_2h_2),
                    ('STRONG', strong_cases, strong_2h_0, strong_2h_1, strong_2h_2),
                    ('LITE', lite_cases, lite_2h_0, lite_2h_1, lite_2h_2),
                    ('EQUAL', equal_cases, equal_2h_0, equal_2h_1, equal_2h_2),
                    (' ', ' ')

                ]
                for row in row_data:
                    sheet.append(row)
        workbook.save('table.xlsx')




    async def daily_scanning_1half_with_2half(self):
        all_matches = await self.get_clear_results()
        print(len(all_matches))

        for first_half_input in soccer_first_half_often:
            print(first_half_input)
            case_counter, half2_eval_1, half2_more_1, half2_eval_0 = 0, 0, 0, 0
            case_counter_favor, half2_eval_1_favor, half2_more_1_favor, half2_eval_0_favor = 0, 0, 0, 0
            for each_match in all_matches:
                # print(each_match)
                half1 = tuple(each_match[0][:2])
                half2 = tuple(each_match[0][2:])
                real_half2 = sum(half2) -sum(half1)
                coefs = tuple(each_match[1])
                # print(half1, half2, real_half2)
                is_favorite = True if 1<coefs[0] < 1.5 or 1<coefs[2]<1.5 else False
                # print(is_favorite)
                if half1 == first_half_input:
                    # print(half1,' --- ',first_half_input)
                    case_counter += 1
                    if is_favorite:
                        case_counter_favor += 1
                    if real_half2 == 1:
                        half2_eval_1 += 1
                        if is_favorite:
                            half2_eval_1_favor += 1
                    elif real_half2 > 1:
                        half2_more_1 += 1
                        if is_favorite:
                            half2_more_1_favor += 1
                    else:
                        half2_eval_0 += 1
                        if is_favorite:
                            half2_eval_0_favor += 1
            if case_counter == 0 or (case_counter_favor == 0 and coefs[0]!= 0):
                continue



            print(f'Total matches with 1h score({first_half_input} : {case_counter} | 2half with 0: {half2_eval_0} | 2half with 1: {half2_eval_1} | 2 half with >2 {half2_more_1}')
            print(
                f'Total matches with 1h score with FAVORIT ({first_half_input} : {case_counter_favor} | 2half with 0: {half2_eval_0_favor} | 2half with 1: {half2_eval_1_favor} | 2 half with >2 {half2_more_1_favor}')


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
        # await soccer.daily_scanning_1half_with_2half()
        # lst = await soccer.extract_link_and_scores()
        # for i in lst:
        #     print(i)
        await soccer.get_league_results_all()
        await asyncio.sleep(3)

asyncio.run(main())