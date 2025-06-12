from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
llm = ChatOpenAI(model="gpt-4.1-mini")

from browser_use import Agent
async def main():
    agent = Agent(
        task="查询《哪吒2魔童闹海》的豆瓣评分",
        llm=llm,
        
        generate_gif=True
    )
    result = await agent.run()
    print(result)

import asyncio
asyncio.run(main())