from llama_index.llms.openai import OpenAI

llm = OpenAI(temperature=0.1, model="gpt-3.5-turbo")

from sqlalchemy import create_engine
from llama_index.core import SQLDatabase

engine = create_engine("sqlite:///./sqlite/Chinook.db")
sql_database = SQLDatabase(engine, include_tables=["Employee"])

from llama_index.core.query_engine import NLSQLTableQueryEngine

query_engine = NLSQLTableQueryEngine(
    sql_database=sql_database, tables=["Employee"], llm=llm
)
response = query_engine.query("How many employees are there?")
print(response)
