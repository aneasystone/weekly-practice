# WEEK040 - 基于 ChatGPT 实现一个划词翻译 Chrome 插件

去年 11 月，美国的 [OpenAI](https://openai.com/) 公司推出了 [ChatGPT](https://chat.openai.com/) 产品，它在发布后的 5 天内用户数就突破了 100 万，两个月后月活用户突破了 1 个亿，成为至今为止人类历史上用户数增长最快的消费级应用。ChatGPT 之所以能在全球范围内火出天际，不仅是因为它能以逼近自然语言的能力和人类对话，而且可以根据不同的提示语解决各种不同场景下的问题，它的推理能力、归纳能力、以及多轮对话能力都让世人惊叹不已，让实现通用人工智能（AGI，Artificial General Intelligence）变成为了现实，也意味着一种新型的人机交互接口由此诞生，这为更智能的 AI 产品提供了无限可能。

很快，OpenAI 推出了相应的 API 接口，所有人都可以基于这套 API 快速实现一个类似 ChatGPT 这样的产品，当然，聊天对话只是这套 API 的基本能力，OpenAI 官方网站有一个 [Examples 页面](https://platform.openai.com/examples)，展示了结合不同的提示语 OpenAI API 在更多场景下的应用：

![](./images/chatgpt-examples.png)

## OpenAI API 快速入门

OpenAI 提供了很多和 AI 相关的接口，如下：

* [Models](https://platform.openai.com/docs/api-reference/models) - 用于列出所有可用的模型；
* [Completions](https://platform.openai.com/docs/api-reference/completions) - 给定一个提示语，让 AI 生成后续内容；
* [Chat](https://platform.openai.com/docs/api-reference/chat) - 给定一系列对话内容，让 AI 生成对应的回复，使用这个接口就可以实现类似 ChatGPT 的功能；
* [Edits](https://platform.openai.com/docs/api-reference/edits) - 给定一个提示语和一条指令，AI 将对提示语进行相应的修改，比如常见的语法纠错场景； 
* [Images](https://platform.openai.com/docs/api-reference/images) - 用于根据提示语生成图片，或对图片进行编辑，可以实现类似于 [Stable Diffusion](https://github.com/CompVis/stable-diffusion) 或 [Midjourney](https://www.midjourney.com/home/) 这样的 AI 绘画应用，这个接口使用的是 OpenAI 的图片生成模型 [DALL·E](https://platform.openai.com/docs/models/dall-e)；
* [Embeddings](https://platform.openai.com/docs/api-reference/embeddings) - 用于获取一个给定文本的向量表示，我们可以将结果保存到一个向量数据库中，一般用于搜索、推荐、分类、聚类等任务；
* [Audio](https://platform.openai.com/docs/api-reference/audio) - 提供了语音转文本的功能，使用了 OpenAI 的 [Whisper](https://openai.com/research/whisper) 模型；
* [Files](https://platform.openai.com/docs/api-reference/files) - 文件管理类接口，便于用户上传自己的文件进行 Fine-tuning；
* [Fine-tunes](https://platform.openai.com/docs/api-reference/fine-tunes) - 用于管理你的 Fine-tuning 任务，详细内容可参考 [Fine-tuning 教程](https://platform.openai.com/docs/guides/fine-tuning)；
* [Moderations](https://platform.openai.com/docs/api-reference/moderations) - 用于判断给定的提示语是否违反 OpenAI 的内容政策；

关于 API 的详细内容可以参考官方的 [API reference](https://platform.openai.com/docs/api-reference) 和 [Documentation](https://platform.openai.com/docs/introduction)。

其中，`Completions`、`Chat` 和 `Edits` 这三个接口都可以用于对话任务，`Completions` 主要解决的是补全问题，也就是说用户给出一段话，模型可以按照提示语续写后面的内容；`Chat` 用于处理聊天任务，它显式的定义了 `system`、`user` 和 `assistant` 三个角色，方便维护对话的语境信息和多轮对话的历史记录；`Edit` 主要用于对用户的输入进行修改和纠正。

要调用 OpenAI 的 API 接口，必须先创建你的 [API Keys](https://platform.openai.com/account/api-keys)，然后请求时像下面这样带上 `Authorization` 头即可：

```
Authorization: Bearer OPENAI_API_KEY
```

下面是直接使用 curl 调用 `Completions` 接口的示例：

```
$ curl https://api.openai.com/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -d '{
     "model": "gpt-3.5-turbo",
     "messages": [{"role": "user", "content": "你好！"}],
     "temperature": 0.7
   }'
```

我们可以得到类似下面的回复：

```
{
  "id": "chatcmpl-7LgiOhYPcGGwoBcEPQmQ2LaO2pObn",
  "object": "chat.completion",
  "created": 1685403440,
  "model": "gpt-3.5-turbo-0301",
  "usage": {
    "prompt_tokens": 11,
    "completion_tokens": 18,
    "total_tokens": 29
  },
  "choices": [
    {
      "message": {
        "role": "assistant",
        "content": "你好！有什么我可以为您效劳的吗？"
      },
      "finish_reason": "stop",
      "index": 0
    }
  ]
}
```

> 如果你无法访问 OpenAI 的接口，或者没有 OpenAI 的 API Keys，网上也有很多免费的方法，比如 [chatanywhere/GPT_API_free](https://github.com/chatanywhere/GPT_API_free)。

OpenAI 官方提供了 Python 和 Node.js 的 SDK 方便我们在代码中调用 OpenAI 接口，下面是使用 Node.js 调用 `Completions` 的示例：

```
import { Configuration, OpenAIApi } from "openai";

const configuration = new Configuration({
    apiKey: process.env.OPENAI_API_KEY,
});
const openai = new OpenAIApi(configuration);

const response = await openai.createCompletion({
    "model": "text-davinci-003",
    "prompt": "你好！",
    "max_tokens": 100,
    "temperature": 0
});
console.log(response.data);
```

由于 SDK 底层使用了 axios 库发请求，所以我们还可以对 axios 进行配置，比如像下面这样设置代理：

```
const response = await openai.createCompletion({
    "model": "text-davinci-003",
    "prompt": "你好",
    "max_tokens": 100,
    "temperature": 0
}, {
    proxy: false,
    httpAgent: new HttpsProxyAgent(process.env.HTTP_PROXY),
    httpsAgent: new HttpsProxyAgent(process.env.HTTP_PROXY)
});
```

### 使用 OpenAI API 实现翻译功能

如果想实现翻译功能，使用 `Completions` 接口即可。

## Chrome 插件快速入门

### 一个简单的例子

### 实现划词翻译功能

## 参考

* [Documentation for Chrome extensions developers](https://developer.chrome.com/docs/extensions/)
* [有手就行，从零开始的V3版本Chrome创意插件开发攻略](https://juejin.cn/post/7121653349669142565)
* [GoogleChrome/chrome-extensions-samples](https://github.com/GoogleChrome/chrome-extensions-samples) - Chrome Extensions Samples
* [openai-translator/openai-translator](https://github.com/openai-translator/openai-translator) - 基于 ChatGPT API 的划词翻译浏览器插件和跨平台桌面端应用
* [CaTmmao/chrome-extension-translate](https://github.com/CaTmmao/chrome-extension-translate) - 谷歌插件划词翻译
