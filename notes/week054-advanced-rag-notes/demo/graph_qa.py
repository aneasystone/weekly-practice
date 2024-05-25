from langchain_community.graphs import Neo4jGraph

graph = Neo4jGraph(url="bolt://localhost:7687", username="neo4j", password="password")

from langchain_openai import ChatOpenAI
from langchain.chains import GraphCypherQAChain

chain = GraphCypherQAChain.from_llm(
    ChatOpenAI(temperature=0), graph=graph, verbose=True
)
response = chain.invoke({"query": "Who played in Top Gun?"})
print(response)
