from langchain.chat_models import ChatOpenAI
from langchain.agents import tool, load_tools
from langchain.agents import initialize_agent
from langchain.agents import AgentType

import langchain

langchain.debug = True

# llm
llm = ChatOpenAI(temperature=0)

# tools
@tool
def get_word_length(word: str) -> int:
    """Returns the length of a word."""
    return len(word)

tools = load_tools(["llm-math"], llm=llm)
tools.append(get_word_length)

# create an agent executor
agent_executor = initialize_agent(tools, llm, agent=AgentType.OPENAI_MULTI_FUNCTIONS, verbose=True)

# run the agent executor
result = agent_executor.run("Calculate the length of the word 'weekly-practice' and the word 'aneasystone'?")
print(result)
