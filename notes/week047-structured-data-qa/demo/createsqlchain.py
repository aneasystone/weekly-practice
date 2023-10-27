#
# pip3 install langchain==0.0.324
#
from langchain.utilities import SQLDatabase

db = SQLDatabase.from_uri("mysql+pymysql://root:123456@192.168.1.44:3306/demo?charset=utf8")

print(db.table_info)

from langchain.chat_models import ChatOpenAI
from langchain.chains import create_sql_query_chain

chain = create_sql_query_chain(ChatOpenAI(temperature=0), db)
response = chain.invoke({"question": "王可可的学号是多少？"})
print(response)
