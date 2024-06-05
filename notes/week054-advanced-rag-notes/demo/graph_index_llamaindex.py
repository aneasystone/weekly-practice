import logging
import sys

logging.basicConfig(
    stream=sys.stdout, level=logging.INFO
)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

from llama_index.llms.openai import OpenAI

llm = OpenAI(temperature=0.1, model="gpt-3.5-turbo")

from llama_index.graph_stores.neo4j import Neo4jGraphStore
from llama_index.core import StorageContext

# define neo4j graph store
graph_store = Neo4jGraphStore(
    username="neo4j",
    password="password",
    url="bolt://localhost:7687",
    database="neo4j",
)
storage_context = StorageContext.from_defaults(graph_store=graph_store)

# Initialize query engine

# from llama_index.core import KnowledgeGraphIndex
# index = KnowledgeGraphIndex.from_documents([], storage_context=storage_context)
# query_engine = index.as_query_engine(
#     include_text=True, response_mode="tree_summarize"
# )

# from llama_index.core.query_engine import RetrieverQueryEngine
# from llama_index.core.retrievers import KnowledgeGraphRAGRetriever
# graph_rag_retriever = KnowledgeGraphRAGRetriever(storage_context=storage_context, verbose=True)
# query_engine = RetrieverQueryEngine.from_args(
#     graph_rag_retriever,
# )

from llama_index.core.prompts.base import PromptTemplate, PromptType

# Define your custom prompt templates
graph_query_synthesis_prompt = PromptTemplate(
    """You are a Graph database expert. You are given a question that requires information retrieval from a Neo4j knowledge graph. \n
    Generate a precise Cypher query that retrieves the relevant information needed to answer the question. 
    """,
    prompt_type=PromptType.QUESTION_ANSWER,
)

from llama_index.core.query_engine import KnowledgeGraphQueryEngine
query_engine = KnowledgeGraphQueryEngine(
    storage_context=storage_context,
    llm=llm,
    graph_query_synthesis_prompt=graph_query_synthesis_prompt,
    verbose=True,
)
response = query_engine.generate_query("Tell me more about Interleaf")
print(response)

# Querying the Knowledge Graph
# response = query_engine.query("Tell me more about Interleaf")
# print(response)
