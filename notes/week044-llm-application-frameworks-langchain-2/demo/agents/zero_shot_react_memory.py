from langchain.chat_models import ChatOpenAI
from langchain.agents import tool, load_tools
from langchain.agents import initialize_agent
from langchain.agents import AgentType
from langchain.memory import ConversationBufferMemory

# llm
llm = ChatOpenAI(temperature=0, verbose=True)

# tools
@tool
def get_word_length(word: str) -> int:
    """Returns the length of a word."""
    return len(word)

tools = load_tools(["llm-math"], llm=llm)
tools.append(get_word_length)

prefix = """Have a conversation with a human, answering the following questions as best you can. You have access to the following tools:"""
suffix = """Begin!"

{chat_history}
Question: {input}
{agent_scratchpad}"""

memory = ConversationBufferMemory(memory_key="chat_history")

# create an agent executor
agent_executor = initialize_agent(
    tools, 
    llm, 
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, 
    verbose=True,
    memory=memory,
    agent_kwargs={
        "prefix": prefix,
        "suffix": suffix,
        "input_variables": ["input", "chat_history", "agent_scratchpad"],
    }
)

print(agent_executor.agent.llm_chain.prompt.template)

# run the agent executor
result = agent_executor.run("how many letters in the word 'weekly-practice'?")
print(result)
result = agent_executor.run("how many letters in the word 'hello-world'?")
print(result)
result = agent_executor.run("what is the product of results above?")
print(result)
