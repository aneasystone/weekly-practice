from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
llm = ChatOpenAI(model="gpt-4.1-mini")

from browser_use.agent.views import AgentOutput
from browser_use.browser.views import BrowserStateSummary
def register_new_step_callback(browser_state_summary: BrowserStateSummary, agent_output: AgentOutput, n_steps: int):
    print(f'========== STEP {n_steps} BEGIN ==========')
    print("BrowserStateSummary:")
    print(f'  Title: {browser_state_summary.title}')
    print(f'  Url: {browser_state_summary.url}')
    print(f'  Screenshot: {browser_state_summary.screenshot[:80]}...')
    print("AgentOutput:")
    print(f'  Previous Goal: {agent_output.current_state.evaluation_previous_goal}')
    print(f'  Next Goal: {agent_output.current_state.next_goal}')
    print(f'========== STEP {n_steps} END ==========')

from browser_use import Agent
async def main():
    agent = Agent(
        task="Compare the price of gpt-4.1-mini and DeepSeek-V3",
        llm=llm,
        
        # 监听每一步执行
        register_new_step_callback=register_new_step_callback,
    )
    result = await agent.run()
    print(result)

import asyncio
asyncio.run(main())