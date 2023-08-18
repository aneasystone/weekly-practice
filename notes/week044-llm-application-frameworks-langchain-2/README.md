# WEEK044 - 大模型应用开发框架 LangChain 学习笔记（二）

在 [上一篇笔记](../week043-llm-application-frameworks-langchain/README.md) 中，我们学习了 LangChain 中的一些基础概念：使用 `LLMs` 和 `ChatModels` 实现基本的聊天功能，使用 `PromptTemplate` 组装提示语，使用 `Document loaders`、`Document transformers`、`Text embedding models`、`Vector stores` 和 `Retrievers` 实现文档问答；然后，我们又学习了 LangChain 的精髓 Chain，以及 Chain 的三大特性：使用 `Memory` 实现 Chain 的记忆功能，使用 `RetrievalQA` 组合多个 Chain 再次实现文档问答，使用 `Callbacks` 对 Chain 进行调试；最后，我们学习了四个基础 Chain：`LLMChain`、`TransformChain`、`SequentialChain` 和 `RouterChain`，使用这四个 Chain 可以组装出更复杂的流程，其中 `RouterChain` 和 `MultiPromptChain` 为我们提出了一种新的思路，使用大模型来决策 Chain 的调用链路，可以动态地解决用户问题；更进一步我们想到，大模型不仅可以动态地选择调用 Chain，也可以动态地选择调用外部的函数，而且使用一些提示语技巧，可以让大模型变成一个推理引擎，这便是 [Agents](https://python.langchain.com/docs/modules/agents/)。

## OpenAI 的插件功能

在学习 LangChain 的 Agents 之前，我们先来学习一下 OpenAI 的插件功能，这可以让我们对 Agents 的基本概念和工作原理有一个更深入的了解。

### ChatGPT Plugins

2023 年 3 月 23 日，OpenAI 重磅推出 [ChatGPT Plugins](https://openai.com/blog/chatgpt-plugins) 功能，引起了全球用户的热议。众所周知，GPT-3.5 是使用 2021 年之前的历史数据训练出来的大模型，所以它无法回答关于最新新闻和事件的问题，比如你问它今天是星期几，它只能让你自己去查日历：

![](./images/day-of-the-week.png)

不仅如此，ChatGPT 在处理数学问题时也表现不佳，而且在回答问题时可能会捏造事实，胡说八道；另一方面，虽然 ChatGPT 非常强大，但它终究只是一个聊天机器，如果要让它成为真正的私人助理，它还得帮助用户去做一些事情，解放用户的双手。引入插件功能后，就使得 ChatGPT 具备了这两个重要的能力：

* 访问互联网：可以实时检索最新的信息以回答用户问题，比如调用搜索引擎接口，获取和用户问题相关的新闻和事件；也可以访问用户的私有数据，比如公司内部的文档，个人笔记等，这样通过插件也可以实现文档问答；
* 执行任务：可以了解用户的意图，代替用户去执行任务，比如调用一些三方服务的接口订机票订酒店等；

暂时只有 GPT-4 才支持插件功能，所以要体验插件功能得有个 ChatGPT Plus 账号。截止目前为止，OpenAI 的插件市场中已经开放了近千个插件，如果我们想让 ChatGPT 回答今天是星期几，可以开启其中的 Wolfram 插件：

![](./images/chatgpt-4-plugins.png)

[Wolfram|Alpha](https://www.wolframalpha.com/) 是一个神奇的网站，建立于 2009 年，它是一个智能搜索引擎，它上知天文下知地理，可以回答关于数学、物理、化学、生命科学、计算机科学、历史、地理、音乐、文化、天气、时间等等方面的问题，它的愿景是 `Making the world's knowledge computable`，让世界的知识皆可计算。Wolfram 插件就是通过调用 Wolfram|Alpha 的接口来实现的，开启 Wolfram 插件后，ChatGPT 就能准确回答我们的问题了：

![](./images/day-of-the-week-with-plugins.png)

从对话的结果中可以看到 ChatGPT 使用了 Wolfram 插件，展开插件的调用详情还可以看到调用的请求和响应：

![](./images/wolfram-detail.png)

#### 开发自己的插件

目前 ChatGPT 的插件功能仍然处于 beta 版本，OpenAI 还没有完全开放插件的开发功能，如果想要体验开发 ChatGPT 插件的流程，需要先 [加入等待列表](https://openai.com/waitlist/plugins)。

开发插件的步骤大致如下：

1. ChatGPT 插件其实就是标准的 Web 服务，可以使用任意的编程语言开发，开发好插件服务之后，将其部署到你的域名下；
2. 准备一个清单文件 `.well-known/ai-plugin.json` 放在你的域名下，清单文件中包含了插件的名称、描述、认证信息、以及所有插件接口的信息等；
3. 在 ChatGPT 的插件中心选择 `Develop your own plugin`，并填上你的插件地址；
4. 开启新会话时，先选择并激活你的插件，然后就可以聊天了；如果 ChatGPT 认为用户问题需要调用你的插件（取决于插件和接口的描述），就会调用你在插件中定义的接口；

其中前两步应该是开发者最为关心的部分，官网提供了一个入门示例供我们参考，这个示例是一个简单的 [TODO List 插件](https://github.com/openai/plugins-quickstart)，可以让 ChatGPT 访问并操作我们的 TODO List 服务，我们就以这个例子来学习如何开发一个 ChatGPT 插件。

首先我们使用 Python 语言开发好 TODO List 服务，支持 TODO List 的增删改查。

然后准备一个插件的清单文件，对我们的插件进行一番描述，这个清单文件的名字必须是 `ai-plugin.json`，并放在你的域名的 `.well-known` 路径下，比如 `https://your-domain.com/.well-known/ai-plugin.json`。文件的内容如下：

```
{
    "schema_version": "v1",
    "name_for_human": "TODO List",
    "name_for_model": "todo",
    "description_for_human": "Manage your TODO list. You can add, remove and view your TODOs.",
    "description_for_model": "Help the user with managing a TODO list. You can add, remove and view your TODOs.",
    "auth": {
        "type": "none"
    },
    "api": {
        "type": "openapi",
        "url": "http://localhost:3333/openapi.yaml"
    },
    "logo_url": "http://localhost:3333/logo.png",
    "contact_email": "support@example.com",
    "legal_info_url": "http://www.example.com/legal"
}
```

清单中有些信息是用于展示在 OpenAI 的插件市场的，比如 `name_for_human`、`description_for_human`、`logo_url`、`contact_email`、`legal_info_url` 等，有些信息是要送给 ChatGPT 的，比如 `name_for_model`、`description_for_model`、`api` 等；送给 ChatGPT 的信息需要仔细填写，确保 ChatGPT 能理解你这个插件的用途，这样 ChatGPT 才会在对话过程中根据需要调用你的插件。

然后我们还需要准备插件的接口定义文件，要让 ChatGPT 知道你的插件都有哪些接口，每个接口的作用是什么，以及每个接口的入参和出参是什么。一般使用 [OpenAPI 规范](https://swagger.io/specification/) 来定义插件的接口，下面是一个简单的示例，定义了一个 `getTodos` 接口用于获取所有的 TODO List：

```
openapi: 3.0.1
info:
  title: TODO Plugin
  description: A plugin that allows the user to create and manage a TODO list using ChatGPT.
  version: 'v1'
servers:
  - url: http://localhost:3333
paths:
  /todos:
    get:
      operationId: getTodos
      summary: Get the list of todos
      responses:
        "200":
          description: OK
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/getTodosResponse'
components:
  schemas:
    getTodosResponse:
      type: object
      properties:
        todos:
          type: array
          items:
            type: string
          description: The list of todos.
```

一切准备就绪后，就可以在 ChatGPT 的插件中心填上你的插件地址并调试了。

除了入门示例，官网还提供了一些其他的 [插件示例](https://platform.openai.com/docs/plugins/examples)，其中 [Chatgpt Retrieval Plugin](https://github.com/openai/chatgpt-retrieval-plugin/) 是一个完整而复杂的例子，对我们开发真实的插件非常有参考价值。

当然，还有很多插件的内容没有介绍，比如 [插件的最佳实践](https://platform.openai.com/docs/plugins/getting-started/best-practices)，[用户认证](https://platform.openai.com/docs/plugins/authentication) 等，更多信息可以参考 [OpenAI 的插件手册](https://platform.openai.com/docs/plugins/introduction)。

### Function Calling

https://zhuanlan.zhihu.com/p/618170820

https://zhuanlan.zhihu.com/p/636975719

6 月 13 日 OpenAI 在 Chat Completions API 中添加了新的函数调用（Function Calling）能力，帮助开发者通过 API 方式实现类似于 ChatGPT 插件的数据交互能力。

https://openai.com/blog/function-calling-and-other-api-updates

https://python.langchain.com/docs/modules/chains/how_to/openai_functions

https://juejin.cn/post/7247059220142948407

## LangChain Agent 入门

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

## LangChain Agent 进阶

https://python.langchain.com/docs/modules/agents/agent_types/

## 参考

* [70款ChatGPT插件评测：惊艳的开发过程与宏大的商业化愿景](https://zhuanlan.zhihu.com/p/629337429)
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
