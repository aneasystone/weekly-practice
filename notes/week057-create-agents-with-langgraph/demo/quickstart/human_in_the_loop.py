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

### 运行

print("-" * 30)
config = {"configurable": {"thread_id": "2"}}

for event in graph.stream({"messages": ("user", "帮我预定一张明天从合肥到北京的机票")}, config):
    for value in event.values():
        value["messages"][-1].pretty_print()

# 修改工具调用的参数
from langchain_core.messages import AIMessage

snapshot = graph.get_state(config)
existing_message = snapshot.values["messages"][-1]
new_tool_call = existing_message.tool_calls[0].copy()
new_tool_call["args"]["date"] = "后天"
new_message = AIMessage(
    content=existing_message.content,
    tool_calls=[new_tool_call],
    # Important! The ID is how LangGraph knows to REPLACE the message in the state rather than APPEND this messages
    id=existing_message.id,
)
graph.update_state(config, {"messages": [new_message]})

### 继续运行

for event in graph.stream(None, config):
    for value in event.values():
        value["messages"][-1].pretty_print()
        
### 运行

print("-" * 30)
config = {"configurable": {"thread_id": "3"}}

for event in graph.stream({"messages": ("user", "帮我预定一张明天从合肥到北京的机票")}, config):
    for value in event.values():
        value["messages"][-1].pretty_print()

# 手动构造回复
from langchain_core.messages import AIMessage, ToolMessage

snapshot = graph.get_state(config)
existing_message = snapshot.values["messages"][-1]
new_messages = [
    # The LLM API expects some ToolMessage to match its tool call. We'll satisfy that here.
    ToolMessage(content="预定失败", tool_call_id=existing_message.tool_calls[0]["id"]),
    # And then directly "put words in the LLM's mouth" by populating its response.
    AIMessage(content="预定失败"),
]
graph.update_state(config, {"messages": new_messages})

### 继续运行

for event in graph.stream(None, config):
    for value in event.values():
        value["messages"][-1].pretty_print()
        
print("\n\nLast 2 messages;")
for message in graph.get_state(config).values["messages"][-2:]:
    message.pretty_print()
    
### 运行

print("-" * 30)
config = {"configurable": {"thread_id": "4"}}

for event in graph.stream({"messages": ("user", "帮我预定一张明天从合肥到北京的机票")}, config):
    for value in event.values():
        value["messages"][-1].pretty_print()

# 手动构造回复
from langchain_core.messages import AIMessage, ToolMessage

snapshot = graph.get_state(config)
existing_message = snapshot.values["messages"][-1]
new_messages = [
    # And then directly "put words in the LLM's mouth" by populating its response.
    AIMessage(content="抱歉，我暂时不能预定机票"),
]
graph.update_state(
    config,
    {"messages": new_messages},
    # Which node for this function to act as. It will automatically continue
    # processing as if this node just ran.
    as_node="chatbot",
)

### 继续运行

for event in graph.stream(None, config):
    for value in event.values():
        value["messages"][-1].pretty_print()
        
print("\n\nLast 1 messages;")
for message in graph.get_state(config).values["messages"][-1:]:
    message.pretty_print()
