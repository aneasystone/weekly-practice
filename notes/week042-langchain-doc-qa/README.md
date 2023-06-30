# WEEK042 - 基于 LangChain 打造的本地知识库助手

基于不同的提示语，可以让 ChatGPT 实现各种不同的功能，比如在 [week040-chrome-extension-with-chatgpt](../week040-chrome-extension-with-chatgpt/README.md) 这篇文章中，我基于 ChatGPT 实现了一个翻译助手，OpenAI 官方的 [Examples 页面](https://platform.openai.com/examples) 也列出了提示语的更多示例，展示了 ChatGPT 在问答、翻译、文本总结、代码生成、推理等各方面的能力。

尽管 ChatGPT 的表现非常亮眼，但是它也有其局限性，由于它是基于互联网上公开的资料训练的，所以它只能回答公开领域的知识的问题，比如你问它是谁发明了空调，第一个登月的人是谁，它都能回答得头头是道，但是对于一些私有领域的知识，比如你问它张三家的宠物狗叫什么名字，它就鞭长莫及了。

## Fine tuning vs. Embedding

打造私有领域的知识库助手对于企业和个人来说是一个非常重要的应用场景，可以实现个性化定制化的问答效果，要实现这个功能，一般有两种不同的方式：[Fine tuning](https://platform.openai.com/docs/guides/fine-tuning) 和 [Embedding](https://platform.openai.com/docs/guides/embeddings)。Fine tuning 又被称为微调，它可以在不改动预训练模型的基础上，对特定任务进一步训练，以适应特定数据和要求。[OpenAI Cookbook](https://github.com/openai/openai-cookbook) 中有一个 [基于 Fine tuning 实现 QA 的例子](https://github.com/openai/openai-cookbook/blob/main/examples/fine-tuned_qa)，不过官方已经不推荐使用这种方式来做知识问答任务，因为 Fine tuning 更适合于学习新任务或新模式，而不是接受新信息，比如我们可以使用 Fine tuning 让模型按特定的语气或风格来回答问题，或者让模型按固定的格式来回答问题；相对应的，Embedding 更适合知识问答任务，我们可以使用语义搜索来快速找到相关的文档，然后将文档组合成固定的提示语，从而让模型来生成特定问题的答案。这种做法比 Fine tuning 速度更快，而且不需要训练，使用上也更灵活。

https://zhuanlan.zhihu.com/p/609359999

## 构建本地知识库

## 实现本地知识库助手

## 基于 LangChain 实现本地知识库助手

https://langchain-langchain.vercel.app/docs/get_started/introduction.html

## 参考

* [快速了解 OpenAI 的 fine-tune 和 Embedding 能力](https://zhuanlan.zhihu.com/p/609359047)
* [Question-answering-using-embeddings-based-search](https://github.com/openai/openai-cookbook/blob/main/examples/Question_answering_using_embeddings.ipynb)
* [推荐LangChain学习过程中的一些资料](https://mp.weixin.qq.com/s/4DjoDeneBWW0DrkUmRMD4w)
* [LangChain 的中文入门教程](https://github.com/liaokongVFX/LangChain-Chinese-Getting-Started-Guide)
* [LangChain and LlamaIndex Projects Lab Book: Hooking Large Language Models Up to the Real World](https://leanpub.com/langchain)
* [基于LangChain构建大语言模型“套壳”应用](https://developer.aliyun.com/article/1218421)
* [chat-langchain，一个优秀的本地文档QA问答](https://mp.weixin.qq.com/s/O67cECXmOXsXccLDcP4akg)
* [让 OpenAI 更 Open，在 ChatGPT 里自由接入数据源](https://soulteary.com/2023/05/19/make-openai-more-open-and-freely-access-data-sources-in-chatgpt.html)
* [10分钟打造基于ChatGPT的Markdown智能文档](https://mp.weixin.qq.com/s/JGwOg5BT2rgfhrBO9JBNOA)

## 更多

### 类似项目

* [Fast GPT](https://fastgpt.run/) - 三分钟搭建 AI 知识库
* [Quivr](https://github.com/StanGirard/quivr) - Your Second Brain, Empowered by Generative AI
* [Local Mind](https://github.com/nigulasikk/local-mind) - 一个本地文件问答应用
* [LlamaIndex：面向QA系统的全新文档摘要索引](https://mp.weixin.qq.com/s/blDKylt4FyZfeSIV6M1d2g)
* [pdf.ai](https://pdf.ai/) - Chat with any document
* [langchain-ChatGLM](https://github.com/imClumsyPanda/langchain-ChatGLM) - 基于本地知识库的 ChatGLM 等大语言模型应用实现
* [BabyAGI](https://github.com/yoheinakajima/babyagi)
* [WritingGPT: 基于ChatGPT和AutoGPT打造个人写作团队](https://mp.weixin.qq.com/s/RJC4pEIsmcebqGJw8AOQig)
* [DB-GPT](https://github.com/csunny/DB-GPT) - Revolutionizing Database Interactions with Private LLM Technology

### Embedding

* [Pinecone](https://www.pinecone.io/) - Long-term Memory for AI
* [向量数据库是如何工作的？](https://mp.weixin.qq.com/s/rwFkl4My9GQYOkJEWwk3bg)
* [矢量数据库和嵌入是当前人工智能领域的热门话题](https://twitter-thread.com/t/ZH/1655626066331938818)
* [浅谈 Semantic Search](https://mp.weixin.qq.com/s/ymlGAhS40ImoaAZviq5lZw)
* [Embedding技术在推荐场景实践](https://mp.weixin.qq.com/s/O26ibGHXxhYOMknleI7yrA)

### 可视化

* [FlowiseAI/Flowise](https://github.com/FlowiseAI/Flowise) - Drag & drop UI to build your customized LLM flow using LangchainJS
* [logspace-ai/langflow](https://github.com/logspace-ai/langflow) - LangFlow is a UI for LangChain, designed with react-flow to provide an effortless way to experiment and prototype flows.
