from langchain.embeddings.openai import OpenAIEmbeddings
embeddings = OpenAIEmbeddings()

doc_result = embeddings.embed_documents(['你好', '再见'])
print(doc_result)

query_result = embeddings.embed_query('你好吗')
print(query_result)
