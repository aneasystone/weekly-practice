from llama_index.core import Document
docs = [Document(text="This is a very very long text.")]

from llama_index.core.node_parser import TokenTextSplitter
splitter = TokenTextSplitter(
    separator=" ",
    chunk_size=512,
    chunk_overlap=0
)
nodes = splitter.get_nodes_from_documents(documents)
for node in nodes:
    print(node)

from llama_index.core.node_parser import SentenceSplitter
node_parser = SentenceSplitter(
    separator=" ",
    paragraph_separator="\n\n",
    chunk_size=512, 
    chunk_overlap=0
)
nodes = node_parser.get_nodes_from_documents(docs, show_progress=False)
for node in nodes:
    print(node)
