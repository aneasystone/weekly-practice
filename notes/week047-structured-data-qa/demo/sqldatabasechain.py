from langchain.utilities import SQLDatabase
from langchain.llms import OpenAI
from langchain_experimental.sql import SQLDatabaseChain

db = SQLDatabase.from_uri("mysql+pymysql://root:123456@192.168.1.45:3306/demo?charset=utf8")
llm = OpenAI(temperature=0, verbose=True)
db_chain = SQLDatabaseChain.from_llm(llm, db, verbose=True)

response = db_chain.run("班上一共有多少个女生？")
print(response)
