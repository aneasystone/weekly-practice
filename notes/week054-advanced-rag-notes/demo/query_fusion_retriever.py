from llama_index.core import SimpleDirectoryReader

documents = SimpleDirectoryReader("./data/").load_data()

from llama_index.core import VectorStoreIndex
from llama_index.core.node_parser import SentenceSplitter

splitter = SentenceSplitter(chunk_size=256)
index = VectorStoreIndex.from_documents(documents, transformations=[splitter])

from llama_index.retrievers.bm25 import BM25Retriever

vector_retriever = index.as_retriever(similarity_top_k=2)

bm25_retriever = BM25Retriever.from_defaults(
    docstore=index.docstore, similarity_top_k=2
)

from llama_index.core.retrievers import QueryFusionRetriever

retriever = QueryFusionRetriever(
    [vector_retriever, bm25_retriever],
    similarity_top_k=2,
    num_queries=4,  # set this to 1 to disable query generation
    mode="reciprocal_rerank",
    use_async=True,
    verbose=True,
    # query_gen_prompt="...",  # we could override the query generation prompt here
)

nodes_with_scores = retriever.retrieve(
    "What happened at Interleafe and Viaweb?"
)
for node in nodes_with_scores:
    print(f"Score: {node.score:.2f} - {node.text}...\n-----\n")
