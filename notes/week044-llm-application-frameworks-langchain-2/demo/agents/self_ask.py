from langchain import SerpAPIWrapper
from langchain.chat_models import ChatOpenAI
from langchain.agents import initialize_agent, Tool
from langchain.agents import AgentType

# llm
llm = ChatOpenAI(temperature=0)

# tools
search = SerpAPIWrapper()
tools = [
    Tool(
        name="Intermediate Answer",
        func=search.run,
        description="useful for when you need to ask with search",
    )
]

# create an agent executor
agent_executor = initialize_agent(tools, llm, agent=AgentType.SELF_ASK_WITH_SEARCH, verbose=True)

print(agent_executor.agent.llm_chain.prompt.template)

# run the agent executor
result = agent_executor.run("When is the current president of the United States born?")
print(result)
