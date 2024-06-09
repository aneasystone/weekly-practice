# load documents
from llama_index.core import SimpleDirectoryReader
documents = SimpleDirectoryReader("./data").load_data()

# build index
from llama_index.core import VectorStoreIndex
index = VectorStoreIndex.from_documents(documents)

# query with seo
from llama_index.core.postprocessor import SentenceEmbeddingOptimizer
query_engine = index.as_query_engine(
    node_postprocessors=[SentenceEmbeddingOptimizer(percentile_cutoff=0.5)]
)
res = query_engine.query("What is the population of Berlin?")
print(res)
