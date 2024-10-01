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

### 定义状态图

from langgraph.graph import StateGraph, MessagesState

graph_builder = StateGraph(MessagesState)

### 定义 tools 节点

from langgraph.prebuilt import ToolNode

tools = [get_weather]
tool_node = ToolNode(tools)

### 定义模型和 chatbot 节点

from langchain_openai import ChatOpenAI

llm = ChatOpenAI()
llm = llm.bind_tools(tools)

def chatbot(state: MessagesState):
    return {"messages": [llm.invoke(state["messages"])]}

### 构建和编译图

from langgraph.graph import END, START
from langgraph.prebuilt import tools_condition

graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("tools", tool_node)
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("tools", 'chatbot')
graph_builder.add_conditional_edges("chatbot", tools_condition)

from langgraph.checkpoint.memory import MemorySaver

memory = MemorySaver()
graph = graph_builder.compile(checkpointer=memory)

print(graph.get_graph().draw_ascii())

### 运行

# for event in graph.stream({"messages": ("user", "合肥今天天气怎么样？")}):
#     for value in event.values():
#         value["messages"][-1].pretty_print()

# for event in graph.stream({"messages": ("user", "要带伞吗？")}):
#     for value in event.values():
#         value["messages"][-1].pretty_print()

config = {"configurable": {"thread_id": "1"}}

for event in graph.stream({"messages": ("user", "合肥今天天气怎么样？")}, config):
    for value in event.values():
        value["messages"][-1].pretty_print()

for event in graph.stream({"messages": ("user", "要带伞吗？")}, config):
    for value in event.values():
        value["messages"][-1].pretty_print()