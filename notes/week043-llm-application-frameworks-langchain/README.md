# WEEK043 - 大模型应用开发框架 LangChain 学习笔记

一场关于大模型的战役正在全世界激烈地上演着，国内外的各大科技巨头和研究机构纷纷投入到这场战役中，光是写名字就能罗列出一大串，比如国外的有 OpenAI 的 [GPT-4](https://openai.com/gpt-4)，Meta 的 [LLaMa](https://github.com/facebookresearch/llama)，Stanford University 的 [Alpaca](https://github.com/tatsu-lab/stanford_alpaca)，Google 的 [LaMDA](https://blog.google/technology/ai/lamda/) 和 [PaLM 2](https://ai.google/discover/palm2/)，Anthropic 的 [Claude](https://www.anthropic.com/index/introducing-claude)，Databricks 的 [Dolly](https://github.com/databrickslabs/dolly)，国内的有百度的 [文心](https://wenxin.baidu.com/)，阿里的 [通义](https://tongyi.aliyun.com/)，科大讯飞的 [星火](https://xinghuo.xfyun.cn/)，华为的 [盘古](https://www.huaweicloud.com/product/pangu.html)，复旦大学的 [MOSS](https://github.com/OpenLMLab/MOSS)，智谱 AI 的 [ChatGLM](https://chatglm.cn/) 等等等等。

一时间大模型如百花齐放，百鸟争鸣，并在向各个行业领域渗透，让人感觉通用人工智能仿佛就在眼前。基于大模型开发的应用和产品也如雨后春笋，让人目不暇接，每天都有很多新奇的应用和产品问世，有的可以充当你的朋友配你聊天解闷，有的可以充当你的老师帮你学习答疑，有的可以帮你写文章编故事，有的可以帮你写代码改 BUG，大模型的崛起正影响着我们生活中的方方面面。

正是在这样的背景下，为了方便和统一基于大模型的应用开发，一批大模型应用开发框架横空出世，LangChain 就是其中最流行的一个。

## 快速开始

正如前文所述，[LangChain](https://github.com/hwchase17/langchain) 是一个基于大语言模型（LLM）的应用程序开发框架，它提供了一整套工具、组件和接口，简化了创建大模型应用程序的过程，方便开发者使用语言模型实现各种复杂的任务，比如聊天机器人、文档问答、各种基于 Prompt 的助手等。根据 [官网的介绍](https://docs.langchain.com/docs/)，它可以让你的应用变得 **Data-aware** 和 **Agentic**：

* **Data-aware**：也就是数据感知，可以将语言模型和其他来源的数据进行连接，比如让语言模型针对指定文档回答问题；
* **Agentic**：可以让语言模型和它所处的环境进行交互，实现类似代理机器人的功能，帮助用户完成指定任务；

LangChain 在 GitHub 上有着异乎寻常的热度，截止目前为止，星星数高达 55k，而且它的更新非常频繁，隔几天就会发一个新版本，有时甚至一天发好几个版本，所以学习的时候最好以官方文档为准，网络上有很多资料都过时了（包括我的这篇笔记）。

LangChain 提供了 [Python](https://python.langchain.com/docs) 和 [JavaScript](https://js.langchain.com/docs) 两个版本的 SDK，这里我主要使用 Python 版本的，在我写这篇笔记的时候，最新的版本为 [0.0.238](https://pypi.org/project/langchain/0.0.238/)，使用下面的命令安装：

```
$ pip install langchain==0.0.238
```

> 注意：Python 版本需要在 3.8.1 及以上，如果低于这个版本，只能安装 [langchain==0.0.27](https://pypi.org/project/langchain/0.0.27/)。

另外要注意的是，这个命令只会安装 LangChain 的基础包，这或许并没有什么用，因为 LangChain 最有价值的地方在于它能和各种各样的语言模型、数据存储、外部工具等进行交互，比如如果我们需要使用 OpenAI，则需要手动安装：

```
$ pip install openai
```

也可以在安装 LangChain 时指定安装可选依赖包：

```
$ pip install langchain[openai]==0.0.238
```

或者使用下面的命令一次性安装所有的可选依赖包（不过很多依赖可能会用不上）：

```
$ pip install langchain[all]==0.0.238
```

LangChain 支持的可选依赖包有：

```
llms = ["anthropic", "clarifai", "cohere", "openai", "openllm", "openlm", "nlpcloud", "huggingface_hub", "manifest-ml", "torch", "transformers"]
qdrant = ["qdrant-client"]
openai = ["openai", "tiktoken"]
text_helpers = ["chardet"]
clarifai = ["clarifai"]
cohere = ["cohere"]
docarray = ["docarray"]
embeddings = ["sentence-transformers"]
javascript = ["esprima"]
azure = [ ... ]
all = [ ... ]
```

可以在项目的 [pyproject.toml](https://github.com/hwchase17/langchain/blob/master/libs/langchain/pyproject.toml) 文件中查看依赖包详情。

### 入门示例

我们首先从一个简单的例子开始：

```
from langchain.llms import OpenAI

llm = OpenAI(temperature=0.9)
response = llm.predict("给水果店取一个名字")
print(response)

# 果舞时光
```

LangChain 集成了许多流行的语言模型，并提供了一套统一的接口方便开发者直接使用，比如在上面的例子中，我们引入了 OpenAI 这个 LLM，然后调用 `llm.predict()` 方法让语言模型完成后续内容的生成。如果用户想使用其他语言模型，只需要将上面的 OpenAI 换成其他的即可，比如流行的 Anthropic 的 [Claude 2](https://www.anthropic.com/index/claude-2)，或者 Google 的 [PaLM 2](https://ai.google/discover/palm2/) 等，[这里](https://github.com/langchain-ai/langchain/tree/master/libs/langchain/langchain/llms) 可以找到 LangChain 目前支持的所有语言模型接口。

回到上面的例子，`llm.predict()` 方法实际上调用的是 OpenAI 的 [Completions](https://platform.openai.com/docs/api-reference/completions) 接口，这个接口的作用是给定一个提示语，让 AI 生成后续内容；我们知道，除了 Completions，OpenAI 还提供了一个 [Chat](https://platform.openai.com/docs/api-reference/chat) 接口，也可以用于生成后续内容，而且比 Completions 更强大，可以给定一系列对话内容，让 AI 生成后续的回复，从而实现类似 ChatGPT 的聊天功能。

> 官方推荐使用 Chat 替换 Completions 接口，在后续的 OpenAI 版本中，Completions 接口可能会被弃用。

https://python.langchain.com/docs/get_started/quickstart.html

### 翻译助手

### 知识库助手

* [LangChain Python 文档](https://python.langchain.com/docs)

## LangChain vs. LlamaIndex

* [LlamaIndex](https://github.com/jerryjliu/llama_index)

## 基于 Agent 的应用开发

## 可视化

## 参考

* [LangChain 完整指南：使用大语言模型构建强大的应用程序](https://zhuanlan.zhihu.com/p/620529542)
* [LangChain 中文入门教程](https://github.com/liaokongVFX/LangChain-Chinese-Getting-Started-Guide)
* [LangChain初学者入门指南](https://mp.weixin.qq.com/s/F4QokLPrimFS1LRjXDbwQQ)
* [LangChain：Model as a Service粘合剂，被ChatGPT插件干掉了吗？](https://36kr.com/p/2203231346847113)

### LangChain 官方资料

* [LangChain GitHub](https://github.com/hwchase17/langchain)
* [LangChain 官方博客](https://blog.langchain.dev/)
* [LangChain 官方文档](https://docs.langchain.com/docs/)
* [LangChain Python 文档](https://python.langchain.com/docs)
* [LangChain JS/TS 文档](https://js.langchain.com/docs)

### LangChain 项目

* [hwchase17/chat-langchain](https://github.com/hwchase17/chat-langchain) - 基于文档的 QA 问答
* [hwchase17/notion-qa](https://github.com/hwchase17/notion-qa) - 基于 Notion 的 QA 问答
* [hwchase17/chat-your-data](https://github.com/hwchase17/chat-your-data)
* [imClumsyPanda/langchain-ChatGLM](https://github.com/imClumsyPanda/langchain-ChatGLM) - 基于本地知识库的 ChatGLM 等大语言模型应用实现

### LangChain 教程

* [gkamradt/langchain-tutorials](https://github.com/gkamradt/langchain-tutorials)
* [A Comprehensive Guide to LangChain](https://nathankjer.com/introduction-to-langchain/)
* [Build a GitHub Support Bot with GPT3, LangChain, and Python](https://dagster.io/blog/chatgpt-langchain)
* [LangChain and LlamaIndex Projects Lab Book: Hooking Large Language Models Up to the Real World](https://leanpub.com/langchain)
* [Re-implementing LangChain in 100 lines of code](https://blog.scottlogic.com/2023/05/04/langchain-mini.html)
* [LangChain + Vectara: better together](https://blog.langchain.dev/langchain-vectara-better-together/)

### LangChain 可视化

* [FlowiseAI/Flowise](https://github.com/FlowiseAI/Flowise) - Drag & drop UI to build your customized LLM flow using LangchainJS
* [logspace-ai/langflow](https://github.com/logspace-ai/langflow) - LangFlow is a UI for LangChain, designed with react-flow to provide an effortless way to experiment and prototype flows.
* [向量脉络 VectorVein](https://github.com/AndersonBY/vector-vein)
* [ChatFlow](https://github.com/prompt-engineering/chat-flow)

### LlamaIndex 参考资料

* [LlamaIndex](https://github.com/jerryjliu/llama_index)
* [面向QA系统的全新文档摘要索引](https://mp.weixin.qq.com/s/blDKylt4FyZfeSIV6M1d2g)
* [LlamaIndex：轻松构建索引查询本地文档的神器](https://blog.csdn.net/FrenzyTechAI/article/details/131336363)
* [后chatgpt时代的对话式文档问答解决方案](https://github.com/xinsblog/try-llama-index)

### 其他

* [Prem](https://github.com/premAI-io/prem-app/) - Self Sovereign AI Infrastructure
* [生成式AI的应用路线图](https://github.com/SeedV/generative-ai-roadmap)

### AI Agents

* [Auto-GPT](https://github.com/Significant-Gravitas/Auto-GPT)
* [AgentGPT](https://github.com/reworkd/AgentGPT)
* [BabyAGI](https://github.com/yoheinakajima/babyagi)
* [SuperAGI](https://github.com/TransformerOptimus/SuperAGI)
* [Haystack](https://github.com/deepset-ai/haystack)
* [Open-Assistant](https://github.com/LAION-AI/Open-Assistant)
* [BentoML](https://github.com/bentoml/BentoML)
