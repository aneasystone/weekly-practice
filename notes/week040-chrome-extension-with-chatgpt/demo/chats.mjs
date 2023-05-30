import { createOpenAiClient, createAxiosOptions } from './openai-util.mjs'

const openai = createOpenAiClient();
const response = await openai.createChatCompletion({
    "model": "gpt-3.5-turbo",
    "messages": [{"role": "user", "content": "你好"}]
  }, createAxiosOptions());
console.log(response.data.choices);
