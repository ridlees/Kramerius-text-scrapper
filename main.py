import asyncio
from playwright.async_api import async_playwright
import time


async def main():
    async with async_playwright() as pw:
        browser = await pw.chromium.launch(headless=False)
        context = await browser.new_context(user_agent="Mozilla/5.0 (Windows NT  10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36");
        page = await context.new_page()
        await page.goto(
            "https://kramerius.lib.cas.cz/view/uuid:cac19033-48e1-11e1-1154-001143e3f55c?page=uuid:cac19034-48e1-11e1-1154-001143e3f55c"
        )
        await page.wait_for_timeout(7000)
        await page.mouse.wheel(10, 30);
        textButton = await page.query_selector_all('//button[@class="mat-focus-indicator mat-tooltip-trigger mat-icon-button mat-button-base ng-star-inserted"]')
        await textButton[3].click()
        await page.wait_for_timeout(5000)

        popup = await page.query_selector_all(
            '//div[@class="app-text-content"]'
        )
        text = await popup[0].text_content()
        print(text)
        await browser.close()


if __name__ == '__main__':
    asyncio.run(main())
