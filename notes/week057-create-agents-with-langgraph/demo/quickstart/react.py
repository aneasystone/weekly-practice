### 定义工具

from pydantic import BaseModel, Field
from langchain_core.tools import tool

class GetWeatherSchema(BaseModel):
    city: str = Field(description = "城市名称，如合肥、北京、上海等")
    date: str = Field(description = "日期，如今天、明天等")

@tool(args_schema = GetWeatherSchema)
def get_weather(city: str, date: str):
    """查询天气"""
    if city == "合肥":
        return "今天晴天，气温30度。"
    return "今天有小雨，气温25度。"

### ReAct 智能体

from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent

llm = ChatOpenAI()
memory = MemorySaver()
tools = [get_weather]
graph = create_react_agent(llm, tools=tools, checkpointer=memory)

### 运行

config = {"configurable": {"thread_id": "1"}}

for event in graph.stream({"messages": ("user", "合肥今天天气怎么样？")}, config):
    for value in event.values():
        value["messages"][-1].pretty_print()

for event in graph.stream({"messages": ("user", "要带伞吗？")}, config):
    for value in event.values():
        value["messages"][-1].pretty_print()