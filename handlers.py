import asyncio
import requests
import re
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright
from time import sleep
from notifiers import get_notifier
from nice import nice, is_it_top_league
from nice_all import nice_all, get_status
from soccer_nice import nice_dict
from ultra_soccer import ultra_dict

token = "5655731349:AAHpSNsDXkUochVg7jtVNeFadDa2JeA9-jE"
id = "5521639964"


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


def get_goals_timeline(lst):
    match = lst[:]
    goal_times = []

    for i, el in enumerate(match):
        try:
            score_change = match[i] + match[i + 2]
            goal_minute = match[i - 1].replace("'", '')
            if el.isdigit() and match[i + 1] == '-' and match[i + 2].isdigit() and goal_minute != 'HALF':
                if '+' in goal_minute:
                    if goal_minute[0] == '4':
                        goal_minute = 45
                    else:
                        goal_minute = 90
                goal_times.append((score_change, int(goal_minute)))
        except:
            break

    half1 = [i for i in goal_times if i[1] < 46]
    half2 = [i for i in goal_times if i[1] > 45]
    goals_before75 = [i for i in goal_times if 45 < i[1] < 75]
    goals_before45_60 = [i for i in goal_times if 45 < i[1] < 61]
    goals_before60_75 = [i for i in goal_times if 60 < i[1] < 75]
    goals_after75 = [i for i in goal_times if i[1] > 74]
    return goals_before45_60, goals_before60_75


def get_champ(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        heading = soup.find('meta', attrs={'name': 'og:description'})
        text_value = heading['content']
        return text_value

    return None

async def extract_match_data(match_handle, monitor):
    id = await match_handle.get_attribute('id')
    current_link = f"{sport_url_soc}match/{id[4:]}"
    champ = 'Unknown (wrong condition)'
    goals_before45_60 = goals_before60_75 = 'No goals timeline'

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

        real_coef1 = float(team1_coef) if bool(re.match(r'\d+(?:\.\d+)?$', team1_coef)) else 0
        real_coef2 = float(team2_coef) if bool(re.match(r'\d+(?:\.\d+)?$', team2_coef)) else 0

        if int(team1_1half_value.strip('()')) == int(team1_current_value) \
                and int(team2_1half_value.strip('()')) == int(team2_current_value):
            if real_time > 68:
                champ = get_champ(current_link)
        if int(team1_1half_value.strip('()')) == 0 and int(team2_1half_value.strip('()')) == 0:
            if 25<real_time<35 and any([1 < real_coef1 < 1.11, 1 < real_coef2 < 1.11]):
                champ = get_champ(current_link)

        if 1.1 < real_coef1 < 2 and int(team1_1half_value.strip('()')) + int(team2_1half_value.strip('()')) > 2:
            if int(team1_1half_value.strip('()')) > int(team2_1half_value.strip('()')):
                if int(team1_current_value) + int(team2_current_value) - int(team1_1half_value.strip('()')) - int(team2_1half_value.strip('()')) >= 2:
                    await monitor.goto(current_link)
                    goals_timeline = await (await monitor.query_selector('.smv__verticalSections')).inner_text()
                    goals_before45_60, goals_before60_75 = get_goals_timeline(goals_timeline.split())
                    print(goals_before45_60, goals_before60_75)



    except Exception as s:
        print(s)
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
        'coef2': float(team2_coef) if bool(re.match(r'\d+(?:\.\d+)?$', team2_coef)) else 0,
        '45_60': goals_before45_60,
        '60_75': goals_before60_75
    }


bet_2half_all = set()
bet_2half_top = set()
bet_2half_ult = set()
bet_1half_all = set()
bet_1half_top = set()
bet_2half_alter = set()

