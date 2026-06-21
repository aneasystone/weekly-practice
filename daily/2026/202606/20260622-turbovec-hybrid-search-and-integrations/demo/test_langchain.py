from langchain_huggingface import HuggingFaceEmbeddings
from turbovec.langchain import TurboQuantVectorStore

# 一批待检索的文档，实际项目里通常来自知识库或文档切片
texts = [
    "TurboQuant is a data-oblivious vector quantizer that needs no training phase.",
    "Product Quantization must train a codebook on representative data before adding vectors.",
    "FAISS is Meta's open-source library for efficient vector similarity search.",
    "HNSW is a graph-based algorithm for approximate nearest neighbor search.",
    "An inverted index is the core data structure of traditional full-text search.",
    "BM25 is a classic keyword-based ranking function used for first-stage retrieval.",
    "Hybrid retrieval combines keyword filtering with dense vector reranking.",
    "RAG augments large language models with knowledge retrieved from external sources.",
    "A vector database stores and searches high-dimensional embedding vectors.",
    "Cosine similarity measures how close the directions of two vectors are.",
]

embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-base-en-v1.5")
store = TurboQuantVectorStore.from_texts(
    texts=texts,
    embedding=embeddings,
    bit_width=4,
)
retriever = store.as_retriever(search_kwargs={"k": 3})

# 检索与查询语义最相关的前 3 条文档
docs = retriever.invoke("a quantization method that compresses vectors without training")
for i, doc in enumerate(docs, 1):
    print(f"{i}. {doc.page_content}")
