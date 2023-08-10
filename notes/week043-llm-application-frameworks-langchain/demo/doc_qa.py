from chains.qdrant import init_qdrant

qdrant = init_qdrant('./kb.txt', "127.0.0.1:6333")

query = "小明家的宠物狗叫什么名字？"
found_docs = qdrant.similarity_search(query)
print(found_docs)
