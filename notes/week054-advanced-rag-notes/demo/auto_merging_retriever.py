from pathlib import Path
from llama_index.readers.file import PyMuPDFReader

# download from https://arxiv.org/pdf/2307.09288.pdf
loader = PyMuPDFReader()
docs = loader.load(file_path=Path("./data/llama2.pdf"))
print(len(docs))

# the PDF reader creates a separate doc for each page
# we stitch docs together into one doc
from llama_index.core import Document
doc_text = "\n\n".join([d.get_content() for d in docs])
docs = [Document(text=doc_text)]
print(len(docs))

# use `HierarchicalNodeParser` to construct a hierarchy of nodes, 
# from top-level nodes with bigger chunk sizes to child nodes with smaller chunk sizes, 
# where each child node has a parent node with a bigger chunk size.
# By default, the hierarchy is:
#   1st level: chunk size 2048
#   2nd level: chunk size 512
#   3rd level: chunk size 128
from llama_index.core.node_parser import HierarchicalNodeParser
from llama_index.core.node_parser import get_leaf_nodes, get_root_nodes
node_parser = HierarchicalNodeParser.from_defaults()
nodes = node_parser.get_nodes_from_documents(docs)
print(len(nodes))
leaf_nodes = get_leaf_nodes(nodes)
print(len(leaf_nodes))
root_nodes = get_root_nodes(nodes)
print(len(root_nodes))

# define a `SimpleDocumentStore` loading all nodes
from llama_index.core.storage.docstore import SimpleDocumentStore
from llama_index.core import StorageContext
docstore = SimpleDocumentStore()
docstore.add_documents(nodes)
storage_context = StorageContext.from_defaults(docstore=docstore)

# define a `VectorStoreIndex` containing just the leaf-level nodes
from llama_index.core import VectorStoreIndex
base_index = VectorStoreIndex(leaf_nodes, storage_context=storage_context)
base_retriever = base_index.as_retriever(similarity_top_k=6)

# define the `AutoMergingRetriever`
from llama_index.core.retrievers import AutoMergingRetriever
retriever = AutoMergingRetriever(base_retriever, storage_context, verbose=True)
query_str = (
    "What could be the potential outcomes of adjusting the amount of safety"
    " data used in the RLHF stage?"
)
nodes = retriever.retrieve(query_str)
print(len(nodes))
base_nodes = base_retriever.retrieve(query_str)
print(len(base_nodes))
