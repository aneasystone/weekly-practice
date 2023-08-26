from langchain.chat_models import ChatOpenAI
from langchain.agents import tool, load_tools
from langchain.agents import initialize_agent
from langchain.agents import AgentType
from langchain.memory import ConversationBufferMemory

# llm
llm = ChatOpenAI(temperature=0)

# tools
@tool
def get_word_length(word: str) -> int:
    """Returns the length of a word."""
    return len(word)

tools = load_tools(["llm-math"], llm=llm)
tools.append(get_word_length)

# memory
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# create an agent executor
agent_executor = initialize_agent(
    tools, 
    llm, 
    agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION, 
    verbose=True,
    memory=memory,
)

# run the agent executor
result = agent_executor.run("how many letters in the word 'weekly-practice'?")
print(result)
result = agent_executor.run("how many letters in the word 'aneasystone'?")
print(result)
result = agent_executor.run("what is the sum of results above?")
print(result)
