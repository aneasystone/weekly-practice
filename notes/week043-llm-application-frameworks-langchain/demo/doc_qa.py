from langchain.document_loaders import TextLoader

loader = TextLoader("./kb.txt")
raw_documents = loader.load()
print(raw_documents)

from langchain.text_splitter import CharacterTextSplitter
text_splitter = CharacterTextSplitter(        
    separator = "\n",
    chunk_size = 0,
    chunk_overlap  = 0,
    length_function = len,
)
documents = text_splitter.split_documents(raw_documents)
print(documents)

from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Qdrant

qdrant = Qdrant.from_documents(
    documents,
    OpenAIEmbeddings(),
    url="127.0.0.1:6333",
    prefer_grpc=False,
    collection_name="my_documents",
)

query = "小明家的宠物狗叫什么名字？"
found_docs = qdrant.similarity_search(query)
print(found_docs)
