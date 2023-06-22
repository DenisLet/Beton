import asyncio
from playwright.async_api import async_playwright
from time import sleep
from notifiers import get_notifier
token = "5655731349:AAHpSNsDXkUochVg7jtVNeFadDa2JeA9-jE"
id = "5521639964"
import re

def bet_siska(data):
    telegram = get_notifier('telegram')
    info = "\n".join([i for i in data])
    telegram.notify(token=token,chat_id = id,message = info)
    print("MSG HAS BEEN SENT")


sport_url = 'https://www.soccer24.com/'
async def get_current_matches(page):
    await page.goto(sport_url)
    await page.locator('.filters__text--short').get_by_text('LIVE').click()
    current_matches = await page.locator("[id^='g_1']").element_handles()
    return current_matches


async def extract_match_data(match_handle):
    id = await match_handle.get_attribute('id')
    current_link = f"{sport_url}match/{id[4:]}"
    match_time = await (await match_handle.query_selector('.event__stage--block')).inner_text()
    try:
        team1_1half_value = await (await match_handle.query_selector('.event__part.event__part--home.event__part--1')).inner_text()
        team2_1half_value = await (await match_handle.query_selector('.event__part.event__part--away.event__part--1')).inner_text()
        team1_current_value = await (await match_handle.query_selector('.event__score.event__score--home')).inner_text()
        team2_current_value = await (await match_handle.query_selector('.event__score.event__score--away')).inner_text()
        team1_coef = await (await match_handle.query_selector('.odds__odd.event__odd--odd1')).inner_text()
        team2_coef = await (await match_handle.query_selector('.odds__odd.event__odd--odd3')).inner_text()
    except AttributeError:
        team1_1half_value, team2_1half_value, team1_current_value, team2_current_value, team1_coef, team2_coef = '0', '0', '0', '0', '0', '0'
    return {
        'link': current_link,
        't1h1': int(team1_1half_value.strip('()')), # team 1 (home team) scored in first half
        't2h1': int(team2_1half_value.strip('()')), # team 2 (away team) scored in first half
        't1all': int(team1_current_value),          # team 1 scored during match
        't2all': int(team2_current_value),          # team 2 scored during match
        'time': int(match_time.split()[0]) if match_time.split()[0].isdigit()  else 0,
        'coef1': float(team1_coef) if bool(re.match(r'\d\.\d\d', team1_coef)) == True else 0,
        'coef2': float(team2_coef) if bool(re.match(r'\d\.\d\d', team2_coef)) == True else 0
    }

bet_2half=set()
async def main():
    async with async_playwright() as pw:
        browser = await pw.chromium.launch(headless=False, args=["--mute-audio"])
        context = await browser.new_context()
        page = await context.new_page()

        await page.goto(sport_url)
        await page.locator('.filters__text--short').get_by_text('LIVE').click()
        # try:
        while True:
                try:
                    current_matches = await page.locator("[id^='g_1']").element_handles()
                    for match_handle in current_matches:
                        match_data = await extract_match_data(match_handle)
                        print(match_data)
                        is_favorite = 1 < match_data['coef1'] < 1.5 or 1 < match_data['coef2'] < 1.5
                        if 64<match_data['time']<90 and match_data['t1all']+match_data['t2all'] == match_data['t1h1'] + match_data['t2h1']:

                            if match_data['t1h1'] == 0 and match_data['t2h1'] == 0 and is_favorite:
                                if match_data['link'] in bet_2half:
                                    continue
                                bet_2half.add(match_data['link'])
                                bet = (match_data['link'],'<< 0 : 0 >>')
                                bet_siska(bet)
                                print('TTTAAAAAKKKEEEEEEEEE IIIIITTTTTTTTTTT')

                            if match_data['t1h1'] == 0 and (match_data['t2h1'] in [2,3,4,5,6,7]) and is_favorite:
                                if match_data['link'] in bet_2half:
                                    continue
                                bet_2half.add(match_data['link'])
                                bet = (match_data['link'],'<< 0 - [2,3,...,7] >>')
                                bet_siska(bet)
                                print('TTTAAAAAKKKEEEEEEEEE IIIIITTTTTTTTTTT')

                            if match_data['t1h1'] == 1 and match_data['t2h1'] == 0 and is_favorite:
                                if match_data['link'] in bet_2half:
                                    continue
                                bet_2half.add(match_data['link'],'<< 1 - 0 >>')
                                bet = (match_data['link'],)
                                bet_siska(bet)
                                print('TTTAAAAAKKKEEEEEEEEE IIIIITTTTTTTTTTT')

                            if match_data['t1h1'] == 1 and match_data['t2h1'] == 2:
                                if match_data['link'] in bet_2half:
                                    continue
                                bet_2half.add(match_data['link'])
                                bet = (match_data['link'],'<< 1 - 2 >>')
                                bet_siska(bet)
                                print('TTTAAAAAKKKEEEEEEEEE IIIIITTTTTTTTTTT')

                            if match_data['t1h1'] == 2 and match_data['t2h1'] == 1 and is_favorite:
                                if match_data['link'] in bet_2half:
                                    continue
                                bet_2half.add(match_data['link'])
                                bet = (match_data['link'],'<< 2 - 1 >>')
                                bet_siska(bet)
                                print('TTTAAAAAKKKEEEEEEEEE IIIIITTTTTTTTTTT')

                            if match_data['t1h1'] == 2 and match_data['t2h1'] == 0 and is_favorite:
                                if match_data['link'] in bet_2half:
                                    continue
                                bet_2half.add(match_data['link'])
                                bet = (match_data['link'],'<< 2 - 0 >>')
                                bet_siska(bet)
                                print('TTTAAAAAKKKEEEEEEEEE IIIIITTTTTTTTTTT')

                            if match_data['t1h1'] + match_data['t2h1'] > 4:
                                if match_data['link'] in bet_2half:
                                    continue
                                bet_2half.add(match_data['link'])
                                bet = (match_data['link'],'JUST 1H MORE THEN 4')
                                bet_siska(bet)
                                print('TTTAAAAAKKKEEEEEEEEE IIIIITTTTTTTTTTT')



                        # '''  additional block just for rest) '''
                        # if match_data['t1h1'] + match_data['t2h1'] >2:
                        #     if match_data['t1all']+match_data['t2all'] == match_data['t1h1'] + match_data['t2h1']:
                        #         if 64<match_data['time']<90:
                        #             if match_data['link'] in bet_2half:
                        #                 continue
                        #             bet_2half.add(match_data['link'])
                        #             bet = (match_data['link'],)
                        #             bet_siska(bet)
                        #             print('TTTAAAAAKKKEEEEEEEEE IIIIITTTTTTTTTTT')



                    await asyncio.sleep(20)  # Пример: задержка в 60 секунд
                except TypeError as e:
                    print(e)
                    continue

        # except Exception as e:
        #     print(f"Произошла ошибка: {e}")


        # В этом месте можно добавить логику для завершения парсинга (например, по условию или сигналу)

        # Браузер не закрывается здесь

# Запуск основной функции

asyncio.run(main())


