from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS

def init_faiss_db(file):

	loader = TextLoader(file)
	raw_documents = loader.load()
	# print(raw_documents)

	text_splitter = CharacterTextSplitter(
		separator = "\n",
		chunk_size = 0,
		chunk_overlap  = 0,
		length_function = len,
	)
	documents = text_splitter.split_documents(raw_documents)
	# print(documents)

	faiss_db = FAISS.from_documents(documents, OpenAIEmbeddings())	
	return faiss_db
