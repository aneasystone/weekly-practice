from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
llm = ChatOpenAI(model="gpt-4.1-mini")

from browser_use import Agent

async def on_step_start(agent: Agent):
    print(f"======== on_step_start {agent.state.n_steps} ========")

async def on_step_end(agent: Agent):
    print(f"======== on_step_end {agent.state.n_steps} ========")

async def main():
    agent = Agent(
        task="Compare the price of gpt-4.1-mini and DeepSeek-V3",
        llm=llm,
    )
    result = await agent.run(
        on_step_start=on_step_start,
        on_step_end=on_step_end
    )
    print(result)

import asyncio
asyncio.run(main())