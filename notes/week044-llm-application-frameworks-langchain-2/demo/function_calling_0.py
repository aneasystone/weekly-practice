import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

completion = openai.ChatCompletion.create(
    temperature=0.7,
    model="gpt-3.5-turbo",
    messages=[
        {'role': 'user', 'content': "今天是星期几？"},
    ],
)
print(completion.choices[0].message.content)

# 很抱歉，我无法回答您的问题，因为我没有时间概念。
# 请您查看日历或使用手机或电脑上的时间显示来获取今天是星期几的信息。
