import asyncio
from playwright.async_api import async_playwright
from time import sleep

sport_url = 'https://www.soccer24.com/'

def current_matchdata_link_handler(link):
    ...



async def main():
    async with async_playwright() as pw:
        browser = await pw.chromium.launch(headless=False, args=["--mute-audio"])
        context = await browser.new_context()
        page = await context.new_page()
        await page.goto(sport_url)
        await page.locator('.filters__text--short').get_by_text('LIVE').click()
        current_matches = await page.locator("[id^='g_1']").element_handles()

        for i in current_matches:
            id = await i.get_attribute('id')
            current_links = f"{sport_url}match/{id[4:]}"
            team1_1half_value = await \
                (await i.query_selector('.event__part.event__part--home.event__part--1')).inner_text()
            team2_1half_value = await \
                (await i.query_selector('.event__part.event__part--away.event__part--1')).inner_text()
            team1_current_value = await \
                (await i.query_selector('.event__score.event__score--home')).inner_text()
            team2_current_value = await \
                (await i.query_selector('.event__score.event__score--away')).inner_text()

            # team1_1half = await i.query_selector('.event__part.event__part--home.event__part--1').
            # team2_1half = await i.query_selector('.event__part.event__part--away.event__part--1')
            # team1_current = await i.query_selector('.event__score.event__score--home')
            # team2_current = await i.query_selector('.event__score.event__score--away')
            # team1_1half_vlaue = await team1_1half.inner_text()
            # team2_1half_value = await team2_1half.inner_text()
            # team1_current_value = await team1_current.inner_text()
            # team2_current_value = await team2_current.inner_text()
            print(f'{team1_current_value}-{team2_current_value}( {team1_1half_value}-{team2_1half_value}')
asyncio.run(main())

# import asyncio
# from playwright.async_api import async_playwright
#
# async def main():
#     async with async_playwright() as pw:
#         browser = await pw.chromium.launch(headless=False, args=["--mute-audio"])
#         context = await browser.new_context()
#         page = await context.new_page()
#         await page.goto('https://www.soccer24.com/')
#
#         element_locator = page.locator("[id^='g_1']")
#         element_handles = await element_locator.element_handles()
#
#         for element in element_handles:
#             element_id = await element.get_attribute('id')
#             print(f"ID элемента: {element_id}")
#
#         await browser.close()
#
# asyncio.run(main())




