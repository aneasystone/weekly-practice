import openai

# 使用 OpenAI Embedding
def embedder(text: str) -> list[float]:
    return openai.embeddings.create(
        input=text, model="text-embedding-3-small"
    ).data[0].embedding

# 连接 LanceDB 数据库
from graphrag.vector_stores.lancedb import LanceDBVectorStore
vector_store = LanceDBVectorStore(collection_name="default-entity-description")
vector_store.connect(db_uri="./ragtest/output/lancedb")

# 向量相似性检索
results = vector_store.similarity_search_by_text(
    "Who is Scrooge?", embedder, k=2
)
print(results)

# 连接 LanceDB 数据库

import lancedb
db_connection = lancedb.connect("./ragtest/output/lancedb")
document_collection = db_connection.open_table("default-entity-description")

# 向量相似性检索
docs = document_collection.search(
    query=embedder("Who is Scrooge?"), vector_column_name="vector"
).limit(2).to_list()
print(docs)
