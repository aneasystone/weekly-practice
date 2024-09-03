from langchain_openai import ChatOpenAI

llm = ChatOpenAI()
res = llm.invoke("What's your name?")
print(res)
