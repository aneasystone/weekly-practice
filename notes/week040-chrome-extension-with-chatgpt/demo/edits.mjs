import { createOpenAiClient, createAxiosOptions } from './openai-util.mjs'

const openai = createOpenAiClient();
const response = await openai.createEdit({
  "model": "text-davinci-edit-001",
  "input": "金天的天气怎么样？",
  "instruction": "修改输入中的错别字",
}, createAxiosOptions());
console.log(response.data);
