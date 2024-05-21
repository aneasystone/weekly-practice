from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings

llm = ChatOpenAI(model="gpt-4", temperature=0)
embeddings_model = OpenAIEmbeddings()

from langchain.sql_database import SQLDatabase

CONNECTION_STRING = "postgresql+psycopg2://root:123456@localhost:5432/vectordb"
db = SQLDatabase.from_uri(CONNECTION_STRING)

def get_schema(_):
    return db.get_table_info()


def run_query(query):
    return db.run(query)


from langchain_core.prompts import ChatPromptTemplate

template = """You are a Postgres expert. Given an input question, first create a syntactically correct Postgres query to run, then look at the results of the query and return the answer to the input question.
Unless the user specifies in the question a specific number of examples to obtain, query for at most 5 results using the LIMIT clause as per Postgres. You can order the results to return the most informative data in the database.
Never query for all columns from a table. You must query only the columns that are needed to answer the question. Wrap each column name in double quotes (") to denote them as delimited identifiers.
Pay attention to use only the column names you can see in the tables below. Be careful to not query for columns that do not exist. Also, pay attention to which column is in which table.
Pay attention to use date('now') function to get the current date, if the question involves "today".

You can use an extra extension which allows you to run semantic similarity using <-> operator on tables containing columns named "embeddings".
<-> operator can ONLY be used on embeddings columns.
The embeddings value for a given row typically represents the semantic meaning of that row.
The vector represents an embedding representation of the question, given below. 
Do NOT fill in the vector values directly, but rather specify a `[search_word]` placeholder, which should contain the word that would be embedded for filtering.
For example, if the user asks for songs about 'the feeling of loneliness' the query could be:
'SELECT "[whatever_table_name]"."SongName" FROM "[whatever_table_name]" ORDER BY "embeddings" <-> '[loneliness]' LIMIT 5'

Use the following format:

Question: <Question here>
SQLQuery: <SQL Query to run>
SQLResult: <Result of the SQLQuery>
Answer: <Final answer here>

Only use the following tables:

{schema}
"""


prompt = ChatPromptTemplate.from_messages(
    [("system", template), ("human", "{question}")]
)

from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

sql_query_chain = (
    RunnablePassthrough.assign(schema=get_schema)
    | prompt
    | llm.bind(stop=["\nSQLResult:"])
    | StrOutputParser()
)

response = sql_query_chain.invoke(
    {
        "question": "Which are the 5 rock songs with titles about deep feeling of dispair?"
    }
)
print(response)

import re

from langchain_core.runnables import RunnableLambda


def replace_brackets(match):
    words_inside_brackets = match.group(1).split(", ")
    embedded_words = [
        str(embeddings_model.embed_query(word)) for word in words_inside_brackets
    ]
    return "', '".join(embedded_words)


def get_query(query):
    sql_query = re.sub(r"\[([\w\s,]+)\]", replace_brackets, query)
    if 'SQLQuery:' in sql_query:
        index = sql_query.index('SQLQuery:')
        sql_query = sql_query[index+9:].strip()
    return sql_query.replace('```', '')


template = """Based on the table schema below, question, sql query, and sql response, write a natural language response:
{schema}

Question: {question}
SQL Query: {query}
SQL Response: {response}"""

prompt = ChatPromptTemplate.from_messages(
    [("system", template), ("human", "{question}")]
)

full_chain = (
    RunnablePassthrough.assign(query=sql_query_chain)
    | RunnablePassthrough.assign(
        schema=get_schema,
        response=RunnableLambda(lambda x: db.run(get_query(x["query"]))),
    )
    | prompt
    | llm
)

response = full_chain.invoke(
    {
        "question": "Which are the 5 rock songs with titles about deep feeling of dispair?"
    }
)
print(response)

response = full_chain.invoke(
    {
        "question": "I want to know the 3 albums which have the most amount of songs in the top 150 saddest songs"
    }
)
print(response)

response = full_chain.invoke(
    {
        "question": "I need the 6 albums with shortest title, as long as they contain songs which are in the 20 saddest song list."
    }
)
print(response)
