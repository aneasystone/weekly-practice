# WEEK061 - 聊聊 Deep Search 和 Deep Research

[2022 年 11 月 30 日](https://openai.com/index/chatgpt/)，OpenAI 正式发布 ChatGPT 产品，仅两个月后，其月活用户就突破了 1 个亿，成为历史上增长最快的消费类应用之一。一时之间，生成式 AI 技术遍地开花，国内外科技大厂紧锣密鼓纷纷入场，各种大模型和 AI 产品以星火燎原之势涌现出来。

ChatGPT 的发布对传统搜索（如 Google）和问答社区（如 StackOverflow）造成了强烈的冲击。用户对传统搜索的不满早已不是秘密，搜索结果中大量的广告和低质的 SEO 内容导致用户体验很差，而 ChatGPT 通过自然语言以对话的方式为用户直接提供答案，省去了用户在海量的搜索页面之间反复跳转和搜集信息的麻烦。谷歌拥有 DeepMind 和 Google Brain 两大顶尖 AI 实验室，原本有机会站在这波生成式 AI 浪潮的最顶端，但是管理层安于现状，不忍放弃广告业务的利润，最终被 ChatGPT 抢占先机。为了应对 ChatGPT 的冲击，谷歌很快开始了反击，公司在内部发布 **红色代码（Red Code）** 预警，进入战备状态，创始人布林甚至亲自下场为聊天机器人 Bard 写代码。

生成式 AI 和传统搜索之间的战争就此拉开了序幕。

## AI + 搜索

不过很快人们就发现了 ChatGPT 的不足，尽管 ChatGPT 能以简洁的交互给出即时答案，但是它的答案中充斥了大量的事实性错误，幻觉问题和静态知识是大模型天生的两大局限，导致其答案准确性达不到搜索引擎的要求。一开始，大家只是作为谈资一笑了之，但是随着大模型在商业化应用中的落地，人们的抱怨声也就越来越多，在某些场景下，比如医疗建议，错误的回复可能导致灾难性后果。

为了解决这些问题，又一项新技术应运而生，那就是 **RAG（Retrieval-Augmented Generation，检索增强生成）**，通过引入外部信息源，包括搜索引擎、企业私域知识、个人笔记等一切能查询的信息，可以有效的缓解大模型的幻觉问题，在生成答案时还可以标注信息来源以提升可信度。

[2024 年 10 月](https://openai.com/index/introducing-chatgpt-search/)，ChatGPT 推出搜索功能：

![](./images/chatgpt-search.png)

国内外产商也纷纷跟进，比如 [DeepSeek](https://chat.deepseek.com/) 的：

![](./images/deepseek-search.png)

[Qwen Chat](https://chat.qwen.ai/) 的：

![](./images/qwen-search.png)

[Kimi](https://kimi.moonshot.cn/) 的：

![](./images/kimi-search.png)

[前不久](https://www.anthropic.com/news/web-search)，Claude 也集成了搜索功能：

![](./images/claude-search.png)

如今 **AI + 搜索** 已经是各家大模型产品的标配。

与此同时，**搜索 + AI** 也不甘示弱，比如 Google 面向美国用户推出的 [AI Overviews](https://blog.google/products/search/ai-overviews-search-october-2024/) 功能，在搜索结果顶部提供自然语言生成的答案摘要；百度在搜索顶部也加入了 AI+ 功能：

![](./images/baidu-ai+.png)

还有一些比较小众的搜索服务和开源项目，比如 [YOU.COM](https://you.com/)、[iAsk](https://iask.ai/)、[Lepton Search](https://search.lepton.run/) 等，感兴趣的也可以尝试下。

### 技术原理

**AI + 搜索** 的本质是 **朴素 RAG**，我曾在 [week042-doc-qa-using-embedding](../week042-doc-qa-using-embedding/README.md) 这篇笔记中简单介绍过 RAG 的基本流程，如下图所示：

![](./images/doc-qa.png)

可以看出它的实现非常简单，唯一的难点是知识库文档和用户问题的向量化以及向量检索，而 **AI + 搜索** 则更简单，直接拿着用户问题去调搜索引擎的接口就行了：

![](./images/search-qa.png)

关于如何组织搜索结果和用户问题，可以参考 [DeepSeek 公开的 Prompt](https://github.com/deepseek-ai/DeepSeek-R1#official-prompts)：

```
# 以下内容是基于用户发送的消息的搜索结果:
{search_results}
在我给你的搜索结果中，每个结果都是[webpage X begin]...[webpage X end]格式的，X代表每篇文章的数字索引。请在适当的情况下在句子末尾引用上下文。
请按照引用编号[citation:X]的格式在答案中对应部分引用上下文。如果一句话源自多个上下文，请列出所有相关的引用编号，例如[citation:3][citation:5]，
切记不要将引用集中在最后返回引用编号，而是在答案对应部分列出。
在回答时，请注意以下几点：
- 今天是{cur_date}。
- 并非搜索结果的所有内容都与用户的问题密切相关，你需要结合问题，对搜索结果进行甄别、筛选。
- 对于列举类的问题（如列举所有航班信息），尽量将答案控制在10个要点以内，并告诉用户可以查看搜索来源、获得完整信息。优先提供信息完整、最相关的列举项；
如非必要，不要主动告诉用户搜索结果未提供的内容。
- 对于创作类的问题（如写论文），请务必在正文的段落中引用对应的参考编号，例如[citation:3][citation:5]，不能只在文章末尾引用。
你需要解读并概括用户的题目要求，选择合适的格式，充分利用搜索结果并抽取重要信息，生成符合用户要求、极具思想深度、富有创造力与专业性的答案。
你的创作篇幅需要尽可能延长，对于每一个要点的论述要推测用户的意图，给出尽可能多角度的回答要点，且务必信息量大、论述详尽。
- 如果回答很长，请尽量结构化、分段落总结。如果需要分点作答，尽量控制在5个点以内，并合并相关的内容。
- 对于客观类的问答，如果问题的答案非常简短，可以适当补充一到两句相关信息，以丰富内容。
- 你需要根据用户要求和回答内容选择合适、美观的回答格式，确保可读性强。
- 你的回答应该综合多个相关网页来回答，不能重复引用一个网页。
- 除非用户要求，否则你回答的语言需要和用户提问的语言保持一致。

# 用户消息为：
{question}
```

这里最大的难点可能不是技术问题，而是去哪里找免费的搜索引擎接口？下面是我搜集的一些常用的搜索服务：

* [Bing Web Search API](https://www.microsoft.com/en-us/bing/apis/bing-web-search-api) - 每月 1000 次免费调用
* [Google Programmable Search Engine](https://developers.google.com/custom-search) - Google 的自定义搜索
* [SearchApi Google Search API](https://www.searchapi.io/) - 注册送 100 次调用
* [Serper API](https://serper.dev/) - 注册送 2500 次调用
* [Serp API](https://serpapi.com/) - 每月 100 次免费调用
* [Brave Search API](https://brave.com/search/api/) - 每月 2000 次免费调用
* [Exa API](https://exa.ai/exa-api) - 注册送 $10 额度
* [YOU API](https://api.you.com/) - 60 天免费使用
* [Tavily](https://tavily.com/) - 每月 1000 次免费调用
* [博查搜索 API](https://open.bochaai.com/) - 国内不错的搜索服务，不免费，但确实便宜，一次调用 3 分钱

除了这些通用搜索服务，还有一些领域类搜索，比如学术搜索可以用 [Google Scholar API](https://serpapi.com/google-scholar-api)、[arXiv API](https://info.arxiv.org/help/api/index.html) 等；本地商业搜索可以用 [Yelp Fusion API](https://docs.developer.yelp.com/docs/fusion-intro)、[高德地图 API](https://lbs.amap.com/product/search) 等。

此外还可以使用诸如 [Meilisearch](https://www.meilisearch.com/) 这样的开源项目，自建本地搜索引擎，完全免费，这非常适用于用户自有数据。

## AI + 深度搜索（Deep Search）

**朴素 RAG** 的弊端很快便浮现了出来：**RAG 中最核心的问题是 R，也就是检索**，在面对模糊问题时，检索结果的精确性往往不高，面对复杂问题时，单次检索又不足以获取足够的上下文信息；为了解决这些问题，人们又提出了 **高级 RAG** 和 **模块化 RAG** 等概念，通过 **查询重写（Query Rewriting）**、**查询扩展（Query Expansion）** 等方法将用户的原始问题转换成更清晰、更适合检索的任务，这种方法也被称为 **查询转换（Query Transformation）**：

![](./images/query-transformation.png)

在过去的一年里，RAG 技术日新月异，感兴趣的可以参见我之前写的 [week054-advanced-rag-notes](../week054-advanced-rag-notes/README.md) 这篇笔记。

### Graph RAG

尽管如此，传统 RAG 在面对更复杂的问题时仍然是捉襟见肘，这些问题往往需要更深入搜索和推理，具体包括：

* **全局性问题理解**：传统 RAG 主要依赖向量检索，擅长回答局部的、具体的问题，但难以处理需要跨文档推理的全局性问题；
    * 近五年人工智能领域的论文中，哪些研究方向的热度增长最快？
* **复杂语义关系问答**：传统 RAG 忽略了实体间的语义关系，导致回答缺乏逻辑连贯性；
    * 《哪吒2》是哪个公司发行的，这个公司还发行过哪些票房超10亿的电影？
* **多跳推理问题**：传统 RAG 无法处理需要多步推理的问题，因为向量检索仅返回单篇文档片段；
    * 《哪吒2》中哪吒配音的老家天气怎么样？
* **复杂条件筛选**：依赖关键词匹配可能漏检，无法处理复合逻辑条件；
    * 找出所有总部在加州、员工超过1万人，且创始人毕业于斯坦福的科技公司。

2024 年上半年，微软公开了 **Graph RAG** 的论文 [From Local to Global: A Graph RAG Approach to Query-Focused Summarization](https://arxiv.org/abs/2404.16130)，将知识图谱的概念引入 RAG 中，通过结构化信息提升大模型生成内容的准确性、相关性和可解释性。在年中的时候，[Graph RAG](https://github.com/microsoft/graphrag) 正式开源，在社区引起了相当的热度，在很短时间内就超过了上万星标。

![](./images/graph-qa.png)

### Agentic RAG

上面这些 RAG 的流程基本上都是线性的，遵循着 **检索-生成-结束** 这样的固定流程。后来，随着智能体的兴起，又出现了 [Agentic RAG](https://arxiv.org/pdf/2501.09136) 的概念，这是传统 RAG 的进阶范式，将智能体的任务规划、工具使用、反思重试等机制引入 RAG 流程中。

![](./images/agentic-rag-overview.png)

智能体的核心是 **思考-行动-观察** 循环，这三个组件在一个持续的循环中协同工作，从而实现智能体的自主性、交互性和决策能力。将智能体引入 RAG 系统，可以让其具备更动态、更灵活的检索与生成能力；最直观的表现就是反复的检索，比如切换不同的数据源（工具使用），切换不同的检索词（子任务拆解、反思），直到用户问题解决为止。

![](./images/agentic-rag.png)

Agentic RAG 的典型能力如下：

* **动态检索**：根据生成内容的中间结果，决定是否需要二次检索，发现答案不完整时自动触发新搜索；或者根据问题类型主动选择检索源，比如优先查数据库还是通用搜索引擎；
* **任务分解**：将复杂问题拆解为子任务，比如用户的问题是 “对比 A 和 B”，那么需要先检索 A 的特性，再检索 B 的特性，最后综合比较；
* **工具调用**：让 RAG 不仅仅局限于检索，也可以调用外部工具获取实时信息，比如查询股票价格和天气情况；又或者执行计算或生成代码，比如通过 Python 代码分析数据，再生成结论；
* **反思与修正**：对生成结果自我评估，发现不足时重新检索或调整生成策略，比如在生成报告时发现缺少某部分数据时能自动补充；
* **多轮交互**：在对话中主动追问用户以澄清需求，比如用户的要求是 “帮我找一些关于人工智能的论文”，可以追问要找的是什么领域，是 NLP 还是计算机视觉。

有很多关于 Agentic RAG 的开源实现，比如 [LlamaIndex](https://www.llamaindex.ai/blog/agentic-rag-with-llamaindex-2721b8a49ff6)、[LangGraph](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/)、[smolagents](https://huggingface.co/learn/cookbook/agent_rag) 等教程。

### Deep Search

接下来，我们再来看下什么是 **深度搜索（Deep Search）**？其实，目前学术界并没有这个概念的明确定义，只是有几个产品或开源项目是以这个命名的，比如 [Grok 3](https://x.ai/news/grok-3) 中推出的 DeepSearch 和 DeeperSearch 功能：

![](./images/grok-deep-search.png)

在回答问题时会经过 **思考-搜索-分析-验证** 等步骤：

![](./images/grok-deep-search-2.png)

这和上面的 Agentic RAG 使用的 **思考-行动-观察** 循环如出一辙，所以本质上来说，**Deep Search 就是 Agentic RAG**。

另一个是 Jina AI 推出的 [深度搜索 API](https://jina.ai/deepsearch/) 服务，它会对用户的问题进行广泛搜索并经过多次迭代，然后给出答案。

![](./images/jina-deep-search.png)

这个 API 和 OpenAI 的接口基本一致，所以很容易接入我们的应用中，官方也提供了 [对话页面](https://search.jina.ai/) 可以体验。同时，这还是一个开源项目，项目名叫 [jina-ai/node-DeepResearch](https://github.com/jina-ai/node-DeepResearch)，虽然名称里有 DeepResearch 但是实际上它只有 DeepSearch 的功能，感兴趣的同学可以去扒一扒它的源码，官方还贴心地写了两篇公众号文章对其实现原理做了详细的讲解，推荐一读：

* [DeepSearch 与 DeepResearch 的设计和实现](https://mp.weixin.qq.com/s/-pPhHDi2nz8hp5R3Lm_mww)
* [DeepSearch/DeepResearch 中最优文本段选择和 URL 重排](https://mp.weixin.qq.com/s/apnorBj4TZs3-Mo23xUReQ)

还有一个是 [Zilliz](https://zilliz.com/) 公司（就是开源 Milvus 向量数据库的那家公司）开源的项目 [zilliztech/deep-searcher](https://github.com/zilliztech/deep-searcher)：

![](./images/zilliz-deep-searcher.png)

细读它的源码可以发现，它主要分为两个部分：

1. 离线数据处理：通过各种 `file_loader` 和 `web_crawler` 加载文件和网页，切片后生成向量，构建离线数据；其中 `web_crawler` 使用了 [Jina Reader](https://jina.ai/reader)、[Firecrawl](https://www.firecrawl.dev/)、[Crawl4AI](https://docs.crawl4ai.com/) 等接口实现网页内容的爬取；
2. 在线实时问答：代码中实现了两个 Agent，根据问题的类型路由到对应的 Agent 来处理：
    * [ChainOfRAG](https://github.com/zilliztech/deep-searcher/blob/master/deepsearcher/agent/chain_of_rag.py)：这个 Agent 可以分解复杂的查询，并逐步找到子查询的事实信息，它非常适合处理具体的事实查询和多跳问题；
    * [DeepSearch](https://github.com/zilliztech/deep-searcher/blob/master/deepsearcher/agent/deep_search.py)：这个 Agent 适合处理一般和简单的查询，例如给定一个主题，然后撰写报告、调查或文章。

下面是我画的一个粗略的流程图：

![](./images/zilliz-deep-searcher-2.png)

其中 `ChainOfRAG` 借鉴了 [Chain-of-Retrieval Augmented Generation](https://arxiv.org/abs/2501.14342) 这篇论文中的思路。可以看到两种 Agent 都具备 Agentic RAG 循环的特点，循环里的每一步都是通过调用大模型来实现的，使用了不少的 Prompt 技巧。

和 Jina AI 的 `node-DeepResearch` 项目对比一下可以发现，Zilliz 的 `deep-searcher` 依赖于向量数据库，着重聚焦于对私有数据的深度检索。虽然两者都有使用 [Jina Reader](https://jina.ai/reader) 接口，但是 `node-DeepResearch` 是作为搜索接口，用户对话时实时请求，而 `deep-searcher` 是用来构建离线数据。另外，Zilliz 也发布了几篇公众号文章，不过其标题和内容颇具争议，在网上引发了不少的讨论，也可以参考下。

* [别搞 Graph RAG 了，拥抱新一代 RAG 范式 DeepSearcher](https://mp.weixin.qq.com/s/gLyaLhWWDj1WoDSxEwpT6Q)
* [DeepSearcher 深度解读：Agentic RAG 的出现，传统 RAG 的黄昏](https://mp.weixin.qq.com/s/N-oPDmkb3EKqB2IM_reO1A)

## AI + 深度研究（Deep Research）

其实，深度搜索早已不是什么新鲜概念，早在两年前就有不少产品提供类似的功能，比如 [天工 AI 搜索](https://www.tiangong.cn/)，号称 “国内第一款AI搜索产品”，于 2023 年 8 月就已经上线了：

![](./images/tiangong.png)

再比如国内的 [秘塔](https://metaso.cn/)：

![](./images/metaso.png)

国外的 [Perplexity](https://www.perplexity.ai/)：

![](./images/perplexity.png)

他们都是在大模型兴起之初就开始 AI + 深度搜索 这方面的研究了，那为什么到今天，这个概念才开始引起各方的关注呢？

### Deep Research 演进历史

我们不妨梳理和回顾下 AI 圈近几个月发生的一些重要事件：

* 2024 年 9 月，OpenAI 发布 [o1-preview](https://openai.com/index/introducing-openai-o1-preview/)，该模型在回答之前会花更多时间思考，使其在复杂推理任务、科学和编程方面显著优于其他模型；
* 2024 年 10 月，Anthropic 推出 [Computer Use](https://www.anthropic.com/news/3-5-models-and-computer-use) 功能，使 AI 能像人类一样操作电脑，通过观看屏幕截图，实现移动光标、点击按钮、使用虚拟键盘输入文本等操作，真正模拟人类与计算机的交互；
* 2024 年 12 月 11 号，Google 发布 Gemini 2.0 Flash，同时还给 Gemini 带了一项名为 [Deep Research](https://blog.google/products/gemini/google-gemini-deep-research/) 的新能力，利用高级推理和长文本处理能力，Deep Research 可以充当个人的研究助理，比如用来做一些复杂的研究报告；
* 2024 年 12 月 19 号，Google 紧接着又发布了 [Gemini 2.0 Flash Thinking](https://deepmind.google/technologies/gemini/flash-thinking/) 公开预览版，这也是一种思考模型，可以在模型生成回答时查看其思考过程，并生成具有更强推理能力的回答；
* 2025 年 1 月 20 号，深度求索的 [DeepSeek-R1](https://api-docs.deepseek.com/news/news250120) 横空出世，用极低的成本达到了比肩 OpenAI o1 的水平，在全球市场上掀起了一股前所未有的热潮，也潜移默化地把 “推理模型” 这个概念带给了千家万户，将思考过程渲染在聊天界面已经变成了一种标准做法；
* 2025 年 1 月 23 号，OpenAI 发布 [Operator](https://openai.com/index/introducing-operator/) 智能体，和 Anthropic 的 Computer Use 类似，可以操作浏览器，为用户执行各种复杂任务；
* 2025 年 2 月 2 号，OpenAI 又发布了 [Deep Research](https://openai.com/index/introducing-deep-research/) 功能，它可以自动搜集大量的网络信息，利用推理能力综合分析，为用户完成更为复杂的研究任务，能在几十分钟内完成人类需要数小时才能完成的工作；
* 2025 年 2 月 14 号，Perplexity 紧随其后，同样也发布了 [Deep Research](https://www.perplexity.ai/hub/blog/introducing-perplexity-deep-research) 功能，能够执行多次搜索、阅读大量来源并生成全面报告；
* 2025 年 2 月 19 号，xAI 推出 [Grok-3](https://x.ai/news/grok-3)，内置 DeepSearch 和 DeeperSearch 功能；
* 2025 年 2 月 25 号，阿里 Qwen 团队发布推理模型 [QwQ-Max-Preview](https://qwenlm.github.io/zh/blog/qwq-max-preview/)，它基于 `Qwen2.5-Max` 构建，在数学、编程以及通用任务中展现了更强的能力，同时在 Agent 相关的工作流中也有不错的表现；
* 2025 年 3 月 5 号，Google 面向 Google One AI Premium 订阅用户推出 [AI Mode](https://blog.google/products/search/ai-mode-search/) 功能，提供对话式搜索体验，支持复杂多轮提问；
* 2025 年 3 月 6 号，中国 AI 创业公司 Monica 发布 [Manus](https://manus.im/)，号称 “全球首款通用 AI 代理”，其应用场景覆盖旅行规划、股票分析、教育内容生成等 40 余个领域；据称，Manus 在 GAIA 基准测试中刷新了 SOTA 记录，性能远超同类产品，凭借 KOL 助力，一时间刷屏全网，内测邀请码一码难求，甚至被炒到 5 万块钱；
* 2025 年 3 月 31 号，在中关村论坛智谱 Open Day 上，智谱发布了 [AutoGLM 沉思](https://autoglm-research.zhipuai.cn/)，这又是一款 Deep Research 类智能体，它能够模拟人类的思维过程，完成从数据检索、分析到生成报告的全过程；

可以看出 2025 年刚过去四分之一，Deep Research 就已经开始卷起来了。这其中，OpenAI 发布的 `o1-preview` 和深度求索发布的 `DeepSeek-R1` 是两个关键里程碑，Gemini 2.0 Flash Thinking 和 QwQ 穷追不舍，这些都被称为推理模型（或思考模型），他们引入了 **推理时计算（test-time compute）** 的概念，也就是在推理阶段投入更多的计算资源，例如评估多个潜在答案、进行更深入的规划、以及在给出最终答案前进行自我反思等。

心理学家卡尼曼提出，人类大脑中存在两套系统：系统1和系统2，系统1是无意识的、快速的、直观的，而系统2则是有意识的、缓慢的、需要付出心理努力的，这两套系统在我们日常生活中相互作用，共同影响着我们的思考、决策和行为。

传统模型和推理模型就好比是人类大脑中的系统1和系统2，推理模型用更长的等待时间，换取更高质量、更具实用性的结果。就像著名的 [斯坦福棉花糖实验](https://zh.wikipedia.org/wiki/%E6%A3%89%E8%8A%B1%E7%B3%96%E5%AE%9E%E9%AA%8C)，那些为了获得两个棉花糖而坚持忍耐更长时间的孩子，往往能取得更好的长期成就。推理模型的发展其实是在引导用户接受一种 **延迟满足** 的观念，为了获得更好的结果，用户需要等待更长的处理时间，无论你是否喜欢这种用户体验，大多数用户都已经默默接受了这一点。

正是在这个背景下，Deep Research 开始流行起来，因为 Deep Research 天生需要深度思考和推理。

### Deep Research 示例

Deep Research 和 Deep Search 的概念由于并没有明确定义，往往被混淆，但在我看来，Deep Research 相比于 Deep Search 有几个更明显的特征：

* 引入推理模型，思考时间更长，能处理更复杂的任务；
* 能使用更多的工具，比如操作电脑、访问浏览器、编写代码等；
* 更擅长论文写作和报告生成；

下图是 [Manus](https://manus.im/usecases) 的部分用例展示：

![](./images/manus-usecases.png)

下图是 [AutoGLM 沉思](https://autoglm-research.zhipuai.cn/) 的部分用例展示：

![](./images/autoglm-usecase.png)

这两个用例展示里列出了一些 Deep Research 的典型场景：解决复杂任务、撰写行业研究报告、生成旅游攻略、竞品对比、教案制作等。比如 AutoGLM 沉思可以通过任务拆解和浏览器轻松解决 `《哪吒2》中哪吒配音的老家天气怎么样？` 这种多跳问题：

![](./images/autoglm.png)

Gemini 的 Deep Research 功能可以结合思考模型和联网搜索对话题进行深度剖析：

![](./images/gemini-deep-research.png)

生成一份长达 7 页的 PDF 文件：

![](./images/gemini-deep-research-pdf.png)

最近秘塔推出了一个 [生成互动网页](https://mp.weixin.qq.com/s/sk0KF9c1MPhpS2oGH-UIKA) 的功能，可以将搜索的内容整合成一份图文并茂的研究报告：

![](./images/metaso-report.png)

### Deep Research 开源实现

目前 Deep Research 开源实现非常多，这一节将挑选几个比较流行的逐一介绍下。

#### assafelovic/gpt-researcher

[GPT Researcher](https://github.com/assafelovic/gpt-researcher) 也被简称为 GPTR，应该是大模型兴起之后最早一批专注于研究报告生成的开源项目。受 [Plan-and-Solve](https://arxiv.org/abs/2305.04091)、[RAG](https://arxiv.org/abs/2005.11401) 和 [STORM](https://arxiv.org/abs/2402.14207) 等论文的启发，GPT Researcher 将系统划分成 **规划者（Planner）**、**研究者（Researcher）** 和 **发布者（Publisher）** 三个部分：

![](./images/gpt-researcher-overview.png)

其中规划者生成研究问题，而研究者根据每个生成的研究问题寻找最相关的信息，最后，发布者筛选和汇总所有相关信息，并生成一份研究报告。

要体验 GPT Researcher，首先下载源码：

```
$ git clone https://github.com/assafelovic/gpt-researcher.git
```

然后进入项目根目录：

```
$ cd gpt-researcher
```

目录下有一个 `.env.example` 文件，复制这个文件并重命名为 `.env`，然后填写 `OPENAI_API_KEY` 和 `TAVILY_API_KEY` 两个环境变量：

```
$ cp .env.example .env
$ vi .env
OPENAI_API_KEY=xxx
TAVILY_API_KEY=xxx
```

接下来安装所需依赖：

```
$ pip install -r requirements.txt
```

安装完成后运行：

```
$ python -m uvicorn main:app --reload
```

这时就可以通过 `http://localhost:8000` 访问并使用 GPT Researcher 了。

要注意的是，这个页面是用 [纯 JS](https://docs.gptr.dev/docs/gpt-researcher/frontend/vanilla-js-frontend) 实现的，不依赖其他 JS 库，所以体验不怎么好，而且更新有些滞后，有些最新特性体验不了。官方还提供了另一个 [Next.js 版本](https://docs.gptr.dev/docs/gpt-researcher/frontend/nextjs-frontend) 的实现，可以通过下面的步骤启动：

```
$ cd frontend/nextjs
$ npm install --legacy-peer-deps
$ npm run dev
```

启动成功后，可以通过 `http://localhost:3000` 访问新 UI：

![](./images/gpt-researcher-ui.png)

新 UI 相对于老 UI 在左下角多了一个高级选项：

![](./images/gpt-researcher-ui-settings.png)

其中 `Report Source` 表示参考数据来源，GPT Researcher 支持从互联网上或本地文档中获取信息：

* **The Internet** - 从互联网上搜索需要的信息，默认使用 Tavily 接口，也支持切换 [其他的搜索引擎](https://docs.gptr.dev/docs/gpt-researcher/search-engines/retrievers)；
* **My Documents** - 将本地文档 [存到向量数据库中](https://docs.gptr.dev/docs/gpt-researcher/context/vector-stores) 进行检索；
* **Hybrid** - [混合检索模式](https://docs.gptr.dev/blog/gptr-hybrid)，同时从互联网上和本地文档中检索；

`Tone` 表示报告的写作风格，GPT Researcher 支持下面十几种不同的写作风格：

* **客观** - 公正和无偏见地呈现事实和发现；
* **正式** - 遵循学术标准，使用复杂的语言和结构；
* **分析** - 对数据和理论进行批判性评估和详细检查；
* **说服** - 使观众信服某种观点或论点；
* **信息** - 提供清晰和全面的主题信息；
* **解释** - 阐明复杂的概念和过程；
* **描述** - 对现象、实验或案例研究进行详细描绘；
* **批判** - 评判研究及其结论的有效性和相关性；
* **比较** - 并列不同的理论、数据或方法，以突出差异和相似性；
* **推测** - 探索假设及其潜在影响或未来研究方向；
* **反思** - 考虑研究过程及个人见解或经历；
* **叙述** - 通过讲述故事来阐明研究发现或方法论；
* **幽默** - 轻松愉快且引人入胜，通常使内容更具亲和力；
* **乐观** - 强调积极发现和潜在益处；
* **悲观** - 关注局限性、挑战或负面结果；
* **简单** - 为年轻读者撰写，使用基本词汇和清晰解释；
* **随意** - 以对话和放松的风格进行轻松的日常阅读；

最后，最上面的 `Report Type` 选项，也是最重要的选项，这个表示生成报告的策略，GPT Researcher 支持四种不同的策略：

* **Summary** - 篇幅短，速度快，生成时间 2min 左右
* **Detailed** - 篇幅长，内容更有深度，生成时间 5min 左右
* **Deep Research Report** - 使用 [深度研究方式](https://docs.gptr.dev/blog/2025/02/26/deep-research) 生成报告
* **Multi Agents Report** - 使用 [多智能体方式](https://docs.gptr.dev/blog/gptr-langgraph) 生成报告

我对这几种不同的生成策略进行了简单的梳理，画了个流程图，感兴趣的同学可以深入到代码里看看：

![](./images/gpt-researcher-flow.png)

#### dzhng/deep-research

[dzhng/deep-research](https://github.com/dzhng/deep-research) 这个项目是由 [Aomni](https://www.aomni.com/) 的 CEO [David Zhang](https://github.com/dzhng) 开发，在 Github 开源后非常受欢迎，很快便成为万星项目。该项目架构简单易懂，核心代码不过 300 行，允许用户调整研究广度和深度，默认通过 [Firecrawl](https://www.firecrawl.dev) 作为信息搜索和抓取的工具，针对用户提供的主题不断探索发现，直到完成用户的研究目标。

下面简单体验下该项目，首先下载源码并进入工作目录：

```
$ git clone https://github.com/dzhng/deep-research.git
$ cd deep-research
```

修改环境变量：

```
$ cp .env.example .env.local
$ vi .env.local
FIRECRAWL_KEY=xxx
OPENAI_KEY=xxx
```

安装所需依赖：

```
$ npm install
```

然后运行：

```
$ npm start
```

这是一个命令行程序，运行后首先会询问你想研究什么主题，并让你填写研究的广度和深度，以及最后希望生成报告还是答案：

```
What would you like to research? A2A
Enter research breadth (recommended 2-10, default 4): 3
Enter research depth (recommended 1-5, default 2): 2
Do you want to generate a long report or a specific answer? (report/answer, default report): report
```

最近 Google 的 A2A 协议比较火，我就让它帮我生成一份 A2A 的调研报告，其中研究广度指的是根据你输入的主题生成 N 个子 query 进行并发搜索和研究，研究深度指的是根据搜索出来的结果进一步生成研究主题的次数，填写完这些信息后，程序会向用户提三个问题，进一步澄清要研究的主题：

```
Creating research plan...

To better understand your research needs, please answer these follow-up questions:

Can you please clarify the meaning of 'A2A' in your query? For instance, are you referring to an 'ask-to-answer' platform mechanism, 'asset-to-asset' exchange, or another concept entirely?
Your answer: google a2a protocol

Could you specify the context or domain where 'A2A' is being applied (e.g., finance, technology, social media)?
Your answer: technology

What specific aspects of 'A2A' are you interested in exploring (e.g., technical functionality, market impact, user engagement, etc.)?
Your answer: technical functionality
```

这里可以看到，由于 A2A 是新发布的协议，大模型并不知道是什么，所以需要我们明确输入。回答完三个问题后，就开始深度研究了：

```
Starting research...

Created 3 queries [
  {
    query: 'Google A2A protocol technical functionality overview',
    researchGoal: 'This query aims to gather comprehensive documentation and analysis of ...'
  },
  {
    query: 'Google A2A protocol design principles and implementation details',
    researchGoal: 'The goal here is to uncover in-depth information about the design philosophies and ...'
  },
  {
    query: 'Performance and scalability evaluation of the Google A2A protocol',
    researchGoal: 'This query targets technical performance metrics and scalability aspects of the Google A2A protocol ...'
  }
]
Ran Google A2A protocol technical functionality overview, found 4 contents
Ran Google A2A protocol design principles and implementation details, found 4 contents
```

经过大约 3 分钟时间，一份 7 页的研究报告就生成好了：

![](./images/dzhng-deep-research-pdf.png)

下面是大致的程序流程图：

![](./images/dzhng-deep-research-flow.png)

此外，有热心网友为这个程序做了 [Web 页面](https://github.com/AnotiaWang/deep-research-web-ui)，你也可以 [在线体验](https://deep-research.ataw.top/)：

![](./images/dzhng-deep-research-ui.png)

#### sentient-agi/OpenDeepSearch

[sentient-agi/OpenDeepSearch](https://github.com/sentient-agi/OpenDeepSearch) 是另一个比较热门的 Deep Research 开源项目，我们来体验下：

```
$ git clone https://github.com/sentient-agi/OpenDeepSearch.git
$ cd OpenDeepSearch
```

安装 OpenDeepSearch：

```
$ pip install -e .
$ pip install -r requirements.txt
```

修改环境变量：

```
SERPER_API_KEY=xxx

JINA_API_KEY=xxx

OPENAI_API_KEY=xxx
OPENAI_API_BASE=xxx
LITELLM_MODEL_ID=gpt-4o-mini
```

主要包括三个部分：

1. 搜索引擎配置：项目默认使用 [Serper](https://serper.dev/) 作为搜索引擎，也支持使用 [SearXNG](https://github.com/searxng/searxng) 搭建自己的聚合搜索引擎；
2. 重排序配置：项目默认使用 [Jina](https://jina.ai/) 作为重排序工具，也支持使用 [Infinity](https://github.com/michaelfeil/infinity) 搭建自己的 Embeddings 服务；
3. 大模型配置：项目使用 [LiteLLM](https://github.com/BerriAI/litellm) 对接大模型，支持多达 100+ 不同的大模型；

OpenDeepSearch 可以作为工具库直接调用：

```
from opendeepsearch import OpenDeepSearchTool

search_agent = OpenDeepSearchTool(
    model_name="gpt-4o-mini",
    reranker="jina"
)

if not search_agent.is_initialized:
    search_agent.setup()
    
query = "Fastest land animal?"
result = search_agent.forward(query)
print(result)
```

由于 `OpenDeepSearchTool` 实现了 [smolagents](https://github.com/huggingface/smolagents) 的 `Tool` 接口，所以也可以集成到 smolagents 智能体框架中作为工具调用，比如下面使用 `ToolCallingAgent` 创建一个 ReAct 智能体：

```
from opendeepsearch import OpenDeepSearchTool
from opendeepsearch.wolfram_tool import WolframAlphaTool
from opendeepsearch.prompts import REACT_PROMPT
from smolagents import LiteLLMModel, ToolCallingAgent

model = LiteLLMModel(
    "gpt-4o-mini",
    temperature=0.7
)
search_agent = OpenDeepSearchTool(
    model_name="gpt-4o-mini",
    reranker="jina"
)
wolfram_tool = WolframAlphaTool(app_id=os.environ["WOLFRAM_ALPHA_APP_ID"])
react_agent = ToolCallingAgent(
    tools=[search_agent, wolfram_tool],
    model=model,
    prompt_templates=REACT_PROMPT
)

query = "How long would a cheetah at full speed take to run the length of Pont Alexandre III?"
result = react_agent.run(query)
print(result)
```

这里的问题是 `一只猎豹以全速奔跑需要多长时间才能跑完亚历山大三世桥的长度？`，运行结果如下：

![](./images/opendeepsearch-react.png)

可以看到程序首先调用搜索工具得知 `亚历山大三世桥的长度为 160 米`，然后模型自己知道 `猎豹的奔跑速度是 30 米/秒`，再调用 WolframAlpha 工具计算 `160 / 30 = 5.333` 从而输出结果。

我们也可以使用 `CodeAgent` 创建一个 [Code 智能体](https://github.com/huggingface/smolagents?tab=readme-ov-file#how-do-code-agents-work)，参考 `gradio_demo.py` 示例代码：

```
$ python gradio_demo.py
```

示例代码集成了 [Gradio](https://github.com/gradio-app/gradio) 框架，提供了可视化页面和智能体进行交互：

![](./images/opendeepsearch-gradio-ui.png)

虽然这个项目的名字叫做 Deep Search，但是我觉得也可以将它划到 Deep Research 的范畴，主要在于它处理搜索结果的过程很值得学习，下面是调用 `OpenDeepSearchTool` 的流程图：

![](./images/opendeepsearch-flow.png)

这里有几个点比较值得关注：

1. 提供了默认和专业两种搜索模式，专业模式会对搜索结果进一步处理；
2. 处理的第一步是抓取页面内容，如果页面是 `wikipedia.org/wiki` 直接使用 [Wikipedia-API](https://github.com/martin-majlis/Wikipedia-API) 获取，否则使用 [Crawl4AI](https://github.com/unclecode/crawl4ai) 爬取；
3. 将爬取的内容分成段落，使用 [kenhktsui/llm-data-textbook-quality-fasttext-classifer-v2](https://huggingface.co/kenhktsui/llm-data-textbook-quality-fasttext-classifier-v2) 分类器对每个段落按 **教育价值（educational value）** 进行分类，过滤掉教育价值偏低的段落；
4. 如果页面内容过长，则使用 LangChain 的 `RecursiveCharacterTextSplitter` 对其进行分片，再通过 **重排序（Reranker）** 模型筛选出和原始问题最接近的片段。

可以看出 OpenDeepSearch 更擅长问答场景而不是报告生成，经过对搜索结果一系列的处理，OpenDeepSearch 在 [SimpleQA](https://openai.com/index/introducing-simpleqa/) 单跳查询方面的表现与闭源搜索产品相当，在 [FRAMES](https://huggingface.co/datasets/google/frames-benchmark) 多跳查询上表现远超闭源搜索产品：

![](./images/opendeepsearch-vs-others.png)

感兴趣的可以看下他们的 [论文](https://arxiv.org/abs/2503.20201)。

#### 更多

关于 Deep Search 和 Deep Research，还有很多优秀的开源项目，这些项目将传统的搜索技术充分融合，不仅在报告生成上有着出色的表现，而且在复杂问题的求解上也处于 SOTA 水平。比如在 OpenAI 发布 Deep Research 之后的 24 小时内，Hugging Face 就基于自家的 [smolagents](https://github.com/huggingface/smolagents/tree/main/examples/open_deep_research) 智能体框架实现了 [Open Deep Research](https://huggingface.co/blog/open-deep-research) 开源项目，能够自主浏览网页，滚动页面，处理文件，甚至编写代码对数据进行计算；在 Monica 发布 Manus 之后，MetaGPT 团队仅花费 3 小时就开发了 [OpenManus](https://github.com/mannaandpoem/OpenManus) 项目，也能够自主浏览网页，查询和总结信息，实现了和 Manus 类似的功能，得到社区的广泛关注；还有 LangChain 团队基于 LangGraph 多智能体框架开发的 [Local Deep Researcher](https://github.com/langchain-ai/local-deep-researcher) 和 [Open Deep Research](https://github.com/langchain-ai/open_deep_research) 项目，使用了和 GPT Researcher 一样的 `Plan and Execute` 思路，先用推理模型撰写报告大纲，然后针对每一节并行地搜集信息，最后生成一份详尽的调研报告，得益于 LangSmith 平台，运行过程中还能清晰地看到智能体的规划和执行链路。

除此之外，还有很多项目，篇幅有限，不能一一介绍。不过这些项目的实现思路大体是类似的，相信对上面几个项目的深度体验，结合对 Deep Search 和 Deep Research 原理的理解，在学习其他项目时也能一通百通。

## 总结

本文探讨了自 ChatGPT 引发生成式 AI 浪潮以来，信息检索与生成领域经历的快速演变，重点梳理了 **AI + 搜索**、**深度搜索（Deep Search）** 和 **深度研究（Deep Research）** 这三个相互关联又各有侧重的范式。

**AI + 搜索** 的兴起，标志着对传统搜索引擎局限性的初步回应。通过结合大语言模型与搜索引擎，它旨在克服传统搜索体验差、信息过载的问题，并缓解大模型固有的幻觉与知识静态性。这种模式直接提供答案，简化了用户获取信息的过程，成为了各大模型产品的标配功能。然而，面对模糊或复杂问题时，其依赖单次、直接检索的 **朴素 RAG** 模式暴露出检索精度不足的弊端。

**深度搜索（Deep Search）** 应运而生，作为对朴素 RAG 局限性的深化解决方案。它本质上是 **Agentic RAG** 的应用，引入了更复杂的检索策略，如查询重写、查询扩展、多步检索、以及通过智能体的 **思考-行动-观察** 循环进行动态、迭代式的信息搜集与初步分析。深度搜索的核心在于优化检索环节，通过更智能、更具韧性的检索过程，提升对复杂、多跳或需要全局理解问题的上下文获取能力，旨在为用户提供更精确、更相关的答案。

**深度研究（Deep Research）** 则代表了当前演进的前沿。它建立在深度搜索的基础之上，但目标更为宏大，不仅追求信息的精确获取，更强调 **深度分析、复杂推理、综合洞察和工具使用**。其显著特征包括：
1. **引入推理（思考）模型**：利用如 OpenAI o1、DeepSeek-R1、Gemini 2.0 Flash Thinking 等模型，通过增加“推理时计算”换取更高质量、更具洞察力的分析结果，用户愿意接受更长的等待时间以获得“延迟满足”带来的优质内容；
2. **更强大的智能体能力**：集成了更广泛的工具使用（如操作浏览器、执行代码、与操作系统交互）和更复杂的任务规划与分解能力；
3. **聚焦复杂任务与报告生成**：更擅长处理需要跨领域知识整合、深度行业分析、复杂问题求解、长篇报告撰写等研究型任务，扮演着“研究助理”的角色。

从 AI + 搜索到深度搜索，再到深度研究，我们见证了 AI 从简单的信息搬运工，逐步进化为能够进行初步分析的助手，最终迈向能够独立执行复杂研究任务的智能伙伴。这一演进的核心驱动力在于不断克服前一阶段的技术瓶颈，并通过引入更先进的 RAG 技术、智能体框架以及推理模型，持续提升 AI 理解、规划、执行和生成复杂内容的能力。未来，随着技术的不断融合与创新，我们有望看到更加智能、自主的研究型 AI 应用涌现。

## 参考

* [PLZ，别再误解大模型联网搜索了](https://www.53ai.com/news/LargeLanguageModel/2025032069843.html)
* [Introducing ChatGPT search](https://openai.com/index/introducing-chatgpt-search/)
* [Claude can now search the web](https://www.anthropic.com/news/web-search)
* [AI Overviews in Search are coming to more places around the world](https://blog.google/products/search/ai-overviews-search-october-2024/)
* [Grok 3 Beta — The Age of Reasoning Agents](https://x.ai/news/grok-3)
* [Introducing computer use, a new Claude 3.5 Sonnet, and Claude 3.5 Haiku](https://www.anthropic.com/news/3-5-models-and-computer-use)
* [Try Deep Research and our new experimental model in Gemini, your AI assistant](https://blog.google/products/gemini/google-gemini-deep-research/)
* [Open-source DeepResearch – Freeing our search agents](https://huggingface.co/blog/open-deep-research)
* [「三小时复刻 Manus，GitHub 2 万星」：OpenManus 多智能体框架的技术拆解](https://mp.weixin.qq.com/s/4Ai2QPYxvD5AVUUz01N0aw)

### Search

* [YOU.COM](https://you.com/)
* [iAsk](https://iask.ai/)
* [Lepton Search](https://search.lepton.run/)
* [Onion AI Search](https://onionai.so/)
* [Scira AI](https://scira.ai/)
* [思·索 MindSearch](https://mindsearch.netlify.app/)
* [Farfalle](https://www.farfalle.dev/)
* [Kagi FastGPT](https://kagi.com/fastgpt)

---

* [Github - zaidmukaddam/scira](https://github.com/zaidmukaddam/scira)
* [Github - rashadphz/farfalle](https://github.com/rashadphz/farfalle)
* [Github - nilsherzig/LLocalSearch](https://github.com/nilsherzig/LLocalSearch)
* [Github - nashsu/FreeAskInternet](https://github.com/nashsu/FreeAskInternet)
* [Github - InternLM/MindSearch](https://github.com/InternLM/MindSearch)

### Deep Search

* [Jina 深度搜索](https://jina.ai/deepsearch/)
* [天工 AI 搜索](https://www.tiangong.cn/)
* [秘塔](https://metaso.cn/)
* [Perplexity](https://www.perplexity.ai/)

---

* [Github - jina-ai/node-DeepResearch](https://github.com/jina-ai/node-DeepResearch)
* [Github - zilliztech/deep-searcher](https://github.com/zilliztech/deep-searcher)

### Deep Research

* [Introducing Operator](https://openai.com/index/introducing-operator/)
* [Introducing deep research](https://openai.com/index/introducing-deep-research/)
* [Introducing Perplexity Deep Research](https://www.perplexity.ai/hub/blog/introducing-perplexity-deep-research)
* [Sider Deep Research](https://sider.ai/wisebase/deep-research)
* [Manus](https://manus.im/)
* [AutoGLM 沉思](https://autoglm-research.zhipuai.cn/)

---

* [GitHub - assafelovic/gpt-researcher](https://github.com/assafelovic/gpt-researcher)
* [Github - dzhng/deep-research](https://github.com/dzhng/deep-research)
* [Github - sentient-agi/OpenDeepSearch](https://github.com/sentient-agi/OpenDeepSearch)
* [Github - nickscamara/open-deep-research](https://github.com/nickscamara/open-deep-research)
* [Github - langchain-ai/open_deep_research](https://github.com/langchain-ai/open_deep_research)
* [Github - langchain-ai/local-deep-researcher](https://github.com/langchain-ai/local-deep-researcher)
* [Github - mannaandpoem/OpenManus](https://github.com/mannaandpoem/OpenManus)
* [Github - stanford-oval/storm](https://github.com/stanford-oval/storm)
* [Github - binary-husky/gpt_academic](https://github.com/binary-husky/gpt_academic)
* [Github - mshumer/OpenDeepResearcher](https://github.com/mshumer/OpenDeepResearcher)
* [Github - camel-ai/owl](https://github.com/camel-ai/owl)
* [Github - browser-use/browser-use](https://github.com/browser-use/browser-use)