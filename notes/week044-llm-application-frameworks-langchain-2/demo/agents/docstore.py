from langchain import Wikipedia
from langchain.chat_models import ChatOpenAI
from langchain.agents import initialize_agent, Tool
from langchain.agents import AgentType
from langchain.agents.react.base import DocstoreExplorer

# llm
llm = ChatOpenAI(temperature=0)

# tools
docstore = DocstoreExplorer(Wikipedia())
tools = [
    Tool(
        name="Search",
        func=docstore.search,
        description="useful for when you need to ask with search",
    ),
    Tool(
        name="Lookup",
        func=docstore.lookup,
        description="useful for when you need to ask with lookup",
    ),
]

# create an agent executor
agent_executor = initialize_agent(tools, llm, agent=AgentType.REACT_DOCSTORE, verbose=True)

print(agent_executor.agent.llm_chain.prompt.template)

# run the agent executor
result = agent_executor.run("Who is the current president of the United States?")
print(result)
