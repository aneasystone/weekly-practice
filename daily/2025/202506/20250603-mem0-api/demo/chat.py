
import os
from mem0.proxy.main import Mem0

client = Mem0(api_key=os.environ.get("MEM0_API_KEY"))

# messages = [{
#     "role": "user",
#     "content": "我喜欢四川美食，但是我对辣过敏，不能吃辣"
# }]
# chat_completion = client.chat.completions.create(
#     messages=messages, model="gpt-4o-mini", user_id="lisi"
# )
# print(chat_completion.choices[0].message.content)

messages = [{
    "role": "user",
    "content": "给我推荐一些四川美食",
}]
chat_completion = client.chat.completions.create(
    messages=messages, model="gpt-4o-mini", user_id="lisi"
)
print(chat_completion.choices[0].message.content)