import { createOpenAiClient, createAxiosOptions } from './openai-util.mjs'

const openai = createOpenAiClient();
const response = await openai.createCompletion({
	"model": "text-davinci-003",
    "prompt": "你好",
    "max_tokens": 100,
    "temperature": 0
}, createAxiosOptions());
console.log(response.data);
