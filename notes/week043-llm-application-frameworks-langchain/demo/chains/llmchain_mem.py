from langchain import PromptTemplate, OpenAI, LLMChain
from langchain.memory import ConversationBufferMemory

llm = OpenAI(temperature=0.9)

template = """
下面是一段人类和人工智能之间的友好对话。

当前对话内容：
{history}
Human: {input}
AI:"""
prompt = PromptTemplate(input_variables=["history", "input"], template=template)
memory = ConversationBufferMemory()

llm_chain = LLMChain(
    llm = llm, 
    prompt = prompt,
    memory = memory
)

result = llm_chain("窗前明月光，下一句是什么？")
print(result['text'])

result = llm_chain("这是谁的诗？")
print(result['text'])
