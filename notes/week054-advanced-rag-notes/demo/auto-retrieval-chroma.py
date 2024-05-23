import logging
import sys

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

import chromadb

chroma_client = chromadb.EphemeralClient()
chroma_collection = chroma_client.create_collection("quickstart")

from llama_index.core import VectorStoreIndex, StorageContext
from llama_index.vector_stores.chroma import ChromaVectorStore

from llama_index.core.schema import TextNode

nodes = [
    TextNode(
        text=(
            "Michael Jordan is a retired professional basketball player,"
            " widely regarded as one of the greatest basketball players of all"
            " time."
        ),
        metadata={
            "category": "Sports",
            "country": "United States",
        },
    ),
    TextNode(
        text=(
            "Angelina Jolie is an American actress, filmmaker, and"
            " humanitarian. She has received numerous awards for her acting"
            " and is known for her philanthropic work."
        ),
        metadata={
            "category": "Entertainment",
            "country": "United States",
        },
    ),
    TextNode(
        text=(
            "Elon Musk is a business magnate, industrial designer, and"
            " engineer. He is the founder, CEO, and lead designer of SpaceX,"
            " Tesla, Inc., Neuralink, and The Boring Company."
        ),
        metadata={
            "category": "Business",
            "country": "United States",
        },
    ),
    TextNode(
        text=(
            "Rihanna is a Barbadian singer, actress, and businesswoman. She"
            " has achieved significant success in the music industry and is"
            " known for her versatile musical style."
        ),
        metadata={
            "category": "Music",
            "country": "Barbados",
        },
    ),
    TextNode(
        text=(
            "Cristiano Ronaldo is a Portuguese professional footballer who is"
            " considered one of the greatest football players of all time. He"
            " has won numerous awards and set multiple records during his"
            " career."
        ),
        metadata={
            "category": "Sports",
            "country": "Portugal",
        },
    ),
]

vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
storage_context = StorageContext.from_defaults(vector_store=vector_store)
index = VectorStoreIndex(nodes, storage_context=storage_context)

from llama_index.core.vector_stores.types import MetadataInfo, VectorStoreInfo
from llama_index.core.retrievers import VectorIndexAutoRetriever

vector_store_info = VectorStoreInfo(
    content_info="brief biography of celebrities",
    metadata_info=[
        MetadataInfo(name="category", type="str", description="Category of the celebrity, one of [Sports, Entertainment, Business, Music]"),
        MetadataInfo(name="country", type="str", description="Country of the celebrity, one of [United States, Barbados, Portugal]"),
    ],
)

retriever = VectorIndexAutoRetriever(
    index, vector_store_info=vector_store_info
)

response = retriever.retrieve("Tell me about Sports celebrities from United States")
print(response)

# from llama_index.indices.managed.vectara import VectaraAutoRetriever
