# WEEK051 - 提示工程学习笔记

在之前的笔记中，我们学习了很多大模型的使用技巧，比如 [实现一个划词翻译插件](../week040-chrome-extension-with-chatgpt/README.md)、[实现基于文档的问答助手](../week042-doc-qa-using-embedding/README.md)、[实现基于数据库的问答助手](../week047-structured-data-qa/README.md) 等等，在这些使用场景中，我们应该都或多或少听过 **提示工程（Prompt Engineering）** 这个概念；另外，在 [大模型应用开发框架 LangChain 学习笔记（二）](../week044-llm-application-frameworks-langchain-2/README.md) 这篇笔记中，我们学习了什么是 **智能体（Agent）**，并使用 LangChain 实现了几种不同类型的智能体，将提示工程技术发挥得淋漓尽致。那么到底什么是提示工程呢？提示工程又有哪些使用技巧呢？这篇笔记就来系统地学习下相关知识。

## 什么是提示工程

根据 [《Prompt Engineering Guide》](https://www.promptingguide.ai/zh) 这份指南中对提示工程的解释，**提示工程（Prompt Engineering）** 是一门关注于提示词的开发和优化的学科，能够帮助用户将大模型用于各种应用场景和研究领域，比如我们可以利用提示工程来提升大模型处理复杂任务的能力（如问答和算术推理）；或者实现大模型与其他生态工具的对接。

## 提示工程技术

### 零样本提示

https://www.promptingguide.ai/zh/techniques/zeroshot

### 少样本提示

https://www.promptingguide.ai/zh/techniques/fewshot

### 思维链（CoT）

https://www.promptingguide.ai/zh/techniques/cot

### 自我一致性

https://www.promptingguide.ai/zh/techniques/consistency

### 生成知识提示

https://www.promptingguide.ai/zh/techniques/knowledge

### 思维树 (ToT)

https://www.promptingguide.ai/zh/techniques/tot

### 检索增强生成 (RAG)

https://www.promptingguide.ai/zh/techniques/rag

### 自动推理并使用工具 (ART)

https://www.promptingguide.ai/zh/techniques/art

### 自动提示工程师（APE）

https://www.promptingguide.ai/zh/techniques/ape

### Active-Prompt

https://www.promptingguide.ai/zh/techniques/activeprompt

### 方向性刺激提示

https://www.promptingguide.ai/zh/techniques/dsp

### ReAct 框架

https://www.promptingguide.ai/zh/techniques/react

### 多模态思维链

https://www.promptingguide.ai/zh/techniques/multimodalcot

### 基于图的提示

https://www.promptingguide.ai/zh/techniques/graph

## 参考

* [提示工程指南](https://www.promptingguide.ai/zh/)
* [Prompt Engineering | Lil'Log](https://lilianweng.github.io/posts/2023-03-15-prompt-engineering/)
* [Brex's Prompt Engineering Guide](https://github.com/brexhq/prompt-engineering)
* [The Prompt Landscape](https://blog.langchain.dev/the-prompt-landscape/)
* [Learn Prompt](https://www.learnprompt.pro/)
* [Learning Prompt](https://learningprompt.wiki/)
* [HuggingLLM](https://github.com/datawhalechina/hugging-llm)
* [OpenAI Cookbook](https://github.com/openai/openai-cookbook)

## 更多

### 应用产品

* [Open Prompt Studio](https://moonvy.com/apps/ops/) - AIGC 提示词可视化编辑器
* [ChatGPT Shortcut](https://www.aishort.top/) - 让生产力加倍的 ChatGPT 快捷指令
* [PromptPerfect](https://promptperfect.jinaai.cn/) - 将您的提示词提升至完美
* [LangGPT](https://github.com/yzfly/LangGPT) - Empowering everyone to create high-quality prompts!
* [Knit](https://promptknit.com/) - A better playground for prompt designers
