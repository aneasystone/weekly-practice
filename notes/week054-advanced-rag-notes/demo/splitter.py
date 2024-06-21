text = "Hello world\n\nHello world"

from langchain.text_splitter import CharacterTextSplitter
text_splitter = CharacterTextSplitter(
    separator = "\n\n",
    chunk_size = 20,
    chunk_overlap  = 0,
    length_function=len,
    is_separator_regex=False,
)
docs = text_splitter.create_documents([text])
print(docs)

from langchain_text_splitters import RecursiveCharacterTextSplitter
text_splitter = RecursiveCharacterTextSplitter(
    separators = ["\n\n", "\n", " ", ""],
    chunk_size = 20,
    chunk_overlap = 0,
    length_function = len,
    is_separator_regex = False,
)
docs = text_splitter.create_documents([text])
print(docs)

from langchain_text_splitters import TokenTextSplitter
text_splitter = TokenTextSplitter(
    model_name="gpt-4",
    chunk_size=10,
    chunk_overlap=0
)
docs = text_splitter.create_documents([text])
print(docs)
