# WEEK057 - 基于 LangGraph 创建智能体应用

早在年初的时候，[LangChain 发布了 v0.1.0 稳定版本](https://blog.langchain.dev/langchain-v0-1-0/)，版本公告里通过大量的篇幅对功能特性做了全面的介绍，最后，在公告的结尾，提到了一个不那么显眼的库，那就是 [LangGraph](https://github.com/langchain-ai/langgraph)。尽管看上去不那么显眼，但是它却非常重要，所以后来官方又 [发表了一篇博客来单独介绍它](https://blog.langchain.dev/langgraph/)，这是一个面向当前大模型领域最火热的智能体应用的库，是 LangChain 在智能体开发，特别是复杂的多智能体系统方面的一次重大尝试。

在之前的 LangChain 版本中，我们可以通过 `AgentExecutor` 实现智能体，在 [大模型应用开发框架 LangChain 学习笔记（二）](../week044-llm-application-frameworks-langchain-2/README.md) 中，我们曾经学习过 `AgentExecutor` 的用法，实现了包括 Zero-shot ReAct Agent、Conversational ReAct Agent、ReAct DocStore Agent、Self-Ask Agent、OpenAI Functions Agent 和 Plan and execute Agent 这些不同类型的智能体。但是这种方式过于黑盒，所有的决策过程都隐藏在 `AgentExecutor` 的背后，缺乏更精细的控制能力，在构建复杂智能体的时候非常受限。

LangGraph 提供了对应用程序的流程和状态更精细的控制，它允许定义包含循环的流程，并使用 **状态图（State Graph）** 来表示 `AgentExecutor` 的黑盒调用过程。

下面是 LangGraph 的关键特性：

* **循环和分支（Cycles and Branching）**：支持在应用程序中实现循环和条件语句；
* **持久性（Persistence）**：自动保存每一步的执行状态，支持在任意点暂停和恢复，以实现错误恢复、人机协同、时间旅行等功能；
* **人机协同（Human-in-the-Loop）**：支持在行动执行前中断执行，允许人工介入批准或编辑；
* **流支持（Streaming Support）**：图中的每个节点都支持实时地流式输出；
* **与 LangChain 的集成（Integration with LangChain）**：LangGraph 与 LangChain 和 LangSmith 无缝集成，但并不强依赖于它们。

## 快速开始

我们从一个最简单的例子开始：

```
### 定义状态图

from langgraph.graph import StateGraph, MessagesState

graph_builder = StateGraph(MessagesState)

### 定义模型和 chatbot 节点

from langchain_openai import ChatOpenAI

llm = ChatOpenAI()

def chatbot(state: MessagesState):
    return {"messages": [llm.invoke(state["messages"])]}

### 构建和编译图

from langgraph.graph import END, START

graph_builder.add_node("chatbot", chatbot)
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)
graph = graph_builder.compile()

### 运行

from langchain_core.messages import HumanMessage

response = graph.invoke(
    {"messages": [HumanMessage(content="合肥今天天气怎么样？")]}
)
response["messages"][-1].pretty_print()
```

在这个例子中，我们使用 LangGraph 定义了一个只有一个节点的图：

![](./images/basic-chatbot.jpg)

### 基本概念

上面的示例非常简单，还称不上什么智能体，尽管如此，它却向我们展示了 LangGraph 中的几个重要概念：

* **图（Graph）** 是 LangGraph 中最为重要的概念，它将智能体的工作流程建模为图结构。大学《数据结构》课程学过，图由 **节点（Nodes）** 和 **边（Edges）** 构成，在 LangGraph 中也是如此，此外，LangGraph 中还增加了 **状态（State）** 这个概念；
* **状态（State）** 表示整个图运行过程中的状态数据，可以理解为应用程序当前快照，为图中所有节点所共享，它可以是任何 Python 类型，但通常是 `TypedDict` 类型或者 Pydantic 的 `BaseModel` 类型；
* **节点（Nodes）** 表示智能体的具体执行逻辑，它接收当前的状态作为输入，执行某些计算，并返回更新后的状态；节点不一定非得是调用大模型，可以是任意的 Python 函数；
* **边（Edges）** 表示某个节点执行后，接下来要执行哪个节点；边的定义可以是固定的，也可以是带条件的；如果是条件边，我们还需要定义一个 **路由函数（Routing function）**，根据当前的状态来确定接下来要执行哪个节点。

通过组合节点和边，我们可以创建复杂的循环工作流，随着节点的执行，不断更新状态。简而言之：*节点用于执行动作，边用于指示下一步动作*。

LangGraph 的实现采用了 [消息传递（Message passing）](https://en.wikipedia.org/wiki/Message_passing) 的机制。其灵感源自 Google 的 [Pregel](https://research.google/pubs/pub37252/) 和 Apache 的 [Beam](https://beam.apache.org/) 系统，当一个节点完成其操作后，它会沿着一条或多条边向其他节点发送消息。这些接收节点随后执行其功能，将生成的消息传递给下一组节点，如此循环往复。

### 代码详解

了解这些基本概念后，再回过头来看下上面的代码，脉络就很清楚了。

首先我们通过 `StateGraph` 定义了状态图：

```
graph_builder = StateGraph(MessagesState)
```

它接受状态的 Schema 作为构造参数，在这里直接使用了内置的 `MessagesState` 类，它的定义如下：

```
class MessagesState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]
```

`MessagesState` 很简单，仅包含一个 LangChain 格式的消息列表，一般在构造聊天机器人或示例代码时使用，在正式环境中用的并不多，因为大多数应用程序需要的状态比消息列表更为复杂。

后面的 `add_messages` 被称为 **规约函数（Reducers）**，表示当节点执行后状态如何更新。当没有定义规约函数时，默认是覆盖的逻辑，比如下面这样的状态 Schema：

```
from typing import TypedDict

class State(TypedDict):
    foo: int
    bar: list[str]
```

假设图的输入为 `{"foo": 1, "bar": ["hi"]}`，接着假设第一个节点返回 `{"foo": 2}`，这时状态被更新为 `{"foo": 2, "bar": ["hi"]}`，注意，节点无需返回整个状态对象，只有返回的字段会被更新，再接着假设第二个节点返回 `{"bar": ["bye"]}`，这时状态将变为 `{"foo": 2, "bar": ["bye"]}`。

当定义了规约函数，更新逻辑就不一样了，比如对上面的状态 Schema 稍作修改：

```
from typing import TypedDict, Annotated
from operator import add

class State(TypedDict):
    foo: int
    bar: Annotated[list[str], add]
```

仍然假设图的输入为 `{"foo": 1, "bar": ["hi"]}`，接着假设第一个节点返回 `{"foo": 2}`，这时状态被更新为 `{"foo": 2, "bar": ["hi"]}`，再接着假设第二个节点返回 `{"bar": ["bye"]}`，这时状态将变为 `{"foo": 2, "bar": ["hi", "bye"]}`。

定义了图之后，我们接下来就要定义节点，这里我们只定义了一个 `chatbot` 节点：

```
def chatbot(state: MessagesState):
    return {"messages": [llm.invoke(state["messages"])]}
```

节点就是普通的 Python 函数，在这里调用大模型得到回复，也可以是任意其他的逻辑，函数的入参就是上面所定义的状态对象，我们可以从状态中取出最新的值，函数的出参也是状态对象，节点执行后，根据规约函数，返回值会被更新到状态中。

定义节点后，我们就可以使用 `add_node` 方法将其添加到图中：

```
graph_builder.add_node("chatbot", chatbot)
```

然后再使用 `add_edge` 方法添加两条边，一条边从 `START` 节点到 `chatbot` 节点，一个边从 `chatbot` 节点到 `END` 结束：

```
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)
```

`START` 和 `END` 是两个特殊节点，`START` 表示开始节点，接受用户的输入，是整个图的入口，`END` 表示结束节点，执行到它之后就没有后续动作了。

值得注意的是，这里构建图的接口形式借鉴了 [NetworkX](https://networkx.org/documentation/latest/) 的设计理念。整个图构建好后，我们还需要调用 `compile` 方法编译图：

```
graph = graph_builder.compile()
```

只有编译后的图才能使用。编译是一个相当简单的步骤，它会对图的结构进行一些基本检查，比如无孤立节点等，也可以在编译时设置一些运行时参数，比如检查点、断点等。

编译后的图是一个 `Runnable` 对象，所以我们可以使用 `invoke/ainvoke` 来调用它：

```
response = graph.invoke(
    {"messages": [HumanMessage(content="合肥今天天气怎么样？")]}
)
response["messages"][-1].pretty_print()
```

也可以使用 `stream/astream` 来调用它：

```
for event in graph.stream({"messages": ("user", "合肥今天天气怎么样？")}):
    for value in event.values():
        value["messages"][-1].pretty_print()
```

输出结果如下：

```
================================== Ai Message ==================================

对不起，我无法提供实时天气信息。您可以通过天气预报应用程序或网站来获取合肥今天的天气情况。
```

## 工具调用

可以看到，现在这个程序只是对大模型进行了一层包装，还谈不上是智能体。Lilian Weng 在 [LLM Powered Autonomous Agents](https://lilianweng.github.io/posts/2023-06-23-agent/) 这篇博客中总结到，智能体至少要包含三个核心组件：**规划（Planning）**、**记忆（Memory）** 和 **工具使用（Tool use）**。

![](./images/agent-overview.png)

其中，规划和记忆好比人的大脑，可以储存历史知识，对问题进行分析思考，现在的大模型都或多或少具备这样的能力；工具使用好比人的五官和手脚，可以感知世界，与外部源（例如知识库或环境）进行交互，以获取额外信息，并执行动作。工具的使用是人类区别于其他动物的重要特征，也是智能体区别于其他应用程序的重要特征。

这一节我们将对上面的 LangGraph 示例做些修改，使其具备工具调用的能力。首先，我们定义一个天气查询的工具：

```
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
```

这里使用了 LangChain 的 `@tool` 注解将一个方法定义成工具，并使用了 `pydantic` 对工具的参数做一些说明，在 [这篇博客](../week044-llm-application-frameworks-langchain-2/README.md) 中我还介绍了一些其他定义工具的方法，也可以使用。

接下来，和之前的示例一样，我们仍然需要定义一个状态图：

```
### 定义状态图

from langgraph.graph import StateGraph, MessagesState

graph_builder = StateGraph(MessagesState)
```

再接下来定义节点：

```
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
```

这和之前的示例有两点区别：

1. 多了一个 `tools` 节点，我们使用 LangGraph 内置的 `ToolNode` 来定义，一个工具节点中可以包含多个工具方法；
2. 在 `chatbot 节点` 中，我们的大模型需要绑定这些工具，通过 `llm.bind_tools()` 实现；

再接下来，将节点添加到图中，并在节点和节点之间连上线：

```
### 构建和编译图

from langgraph.graph import END, START
from langgraph.prebuilt import tools_condition

graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("tools", tool_node)
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("tools", 'chatbot')
graph_builder.add_conditional_edges("chatbot", tools_condition)
graph = graph_builder.compile()
```

构建出的图如下所示：

![](./images/tools-chatbot.jpg)

可以看到这里有两条比较特别的连线，是虚线，这被称为 **条件边（Conditional Edges）**，LangGraph 通过调用某个函数来确定下一步将执行哪个节点，这里使用了内置的 `tools_condition` 函数，当大模型返回 `tool_calls` 时执行 `tools` 节点，否则则执行 `END` 节点。

此时，一个简单的智能体就构建好了，我们再次运行之：

```
### 运行

for event in graph.stream({"messages": ("user", "合肥今天天气怎么样？")}):
    for value in event.values():
        value["messages"][-1].pretty_print()
```

运行结果如下：

```
================================== Ai Message ==================================
Tool Calls:
  get_weather (call_Jjp7SNIQkJWpLUdTL4uL1h1O)
 Call ID: call_Jjp7SNIQkJWpLUdTL4uL1h1O
  Args:
    city: 合肥
    date: 今天
================================= Tool Message =================================
Name: get_weather

今天晴天，气温30度。
================================== Ai Message ==================================

合肥今天是晴天，气温30度。
```

完整的代码 [参考这里](./demo/quickstart/tools.py)。

### 深入 Tool Call 的原理

从上面的运行结果中可以看出，用户消息首先进入 `chatbot` 节点，也就是调用大模型，大模型返回 `tool_calls` 响应，因此进入 `tools` 节点，接着调用我们定义的 `get_weather` 函数，得到合肥的天气，然后再次进入 `chatbot` 节点，将函数结果送给大模型，最后大模型就可以回答出用户的问题了。

这个调用的流程图如下：

![](./images/tool-calling-flow.png)

[OpenAI 官方文档](https://platform.openai.com/docs/guides/function-calling) 中有一张更详细的流程图：

![](./images/function-calling-diagram.png)

其中要注意的是，第二次调用大模型时，可能仍然会返回 `tool_calls` 响应，这时可以循环处理。

为了更好的理解 LangGraph 是如何调用工具的，我们不妨深入接口层面一探究竟。总的来说，LangGraph [利用大模型的 Tool Call 功能](https://python.langchain.com/v0.2/docs/how_to/tool_calling/)，实现动态的选择工具，提取工具参数，执行工具函数，并根据工具运行结果回答用户问题。

有很多大模型具备 Tool Call 功能，比如 OpenAI、Anthropic、Gemini、Mistral AI 等，我们可以通过 `llm.bind_tools(tools)` 给大模型绑定可用的工具，实际上，绑定工具就是在请求大模型的时候，在入参中多加一个 `tools` 字段：

```
{
    "model": "gpt-4",
    "messages": [
        {
            "role": "user",
            "content": "合肥今天天气怎么样？"
        }
    ],
    "stream": false,
    "n": 1,
    "temperature": 0.7,
    "tools": [
        {
            "type": "function",
            "function": {
                "name": "get_weather",
                "description": "查询天气",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "city": {
                            "type": "string",
                            "description": "城市名称，如合肥、北京、上海等"
                        },
                        "date": {
                            "type": "string",
                            "description": "日期，如今天、明天等"
                        }
                    },
                    "required": [
                        "city",
                        "date"
                    ]
                }
            }
        }
    ],
    "tool_choice": "auto"
}
```

这时大模型返回的结果类似于下面这样，也就是上面所说的 `tool_calls` 响应：

```
{
    "id": "chatcmpl-ABDVbXhhQLF8yN3xZV5FpW10vMQpP",
    "object": "chat.completion",
    "created": 1727236899,
    "model": "gpt-4-0613",
    "choices": [
        {
            "index": 0,
            "message": {
                "role": "assistant",
                "content": "",
                "tool_calls": [
                    {
                        "id": "call_aZaHgkaSmzq7kWX5f73h7nGg",
                        "type": "function",
                        "function": {
                            "name": "get_weather",
                            "arguments": "{\n  \"city\": \"合肥\",\n  \"date\": \"今天\"\n}"
                        }
                    }
                ]
            },
            "finish_reason": "tool_calls"
        }
    ],
    "usage": {
        "prompt_tokens": 91,
        "completion_tokens": 25,
        "total_tokens": 116
    },
    "system_fingerprint": ""
}
```

我们只需要判断大模型返回的结果中是否有 `tool_calls` 字段就能知道下一步是不是要调用工具，这其实就是 `tools_condition` 这个条件函数的逻辑：

```
def tools_condition(
    state: Union[list[AnyMessage], dict[str, Any]],
) -> Literal["tools", "__end__"]:

    if isinstance(state, list):
        ai_message = state[-1]
    elif messages := state.get("messages", []):
        ai_message = messages[-1]
    else:
        raise ValueError(f"No messages found in input state to tool_edge: {state}")
    if hasattr(ai_message, "tool_calls") and len(ai_message.tool_calls) > 0:
        return "tools"
    return "__end__"
```

`tools_condition` 函数判断 `messages` 中如果有 `tool_calls` 字段且不为空，则返回 `tools`，也就是工具节点，否则返回 `__end__` 也就是结束节点。

工具节点的执行，我们使用的是 LangGraph 内置的 `ToolNode` 类，它的实现比较复杂，感兴趣的可以翻看下它的源码，但是大体流程可以用下面几行代码表示：

```
tools_by_name = {tool.name: tool for tool in tools}
def tool_node(state: dict):
    result = []
    for tool_call in state["messages"][-1].tool_calls:
        tool = tools_by_name[tool_call["function"]["name"]]
        observation = tool.invoke(tool_call["function"]["arguments"])
        result.append(ToolMessage(content=observation, tool_call_id=tool_call["id"]))
    return {"messages": result}
```

工具节点遍历 `tool_calls` 数组，根据大模型返回的函数名 `name` 和函数参数 `arguments` 依次调用工具，并将工具结果以 `ToolMessage` 形式附加到 `messages` 中。这样再次进入 `chatbot` 节点时，向大模型发起的请求就如下所示（多了一个角色为 `tool` 的消息）：

```
{
    "model": "gpt-4",
    "messages": [
        {
            "role": "user",
            "content": "合肥今天天气怎么样？"
        },
        {
            "role": "assistant",
            "content": "",
            "tool_calls": [
                { 
                    "id": "call_aZaHgkaSmzq7kWX5f73h7nGg",
                    "type": "function",
                    "function": {
                        "name": "get_weather",
                        "arguments": "{\n  \"city\": \"合肥\",\n  \"date\": \"今天\"\n}" 
                    }
                }
            ]
        },
        {
            "role": "tool",
            "content": "晴，27度",
            "tool_call_id": "call_aZaHgkaSmzq7kWX5f73h7nGg"
        }
    ],
    "stream": false,
    "n": 1,
    "temperature": 0.7,
    "tools": [
        ...
    ],
    "tool_choice": "auto"
}
```

大模型返回消息如下：

```
{
    "id": "chatcmpl-ABDeUc21mx3agWVPmIEHndJbMmYTP",
    "object": "chat.completion",
    "created": 1727237450,
    "model": "gpt-4-0613",
    "choices": [
        {
            "index": 0,
            "message": {
                "role": "assistant",
                "content": "合肥今天的天气是晴朗，气温为27度。"
            },
            "finish_reason": "stop"
        }
    ],
    "usage": {
        "prompt_tokens": 129,
        "completion_tokens": 24,
        "total_tokens": 153
    },
    "system_fingerprint": ""
}
```

此时 `messages` 中没有 `tool_calls` 字段，因此，进入 `END` 节点，这一轮的会话就结束了。

### 适配 Function Call 接口

经过上面的学习，我们知道，LangGraph 默认会使用大模型接口的 Tool Call 功能。Tool Call 是 OpenAI 推出 [Assistants API](https://platform.openai.com/docs/assistants/overview) 时引入的一种新特性，它相比于传统的 [Function Call](https://openai.com/blog/function-calling-and-other-api-updates) 来说，控制更灵活，比如支持一次返回多个函数，从而可以并发调用。

目前大多数大模型产商的接口都已经紧跟 OpenAI 的规范，推出了 Tool Call 功能，但是也有部分产商或开源模型只支持 Function Call，对于这些模型如何在 LangGraph 中适配呢？

Function Call 和 Tool Call 的区别在于，请求的参数中是 `functions` 而不是 `tools`，如下所示：

```
{
    "messages": [
        {
            "role": "user",
            "content": "合肥今天天气怎么样？"
        }
    ],
    "model": "gpt-4",
    "stream": false,
    "n": 1,
    "temperature": 0.7,
    "functions": [
        {
            "name": "get_weather",
            "description": "查询天气",
            "parameters": {
                "properties": {
                    "city": {
                        "description": "城市名称，如合肥、北京、上海等",
                        "type": "string"
                    },
                    "date": {
                        "description": "日期，如今天、明天等",
                        "type": "string"
                    }
                },
                "required": [
                    "city",
                    "date"
                ],
                "type": "object"
            }
        }
    ]
}
```

LangChain 提供了 `llm.bind_functions(tools)` 方法来给大模型绑定可用的工具，这里的工具定义和 `llm.bind_tools(tools)` 是一模一样的：

```
### 定义模型和 chatbot 节点

from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4")
llm = llm.bind_functions(tools)

def chatbot(state: MessagesState):
    return {"messages": [llm.invoke(state["messages"])]}
```

大模型返回结果如下，`messages` 中会包含 `function_call` 字段而不是 `tool_calls`：

```
{
    "id": "chatcmpl-ACcnVWbuWbyxuO0eWqQrKBE0dB921",
    "object": "chat.completion",
    "created": 1727572437,
    "model": "gpt-4-0613",
    "choices": [
        {
            "index": 0,
            "message": {
                "role": "assistant",
                "content": "",
                "function_call": {
                    "name": "get_weather",
                    "arguments": "{\"city\":\"合肥\",\"date\":\"今天\"}"
                }
            },
            "finish_reason": "function_call"
        }
    ],
    "usage": {
        "prompt_tokens": 91,
        "completion_tokens": 21,
        "total_tokens": 112
    },
    "system_fingerprint": "fp_5b26d85e12"
}
```

因此我们条件边的判断函数就不能以 `tool_calls` 来作为判断依据了，我们对其稍加修改：

```
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
```

> 注意 LangChain 将 `function_call` 放在消息的额外字段 `additional_kwargs` 里。

最后是工具节点的实现，上面我们使用的是 LangGraph 内置的 `ToolNode` 类，它的实现比较复杂，要考虑工具的异步执行和并发执行等情况，我们不用实现和它完全一样的功能。最简单的做法是自定义一个 `BasicToolNode` 类，并实现一个 `__call__` 方法：

```
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
```

我们从 `function_call` 字段中提取出工具名称 `name` 和工具参数 `arguments`，然后调用相应的工具，最后最重要的一步是将工具调用结果包装成一个 `FunctionMessage` 并附加到 `messages` 中。当程序流程再次进入 `chatbot` 节点时，向大模型发起的请求就如下所示（多了一个角色为 `function` 的消息）：

```
{
    "messages": [
        {
            "role": "user",
            "content": "合肥今天天气怎么样？"
        },
        {
            "role": "assistant",
            "content": "",
            "function_call": {
                "name": "get_weather",
                "arguments": "{\"city\":\"合肥\",\"date\":\"今天\"}"
            }
        },
        {
            "role": "function",
            "content": "晴，27度",
            "name": "get_weather"
        }
    ],
    "model": "gpt-4",
    "stream": false,
    "n": 1,
    "temperature": 0.7,
    "functions": [
        ...
    ]
}
```

至此，我们就通过 Function Call 实现了 LangGraph 的调用逻辑，完整的代码 [参考这里](./demo/quickstart/functions.py)。

可以看出其中有三步是关键：

1. 给大模型绑定工具，可以通过 `llm.bind_tools()` 或 `llm.bind_functions()` 实现，对于不支持 Function Call 的模型，甚至可以通过自定义 Prompt 来实现；
2. 解析大模型的返回结果，根据返回的结果中是否有 `tool_calls` 或 `function_call` 字段，判断是否需要使用工具；
3. 根据大模型的返回结果，调用一个或多个工具方法。

## 记忆

## 高级特性

### Part 4: Human-in-the-loop

### Part 5: Manually Updating the State

### Part 6: Customizing State

### Part 7: Time Travel

## 参考

* [LangGraph Quick Start](https://langchain-ai.github.io/langgraph/tutorials/introduction/)
* [LangGraph How-to Guides](https://langchain-ai.github.io/langgraph/how-tos/)
* [LangGraph Conceptual Guides](https://langchain-ai.github.io/langgraph/concepts/)
* [LangGraph Examples](https://github.com/langchain-ai/langgraph/tree/main/examples)

### LangGraph Blogs

* [LangGraph](https://blog.langchain.dev/langgraph/)
* [LangGraph for Code Generation](https://blog.langchain.dev/code-execution-with-langgraph/)
* [LangGraph: Multi-Agent Workflows](https://blog.langchain.dev/langgraph-multi-agent-workflows/)
* [Announcing LangGraph v0.1 & LangGraph Cloud: Running agents at scale, reliably](https://blog.langchain.dev/langgraph-cloud/)
* [LangGraph v0.2: Increased customization with new checkpointer libraries](https://blog.langchain.dev/langgraph-v0-2/)
* [Jockey: A Conversational Video Agent Powered by Twelve Labs APIs and LangGraph](https://blog.langchain.dev/jockey-twelvelabs-langgraph/)
* [LangGraph Studio: The first agent IDE](https://blog.langchain.dev/langgraph-studio-the-first-agent-ide/)
* [Reflection Agents](https://blog.langchain.dev/reflection-agents/)
* [Plan-and-Execute Agents](https://blog.langchain.dev/planning-agents/)

### Cobus Greyling

* [LangChain Just Launched LangGraph Cloud](https://cobusgreyling.medium.com/langchain-just-launched-langgraph-cloud-bf8f65e45a54)
* [LangGraph Cloud](https://cobusgreyling.medium.com/langgraph-cloud-add1ddc25cf1)
* [LangGraph Studio From LangChain](https://cobusgreyling.medium.com/langgraph-studio-from-langchain-4242d58b4bf4)
* [LangGraph From LangChain Explained In Simple Terms](https://cobusgreyling.medium.com/langgraph-from-langchain-explained-in-simple-terms-f7cd0c12cdbf)
* [LangGraph Introduced SubGraphs](https://cobusgreyling.medium.com/langgraph-introduced-subgraphs-127424fcd182)
* [LangSmith, LangGraph Cloud & LangGraph Studio](https://cobusgreyling.medium.com/langsmith-langgraph-cloud-langgraph-studio-99631dae1be8)
* [LangGraph Agents By LangChain](https://cobusgreyling.medium.com/langgraph-agents-by-langchain-c1f6ebd86c38)
* [Flows Are So Back](https://cobusgreyling.medium.com/flows-are-so-back-5a4d0ee95661)

### 中文资料

* [使用LangChain来实现大模型agent](https://it.deepinmind.com/llm/2024/04/08/intro-to-llm-agents-with-langchain-when-rag-is-not-enough.html)
* [彻底搞懂LangGraph：构建强大的Multi-Agent多智能体应用的LangChain新利器 【1】](https://mp.weixin.qq.com/s/MzLz4lJF0WMsWrThiOWPog)
* [使用LangChain、LangGraph和LangSmith来创建AI Agent](http://www.mfbz.cn/a/493480.html)
* [Code Interpreter: 使用PandoraBox和LangGraph构建的Agent](https://lengm.cn/post/20240625_code_interpreter_langgraph/)
* [使用LangGraph实现时光旅行](https://www.1goto.ai/article/9bf3c614-5efc-41b1-8961-c267240b5eea)
* [AI Agent 终结者 LangGraph！](https://www.nowcoder.com/discuss/651573869014233088)
* [LangGraph | 新手入门](https://mp.weixin.qq.com/s/R4tvoOY3AFNHypvVoOKMsQ)
* [彻底搞懂LangGraph【1】：构建复杂智能体应用的LangChain新利器](https://blog.csdn.net/juan9872/article/details/137658555)
* [LangGraph实战](https://www.cnblogs.com/smartloli/p/18276355)
* [LangGraph介绍](https://theguodong.com/articles/LangChain/LangGraph%E4%BB%8B%E7%BB%8D/)
* [LangChain补充五：Agent之LangGraph的使用](https://www.cnblogs.com/ssyfj/p/18308248)
* [使用 LangGraph 构建可靠的 RAG 代理](https://blog.csdn.net/wjjc1017/article/details/138518087)

## 更多

### LangGraph 应用场景

官网文档提供了很多 LangGraph 的应用场景，包括 聊天机器人、RAG、智能体架构、评估分析等。

#### Chatbots

* [Build a Customer Support Bot](https://langchain-ai.github.io/langgraph/tutorials/customer-support/customer-support/)
* [Prompt Generation from User Requirements](https://langchain-ai.github.io/langgraph/tutorials/chatbots/information-gather-prompting/)
* [Code generation with RAG and self-correction](https://langchain-ai.github.io/langgraph/tutorials/code_assistant/langgraph_code_assistant/)

#### RAG

* [Adaptive RAG](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_adaptive_rag/)
* [Adaptive RAG using local LLMs](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_adaptive_rag_local/)
* [Agentic RAG](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/)
* [Corrective RAG (CRAG)](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_crag/)
* [Corrective RAG (CRAG) using local LLMs](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_crag_local/)
* [Self-RAG](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_self_rag/)
* [Self RAG using local LLMs](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_self_rag_local/)
* [An agent for interacting with a SQL database](https://langchain-ai.github.io/langgraph/tutorials/sql-agent/)

#### Agent Architectures

##### Multi-Agent Systems

* [Basic Multi-agent Collaboration](https://langchain-ai.github.io/langgraph/tutorials/multi_agent/multi-agent-collaboration/)
* [Supervision](https://langchain-ai.github.io/langgraph/tutorials/multi_agent/agent_supervisor/)
* [Hierarchical Teams](https://langchain-ai.github.io/langgraph/tutorials/multi_agent/hierarchical_agent_teams/)

##### Planning Agents

* [Plan-and-Execute](https://langchain-ai.github.io/langgraph/tutorials/plan-and-execute/plan-and-execute/)
* [Reasoning without Observation](https://langchain-ai.github.io/langgraph/tutorials/rewoo/rewoo/)
* [LLMCompiler](https://langchain-ai.github.io/langgraph/tutorials/llm-compiler/LLMCompiler/)

##### Reflection & Critique

* [Reflection](https://langchain-ai.github.io/langgraph/tutorials/reflection/reflection/)
* [Reflexion](https://langchain-ai.github.io/langgraph/tutorials/reflexion/reflexion/)
* [Language Agent Tree Search](https://langchain-ai.github.io/langgraph/tutorials/lats/lats/)
* [Self-Discover Agent](https://langchain-ai.github.io/langgraph/tutorials/self-discover/self-discover/)

#### Evaluation & Analysis

* [Chat Bot Evaluation as Multi-agent Simulation](https://langchain-ai.github.io/langgraph/tutorials/chatbot-simulation-evaluation/agent-simulation-evaluation/)
* [Chat Bot Benchmarking using Simulation](https://langchain-ai.github.io/langgraph/tutorials/chatbot-simulation-evaluation/langsmith-agent-simulation-evaluation/)

#### Experimental

* [Web Research (STORM)](https://langchain-ai.github.io/langgraph/tutorials/storm/storm/)
* [TNT-LLM: Text Mining at Scale](https://langchain-ai.github.io/langgraph/tutorials/tnt-llm/tnt-llm/)
* [Web Navigation](https://langchain-ai.github.io/langgraph/tutorials/web-navigation/web_voyager/)
* [Competitive Programming](https://langchain-ai.github.io/langgraph/tutorials/usaco/usaco/)
* [Complex data extraction with function calling](https://langchain-ai.github.io/langgraph/tutorials/extraction/retries/)
