from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
llm = ChatOpenAI(model="gpt-4.1-mini")

from playwright.async_api import async_playwright
from browser_use import Agent, BrowserSession


async def main():
    async with async_playwright() as p:
        
        # 手动打开页面
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        await page.goto("https://playwright.dev")

        browser_session = BrowserSession(
            browser=browser,
            browser_context=context,
            page=page,
        )

        agent = Agent(
            task="这个页面讲的是什么？",
            llm=llm,
            browser_session=browser_session
            # browser=browser,
            # browser_context=browser_context,
            # page=page,
        )
        result = await agent.run()
        print(result)

import asyncio
asyncio.run(main())