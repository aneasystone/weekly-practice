from llama_index.core import SimpleDirectoryReader

# load the documents
documents = SimpleDirectoryReader("./data").load_data()

from llama_index.graph_stores.neo4j import Neo4jGraphStore
from llama_index.core import StorageContext

# define neo4j graph store
graph_store = Neo4jGraphStore(
    username="neo4j",
    password="password",
    url="bolt://localhost:7687",
    database="neo4j",
)
storage_context = StorageContext.from_defaults(graph_store=graph_store)

# init graph data, this can take a while!
from llama_index.core import KnowledgeGraphIndex
index = KnowledgeGraphIndex.from_documents(
    documents,
    storage_context=storage_context,
    max_triplets_per_chunk=2,
)
