# WEEK047 - 基于结构化数据的文档问答

利用大模型打造文档问答系统对于个人和企业来说都是一个非常重要的应用场景，也是各大公司争相推出的基于大模型的落地产品之一，同时，在开源领域，文档问答也是非常火热，涌现出了一大批与之相关的开源项目，比如：[Quivr](https://github.com/StanGirard/quivr)、[PrivateGPT](https://github.com/imartinez/privateGPT)、[document.ai](https://github.com/GanymedeNil/document.ai)、[FastGPT](https://fastgpt.run/)、[DocsGPT](https://github.com/arc53/DocsGPT) 等等。我在 [week042-doc-qa-using-embedding](../week042-doc-qa-using-embedding/README.md) 这篇笔记中介绍了文档问答的基本原理，通过 OpenAI 的 Embedding 接口实现了一个最简单的本地知识库助手，并在 [week043-llm-application-frameworks-langchain](../week043-llm-application-frameworks-langchain/README.md) 这篇笔记中通过 LangChain 的 `RetrievalQA` 再次实现了基于文档的问答，还介绍了四种处理大文档的方法（`Stuff` `Refine` `MapReduce` 和 `MapRerank`）。

大抵来说，这类文档问答系统基本上都是基于 Embedding 和向量数据库来实现的，首先将文档分割成片段保存在向量库中，然后拿着用户的问题在向量库中检索，检索出来的结果是和用户问题最接近的文档片段，最后再将这些片段和用户问题一起交给大模型进行总结和提炼，从而给出用户问题的答案。在这个过程中，向量数据库是最关键的一环，这也是前一段时间向量数据库火得飞起的原因。

不过，并不是所有的知识库都是以文档的形式存在的，还有很多结构化的知识散落在企业的各种数据源中，数据源可能是 MySQL、Mongo 等数据库，也可能是 CSV、Excel 等表格，还可能是 Neo4j、Nebula 等图谱数据库。如果要针对这些知识进行问答，Embedding 基本上就派不上用场了，所以我们还得想另外的解决方案，这篇文章将针对这种场景做一番粗略的研究。

## 基本思路

我们知道，几乎每种数据库都提供了对应的查询方法，比如可以使用 SQL 查询 MySQL，使用 VBA 查询 Excel，使用 Cipher 查询 Neo4j 等等。那么很自然的一种想法是，如果能将用户的问题转换为查询语句，就可以先对数据库进行查询得到结果，这和从向量数据库中查询文档是类似的，再将查询出来的结果丢给大模型，就可以回答用户的问题了：

![](./images/db-qa.png)

那么问题来了，如何将用户的问题转换为查询语句呢？毋庸置疑，当然是让大模型来帮忙。

### 准备数据

首先，我们创建一个测试数据库，然后创建一个简单的学生表，包含学生的姓名、学号、性别等信息：

```
/*!40101 SET NAMES utf8 */;

CREATE DATABASE IF NOT EXISTS `demo` DEFAULT CHARSET utf8 COLLATE utf8_general_ci;

USE `demo`;

CREATE TABLE IF NOT EXISTS `students`(
   `id` INT UNSIGNED AUTO_INCREMENT,
   `no` VARCHAR(100) NOT NULL,
   `name` VARCHAR(100) NOT NULL,
   `sex` INT NULL,
   `birthday` DATE NULL,
   PRIMARY KEY ( `id` )
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE utf8_general_ci;
```

接着插入 10 条测试数据：

```
INSERT INTO `students` (`no`, `name`, `sex`, `birthday`) VALUES
('202301030001', '张启文', 1, '2015-04-14'),
('202301030002', '李金玉', 2, '2015-06-28'),
('202301030003', '王海红', 2, '2015-07-01'),
('202301030004', '王可可', 2, '2015-04-03'),
('202301030005', '郑丽英', 2, '2015-10-19'),
('202301030006', '张海华', 1, '2015-01-04'),
('202301030007', '文奇', 1, '2015-11-03'),
('202301030008', '孙然', 1, '2014-12-29'),
('202301030009', '周军', 1, '2015-07-15'),
('202301030010', '罗国华', 1, '2015-08-01');
```

然后将上面的初始化 SQL 语句放在 `init` 目录下，通过下面的命令启动 MySQL 数据库：

```
$ docker run -d -p 3306:3306 --name mysql \
	-v $PWD/init:/docker-entrypoint-initdb.d \
	-e MYSQL_ROOT_PASSWORD=123456 \
	mysql:5.7
```

### 将用户问题转为 SQL

接下来，我们尝试一下让大模型将用户问题转换为 SQL 语句。实际上，这被称之为 **Text-to-SQL**，有很多研究人员对这个课题进行过探讨和研究，Nitarshan Rajkumar 等人在 [Evaluating the Text-to-SQL Capabilities of Large Language Models](https://arxiv.org/abs/2204.00498) 这篇论文中对各种提示语的效果进行了对比测试，他们发现，当在提示语中使用 `CREATE TABLE` 来描述数据库表结构时，模型的效果最好。所以我们构造如下的提示语：

```
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate

llm = OpenAI(temperature=0.9)

prompt = PromptTemplate.from_template("""根据下面的数据库表结构，生成一条 SQL 查询语句来回答用户的问题：

{schema}

用户问题：{question}
SQL 查询语句：""")

def text_to_sql(schema, question):
	text = prompt.format(schema=schema, question=question)
	response = llm.predict(text)
	return response
```

这个提示语非常直白，直接将数据库表结构和用户问题丢给大模型，让其生成一条 SQL 查询语句。使用几个简单的问题测试下，发现效果还可以：

```
schema = "CREATE TABLE ..."
question = "王可可的学号是多少？"
sql = text_to_sql(schema=schema, question=question)
print(sql)

# SELECT no FROM students WHERE name = '王可可';
```

```
question = "王可可今年多大？"
sql = text_to_sql(schema=schema, question=question)
print(sql)

# SELECT YEAR(CURRENT_DATE) - YEAR(birthday) FROM students WHERE NAME='王可可';
```

```
question = "王可可和孙然谁的年龄大？"
sql = text_to_sql(schema=schema, question=question)
print(sql)

# SELECT NAME, YEAR(CURDATE())-YEAR(birthday) AS age
# FROM students
# WHERE NAME IN ("王可可", "孙然")
# ORDER BY age DESC LIMIT 1;
```

不过，当我们的字段有特殊含义时，生成的 SQL 语句就不对了，比如这里我们使用 `sex=1` 表示男生，`sex=2` 表示女生，但是 ChatGPT 生成 SQL 的时候，认为 `sex=0` 表示女生：

```
question = "班上一共有多少个女生？"
sql = text_to_sql(schema=schema, question=question)
print(sql)

# SELECT COUNT(*) FROM students WHERE sex=0;
```

为了让大模型知道字段的确切含义，我们可以在数据库表结构中给字段加上注释：

```
schema = """CREATE TABLE IF NOT EXISTS `students`(
   `id` INT UNSIGNED AUTO_INCREMENT,
   `no` VARCHAR(100) NOT NULL,
   `name` VARCHAR(100) NOT NULL,
   `sex` INT NULL COMMENT '1表示男生，2表示女生',
   `birthday` DATE NULL,
   PRIMARY KEY ( `id` )
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE utf8_general_ci;
"""
```

这样生成的 SQL 语句就没问题了：

```
question = "班上一共有多少个女生？"
sql = text_to_sql(schema=schema, question=question)
print(sql)

# SELECT COUNT(*) FROM students WHERE sex=2;
```

根据 Nitarshan Rajkumar 等人的研究，我们还可以对提示语做进一步的优化，比如在 `CREATE TABLE` 表结构的后面加几条表中具有代表性的示例数据，或者增加几个 SQL 查询的例子等等。

### 执行 SQL

得到 SQL 语句之后，接下来，我们就可以查询数据库了。在 Python 里操作 MySQL 数据库，有两个库经常被人提到：

* [PyMySQL](https://github.com/PyMySQL/PyMySQL)
* [mysqlclient](https://github.com/PyMySQL/mysqlclient)

这两个库的区别在于：PyMySQL 是使用纯 Python 实现的，使用起来简单方便，可以直接通过 `pip install PyMySQL` 进行安装；mysqlclient 其实就是 Python 3 版本的 MySQLdb，它是基于 C 扩展模块实现的，需要针对不同平台进行编译安装，但正因为此，mysqlclient 的速度非常快，在正式项目中推荐使用它。

这里我们就使用 mysqlclient 来执行 SQL，首先安装它：

```
$ sudo apt-get install python3-dev default-libmysqlclient-dev build-essential pkg-config
$ pip3 install mysqlclient
```

然后连接数据库执行 SQL 语句，它的用法和 MySQLdb 几乎完全兼容：

```
import MySQLdb

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
```

### 回答用户问题

拿到 SQL 语句的执行结果之后，我们就可以再次组织下提示语，让大模型以自然语言的形式来回答用户的问题：

```
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
```

测试效果如下：

```
schema = "CREATE TABLE ..."
question = "王可可的学号是多少？"
answer = qa(schema=schema, question=question)
print(answer)

# 王可可的学号是202301030004。
```

## LangChain

上面的步骤我们也可以使用 LangChain 来实现。

### 使用 `SQLDatabase` 获取数据库表结构信息

在 LangChain 的最新版本中，引入了 `SQLDatabase` 类可以方便地获取数据库表结构信息。我们首先安装 LangChain 的最新版本：

> 在写这篇博客时，最新版本是 0.0.324，LangChain 的版本更新很快，请随时关注官方文档。

```
$ pip3 install langchain==0.0.324
```

然后使用 `SQLDatabase.from_uri()` 初始化一个 `SQLDatabase` 实例，由于 `SQLDatabase` 是基于 [SQLAlchemy](https://www.sqlalchemy.org/) 实现的，所以参数格式和 SQLAlchemy 的 [create_engine](https://docs.sqlalchemy.org/en/20/core/engines.html) 是一致的：

```
from langchain.utilities import SQLDatabase

db = SQLDatabase.from_uri("mysql+pymysql://root:123456@192.168.1.45:3306/demo?charset=utf8")
```

然后我们就可以使用 `get_table_info()` 方法来获取表结构信息：

```
print(db.get_table_info())
```

默认情况下该方法会返回数据库中所有表的信息，通过 `table_names` 参数指定只返回某个表的信息：

```
print(db.get_table_info(table_names=["students"]))
```

查询结果如下：

```
CREATE TABLE students (
        id INTEGER(10) UNSIGNED NOT NULL AUTO_INCREMENT, 
        no VARCHAR(100) NOT NULL, 
        name VARCHAR(100) NOT NULL, 
        sex INTEGER(11) COMMENT '1表示男生，2表示女生', 
        birthday DATE, 
        PRIMARY KEY (id)
)DEFAULT CHARSET=utf8 ENGINE=InnoDB

/*
3 rows from students table:
id      no      name    sex     birthday
1       202301030001    张启文  1       2015-04-14
2       202301030002    李金玉  2       2015-06-28
3       202301030003    王海红  2       2015-07-01
*/
```

可以看出 `SQLDatabase` 不仅查询了表的结构信息，还将表中前三条数据一并返回了，用于组装提示语。

### 使用 `create_sql_query_chain` 转换 SQL 语句

接下来我们将用户问题转换为 SQL 语句。LangChain 提供了一个 Chain 来做这个事，这个 Chain 并没有具体的名字，但是我们可以使用 `create_sql_query_chain` 来创建它：

```
from langchain.chat_models import ChatOpenAI
from langchain.chains import create_sql_query_chain

chain = create_sql_query_chain(ChatOpenAI(temperature=0), db)
```

`create_sql_query_chain` 的第一个参数是大模型，第二个参数是上一节创建的 `SQLDatabase`，注意这里大模型的参数 `temperature=0`，因为我们希望大模型生成的 SQL 语句越固定越好，而不是随机变化。

得到 Chain 之后，就可以调用 `chain.invoke()` 将用户问题转换为 SQL 语句：

```
response = chain.invoke({"question": "班上一共有多少个女生？"})
print(response)

# SELECT COUNT(*) AS total_female_students
# FROM students
# WHERE sex = 2
```

其实，`create_sql_query_chain` 还有第三个参数，用于设置提示语，不设置的话将使用下面的默认提示语：

```
PROMPT_SUFFIX = """Only use the following tables:
{table_info}

Question: {input}"""

_mysql_prompt = """You are a MySQL expert. Given an input question, first create a syntactically correct MySQL query to run, then look at the results of the query and return the answer to the input question.
Unless the user specifies in the question a specific number of examples to obtain, query for at most {top_k} results using the LIMIT clause as per MySQL. You can order the results to return the most informative data in the database.
Never query for all columns from a table. You must query only the columns that are needed to answer the question. Wrap each column name in backticks (`) to denote them as delimited identifiers.
Pay attention to use only the column names you can see in the tables below. Be careful to not query for columns that do not exist. Also, pay attention to which column is in which table.
Pay attention to use CURDATE() function to get the current date, if the question involves "today".

Use the following format:

Question: Question here
SQLQuery: SQL Query to run
SQLResult: Result of the SQLQuery
Answer: Final answer here

"""

MYSQL_PROMPT = PromptTemplate(
    input_variables=["input", "table_info", "top_k"],
    template=_mysql_prompt + PROMPT_SUFFIX,
)
```

### QA over structured data

https://python.langchain.com/docs/expression_language/cookbook/sql_db

https://python.langchain.com/docs/use_cases/qa_structured/sql

### SQL Database Toolkit and Agent

https://python.langchain.com/docs/integrations/toolkits/sql_database

## DB-GPT

https://db-gpt.readthedocs.io/en/latest/

## 常见 SQL 用例

## 参考

* [Querying a SQL DB](https://python.langchain.com/docs/expression_language/cookbook/sql_db)
* [QA over structured data](https://python.langchain.com/docs/use_cases/qa_structured/sql)
* [SQL Database Toolkit and Agent](https://python.langchain.com/docs/integrations/toolkits/sql_database)
* [LLMs and SQL](https://blog.langchain.dev/llms-and-sql/)
* [‘Talk’ to Your SQL Database Using LangChain and Azure OpenAI](https://towardsdatascience.com/talk-to-your-sql-database-using-langchain-and-azure-openai-bb79ad22c5e2)
* [大模型与数据科学：从Text-to-SQL 开始（一）](https://zhuanlan.zhihu.com/p/640580808)
* [大模型与商业智能BI：LLM-as-数据小助理（二）](https://zhuanlan.zhihu.com/p/640696719)
* [大模型+知识库/数据库问答的若干问题（三）](https://zhuanlan.zhihu.com/p/642125832)
* [How can I connect to MySQL in Python 3 on Windows?](https://stackoverflow.com/questions/4960048/how-can-i-connect-to-mysql-in-python-3-on-windows)

## 更多

### Semi-structured and Multi-modal RAG

* [Semi-structured RAG](https://github.com/langchain-ai/langchain/blob/master/cookbook/Semi_Structured_RAG.ipynb)
* [Private Semi-structured and Multi-modal RAG w/ LLaMA2 and LLaVA](https://github.com/langchain-ai/langchain/blob/master/cookbook/Semi_structured_multi_modal_RAG_LLaMA2.ipynb)
