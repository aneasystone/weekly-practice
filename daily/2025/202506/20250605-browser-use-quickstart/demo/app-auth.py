from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
llm = ChatOpenAI(model="gpt-4.1-mini")

from browser_use import Agent
from browser_use.browser import BrowserSession
async def main():
    agent = Agent(
        task="打开 https://www.aneasystone.com/admin",
        llm=llm,

        # 复用已有的 cookies
        browser_session=BrowserSession(
            storage_state='./auth.json',
            user_data_dir=None
        )
    )
    result = await agent.run()
    print(result)

import asyncio
asyncio.run(main())