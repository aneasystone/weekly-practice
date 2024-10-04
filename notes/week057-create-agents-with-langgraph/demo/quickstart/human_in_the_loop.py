### 定义工具

from pydantic import BaseModel, Field
from langchain_core.tools import tool

class BookTicketSchema(BaseModel):
    from_city: str = Field(description = "出发城市名称，如合肥、北京、上海等")
    to_city: str = Field(description = "到达城市名称，如合肥、北京、上海等")
    date: str = Field(description = "日期，如今天、明天等")

@tool(args_schema = BookTicketSchema)
def book_ticket(from_city: str, to_city: str, date: str):
    """预定机票"""
    return "您已成功预定 %s 从 %s 到 %s 的机票" % (date, from_city, to_city)

### 定义状态图

from langgraph.graph import StateGraph, MessagesState

graph_builder = StateGraph(MessagesState)

### 定义 tools 节点

from langgraph.prebuilt import ToolNode

tools = [book_ticket]
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
graph = graph_builder.compile(
    checkpointer=memory,
    interrupt_before=["tools"]
)

print(graph.get_graph().draw_ascii())

### 运行

config = {"configurable": {"thread_id": "1"}}

for event in graph.stream({"messages": ("user", "帮我预定一张明天从合肥到北京的机票")}, config):
    for value in event.values():
        value["messages"][-1].pretty_print()

snapshot = graph.get_state(config)
print(snapshot.values["messages"][-1])
print(snapshot.next)

### 继续运行

for event in graph.stream(None, config):
    for value in event.values():
        value["messages"][-1].pretty_print()