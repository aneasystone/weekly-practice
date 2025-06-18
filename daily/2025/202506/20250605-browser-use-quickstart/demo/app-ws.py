from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
llm = ChatOpenAI(model="gpt-4.1-mini")


from browser_use import BrowserSession
from browser_use import Agent
async def main():

    browser_session = BrowserSession(    
        wss_url="ws://localhost:55660/4b762d7e1b8b9a66d8c3ece7a5dd3b81"
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