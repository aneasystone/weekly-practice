from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Qdrant

def init_qdrant(file, qdrant_url):

	loader = TextLoader(file)
	raw_documents = loader.load()
	print(raw_documents)

	text_splitter = CharacterTextSplitter(
		separator = "\n",
		chunk_size = 0,
		chunk_overlap  = 0,
		length_function = len,
	)
	documents = text_splitter.split_documents(raw_documents)
	print(documents)

	qdrant = Qdrant.from_documents(
		documents,
		OpenAIEmbeddings(),
		url=qdrant_url,
		prefer_grpc=False,
		collection_name="my_documents",
	)
	return qdrant
