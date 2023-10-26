from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate

#
# Install mysqlclient: https://github.com/PyMySQL/mysqlclient
#
# $ sudo apt-get install python3-dev default-libmysqlclient-dev build-essential pkg-config
# $ pip3 install mysqlclient
#
import MySQLdb

llm = OpenAI(temperature=0.9)

prompt = PromptTemplate.from_template("""根据下面的数据库表结构，生成一条 SQL 查询语句来回答用户的问题：

{schema}

用户问题：{question}
SQL 查询语句：""")

def text_to_sql(schema, question):
	text = prompt.format(schema=schema, question=question)
	response = llm.predict(text)
	return response

prompt_qa = PromptTemplate.from_template("""根据下面的数据库表结构，SQL 查询语句和结果，以自然语言回答用户的问题：

{schema}

用户问题：{question}
SQL 查询语句：{query}
SQL 查询结果：{result}
回答：""")

def qa(schema, question):
	query = text_to_sql(schema=schema, question=question)
	print(query)
	result = execute_sql(query)
	text = prompt_qa.format(schema=schema, question=question, query=query, result=result)
	response = llm.predict(text)
	return response

def execute_sql(sql):
	result = ''
	db = MySQLdb.connect("192.168.1.44", "root", "123456", "demo", charset='utf8' )
	cursor = db.cursor()
	try:
		cursor.execute(sql)
		results = cursor.fetchall()
		for row in results:
			result += ' '.join(str(x) for x in row) + '\n'
	except:
		print("Error: unable to fetch data")
	db.close()
	return result
