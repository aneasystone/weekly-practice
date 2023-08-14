from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain.llms import OpenAI
from langchain.agents import AgentType

# llm
llm = OpenAI(temperature=0, max_tokens=2048) 

# tools
tools = load_tools(["serpapi"])

# create an agent executor
agent_executor = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)

# run the agent executor
result = agent_executor.run("What's the date today? What great events have taken place today in history?")
print(result)
