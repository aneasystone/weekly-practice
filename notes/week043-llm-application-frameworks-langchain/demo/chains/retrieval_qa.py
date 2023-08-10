from qdrant import init_qdrant

qdrant = init_qdrant('./kb.txt', "127.0.0.1:6333")

from langchain.chains import RetrievalQA
from langchain.llms import OpenAI

qa = RetrievalQA.from_chain_type(llm=OpenAI(), chain_type="stuff", retriever=qdrant.as_retriever())
query = "小明家的宠物狗比小红家的大几岁？"
result = qa.run(query)
print(result)

# 毛毛比大白大两岁，毛毛今年3岁，大白今年1岁。
