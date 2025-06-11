from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
llm = ChatOpenAI(model="gpt-4.1-mini")

from playwright.async_api import async_playwright
from browser_use import Agent
async def main():
    async with async_playwright() as p:
        
        # 手动打开页面
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        await page.goto("https://playwright.dev")

        agent = Agent(
            task="这个页面讲的是内容？",
            llm=llm,

            # 使用已有页面
            page=page
        )
        result = await agent.run()
        print(result)

import asyncio
asyncio.run(main())