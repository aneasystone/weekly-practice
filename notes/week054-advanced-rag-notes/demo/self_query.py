from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings

docs = [
    Document(
        page_content="A bunch of scientists bring back dinosaurs and mayhem breaks loose",
        metadata={"year": 1993, "rating": 7.7, "genre": "science fiction"},
    ),
    Document(
        page_content="Leo DiCaprio gets lost in a dream within a dream within a dream within a ...",
        metadata={"year": 2010, "director": "Christopher Nolan", "rating": 8.2},
    ),
    Document(
        page_content="A psychologist / detective gets lost in a series of dreams within dreams within dreams and Inception reused the idea",
        metadata={"year": 2006, "director": "Satoshi Kon", "rating": 8.6},
    ),
    Document(
        page_content="A bunch of normal-sized women are supremely wholesome and some men pine after them",
        metadata={"year": 2019, "director": "Greta Gerwig", "rating": 8.3},
    ),
    Document(
        page_content="Toys come alive and have a blast doing so",
        metadata={"year": 1995, "genre": "animated"},
    ),
    Document(
        page_content="Three men walk into the Zone, three men walk out of the Zone",
        metadata={"year": 1979, "director": "Andrei Tarkovsky", "genre": "thriller", "rating": 9.9},
    ),
]
vectorstore = Chroma.from_documents(docs, OpenAIEmbeddings())

###

from langchain.chains.query_constructor.base import AttributeInfo
from langchain.retrievers.self_query.base import SelfQueryRetriever
from langchain_openai import OpenAI

llm = OpenAI(temperature=0)

metadata_field_info = [
    AttributeInfo(name="genre", description="The genre of the movie", type="string or list[string]"),
    AttributeInfo(name="year", description="The year the movie was released", type="integer" ),
    AttributeInfo(name="director", description="The name of the movie director", type="string" ),
    AttributeInfo(name="rating", description="A 1-10 rating for the movie", type="float"),
]
document_content_description = "Brief summary of a movie"

retriever = SelfQueryRetriever.from_llm(
    llm, vectorstore, document_content_description, metadata_field_info, verbose=True
)

# This example only specifies a relevant query
response = retriever.invoke("What are some movies about dinosaurs")
print(response)
