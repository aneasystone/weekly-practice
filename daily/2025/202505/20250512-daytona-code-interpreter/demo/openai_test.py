from dotenv import load_dotenv
load_dotenv()

import os
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_API_BASE = os.getenv("OPENAI_API_BASE")

from openai import OpenAI
client = OpenAI(api_key=OPENAI_API_KEY, base_url=OPENAI_API_BASE)
completion = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {
            "role": "system", 
            "content": "你是一个翻译助手，请将用户提供的中文翻译成英文。"
        },
        {
            "role": "user",
            "content": "你好",
        },
    ],
)

print(completion.choices[0].message.content)
