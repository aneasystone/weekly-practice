from langchain.chat_models import ChatOpenAI
from langchain.agents import tool
from langchain.agents import initialize_agent
from langchain.agents import AgentType
from pydantic import BaseModel, Field

# llm
llm = ChatOpenAI(temperature=0)

class WordLengthSchema(BaseModel):
    word: str = Field(description = "the word to be calculating")

# tools
@tool(args_schema = WordLengthSchema)
def get_word_length(word: str) -> int:
    """Returns the length of a word."""
    return len(word)

tools = [get_word_length]

# create an agent executor
agent_executor = initialize_agent(tools, llm, agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION, verbose=True)

# run the agent executor
result = agent_executor.run("how many letters in the word 'weekly-practice'?")
print(result)
