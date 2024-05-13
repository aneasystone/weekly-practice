# Build a sample vectorDB
from langchain_chroma import Chroma
from langchain_community.document_loaders import WebBaseLoader
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Load blog post
loader = WebBaseLoader("https://lilianweng.github.io/posts/2023-06-23-agent/")
data = loader.load()

# Split
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=0)
splits = text_splitter.split_documents(data)

# VectorDB
embedding = OpenAIEmbeddings()
vectordb = Chroma.from_documents(documents=splits, embedding=embedding)

from langchain.retrievers.multi_query import MultiQueryRetriever, LineListOutputParser
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_openai import ChatOpenAI

QUERY_PROMPT = PromptTemplate(
    input_variables=["question"],
    template="""你是一个 AI 语言助手，你的任务是将用户的问题拆解成多个子问题便于检索，多个子问题以换行分割，保证每行一个。
    用户的原始问题为：{question}""",
)

llm = ChatOpenAI(temperature=0)
output_parser = LineListOutputParser()
llm_chain = LLMChain(llm=llm, prompt=QUERY_PROMPT, output_parser=output_parser)
retriever = MultiQueryRetriever(
    retriever=vectordb.as_retriever(), llm_chain=llm_chain
)

# Set logging for the queries
import logging

logging.basicConfig()
logging.getLogger("langchain.retrievers.multi_query").setLevel(logging.INFO)

question = "微软和苹果哪一个成立时间更早？"
unique_docs = retriever.invoke(question)
print(len(unique_docs))
