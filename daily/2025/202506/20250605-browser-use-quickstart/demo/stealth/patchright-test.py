import asyncio
from patchright.async_api import async_playwright

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
#         await page.screenshot(path='patchright-rebrowser.png')

#         await browser.close()

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        # await page.goto("https://nowsecure.nl")
        await page.goto("https://fingerprint.com/products/bot-detection/")
        
        input()

        await browser.close()

asyncio.run(main())