from llama_index.core import SimpleDirectoryReader
from llama_index.core.node_parser import SentenceSplitter
from llama_index.retrievers.bm25 import BM25Retriever
from llama_index.core.schema import QueryBundle

# load documents
documents = SimpleDirectoryReader("./data").load_data()
splitter = SentenceSplitter(chunk_size=1024)
nodes = splitter.get_nodes_from_documents(documents)

# retrieve with bm25
query_str = "What happened at Viaweb and Interleaf?"
retriever = BM25Retriever.from_defaults(nodes=nodes, similarity_top_k=5)
nodes = retriever.retrieve(query_str)
for node in nodes:
    print(node)
    
print('--------------------')

# similarity post processor
from llama_index.core.postprocessor import SimilarityPostprocessor
postprocessor = SimilarityPostprocessor(similarity_cutoff=1.0)
postprocessor.postprocess_nodes(nodes)
nodes = postprocessor.postprocess_nodes(nodes)
for node in nodes:
    print(node)

# keyword node post processor (with spacy)
from llama_index.core.postprocessor import KeywordNodePostprocessor
postprocessor = KeywordNodePostprocessor(
    required_keywords=["Mike"],
    exclude_keywords=["philosophy"]
)
nodes = postprocessor.postprocess_nodes(nodes)
for node in nodes:
    print(node)

# fixed recency post processor
from llama_index.core.postprocessor import FixedRecencyPostprocessor
postprocessor = FixedRecencyPostprocessor(
    date_key="date", tok_k=1
)
nodes = postprocessor.postprocess_nodes(nodes)
for node in nodes:
    print(node)

# embedding recency post processor
from llama_index.core.postprocessor import EmbeddingRecencyPostprocessor
postprocessor = EmbeddingRecencyPostprocessor(
    date_key="date", similarity_cutoff=0.7
)
nodes = postprocessor.postprocess_nodes(nodes)
for node in nodes:
    print(node)

# time weighted post processor
from llama_index.core.postprocessor import TimeWeightedPostprocessor
postprocessor = TimeWeightedPostprocessor(
    time_decay=0.99, top_k=1
)
nodes = postprocessor.postprocess_nodes(nodes)
for node in nodes:
    print(node)

# prev next node post processor
from llama_index.core.postprocessor import PrevNextNodePostprocessor
postprocessor = PrevNextNodePostprocessor(
    docstore=index.docstore,
    num_nodes=1,  # number of nodes to fetch when looking forawrds or backwards
    mode="next",  # can be either 'next', 'previous', or 'both'
)
nodes = postprocessor.postprocess_nodes(nodes)
for node in nodes:
    print(node)

# long context reorder
from llama_index.core.postprocessor import LongContextReorder
postprocessor = LongContextReorder()
nodes = postprocessor.postprocess_nodes(nodes)
for node in nodes:
    print(node)
