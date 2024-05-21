import logging
import sys

# logging.basicConfig(stream=sys.stdout, level=logging.INFO)
# logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

from llama_index.core import PromptTemplate

text_to_sql_tmpl = """\
Given an input question, first create a syntactically correct {dialect} \
query to run, then look at the results of the query and return the answer. \
You can order the results by a relevant column to return the most \
interesting examples in the database.

Pay attention to use only the column names that you can see in the schema \
description. Be careful to not query for columns that do not exist. \
Pay attention to which column is in which table. Also, qualify column names \
with the table name when needed. 

IMPORTANT NOTE: you can use specialized pgvector syntax (`<->`) to do nearest \
neighbors/semantic search to a given vector from an embeddings column in the table. \
The embeddings value for a given row typically represents the semantic meaning of that row. \
The vector represents an embedding representation \
of the question, given below. Do NOT fill in the vector values directly, but rather specify a \
`[query_vector]` placeholder. For instance, some select statement examples below \
(the name of the embeddings column is `embedding`):
SELECT * FROM "items" ORDER BY embedding <-> '[query_vector]' LIMIT 5;
SELECT * FROM "items" WHERE id != 1 ORDER BY embedding <-> (SELECT embedding FROM "items" WHERE id = 1) LIMIT 5;
SELECT * FROM "items" WHERE embedding <-> '[query_vector]' < 5;

You are required to use the following format, \
each taking one line:

Question: Question here
SQLQuery: SQL Query to run
SQLResult: Result of the SQLQuery
Answer: Final answer here

Only use tables listed below.
{schema}


Question: {query_str}
SQLQuery: \
"""
text_to_sql_prompt = PromptTemplate(text_to_sql_tmpl)

response_synthesis_prompt_tmpl = (
    "Given an input question, synthesize a response from the query results.\n"
    "Query: {query_str}\n"
    "SQL: {sql_query}\n"
    "SQL Response: {sql_response_str}\n"
    "Response: "
)
response_synthesis_prompt = PromptTemplate(response_synthesis_prompt_tmpl)

from sqlalchemy import create_engine
from llama_index.core import SQLDatabase
from llama_index.llms.openai import OpenAI
from llama_index.core.query_engine import PGVectorSQLQueryEngine
from llama_index.core import Settings

engine = create_engine("postgresql+psycopg2://root:123456@localhost:5432/vectordb")
sql_database = SQLDatabase(engine, include_tables=["Track"])

Settings.llm = OpenAI(model="gpt-4")

table_desc = """\
This table represents trucks. Each row contains the following columns:

TrackId: id of row
Name: name of the track
embeddings: the embeddings representing the name

For most queries you should perform semantic search against the `embeddings` column values, since \
that encodes the meaning of the text.

"""

context_query_kwargs = {"Track": table_desc}

query_engine = PGVectorSQLQueryEngine(
    sql_database=sql_database,
    text_to_sql_prompt=text_to_sql_prompt,
    context_query_kwargs=context_query_kwargs,
    # sql_only=True,
    # verbose=True,
    
    # 开启响应合成后，超出大模型 token 限制
    # 不应该 pgvector 的 sql 送到大模型，可以将 sql 里的向量做个精简
    response_synthesis_prompt=response_synthesis_prompt,
    synthesize_response=True
)
response = query_engine.query(
    "Give me 5 songs with titles about deep feeling of dispair?",
)
print(response)
