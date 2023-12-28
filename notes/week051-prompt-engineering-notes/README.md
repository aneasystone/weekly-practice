# WEEK051 - 提示工程学习笔记

在之前的笔记中，我们学习了很多大模型的使用技巧，比如 [实现一个划词翻译插件](../week040-chrome-extension-with-chatgpt/README.md)、[实现基于文档的问答助手](../week042-doc-qa-using-embedding/README.md)、[实现基于数据库的问答助手](../week047-structured-data-qa/README.md) 等等，在这些使用场景中，我们应该都或多或少听过 **提示工程（Prompt Engineering）** 这个概念；另外，在 [大模型应用开发框架 LangChain 学习笔记（二）](../week044-llm-application-frameworks-langchain-2/README.md) 这篇笔记中，我们学习了什么是 **智能体（Agent）**，并使用 LangChain 实现了几种不同类型的智能体，将提示工程技术发挥得淋漓尽致。那么到底什么是提示工程呢？提示工程又有哪些使用技巧呢？这篇笔记就来系统地学习下相关知识。

## 什么是提示工程

根据 [《Prompt Engineering Guide》](https://www.promptingguide.ai/zh) 这份指南中对提示工程的解释，**提示工程（Prompt Engineering）** 是一门关注于 **提示词（Prompt）** 的开发和优化的学科，能够帮助用户将大模型用于各种应用场景和研究领域，比如我们可以利用提示工程来提升大模型处理复杂任务的能力（如问答和算术推理）；或者实现大模型与其他生态工具的对接。

所谓提示词，说白了就是我们给大模型下发的指令，提示词写对了，大模型才能输出相应的结果，提示词写的越好，大模型输出的结果就越准确。提示词由下面的一个或多个要素组成：

* **指令**：给模型下达指令，或者描述要执行的任务；
* **上下文**：给模型提供额外的上下文信息，引导模型更好地响应；
* **输入数据**：用户输入的内容或问题；
* **输出指示**：指定输出的类型或格式；

提示词所需的格式取决于你完成的任务类型，并非所有以上要素都是必须的。比如在前面的笔记中，我通过下面的提示词实现了英汉翻译：

```
Translate this into Simplified Chinese:

The OpenAI API can be applied to virtually any task that involves understanding or generating natural language, code, or images.
```

这个提示词只包含了 **指令** 和 **输入数据** 两个部分。我还通过下面的提示词实现了基于文档的问答：

```
你是一个知识库助手，你将根据我提供的知识库内容来回答问题
已知有知识库内容如下：
1. 小明家有一条宠物狗，叫毛毛，这是他爸从北京带回来的。
2. 小红家也有一条宠物狗，叫大白，非常听话。
3. 小红的好朋友叫小明，他们是同班同学。
请根据知识库回答以下问题：小明家的宠物狗叫什么名字？
```

这里除 **指令** 和 **输入数据** 之外，还新增了 **上下文** 部分。可以看到，这些提示词都非常简单，而且效果也都还不错，这其实得益于大模型强大的自然语言处理能力。对于这种简单的任务，提示工程的作用并不明显。但是对于一些复杂的任务，比如算术和推理，或者解决大模型的局限性问题，比如幻觉和上下文限制等，不同的提示工程技术可以大大改善大模型的输出效果。

## 基本原则

提示工程是一门经验科学，提示词的细微差别可能会导致不一样的输出结果，甚至相同的提示工程技术，在不同模型之间也可能效果会有很大的差异，因此提示工程需要进行大量的实验和测试。尽管如此，编写提示词还是有一些通用的原则可以遵守的。

### 从简单开始

在设计提示词时，需要记住这是一个迭代的过程，需要大量的实验来获得最佳结果。避免从一开始就引入过多的复杂性，而应该从简单的提示词开始，然后不断地添加更多的元素和上下文，观察效果是否提高，在这个过程中对提示词进行版本控制。

比如你可以从零样本提示开始，如果效果不好，再改用少样本提示，如果效果还不好，再改用 [Fine-tuning](https://platform.openai.com/docs/guides/fine-tuning) 方案。

另外，当你面对一个复杂的大任务时，可以尝试将任务分解为更简单的子任务，通过构建不同的提示词来解决每个子任务。

### 使用指令

正如前文所述，指令是提示词的几大要素之一，通过指令可以完成一些简单任务，比如：分类、总结、翻译等。在 [OpenAI 的提示工程最佳实践](https://help.openai.com/en/articles/6654000-best-practices-for-prompt-engineering-with-openai-api) 中，建议将指令放在提示的开头，并使用一些诸如 `###` 或 `'''` 的分隔符来分隔指令和上下文：

```
总结下面的文本内容，将其中的要点以列表形式展示出来。

文本内容："""
{text input here}
"""
```

### 减少不精确的描述

确保你的提示词是明确的（Be specific）、具体的（Descriptive）、并且尽可能详细的（As detailed as possible），可以把和大模型的对话类比为和人的对话，沟通越直接，信息传递就越有效。比如下面是一个反例：

```
写一首关于 OpenAI 的诗
```

这个提示词就不够精确，我们应该对诗的内容做进一步描述才能让大模型更好的生成内容：

```
写一首鼓舞人心的关于 OpenAI 的短诗，聚焦最近的 DALL-E 产品发布（DALL-E 是一种文本到图像的机器学习模型），风格类似于莎士比亚。
```

下面是另一个描述不够精确的例子：

```
对该产品进行描述，描述应该相当简短，只有几句话，不能过多。
```

这个提示词啰里啰嗦，而且使用了一些模糊不清的概念，我们可以改得更直接、更具体、更简洁：

```
使用 3 到 5 句话描述该产品。
```

### 通过示例明确输出的格式

我们如果对模型的输出格式有特殊要求，最好提供几个示例，比如下面这个例子：

```
提取下面文本中的公司名称和成立时间。

以 JSON 格式输出：
[
    { "name": "XXX", "establish_time": "XXX" },
    { "name": "YYY", "establish_time": "YYY" }
]

文本内容："""
{text input here}
"""
```

这样的输出格式有一个好处，我们可以在程序中对大模型的输出进行可靠地解析。

### 避免说不要做什么

设计提示词的另一个常见技巧是避免说不要做什么，而是说要做什么。下面是一个反例：

```
下面是客户和代理商之间的对话。不要问客户的用户名和密码。不要重复回复的内容。

客户：我登录不了我的账号
代理商：
```

改成下面这样会更好：

```
下面是客户和代理商之间的对话。代理商将尝试诊断问题并给出解决方案，同时避免询问客户的个人信息（如用户名和密码），当涉及到这些信息时，建议用户访问帮助文档：www.samplewebsite.com/help/faq

客户：我登录不了我的账号
代理商：
```

### 角色扮演

当我们使用大模型构建一个客服聊天机器人之类的对话系统时，可以在提示词中明确它的身份和意图，就像玩角色扮演一样，比如：

```
我希望你扮演面试官的角色。我会充当一名 Java 开发工程师的候选人，然后你要问我关于这个职位的面试问题。你要像面试官一样说话。
不要一次写下所有的对话，不要写解释，像面试官一样一个接一个地问我问题，然后等待我的答复。我的第一句话是 “你好”。
```

这时大模型就变成了一位 Java 面试官，这种技巧有时也被称为 **角色提示（Role Prompting）**。你也可以尝试其他角色，比如教师、小说家、医生、足球评论员，甚至可以让它扮演 Linux 终端、浏览器、Python 执行器等等，这里有大量案例可供参考：[Awesome ChatGPT Prompts](https://github.com/f/awesome-chatgpt-prompts)。

## 提示词框架

上面提到，一个提示词是由指令、上下文、输入数据和输出指示这几个要素中的一个或多个组成的，这其实就为如何编写提示词提供了一个基础框架，最初由 Elavis Saravia 在 [《Prompt Engineering Guide》](https://www.promptingguide.ai/introduction/elements) 中总结的。

除此之外，还有一些提示词框架对提示词的格式和内容做了更明确的定义，比如 Matt Nigh 的 [CRISPE 框架](https://github.com/mattnigh/ChatGPT3-Free-Prompt-List)：

* CR： Capacity and Role（能力与角色）。你希望 ChatGPT 扮演怎样的角色。
* I： Insight（洞察力），背景信息和上下文。
* S： Statement（指令），你希望 ChatGPT 做什么。
* P： Personality（个性），你希望 ChatGPT 以什么风格或方式回答你。
* E： Experiment（实验），要求 ChatGPT 为你提供多个答案。

云中江树的 [结构化提示词](https://github.com/EmbraceAGI/LangGPT)：

```
# Role: Your_Role_Name

## Profile

- Author: YZFly
- Version: 0.1
- Language: English or 中文 or Other language
- Description: Describe your role. Give an overview of the character's characteristics and skills

### Skill 1
1. xxx
2. xxx

### Skill 2
1. xxx
2. xxx

## Rules
1. Don't break character under any circumstance.
2. Don't talk nonsense and make up facts.

## Workflow
1. First, xxx
2. Then, xxx
3. Finally, xxx

## Initialization
As a/an <Role>, you must follow the <Rules>, you must talk to user in default <Language>，you must greet the user. Then introduce yourself and introduce the <Workflow>.
```

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
* [Learn Prompt](https://www.learnprompt.pro/)
* [Learn Prompting](https://learnprompting.org/zh-Hans/docs/intro)
* [Learning Prompt](https://learningprompt.wiki/)
* [Prompt Engineering | Lil'Log](https://lilianweng.github.io/posts/2023-03-15-prompt-engineering/)
* [Brex's Prompt Engineering Guide](https://github.com/brexhq/prompt-engineering)
* [The Prompt Landscape](https://blog.langchain.dev/the-prompt-landscape/)
* [HuggingLLM](https://github.com/datawhalechina/hugging-llm)
* [OpenAI Cookbook](https://github.com/openai/openai-cookbook)
* [Best practices for prompt engineering with OpenAI API](https://help.openai.com/en/articles/6654000-best-practices-for-prompt-engineering-with-openai-api)
* [OpenAI 官方提示工程指南 [译]](https://baoyu.io/translations/openai/openai-prompt-engineering-guides)

## 更多

### 结构化 Prompt

* [如何写好Prompt: 结构化](https://www.lijigang.com/posts/chatgpt-prompt-structure/)
* [LangGPT 结构化提示词](https://aq92z6vors3.feishu.cn/wiki/RXdbwRyASiShtDky381ciwFEnpe)
* [LangGPT — Empowering everyone to create high-quality prompts!](https://github.com/EmbraceAGI/LangGPT)
* [Mr. Ranedeer: Your personalized AI Tutor!](https://github.com/JushBJJ/Mr.-Ranedeer-AI-Tutor)
* [CRISPE Prompt Framework](https://github.com/mattnigh/ChatGPT3-Free-Prompt-List)

### 应用产品

* [Open Prompt Studio](https://moonvy.com/apps/ops/) - AIGC 提示词可视化编辑器
* [ChatGPT Shortcut](https://www.aishort.top/) - 让生产力加倍的 ChatGPT 快捷指令
* [PromptPerfect](https://promptperfect.jinaai.cn/) - 将您的提示词提升至完美
* [LangGPT](https://github.com/yzfly/LangGPT) - Empowering everyone to create high-quality prompts!
* [Knit](https://promptknit.com/) - A better playground for prompt designers
