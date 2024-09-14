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

运行结果如下：

```
================================== Ai Message ==================================

抱歉，我无法提供今天合肥的实时天气信息。你可以通过天气预报网站或者天气App查看当天的天气预报。
```

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

### 工具调用

### 记忆

## 高级特性

### Part 4: Human-in-the-loop

### Part 5: Manually Updating the State

### Part 6: Customizing State

### Part 7: Time Travel

## 参考

* [LangGraph Quick Start](https://langchain-ai.github.io/langgraph/tutorials/introduction/)
* [LangGraph How-to Guides](https://langchain-ai.github.io/langgraph/how-tos/)
* [LangGraph Conceptual Guides](https://langchain-ai.github.io/langgraph/concepts/)

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

### LangGraph Examples

* [Adaptive RAG Cohere Command R](https://github.com/langchain-ai/langgraph/blob/main/examples/rag/langgraph_adaptive_rag_cohere.ipynb)

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
