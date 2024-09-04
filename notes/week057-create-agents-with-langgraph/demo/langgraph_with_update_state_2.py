from typing import Annotated

from typing_extensions import TypedDict

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages

### Creating a StateGraph

class State(TypedDict):
    # Messages have the type "list". The `add_messages` function
    # in the annotation defines how this state key should be updated
    # (in this case, it appends messages to the list, rather than overwriting them)
    messages: Annotated[list, add_messages]


graph_builder = StateGraph(State)

### Define the tools

from langchain_community.tools.tavily_search import TavilySearchResults

tool = TavilySearchResults(max_results=2)
tools = [tool]

### Add a "chatbot" node, binding the tools

# from langchain_community.llms import SparkLLM
# llm = SparkLLM(
#     spark_api_url="wss://spark-api.xf-yun.com/v4.0/chat",
#     spark_llm_domain="4.0Ultra"
# )

from langchain_openai import ChatOpenAI
llm = ChatOpenAI()

llm_with_tools = llm.bind_tools(tools)

def chatbot(state: State):
    return {"messages": [llm_with_tools.invoke(state["messages"])]}

# The first argument is the unique node name
# The second argument is the function or object that will be called whenever
# the node is used.
graph_builder.add_node("chatbot", chatbot)

### Add a "tools" node

from langgraph.prebuilt import ToolNode

tool_node = ToolNode(tools=tools)
graph_builder.add_node("tools", tool_node)

### Build and compile the graph

from langgraph.prebuilt import tools_condition

graph_builder.add_conditional_edges("chatbot", tools_condition)
graph_builder.add_edge("tools", "chatbot")
graph_builder.add_edge(START, "chatbot")

### Compile with memory

from langgraph.checkpoint.memory import MemorySaver

memory = MemorySaver()

graph = graph_builder.compile(
    checkpointer=memory,
    interrupt_before=["tools"],
)

print(graph.get_graph().draw_ascii())

### Run the chatbot

from langchain_core.messages import BaseMessage

config = {"configurable": {"thread_id": "1"}}

user_input = "I'm learning LangGraph. Could you do some research on it for me?"

events = graph.stream({"messages": [("user", user_input)]}, config, stream_mode="values")

for event in events:
    if "messages" in event:
        event["messages"][-1].pretty_print()
        
snapshot = graph.get_state(config)
existing_message = snapshot.values["messages"][-1]
# existing_message.pretty_print()

### Update the AI Messages

from langchain_core.messages import ToolMessage
from langchain_core.messages import AIMessage

new_tool_call = existing_message.tool_calls[0].copy()
new_tool_call["args"]["query"] = "LangGraph human-in-the-loop workflow"

new_messages = [
    AIMessage(
        content=existing_message.content,
        tool_calls=[new_tool_call],
        # Important! The ID is how LangGraph knows to REPLACE the message in the state rather than APPEND this messages
        id=existing_message.id,
    ),
]

graph.update_state(
    config,
    {"messages": new_messages},
)

snapshot = graph.get_state(config)
snapshot.values["messages"][-1].pretty_print()

# AIMessage contains `tool_calls`, so next is tools.
print(snapshot.next)

### Resume the graph

events = graph.stream(None, config, stream_mode="values")
for event in events:
    if "messages" in event:
        event["messages"][-1].pretty_print()