from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
llm = ChatOpenAI(model="gpt-4.1-mini")

from browser_use import Agent
async def main():

    initial_actions = [
		{'open_tab': {'url': 'https://playwright.dev'}},
	]
    
    agent = Agent(
        task="这个页面讲的是内容？",
        llm=llm,

        # 初始化动作
        initial_actions=initial_actions
    )
    result = await agent.run()
    print(result)

import asyncio
asyncio.run(main())