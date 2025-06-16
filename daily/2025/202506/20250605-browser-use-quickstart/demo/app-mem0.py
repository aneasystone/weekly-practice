from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
llm = ChatOpenAI(model="gpt-4.1-mini")

from browser_use.agent.memory import MemoryConfig
from browser_use import Agent
async def main():
    agent = Agent(
        task="Compare the price of gpt-4.1-mini and DeepSeek-V3",
        llm=llm,
        
        enable_memory=True,
        memory_config=MemoryConfig(
            llm_instance=llm,
            agent_id="my_custom_agent",
            memory_interval=5,
            vector_store_base_path="./agent_memory", 
        )
    )
    result = await agent.run()
    print(result)
    print(agent.memory.mem0.get_all())

import asyncio
asyncio.run(main())