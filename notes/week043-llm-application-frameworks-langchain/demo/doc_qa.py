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
embeddings = OpenAIEmbeddings()

# query_result = embeddings.embed_query(query)
# doc_result = embeddings.embed_documents(docs)

from langchain.vectorstores import Qdrant
qdrant = Qdrant.from_documents(
    documents,
    embeddings,
    url="127.0.0.1:6333",
    prefer_grpc=False,
    collection_name="my_documents",
)
