import { createOpenAiClient, createAxiosOptions } from './openai-util.mjs'

const openai = createOpenAiClient();
const response = await openai.listModels(createAxiosOptions());
console.log(response.data);
