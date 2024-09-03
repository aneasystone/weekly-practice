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

while True:
    user_input = input("User: ")
    if user_input.lower() in ["quit", "exit", "q"]:
        print("Goodbye!")
        break
    # TODO: How to change the tool call args
    m = {"messages": ("user", user_input)}
    if user_input.lower() in ["yes", "y"]:
        m = None
    for event in graph.stream(m, config, stream_mode="values"):
        event["messages"][-1].pretty_print()
