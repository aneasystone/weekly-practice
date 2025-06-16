from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
llm = ChatOpenAI(model="gpt-4.1-mini")

import anyio
from browser_use import Agent
async def main():
    agent = Agent(
        task="Compare the price of gpt-4.1-mini and DeepSeek-V3",
        llm=llm,
    )

    for i in range(100):
        done, valid = await agent.take_step()
        print(f'Step {i}: Done: {done}, Valid: {valid}')

		# Save state to file
        if i == 3:
            async with await anyio.open_file('agent_state.json', 'w') as f:
                serialized = agent.state.model_dump_json(exclude={'history'})
                await f.write(serialized)
            break

        if done and valid:
            break

    result = agent.state.last_result
    print(result)

import asyncio
asyncio.run(main())