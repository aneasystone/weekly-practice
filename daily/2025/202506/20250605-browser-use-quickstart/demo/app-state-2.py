from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
llm = ChatOpenAI(model="gpt-4.1-mini")

import anyio
from browser_use import Agent
from browser_use.agent.views import AgentState
async def main():
    # Load state back from file
    async with await anyio.open_file('agent_state.json', 'r') as f:
        loaded_json = await f.read()
        agent_state = AgentState.model_validate_json(loaded_json)

    agent = Agent(
        task="Compare the price of gpt-4.1-mini and DeepSeek-V3",
        llm=llm,

        # 注入已有状态
        injected_agent_state=agent_state
    )

    for i in range(100):
        done, valid = await agent.take_step()
        print(f'Step {i}: Done: {done}, Valid: {valid}')
        if done and valid:
            break

    result = agent.state.last_result
    print(result)

import asyncio
asyncio.run(main())