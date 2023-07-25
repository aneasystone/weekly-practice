from langchain.chat_models import ChatOpenAI
from langchain.schema import AIMessage, HumanMessage, SystemMessage

chat = ChatOpenAI(temperature=0.9)
response = chat.predict_messages([
    HumanMessage(content="窗前明月光，下一句是什么？"),
])
print(response.content)

# 疑是地上霜。

chat = ChatOpenAI(temperature=0.9)
response = chat.predict_messages([
    SystemMessage(content="你是一个诗词助手，帮助用户回答诗词方面的问题"),
    HumanMessage(content="窗前明月光，下一句是什么？"),
    AIMessage(content="疑是地上霜。"),
    HumanMessage(content="这是谁的诗？"),
])
print(response.content)

# 这是李白的《静夜思》。

response = chat.predict("给水果店取一个名字")
print(response)

# 果香居

response = chat.predict("将下面的句子翻译成英文：今天的天气真不错")
print(response)

# The weather is really nice today.

response = chat.predict_messages([
    SystemMessage(content="你是一个翻译助手，可以将中文翻译成英文。"),
    HumanMessage(content="今天的天气真不错"),
])
print(response.content)

# The weather is really nice today.
