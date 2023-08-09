from langchain import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)

prompt = ChatPromptTemplate(
    messages=[
        SystemMessagePromptTemplate.from_template("你是一个聊天助手，和人类进行聊天。"),
        MessagesPlaceholder(variable_name="history"),
        HumanMessagePromptTemplate.from_template("{input}")
    ]
)

chat = ChatOpenAI(temperature=0.9)

memory = ConversationBufferMemory(return_messages=True)

llm_chain = LLMChain(
    llm = chat, 
    prompt = prompt,
    memory = memory,
    verbose=True
)

result = llm_chain("窗前明月光，下一句是什么？")
print(result['text'])

result = llm_chain("这是谁的诗？")
print(result['text'])
