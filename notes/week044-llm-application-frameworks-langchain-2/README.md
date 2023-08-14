# WEEK044 - 大模型应用开发框架 LangChain 学习笔记（二）

### LangChain Agent 入门

我们知道，大模型虽然擅长推理，但是却不擅长算术和计数，比如问它单词 `hello` 是由几个字母组成的，它就有可能胡编乱造，我们可以自定义一个函数 `get_word_length()` 帮助大模型来回答关于单词长度的问题：

```
from langchain.chat_models import ChatOpenAI
from langchain.agents import tool
from langchain.schema import SystemMessage
from langchain.agents import OpenAIFunctionsAgent
from langchain.agents import AgentExecutor

# llm
llm = ChatOpenAI(temperature=0)

# tools
@tool
def get_word_length(word: str) -> int:
    """Returns the length of a word."""
    return len(word)

tools = [get_word_length]

# prompt
system_message = SystemMessage(
    content="You are very powerful assistant, but bad at calculating lengths of words."
)
prompt = OpenAIFunctionsAgent.create_prompt(system_message=system_message)

# create an agent
agent = OpenAIFunctionsAgent(llm=llm, tools=tools, prompt=prompt)

# create an agent executor
agent_executor = AgentExecutor(agent=agent, tools=tools)

# run the agent executor
result = agent_executor.run("how many letters in the word 'hello'?")
print(result)
```

这是 LangChain 官方文档中关于 Agent 的一个入门示例，从上面的代码中我们可以注意到 Agent 有这么几个重要的概念：

* Tools - 希望被 Agent 执行的函数，被称为工具，我们需要尽可能地描述清楚每个工具的功能，以便 Agent 能选择合适的工具；官方 [内置了一些常用的工具](https://python.langchain.com/docs/modules/agents/tools/)，我们可以直接使用 `load_tools()` 来加载；

* Agent - 经常被翻译成 **代理**，可以帮我们将用户的问题拆解成多个子任务，然后动态地选择和调用 Chain 或工具依次解决这些子任务，直到用户的问题完全被解决；根据所使用的策略，可以将 Agent [划分成不同的类型](https://python.langchain.com/docs/modules/agents/agent_types/)；Agent 的执行流程如下图所示：

![](./images/agent.png)

* Agent Executor - Agent 执行器，它本质上是一个 Chain，所以可以和其他的 Chain 或 Agent Executor 进行组合；它会递归地调用 Agent 获取下一步的动作，并执行 Agent 中定义的工具，直到 Agent 认为问题已经解决，则递归结束，下面是整个过程的伪代码：

```
next_action = agent.get_action(...)
while next_action != AgentFinish:
    observation = run(next_action)
    next_action = agent.get_action(..., next_action, observation)
return next_action
```

### LangChain Agent 进阶

https://python.langchain.com/docs/modules/agents/agent_types/

## 参考

* [LangChain 完整指南：使用大语言模型构建强大的应用程序](https://zhuanlan.zhihu.com/p/620529542)
* [LangChain 中文入门教程](https://github.com/liaokongVFX/LangChain-Chinese-Getting-Started-Guide)
* [LangChain初学者入门指南](https://mp.weixin.qq.com/s/F4QokLPrimFS1LRjXDbwQQ)
* [LangChain：Model as a Service粘合剂，被ChatGPT插件干掉了吗？](https://36kr.com/p/2203231346847113)

### AI Agents

* [Auto-GPT](https://github.com/Significant-Gravitas/Auto-GPT)
* [AgentGPT](https://github.com/reworkd/AgentGPT)
* [BabyAGI](https://github.com/yoheinakajima/babyagi)
* [SuperAGI](https://github.com/TransformerOptimus/SuperAGI)
* [Haystack](https://github.com/deepset-ai/haystack)
* [Open-Assistant](https://github.com/LAION-AI/Open-Assistant)
* [BentoML](https://github.com/bentoml/BentoML)
