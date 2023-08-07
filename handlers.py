import asyncio
from playwright.async_api import async_playwright
from time import sleep
from notifiers import get_notifier
from nice import nice, is_it_top_league
from nice_all import nice_all, get_status
from bs4 import BeautifulSoup
from soccer_nice import nice_dict
from ultra_soccer import ultra_dict
import requests


token = "5655731349:AAHpSNsDXkUochVg7jtVNeFadDa2JeA9-jE"
id = "5521639964"
import re

def bet_siska(data):
    telegram = get_notifier('telegram')
    info = "\n".join([i for i in data])
    telegram.notify(token=token,chat_id = id,message = info)
    print("MSG HAS BEEN SENT")


sport_url_soc = 'https://www.soccer24.com/'
sport_url_bb = 'https://www.basketball24.com/'
async def get_current_matches(page):
    await page.goto(sport_url)
    await page.locator('.filters__text--short').get_by_text('LIVE').click()
    current_matches = await page.locator("[id^='g_1']").element_handles()
    return current_matches


def get_champ(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        heading = soup.find('meta', attrs={'name': 'og:description'})
        text_value = heading['content']
        return text_value

    return None

async def extract_match_data(match_handle):
    id = await match_handle.get_attribute('id')
    current_link = f"{sport_url_soc}match/{id[4:]}"
    champ = 'Unknown (match time less 69)'

    try:
        match_time = await (await match_handle.query_selector('.event__stage--block')).inner_text()
        real_time = int(match_time.split()[0]) if match_time.split()[0].isdigit() else 0
        team1_1half_value = await (
            await match_handle.query_selector('.event__part.event__part--home.event__part--1')).inner_text()
        team2_1half_value = await (
            await match_handle.query_selector('.event__part.event__part--away.event__part--1')).inner_text()
        team1_current_value = await (await match_handle.query_selector('.event__score.event__score--home')).inner_text()
        team2_current_value = await (await match_handle.query_selector('.event__score.event__score--away')).inner_text()
        team1_coef = await (await match_handle.query_selector('.odds__odd.event__odd--odd1')).inner_text()
        team2_coef = await (await match_handle.query_selector('.odds__odd.event__odd--odd3')).inner_text()

        if int(team1_1half_value.strip('()')) == int(team1_current_value) \
                and int(team2_1half_value.strip('()')) == int(team2_current_value):
            if real_time > 68:
                champ = get_champ(current_link)

    except AttributeError:
        team1_1half_value, team2_1half_value, team1_current_value, team2_current_value, team1_coef, team2_coef = '0', '0', '0', '0', '0', '0'
        match_time = '0'
        real_time = 0

    return {
        'champ': champ,
        'link': current_link,
        't1h1': int(team1_1half_value.strip('()')),
        't2h1': int(team2_1half_value.strip('()')),
        't1all': int(team1_current_value),
        't2all': int(team2_current_value),
        'time': real_time,
        'coef1': float(team1_coef) if bool(re.match(r'\d+(?:\.\d+)?$', team1_coef)) else 0,
        'coef2': float(team2_coef) if bool(re.match(r'\d+(?:\.\d+)?$', team2_coef)) else 0
    }


bet_2half_all=set()
bet_2half_top=set()
bet_2half_ult = set()
# async def main():
#     async with async_playwright() as pw:
#         browser = await pw.chromium.launch(headless=False, args=["--mute-audio"])
#         context = await browser.new_context()
#         # context_bb = await browser.new_context()
#         page = await context.new_page()
#         # page_bb = await context.new_page()
#         await page.goto(sport_url_soc)
#         await page.locator('.filters__text--short').get_by_text('LIVE').click()
#         await page_bb.goto(sport_url_bb)
#         await page_bb.locator('.filters__text--short').get_by_text('LIVE').click()
#         # title = await (await match_handle.query_selector()).inner_text()
#         while True:
#             try:
#                 current_matches = await page.locator("[id^='g_1']").element_handles()
#                 for num ,match_handle in enumerate(current_matches):
#                     match_data = await extract_match_data(match_handle)
#                     print(match_data)
#                     where, status = get_status(match_data['coef1'], match_data['coef2'])
#                     no_changes_before_69 = all([68<match_data['time']<90, match_data['t1all']+match_data['t2all'] == match_data['t1h1'] + match_data['t2h1']])
#                     string_scores = f"{match_data['t1h1']}{match_data['t2h1']}"
#                     print(f' current: {string_scores}, favor: {where.upper()} {status.upper()} is ok for all?: {string_scores in nice_all[where][status]} no changes: {no_changes_before_69}')
#                     print(nice_all[where][status])
#
#                     if no_changes_before_69:
#                         if string_scores in nice_all[where][status]:
#                             if match_data['link'] in bet_2half_all:
#                                 continue
#                             bet_2half_all.add(match_data['link'])
#                             bet = (match_data['link'], f'{where}{status}', string_scores, 'General settings')
#                             bet_siska(bet)
#                             print('-' * 50)
#
#                     top_league = is_it_top_league(match_data['champ'], nice)
#                     try:
#                         if no_changes_before_69 and top_league is not None:
#                             if string_scores in nice[top_league][where][status]:
#                                 if match_data['link'] in bet_2half_top:
#                                     continue
#                                 bet_2half_top.add(match_data['link'])
#                                 bet = (match_data['link'], f'{where}{status}', string_scores, 'Advanced settings')
#                                 bet_siska(bet)
#                                 print('-' * 50)
#                     except KeyError:
#                         print("KEY ERROR (no coefs for analize) ")
#                         continue
#
#
#
#                 await asyncio.sleep(20)
#             except TypeError as e:
#                 print(e)
#                 continue
#
# asyncio.run(main())


async def main():
    while True:
        try:
            async with async_playwright() as pw:
                browser = await pw.chromium.launch(headless=False, args=["--mute-audio"])
                context = await browser.new_context()
                page = await context.new_page()
                await page.goto(sport_url_soc)
                await page.locator('.filters__text--short').get_by_text('LIVE').click()

                while True:
                    try:
                        current_matches = await page.locator("[id^='g_1']").element_handles()
                        for num, match_handle in enumerate(current_matches):
                            match_data = await extract_match_data(match_handle)

                            print(match_data)
                            where, status = get_status(match_data['coef1'], match_data['coef2'])
                            no_changes_before_69 = all([72 < match_data['time'] < 90,
                                                        match_data['t1all'] + match_data['t2all'] == match_data[
                                                            't1h1'] + match_data['t2h1']])
                            string_scores = f"{match_data['t1h1']}{match_data['t2h1']}"
                            print(
                                f' current: {string_scores}, favor: {where.upper()} {status.upper()} is ok for all?: {string_scores in nice_all[where][status]} no changes: {no_changes_before_69}')
                            print(nice_all[where][status])

                            if no_changes_before_69:
                                if string_scores in nice_all[where][status]:
                                    if match_data['link'] in bet_2half_all:
                                        continue
                                    bet_2half_all.add(match_data['link'])
                                    bet = (match_data['link'], f'{where}{status}', string_scores, 'General settings')
                                    bet_siska(bet)
                                    print('-' * 50)

                            top_league = is_it_top_league(match_data['champ'], nice_dict)
                            try:
                                if no_changes_before_69 and top_league is not None:
                                    if string_scores in nice_dict[top_league][where][status]:
                                        if match_data['link'] in bet_2half_top:
                                            continue
                                        bet_2half_top.add(match_data['link'])
                                        bet = (
                                        match_data['link'], f'{where}{status}', string_scores, 'Advanced settings')
                                        bet_siska(bet)
                                        print('-' * 50)
                            except KeyError:
                                print("KEY ERROR (no coefs for analize) ")
                                continue



                            try:
                                if no_changes_before_69 and top_league is not None:
                                    if string_scores in ultra_dict[top_league][where][status]:
                                        if match_data['link'] in bet_2half_ult:
                                            continue
                                        bet_2half_ult.add(match_data['link'])
                                        bet = (
                                        match_data['link'], f'{where}{status}', string_scores, 'Ultimate settings')
                                        bet_siska(bet)
                                        print('-' * 50)
                            except KeyError:
                                print("KEY ERROR (no coefs for analize) ")
                                continue


                        await asyncio.sleep(20)
                    except TypeError as e:
                        print(e)
                        continue

        except Exception as e:

            print(f"An error occurred: {e}")

            await asyncio.sleep(60)
            continue  # Перезапуск цикла


if __name__ == "__main__":
    asyncio.run(main())