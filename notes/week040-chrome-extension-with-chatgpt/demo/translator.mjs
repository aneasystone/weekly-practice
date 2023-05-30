import { createOpenAiClient, createAxiosOptions } from './openai-util.mjs'

async function translate(text) {

    const prompt = `Translate this into Simplified Chinese:\n\n${text}\n\n`
    
    const openai = createOpenAiClient();
    const response = await openai.createCompletion({
        "model": "text-davinci-003",
        "prompt": prompt,
        "max_tokens": 100,
        "temperature": 0
    }, createAxiosOptions());
    return response.data.choices[0].text
}

console.log(await translate("The OpenAI API can be applied to virtually any task that involves understanding or generating natural language, code, or images."));

console.log(await translate("どの部屋が利用可能ですか？"));
