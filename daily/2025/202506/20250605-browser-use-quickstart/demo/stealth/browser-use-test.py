import asyncio
from browser_use.browser import BrowserSession

from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
llm = ChatOpenAI(model="gpt-4.1-mini")

from browser_use import Agent
# async def main():
#     browser_session = BrowserSession(
#         user_data_dir='~/.config/browseruse/profiles/demo',
#         headless=False,
#         stealth=True,
#     )
#     agent = Agent(
#         task="打开 https://bot-detector.rebrowser.net/ 验证机器人检测是否通过",
#         llm=llm,
#         browser_session=browser_session,
#     )
#     result = await agent.run()
#     print(result)

# async def main():
#     browser_session = BrowserSession(
#         user_data_dir='~/.config/browseruse/profiles/demo',
#         headless=False,
#         stealth=False,
#     )
#     agent = Agent(
#         task="""
#             打开 https://nowsecure.nl/
#             然后点击 ‘确认您是真人’ 这个复选框
#         """,
#         llm=llm,
#         browser_session=browser_session,
#         generate_gif=True
#     )
#     result = await agent.run()
#     print(result)

# from patchright.async_api import async_playwright
# from playwright.async_api import async_playwright

# async def main():
#     playwright = await async_playwright().start()
#     browser_session = BrowserSession(
#         playwright=playwright
#     )
#     agent = Agent(
#         task="""
#             打开 https://fingerprint.com/products/bot-detection/
#             检查你是否被检测为机器人
#         """,
#         llm=llm,
#         browser_session=browser_session,
#         generate_gif=True
#     )
#     result = await agent.run()
#     print(result)

async def main():
    browser_session = BrowserSession(
        stealth=False
    )
    agent = Agent(
        # task="打开 https://fingerprint.com/products/bot-detection/ 检查你是否被检测为机器人",
        task="打开 https://bot-detector.rebrowser.net/ 验证机器人检测是否通过",
        llm=llm,
        browser_session=browser_session,
    )
    result = await agent.run()
    print(result)

asyncio.run(main())
