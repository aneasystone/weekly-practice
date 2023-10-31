#
# pip3 install langchain==0.0.324
#
from langchain.utilities import SQLDatabase

db = SQLDatabase.from_uri("mysql+pymysql://root:123456@192.168.1.45:3306/demo?charset=utf8")

print(db.get_table_info(table_names=["students"]))

from langchain.chat_models import ChatOpenAI
from langchain.chains import create_sql_query_chain

chain = create_sql_query_chain(ChatOpenAI(temperature=0), db)
response = chain.invoke({"question": "班上一共有多少个女生？"})
print(response)

# SELECT COUNT(*) AS total_female_students
# FROM students
# WHERE sex = 2

result = db.run(response)
print(result)

# [(4,)]
