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

from langgraph.checkpoint.postgres import PostgresSaver

# database setting
DB_URI = "postgresql://postgres:123456@localhost:5432/postgres?sslmode=disable"
connection_kwargs = {
    "autocommit": True,
    "prepare_threshold": 0,
}

config = {"configurable": {"thread_id": "3"}}
with PostgresSaver.from_conn_string(DB_URI) as checkpointer:
    
    # 第一次运行时初始化
    checkpointer.setup()
    
    graph = graph_builder.compile(checkpointer=checkpointer)
    for event in graph.stream({"messages": ("user", "合肥今天天气怎么样？")}, config):
        for value in event.values():
            value["messages"][-1].pretty_print()

### With a connection

from psycopg import Connection

with Connection.connect(DB_URI, **connection_kwargs) as conn:
    checkpointer = PostgresSaver(conn)
    graph = graph_builder.compile(checkpointer=checkpointer)
    for event in graph.stream({"messages": ("user", "要带伞吗？")}, config):
        for value in event.values():
            value["messages"][-1].pretty_print()
            
### With a connection pool

from psycopg_pool import ConnectionPool

with ConnectionPool(conninfo=DB_URI, max_size=20, kwargs=connection_kwargs) as pool:
    checkpointer = PostgresSaver(pool)
    graph = graph_builder.compile(checkpointer=checkpointer)
    for event in graph.stream({"messages": ("user", "北京呢？")}, config):
        for value in event.values():
            value["messages"][-1].pretty_print()