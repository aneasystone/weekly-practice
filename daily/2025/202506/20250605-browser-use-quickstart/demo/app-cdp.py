from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
llm = ChatOpenAI(model="gpt-4.1-mini")


from browser_use import BrowserSession
from browser_use import Agent
async def main():

    browser_session = BrowserSession(    
        cdp_url="http://localhost:9222"
    )
    agent = Agent(
        task="访问 https://playwright.dev 总结页面内容",
        llm=llm,
        browser_session=browser_session
    )
    result = await agent.run()
    print(result)

import asyncio
asyncio.run(main())