import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        # await page.goto("https://playwright.dev")
        await page.goto("https://fingerprint.com/products/bot-detection/")
        input()
        print(await page.title())
        await browser.close()

asyncio.run(main())