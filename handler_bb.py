import asyncio
import requests
import re
import datetime
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
    current_matches = await page.locator("[id^='g_3']").element_handles()
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
    current_link = f"{sport_url_bb}match/{id[4:]}"
    champ = 'Unknown (wrong condition)'


    match_time = await (await match_handle.query_selector('.event__stage--block')).inner_text()
    try:
        t1q1 = await (
                await match_handle.query_selector('.event__part.event__part--home.event__part--1')).inner_text()
        t2q1 = await (
                await match_handle.query_selector('.event__part.event__part--away.event__part--1')).inner_text()
    except AttributeError:
        t1q1 = t2q1 = 0

    try:
        t1q2 = await (
                await match_handle.query_selector('.event__part.event__part--home.event__part--2')).inner_text()
        t2q2 = await (
                await match_handle.query_selector('.event__part.event__part--away.event__part--2')).inner_text()
    except AttributeError:
        t1q2 = t2q2 = 0

    try:
        t1q3 = await (
                await match_handle.query_selector('.event__part.event__part--home.event__part--3')).inner_text()
        t2q3 = await (
                await match_handle.query_selector('.event__part.event__part--away.event__part--3')).inner_text()
    except AttributeError:
        t1q3= t2q3 = 0

    try:
        t1q4 = await (
                await match_handle.query_selector('.event__part.event__part--home.event__part--4')).inner_text()
        t2q4 = await (
                await match_handle.query_selector('.event__part.event__part--away.event__part--4')).inner_text()
    except AttributeError:
        t1q4 = t2q4 = 0
    team1_coef = await (await match_handle.query_selector('.odds__odd.event__odd--odd1')).inner_text()
    team2_coef = await (await match_handle.query_selector('.odds__odd.event__odd--odd2')).inner_text()
    real_coef1 = float(team1_coef) if bool(re.match(r'\d+(?:\.\d+)?$', team1_coef)) else 0
    real_coef2 = float(team2_coef) if bool(re.match(r'\d+(?:\.\d+)?$', team2_coef)) else 0
    time_line = match_time.split()
    print(time_line)
    try:
        if 'Half' in time_line:
            quarter = 0.5
            minute = 0
        else:
            quarter = int(time_line[0][0])
            minute = int(time_line[-1])
    except:
        quarter = minute = 0
    # print(match_time)
    # except:
    #     t1q1=t2q1=t1q2=t2q2=t1q3=t2q3=t1q4=t2q4=real_coef1=real_coef2=quarter=minute = 0


    return {
        'champ': champ,
        'link': current_link,
        't1q1': int(t1q1),
        't2q1': int(t2q1),
        't1q2': int(t1q2),
        't2q2': int(t2q2),
        't1q3': int(t1q3),
        't2q3': int(t2q3),
        't1q4': int(t1q4),
        't2q4': int(t2q4),
        'coef1': real_coef1,
        'coef2': real_coef2,
        'quarter': quarter,
        'minute': minute
    }


underdog_ind_3q = set()
reloader = 0
async def main():
    while True:
        try:
            async with async_playwright() as pw:
                browser = await pw.chromium.launch(headless=False, args=["--mute-audio"])
                context = await browser.new_context()
                page = await context.new_page()
                await page.goto(sport_url_bb)
                await page.locator('.filters__text--short').get_by_text('LIVE').click()

                while True:
                    try:
                        current_matches = await page.locator("[id^='g_3']").element_handles()
                        for num, match_handle in enumerate(current_matches):
                            match_data = await extract_match_data(match_handle)
                            print(match_data)
                            where, status = get_status(match_data['coef1'], match_data['coef2'])
                            quarter = match_data['quarter']
                            minute = match_data['minute']
                    except:
                        True

                    now = datetime.datetime.now()
                    if (now.hour == 8 or now.hour == 12) and now.minute == range(2) and now.second in range(8):
                        await browser.close()
                        break


        except Exception as e:

            print(f"An error occurred: {e}")

            await asyncio.sleep(60)
            continue


if __name__ == "__main__":
    asyncio.run(main())