from llama_index.core import SimpleDirectoryReader
from llama_index.core.node_parser import SentenceSplitter
from llama_index.retrievers.bm25 import BM25Retriever

# load documents
documents = SimpleDirectoryReader("./data").load_data()
splitter = SentenceSplitter(chunk_size=1024)
nodes = splitter.get_nodes_from_documents(documents)

# We can pass in the index, doctore, or list of nodes to create the retriever
retriever = BM25Retriever.from_defaults(nodes=nodes, similarity_top_k=2)

# will retrieve context from specific companies
nodes = retriever.retrieve("What happened at Viaweb and Interleaf?")
for node in nodes:
    print(node)
    