from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory

chat = ChatOpenAI(temperature=0.9)
memory = ConversationBufferMemory()

conversation = ConversationChain(
    llm = chat,
    memory = memory
)

result = conversation.run("窗前明月光，下一句是什么？")
print(result)

# 疑是地上霜。

result = conversation.run("这是谁的诗？")
print(result)

# 这是李白的《静夜思》。
