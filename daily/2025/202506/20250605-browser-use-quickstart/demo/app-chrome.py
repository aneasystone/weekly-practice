from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
llm = ChatOpenAI(model="gpt-4.1-mini")

from browser_use import BrowserSession
from browser_use.browser.profile import BrowserChannel
browser_session = BrowserSession(    
    executable_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    # executable_path='C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
    # executable_path='/usr/bin/google-chrome',
    
    user_data_dir='/Users/aneasystone/.config/browseruse/profiles/default',

    # channel=BrowserChannel.MSEDGE
    # channel=BrowserChannel.CHROMIUM
    # channel=BrowserChannel.CHROME
)

from browser_use import Agent
async def main():
    agent = Agent(
        task="访问 https://playwright.dev",
        llm=llm,
        browser_session=browser_session
    )
    result = await agent.run()
    print(result)

import asyncio
asyncio.run(main())