async def main():
    while True:
        try:
            async with async_playwright() as pw:
                browser = await pw.chromium.launch(headless=False, args=["--mute-audio"])
                context = await browser.new_context()
                monitor = await context.new_page()
                page = await context.new_page()
                await page.goto(sport_url_soc)
                await page.locator('.filters__text--short').get_by_text('LIVE').click()


                while True:
                    try:
                        current_matches = await page.locator("[id^='g_1']").element_handles()
                        for num, match_handle in enumerate(current_matches):
                            match_data = await extract_match_data(match_handle, monitor)

                            print(match_data)
                            where, status = get_status(match_data['coef1'], match_data['coef2'])
                            no_changes_before_69 = all([72 < match_data['time'] < 90,
                                                        match_data['t1all'] + match_data['t2all'] == match_data[
                                                            't1h1'] + match_data['t2h1']])
                            string_scores = f"{match_data['t1h1']}{match_data['t2h1']}"
                            print(
                                f' current: {string_scores}, favor: {where.upper()} {status.upper()} is ok for all?: {string_scores in nice_all[where][status]} no changes: {no_changes_before_69}')
                            print(nice_all[where][status])

                            still_no_goal_1half = all([25<match_data['time']<41, match_data['t1h1'] + match_data['t2h1'] == 0])

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
                                print("KEY ERROR (no coefs for analyze) ")
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
                                print("KEY ERROR (no coefs for analyze) ")
                                continue



                            try:
                                if still_no_goal_1half:
                                    if  1 < match_data['coef1'] < 1.11 or 1 < match_data['coef2'] < 1.11:
                                        if match_data['link'] in bet_1half_all:
                                            continue
                                        bet_1half_all.add(match_data['link'])
                                        bet = (
                                        match_data['link'], f'{where}{status}', string_scores, '1 half general')
                                        bet_siska(bet)
                                        print('-' * 50)
                            except KeyError:
                                print("KEY ERROR (no coefs for analize) ")
                                continue

                            '''   ALTERNATIVE SECTION   '''

                            try:
                                if no_changes_before_69:
                                    if 1.1<match_data['coef1'] < 1.51 and match_data['t1h1'] + match_data['t2h1'] > 0 and match_data['t1h1'] < match_data['t2h1']:
                                        if match_data['link'] in bet_2half_alter:
                                            continue
                                        bet_2half_alter.add(match_data['link'])
                                        bet = (
                                        match_data['link'], f'{where}{status}', string_scores, 'Alternative home over 11%')
                                        bet_siska(bet)
                                        print('-' * 50)
                            except KeyError:
                                print("KEY ERROR (no coefs for analyze) ")
                                continue


                            try:
                                if no_changes_before_69:
                                    if 1 < match_data['coef2'] < 1.3 and match_data['t1h1'] + match_data['t2h1'] > 0 and match_data['t1h1'] > match_data['t2h1']:
                                        if match_data['link'] in bet_2half_alter:
                                            continue
                                        bet_2half_alter.add(match_data['link'])
                                        bet = (
                                        match_data['link'], f'{where}{status}', string_scores, 'Alternative away over 14%')
                                        bet_siska(bet)
                                        print('-' * 50)
                            except KeyError:
                                print("KEY ERROR (no coefs for analyze) ")
                                continue


                            try:
                                if no_changes_before_69:
                                    if 1.1<match_data['coef1'] < 2 and match_data['t1h1'] + match_data['t2h1'] >= 2\
                                            and match_data['t1h1'] > match_data['t2h1']\
                                            and len(match_data['45_60'] == 0) and len(match_data['60_75'] == 0):
                                        if match_data['link'] in bet_2half_alter:
                                            continue
                                        bet_2half_alter.add(match_data['link'])
                                        bet = (
                                        match_data['link'], f'{where}{status}', string_scores, 'Alternative over 14% K=1.8')
                                        bet_siska(bet)
                                        print('-' * 50)
                            except KeyError:
                                print("KEY ERROR (no coefs for analyze) ")
                                continue



                        await asyncio.sleep(20)
                    except TypeError as e:
                        print(e)
                        continue

        except Exception as e:

            print(f"An error occurred: {e}")

            await asyncio.sleep(60)
            continue


if __name__ == "__main__":
    asyncio.run(main())