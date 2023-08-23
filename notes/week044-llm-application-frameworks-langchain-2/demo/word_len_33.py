from langchain.chat_models import ChatOpenAI
from langchain.tools import BaseTool
from langchain.schema import SystemMessage
from langchain.agents import OpenAIFunctionsAgent
from langchain.agents import AgentExecutor
from typing import Optional, Type
from langchain.callbacks.manager import AsyncCallbackManagerForToolRun, CallbackManagerForToolRun
from pydantic import BaseModel, Field

# llm
llm = ChatOpenAI(temperature=0)

class WordLengthSchema(BaseModel):
    word: str = Field(description = "the word to be calculating")
    excluding_hyphen: bool = Field(description = "excluding the hyphen or not, default to false")

# tools
class WordLengthTool(BaseTool):
    name = "get_word_length"
    description = "Returns the length of a word."
    args_schema: Type[WordLengthSchema] = WordLengthSchema

    def _run(
        self, word: str, excluding_hyphen: bool = False, run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool."""
        if excluding_hyphen:
            return len(word.replace('-', ''))
        else:
            return len(word)

    async def _arun(
        self, word: str, run_manager: Optional[AsyncCallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("get_word_length does not support async")

tools = [
    WordLengthTool()
]

# prompt
system_message = SystemMessage(
    content="You are very powerful assistant, but bad at calculating lengths of words."
)
prompt = OpenAIFunctionsAgent.create_prompt(system_message=system_message)

# create an agent
agent = OpenAIFunctionsAgent(llm=llm, tools=tools, prompt=prompt)

# create an agent executor
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# run the agent executor
result = agent_executor.run("how many letters in the word 'weekly-practice', including the hyphen?")
print(result)
result = agent_executor.run("how many letters in the word 'weekly-practice', excluding the hyphen?")
print(result)
