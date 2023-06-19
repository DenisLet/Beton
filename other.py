import asyncio
from playwright.async_api import async_playwright


class Sport:
    def __init__(self, url, duration, period_duration, number_of_periods, locator):
        self.url = url
        self.duration = duration
        self.period_duration = period_duration
        self.number_of_periods = number_of_periods
        self.locator =  "[id^='g_{}']".format(locator)

    async def navigate_and_click_live_filter(self, page):
        await page.goto(self.url)
        await page.locator('.filters__text--short').get_by_text('LIVE').click()


async def process_sport(sport):
    async with async_playwright() as pw:
        browser = await pw.chromium.launch(headless=False, args=["--mute-audio"])
        context = await browser.new_context()
        page = await context.new_page()
        await sport.navigate_and_click_live_filter(page)

        while True:
            # Ваш код для работы со страницей и обработки динамического контента
            # ...

            # Получить ссылки с использованием CSS-локатора
            links = await page.query_selector_all(sport.locator)
            for link in links:
                href = await link.get_attribute('href')
                print(href)

            # Добавьте задержку перед следующей итерацией цикла
            await asyncio.sleep(10)

        # Закрытие страницы и контекста не выполняется, так как цикл while будет продолжаться бесконечно


async def main():
    # Создайте экземпляры класса Sport для каждого вида спорта
    basketball = Sport('https://www.basketball24.com/', 40, 10, 3, 'basketball')
    soccer = Sport('https://www.soccer24.com/', 90, 45, 2, 'soccer')
    handball = Sport('https://www.handball24.com/', 60, 30, 2, 'handball')
    hockey = Sport('https://www.icehockey24.com/', 60, 20, 3, 'hockey')

    # Запустите выполнение задачи для каждого вида спорта
    await asyncio.gather(
        process_sport(basketball),
        process_sport(soccer),
        process_sport(handball),
        process_sport(hockey)
    )


# Запустите основную асинхронную функцию
asyncio.run(main())
