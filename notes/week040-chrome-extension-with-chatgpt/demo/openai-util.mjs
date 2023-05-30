import { Configuration, OpenAIApi } from "openai";
import { HttpsProxyAgent } from 'https-proxy-agent'
import dotenv from 'dotenv'

dotenv.config({ path: `.env.local`, override: true });

function createOpenAiClient() {
    const configuration = new Configuration({
        apiKey: process.env.OPENAI_API_KEY,
    });
    const openai = new OpenAIApi(configuration);
    return openai;
}

function createAxiosOptions() {
    return {
        proxy: false,
        httpAgent: new HttpsProxyAgent(process.env.HTTP_PROXY),
        httpsAgent: new HttpsProxyAgent(process.env.HTTP_PROXY)
    }
}

export {
	createOpenAiClient,
	createAxiosOptions
}
