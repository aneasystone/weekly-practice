import asyncio
from playwright.async_api import async_playwright

# async def main():
#     async with async_playwright() as p:
#         browser = await p.chromium.launch(headless=True)
#         page = await browser.new_page()

#         await page.goto("https://arh.antoinevastel.com/bots/areyouheadless")
#         answer_element = page.locator("#res")
#         answer = await answer_element.text_content()
#         print(f'The result is: "{answer}"')

#         await browser.close()

# async def main():
#     async with async_playwright() as p:
#         browser = await p.chromium.launch(headless=True)
#         page = await browser.new_page()

#         await page.goto("https://bot-detector.rebrowser.net/")
#         await asyncio.sleep(5)
#         await page.screenshot(path='playwright-rebrowser.png')

#         await browser.close()

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, args=['--disable-blink-features=AutomationControlled'])
        browser_context = await browser.new_context(viewport={"height":721,"width":1281})
        # await browser_context.add_init_script("""
        #     Object.defineProperty(navigator, 'webdriver', {
        #         get: () => false,
        #     });
        # """)
        page = await browser_context.new_page()

        # await page.goto("https://nowsecure.nl")
        # await page.goto("https://fingerprint.com/products/bot-detection/")
        # await page.goto("https://bot.sannysoft.com/")
        await page.goto("https://bot-detector.rebrowser.net/")
        
        input()

        await browser.close()

asyncio.run(main())