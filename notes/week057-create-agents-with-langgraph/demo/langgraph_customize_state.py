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
    
     # This flag is new
    ask_human: bool


graph_builder = StateGraph(State)

### Define the tools

from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.pydantic_v1 import BaseModel, Field

class RequestAssistance(BaseModel):
    """Escalate the conversation to an expert.
    Use this if you are unable to assist directly or if the user requires support beyond your permissions.
    To use this function, relay the user's 'request' so the expert can provide the right guidance.
    """
    
    request: str = Field(description="the user's request")

tools = [TavilySearchResults(max_results=2)]

### Add a "chatbot" node, binding the tools

# from langchain_community.llms import SparkLLM
# llm = SparkLLM(
#     spark_api_url="wss://spark-api.xf-yun.com/v4.0/chat",
#     spark_llm_domain="4.0Ultra"
# )

from langchain_openai import ChatOpenAI
llm = ChatOpenAI()

# We can bind the llm to a tool definition, a pydantic model, or a json schema
llm_with_tools = llm.bind_tools(tools + [RequestAssistance])

def chatbot(state: State):
    response = llm_with_tools.invoke(state["messages"])
    ask_human = False
    if response.tool_calls and response.tool_calls[0]["name"] == RequestAssistance.__name__:
        ask_human = True
    return {"messages": [response], "ask_human": ask_human}

# The first argument is the unique node name
# The second argument is the function or object that will be called whenever
# the node is used.
graph_builder.add_node("chatbot", chatbot)

### Add a "tools" node

from langgraph.prebuilt import ToolNode

tool_node = ToolNode(tools=tools)
graph_builder.add_node("tools", tool_node)

### Add a "human" node

from langchain_core.messages import ToolMessage

def human_node(state: State):
    new_messages = []
    if not isinstance(state["messages"][-1], ToolMessage):
        # Typically, the user will have updated the state during the interrupt.
        # If they choose not to, we will include a placeholder ToolMessage to
        # let the LLM continue.
        new_messages.append(
            ToolMessage(
                content="No response from human.",
                tool_call_id=state["messages"][-1].tool_calls[0]["id"],
            )
        )
    return {
        # Append the new messages
        "messages": new_messages,
        # Unset the flag
        "ask_human": False,
    }

graph_builder.add_node("human", human_node)

### Build and compile the graph

from langgraph.prebuilt import tools_condition

def select_next_node(state: State):
    if state["ask_human"]:
        return "human"
    # Otherwise, we can route as before
    return tools_condition(state)

graph_builder.add_conditional_edges(
    "chatbot",
    select_next_node,
    {"human": "human", "tools": "tools", "__end__": "__end__"},
)
graph_builder.add_edge("tools", "chatbot")
graph_builder.add_edge("human", "chatbot")
graph_builder.add_edge(START, "chatbot")

### Compile with memory

from langgraph.checkpoint.memory import MemorySaver

memory = MemorySaver()

graph = graph_builder.compile(
    checkpointer=memory,
    interrupt_before=["human"],
)

print(graph.get_graph().draw_ascii())

### Run the chatbot

from langchain_core.messages import BaseMessage

config = {"configurable": {"thread_id": "1"}}

user_input = "I need some expert guidance for building this AI agent. Could you request assistance for me?"

events = graph.stream({"messages": [("user", user_input)]}, config, stream_mode="values")

for event in events:
    if "messages" in event:
        event["messages"][-1].pretty_print()
        
snapshot = graph.get_state(config)
existing_message = snapshot.values["messages"][-1]
# existing_message.pretty_print()

### Update the Tool Messages

human_response = (
    "We, the experts are here to help! We'd recommend you check out LangGraph to build your agent."
    " It's much more reliable and extensible than simple autonomous agents."
)
tool_messages = [
    ToolMessage(
        content=human_response,
        tool_call_id=existing_message.tool_calls[0]["id"],
    ),
]

graph.update_state(
    config,
    {"messages": tool_messages},
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