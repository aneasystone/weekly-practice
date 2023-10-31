from langchain.utilities import SQLDatabase
from langchain.prompts import ChatPromptTemplate

template = """Based on the table schema below, write a SQL query that would answer the user's question:
{schema}

Question: {question}
SQL Query:"""
prompt = ChatPromptTemplate.from_template(template)

db = SQLDatabase.from_uri("mysql+pymysql://root:123456@192.168.1.45:3306/demo?charset=utf8")

def get_schema(_):
    return db.get_table_info()

def run_query(query):
    return db.run(query)

from langchain.chat_models import ChatOpenAI
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough

model = ChatOpenAI()

sql_response = (
        RunnablePassthrough.assign(schema=get_schema)
        | prompt
        | model.bind(stop=["\nSQLResult:"])
        | StrOutputParser()
    )

response = sql_response.invoke({"question": "王可可的学号是多少？"})
print(response)

template = """Based on the table schema below, question, sql query, and sql response, write a natural language response:
{schema}

Question: {question}
SQL Query: {query}
SQL Response: {response}"""
prompt_response = ChatPromptTemplate.from_template(template)

full_chain = (
    RunnablePassthrough.assign(query=sql_response) 
    | RunnablePassthrough.assign(
        schema=get_schema,
        response=lambda x: db.run(x["query"]),
    )
    | prompt_response 
    | model
)

response = full_chain.invoke({"question": "王可可的学号是多少？"})
print(response.content)
