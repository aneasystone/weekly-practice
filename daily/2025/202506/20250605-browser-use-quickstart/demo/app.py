from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
llm = ChatOpenAI(model="gpt-4.1-mini")

from browser_use import Agent
async def main():
    agent = Agent(
        task="Compare the price of gpt-4.1-mini and DeepSeek-V3",
        llm=llm,
        # save_conversation_path="logs/conversation"
    )
    result = await agent.run()
    print(result)

import asyncio
asyncio.run(main())