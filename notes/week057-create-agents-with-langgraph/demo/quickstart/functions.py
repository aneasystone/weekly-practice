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

import json
from langchain_core.messages import FunctionMessage

class BasicToolNode:

    def __init__(self, tools: list) -> None:
        self.tools_by_name = {tool.name: tool for tool in tools}

    def __call__(self, inputs: dict):
        if messages := inputs.get("messages", []):
            message = messages[-1]
        else:
            raise ValueError("No message found in input")
        outputs = []
        if "function_call" in message.additional_kwargs:
            tool_call = message.additional_kwargs["function_call"]
            tool_result = self.tools_by_name[tool_call["name"]].invoke(
                json.loads(tool_call["arguments"])
            )
            outputs.append(
                FunctionMessage(
                    content=json.dumps(tool_result),
                    name=tool_call["name"]
                )
            )
        return {"messages": outputs}

tools = [get_weather]
tool_node = BasicToolNode(tools=tools)

### 调试用

class Wrapper:
    ''' 包装类，用于调试 OpenAI 接口的原始入参和出参
    '''
    def __init__(self, wrapped_class):
        self.wrapped_class = wrapped_class

    def __getattr__(self, attr):
        original_func = getattr(self.wrapped_class, attr)

        def wrapper(*args, **kwargs):
            print(f"Calling function: {attr}")
            print(f"Arguments: {args}, {kwargs}")
            result = original_func(*args, **kwargs)
            print(f"Response: {result}")
            return result
        return wrapper

### 定义模型和 chatbot 节点

from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4")
# llm.client = Wrapper(llm.client)
llm = llm.bind_functions(tools)

def chatbot(state: MessagesState):
    return {"messages": [llm.invoke(state["messages"])]}

### 构建和编译图

from langgraph.graph import END, START

from typing import Literal

def tools_condition(
    state: MessagesState,
) -> Literal["tools", "__end__"]:

    if isinstance(state, list):
        ai_message = state[-1]
    elif messages := state.get("messages", []):
        ai_message = messages[-1]
    else:
        raise ValueError(f"No messages found in input state to tool_edge: {state}")
    if "function_call" in ai_message.additional_kwargs:
        return "tools"
    return "__end__"

graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("tools", tool_node)
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("tools", 'chatbot')
graph_builder.add_conditional_edges("chatbot", tools_condition)
graph = graph_builder.compile()

print(graph.get_graph().draw_ascii())

### 运行

for event in graph.stream({"messages": ("user", "合肥今天天气怎么样？")}):
    for value in event.values():
        value["messages"][-1].pretty_print()
