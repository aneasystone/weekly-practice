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

根据 Nitarshan Rajkumar 等人的研究，我们还可以对提示语做进一步的优化，比如：

* 给表结构进行更详细的说明；
* 在表结构后面加几条具有代表性的示例数据；
* 增加几个用户问题和对应的 SQL 查询的例子；
* 使用向量数据库，根据用户问题动态查询相关的 SQL 查询的例子；

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

> 注意，大模型生成的 SQL 可能会对数据库造成破坏，所以在生产环境一定要做好安全防护，比如：使用只读的账号，限制返回结果的条数，等等。

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

默认情况下该方法会返回数据库中所有表的信息，可以通过 `table_names` 参数指定只返回某个表的信息：

```
print(db.get_table_info(table_names=["students"]))
```

也可以在 `SQLDatabase.from_uri()` 时通过 `include_tables` 参数指定：

```
from langchain.utilities import SQLDatabase

db = SQLDatabase.from_uri("mysql+pymysql://root:123456@192.168.1.45:3306/demo?charset=utf8", include_tables=["students"])
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

### 执行 SQL 语句并回答用户问题

得到 SQL 语句之后，我们就可以通过 `SQLDatabase` 运行它：

```
result = db.run(response)
print(result)

# [(4,)]
```

然后再重新组织提示语，让大模型以自然语言的形式对用户问题进行回答，跟上面类似，此处略过。

#### 使用 `SQLDatabaseChain` 实现数据库问答

不过 LangChain 提供了更方便的方式实现数据库问答，那就是 `SQLDatabaseChain`，可以将上面几个步骤合而为一。不过 `SQLDatabaseChain` 目前还处于实验阶段，我们需要先安装 `langchain_experimental`：

```
$ pip3 install langchain_experimental==0.0.32
```

然后就可以使用 `SQLDatabaseChain` 来回答用户问题了：

```
from langchain.utilities import SQLDatabase
from langchain.llms import OpenAI
from langchain_experimental.sql import SQLDatabaseChain

db = SQLDatabase.from_uri("mysql+pymysql://root:123456@192.168.1.45:3306/demo?charset=utf8")
llm = OpenAI(temperature=0, verbose=True)
db_chain = SQLDatabaseChain.from_llm(llm, db, verbose=True)

response = db_chain.run("班上一共有多少个女生？")
print(response)
```

我们通过 `verbose=True` 参数让 `SQLDatabaseChain` 输出执行的详细过程，结果如下：

```
> Entering new SQLDatabaseChain chain...
班上一共有多少个女生？
SQLQuery:SELECT COUNT(*) FROM students WHERE sex = 2;
SQLResult: [(4,)]
Answer:班上一共有4个女生。
> Finished chain.
班上一共有4个女生。
```

> 注意：`SQLDatabaseChain` 会一次性查询出数据库中所有的表结构，然后丢给大模型生成 SQL，当数据库中表较多时，生成效果可能并不好，这时最好手工指定使用哪些表，再生成 SQL，或者使用 `SQLDatabaseSequentialChain`，它第一步会让大模型确定该使用哪些表，然后再调用 `SQLDatabaseChain`。

#### 使用 SQL Agent 实现数据库问答

在 [week044-llm-application-frameworks-langchain-2](../week044-llm-application-frameworks-langchain-2/README.md) 这篇笔记中，我们学习了 LangChain 的 Agent 功能，借助 ReAct 提示工程或 OpenAI 的 Function Calling 技术，可以让大模型具有推理和使用外部工具的能力。很显然，如果我们将数据库相关的操作都定义成一个个的工具，那么通过 LangChain Agent 应该也可以实现数据库问答功能。

LangChain 将数据库相关的操作封装在 `SQLDatabaseToolkit` 工具集中，我们可以直接使用：

```
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.sql_database import SQLDatabase
from langchain.llms.openai import OpenAI

db = SQLDatabase.from_uri("mysql+pymysql://root:123456@192.168.1.45:3306/demo?charset=utf8")
toolkit = SQLDatabaseToolkit(db=db, llm=OpenAI(temperature=0))
```

这个工具集中实际上包含了四个工具：

| 工具名 | 工具类 | 工具说明 |
| ----- | ------ | ------- |
| `sql_db_list_tables` | `ListSQLDatabaseTool` | 查询数据库中所有表名 |
| `sql_db_schema` | `InfoSQLDatabaseTool` | 根据表名查询表结构信息和示例数据 |
| `sql_db_query` | `QuerySQLDataBaseTool` | 执行 SQL 返回执行结果 |
| `sql_db_query_checker` | `QuerySQLCheckerTool` | 使用大模型分析 SQL 语句是否正确 |

另外，LangChain 还提供了 `create_sql_agent` 方法用于快速创建一个用于处理数据库的 Agent：

```
from langchain.agents import create_sql_agent
from langchain.agents.agent_types import AgentType

agent_executor = create_sql_agent(
    llm=OpenAI(temperature=0),
    toolkit=toolkit,
    verbose=True,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
)
```

其中 `agent_type` 只能选 `ZERO_SHOT_REACT_DESCRIPTION` 和 `OPENAI_FUNCTIONS` 这两种，实际上就对应着 `ZeroShotAgent` 和 `OpenAIFunctionsAgent`，在使用上和其他的 Agent 并无二致：

```
response = agent_executor.run("班上一共有多少个女生？")
print(response)
```

执行结果如下：

```
> Entering new AgentExecutor chain...
Thought: I should query the database to get the answer.
Action: sql_db_list_tables
Action Input: ""
Observation: students
Thought: I should query the schema of the students table.
Action: sql_db_schema
Action Input: "students"
Observation: 
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
Thought: I should query the database to get the number of female students.
Action: sql_db_query
Action Input: SELECT COUNT(*) FROM students WHERE sex = 2
Observation: [(4,)]
Thought: I now know the final answer.
Final Answer: 班上一共有4个女生。

> Finished chain.
班上一共有4个女生。
```

可以看出整个执行过程非常流畅，首先获取数据库中的表，然后查询表结构，接着生成 SQL 语句并执行，最后得到用户问题的答案。

使用 SQL Agent 比 `SQLDatabaseChain` 要灵活的多，我们不仅可以实现数据库问答，还可以实现一些其他功能，比如 SQL 生成，SQL 校验，SQL 解释和优化，生成数据库描述，等等，我们还可以根据需要在工具集中添加自己的工具，扩展出更丰富的功能。

LangChain 的 [这篇文档中](https://python.langchain.com/docs/use_cases/qa_structured/sql#extending-the-sql-toolkit) 就给出了两个拓展工具集的例子，我觉得很有参考意义：

* **Including dynamic few-shot examples**：这个例子将一些用户问题和对应的 SQL 示例存储到向量数据库中，然后创建一个额外的名为 `sql_get_similar_examples` 的工具用于从向量库中获取类似示例，并将提示语修改为：先从向量库中查找类似的示例，判断示例能否构造出回答用户问题的 SQL 语句，如果能，直接通过示例构造出 SQL 语句，如果不能，则通过查询数据库的表结构来构造；
* **Finding and correcting misspellings for proper nouns**：这也是一个很实用的示例，用户在提问时往往会输入一些错别字，特别是人物名称、公司名称或地址信息等专有名词，比如将 `张晓红今年多大？` 写成了 `张小红今年多大？`，这时直接搜索数据库肯定是搜不出结果的。在这个例子中，首先将数据库中所有艺人名称和专辑名称存储到向量数据库中，然后创建了一个额外的名为 `name_search` 的工具用于从向量库中获取近似的名称，并将提示语修改为：如果用户问题设计到专有名词，首先搜索向量库判断名称的拼写是否有误，如果拼写有误，要使用正确的名称构造 SQL 语句来回答用户的问题。

## 一些开源项目

目前市面上已经诞生了大量基于结构化数据的问答产品，比如 [酷表Excel](https://chatexcel.com/)、[Sheet+](https://sheetplus.ai/)、[Julius AI](https://julius.ai/) 等，它们通过聊天的方式来操控 Excel 或 Google Sheet 表格，还有 [AI Query](https://aiquery.co/)、[AI2sql](https://www.ai2sql.io/) 等，它们将自然语言转化为可以执行的 SQL 语句，让所有数据库小白也可以做数据分析。

在开源社区，类似的项目也是百花齐放，比如 [sql-translator](https://github.com/whoiskatrin/sql-translator)、[textSQL](https://github.com/caesarhq/textSQL)、[sqlchat](https://github.com/sqlchat/sqlchat)、[Chat2DB](https://github.com/chat2db/Chat2DB)、[DB-GPT](https://github.com/eosphoros-ai/DB-GPT) 等等，其中热度最高的当属 Chat2DB 和 DB-GPT 这两个开源项目。

### Chat2DB

[Chat2DB](https://github.com/chat2db/Chat2DB) 是一款智能的数据库客户端软件，和 Navicat、DBeaver 相比，Chat2DB 集成了 AIGC 的能力，能够将自然语言转换成 SQL，也可以将 SQL 翻译成自然语言，或对 SQL 提出优化建议；此外，Chat2DB 还集成了报表能力，用户可以用对话的形式进行数据统计和分析。

Chat2DB 提供了 Windows、Mac、Linux 等平台的安装包，也支持以 Web 形式进行部署，我们直接通过官方镜像安装：

```
$ docker run --name=chat2db -ti -p 10824:10824 chat2db/chat2db:latest
```

启动成功后，访问 `http://localhost:10824` 会进入 Chat2DB 的登录页面，默认的用户名和密码是 `chat2db/chat2db`，登录成功后，添加数据库连接，然后可以创建新的表，查看表结构，查看表中数据，等等，这和传统的数据库客户端软件并无二致：

![](./images/chat2db-console.png)

和传统的数据库客户端软件相比，Chat2DB 最重要的一点区别在于，用户可以在控制台中输入自然语言，比如像下面这样，输入 `查询王可可的学号` 并回车，这时会自动生成 SQL 语句，点击执行按钮就可以得到结果：

![](./images/chat2db-generate-sql-select.png)

通过这种方式来管理数据库让人感觉很自然，即使数据库小白也能对数据库进行各种操作，比如要创建一个表：

![](./images/chat2db-generate-sql-create-table.png)

插入一些测试数据：

![](./images/chat2db-generate-sql-insert.png)

遇到不懂的 SQL 语句，用户还可以对 SQL 语句进行解释和优化，整个体验可以说是非常流畅，另外，Chat2DB 还支持通过自然语言的方式生成报表，比如柱状图、折线图、饼图等，便于用户进行数据统计和分析：

![](./images/chat2db-dashboard.png)

默认情况下，Chat2DB 使用的是 Chat2DB AI 接口，关注官方公众号后就可以免费使用，我们也可以切换成 OpenAI 或 AzureAI 接口，或使用自己部署的大模型接口，具体内容请参考官方提供的 [ChatGLM-6B](https://github.com/chat2db/chat2db-chatglm-6b-deploy/blob/main/README_CN.md) 和 [sqlcoder](https://github.com/chat2db/chat2db-sqlcoder-deploy/blob/main/README_CN.md) 的部署方法。

### DB-GPT

[DB-GPT](https://github.com/eosphoros-ai/DB-GPT) 是一款基于知识库的问答产品，它同时支持结构化和非结构化数据的问答，支持生成报表，还支持自定义插件，在交互形式上和 ChatGPT 类似。它的一大特点是支持海量的模型管理，包括开源模型和 API 接口，并支持模型的自动化微调。

DB-GPT 的侧重点在于私有化，它强调数据的隐私安全，可以做到整个系统都不依赖于外部环境，完全避免了数据泄露的风险，是一款真正意义上的本地知识库问答产品。它集成了常见的开源大模型和向量数据库，因此，在部署上复杂一点，而且对硬件的要求也要苛刻一点。不过对于哪些没有条件部署大模型的用户来说，DB-GPT 也支持直接 [使用 OpenAI 或 Bard 等接口](https://db-gpt.readthedocs.io/en/latest/getting_started/install/llm/proxyllm/proxyllm.html)。

DB-GPT 支持 [从源码安装](https://db-gpt.readthedocs.io/en/latest/getting_started/install/deploy.html) 和 [从 Docker 镜像安装](https://db-gpt.readthedocs.io/en/latest/getting_started/install/docker/docker.html)，不过官方提供的 Docker 镜像缺少 `openai` 等依赖，需要我们手工安装，所以不建议直接启动，而是先通过 bash 进入容器做一些准备工作：

```
$ docker run --rm -ti -p 5000:5000 eosphorosai/dbgpt:latest bash
```

安装 `openai` 依赖：

```
# pip3 install openai
```

然后设置一些环境变量，让 DB-GPT 使用 OpenAI 的 Completions 和 Embedding 接口：

```
# export LLM_MODEL=chatgpt_proxyllm
# export PROXY_SERVER_URL=https://api.openai.com/v1/chat/completions
# export PROXY_API_KEY=sk-xx
# export EMBEDDING_MODEL=proxy_openai
# export proxy_openai_proxy_server_url=https://api.openai.com/v1
# export proxy_openai_proxy_api_key=sk-xxx
```

如果由于网络原因导致 OpenAI 接口无法访问，还需要配置代理（注意先安装 `pysocks` 依赖）：

```
# pip3 install pysocks
# export https_proxy=socks5://192.168.1.45:7890
# export http_proxy=socks5://192.168.1.45:7890
```

一切准备就绪后，启动 DB-GPT server：

```
# python3 pilot/server/dbgpt_server.py
```

等待服务启动成功，访问 `http://localhost:5000/` 即可进入 DB-GPT 的首页：

![](./images/dbgpt-home.png)

DB-GPT 支持几种类型的聊天功能：

* Chat Data
* Chat Excel
* Chat DB
* Chat Knowledge
* Dashboard
* Agent Chat

#### Chat DB & Chat Data & Dashboard

Chat DB、Chat Data 和 Dashboard 这三个功能都是基于数据库的问答，要使用它们，首先需要在 `数据库管理` 页面添加数据库。Chat DB 会根据数据库和表的结构信息帮助用户编写 SQL 语句：

![](./images/dbgpt-chat-db.png)

Chat Data 不仅会生成 SQL 语句，还会自动执行并得到结果：

![](./images/dbgpt-chat-data.png)

Dashboard 则比 Chat Data 更进一步，它会生成 SQL 语句，执行得到结果，并生成相应的图表：

![](./images/dbgpt-chat-dashboard.png)

#### Chat Excel

Chat Excel 功能依赖 `openpyxl` 库，需要提前安装：

```
# pip3 install openpyxl
```

然后就可以上传 Excel 文件，对其进行分析，并回答用户问题：

![](./images/dbgpt-chat-excel.png)

#### 其他功能

DB-GPT 除了支持结构化数据的问答，也支持非结构化数据的问答，Chat Knowledge 实现的就是这样的功能。要使用它，首先需要在 `知识库管理` 页面添加知识，DB-GPT 支持从文本，URL 或各种文档中导入：

![](./images/dbgpt-chat-kb.png)

然后在 Chat Knowledge 页面就可以选择知识库进行问答了。

DB-GPT 还支持插件功能，你可以从 [DB-GPT-Plugins](https://github.com/eosphoros-ai/DB-GPT-Plugins) 下载插件，也可以 [编写自己的插件并上传](https://db-gpt.readthedocs.io/en/latest/modules/plugins.html)，而且 DB-GPT 兼容 [Auto-GPT 的插件](https://github.com/Significant-Gravitas/Auto-GPT-Plugins) 接口，原则上，所有的 Auto-GPT 插件都可以在这里使用：

![](./images/dbgpt-chat-plugins.png)

然后在 Agent Chat 页面，就可以像 ChatGPT Plus 一样，选择插件进行问答了。

另外，DB-GPT 的模型管理功能也很强大，不仅支持像 OpenAI 或 Bard 这样的大模型代理接口，还集成了大量的开源大模型，而且在 [DB-GPT-Hub](https://github.com/eosphoros-ai/DB-GPT-Hub) 项目中还提供了大量的数据集、工具和文档，让我们可以对这些大模型进行微调，实现更强大的 Text-to-SQL 能力。

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

### 基于其他结构化数据源的文档问答

#### Neo4j

* [Using a Knowledge Graph to implement a DevOps RAG application](https://blog.langchain.dev/using-a-knowledge-graph-to-implement-a-devops-rag-application/)
* [Constructing knowledge graphs from text using OpenAI functions: Leveraging knowledge graphs to power LangChain Applications](https://blog.langchain.dev/constructing-knowledge-graphs-from-text-using-openai-functions/)

#### Elasticsearch

* [使用 `ElasticsearchDatabaseChain` 实现基于 ES 的文档问答](https://python.langchain.com/docs/use_cases/qa_structured/sql#elastic-search)

#### CSV

* [Benchmarking Question/Answering Over CSV Data](https://blog.langchain.dev/benchmarking-question-answering-over-csv-data/)
* [Pandas Dataframe Agent](https://python.langchain.com/docs/integrations/toolkits/pandas)
* [CSV Agent](https://python.langchain.com/docs/integrations/toolkits/csv)

#### Excel

* [Summarizing and Querying Data from Excel Spreadsheets Using eparse and a Large Language Model](https://blog.langchain.dev/summarizing-and-querying-data-from-excel-spreadsheets-using-eparse-and-a-large-language-model/)

### 基于半结构化和多模数据源的文档问答

* [Multi-Vector Retriever for RAG on tables, text, and images](https://blog.langchain.dev/semi-structured-multi-modal-rag/)
* [Semi-structured RAG](https://github.com/langchain-ai/langchain/blob/master/cookbook/Semi_Structured_RAG.ipynb)
* [Semi-structured and Multi-modal RAG](https://github.com/langchain-ai/langchain/blob/master/cookbook/Semi_structured_and_multi_modal_RAG.ipynb)
* [Private Semi-structured and Multi-modal RAG w/ LLaMA2 and LLaVA](https://github.com/langchain-ai/langchain/blob/master/cookbook/Semi_structured_multi_modal_RAG_LLaMA2.ipynb)

### 学习 LCEL

在 LangChain 中，我们还可以通过 [LCEL（LangChain Expression Language）](https://python.langchain.com/docs/expression_language/) 来简化 Chain 的创建，比如对数据库进行问答，[官方有一个示例](https://python.langchain.com/docs/expression_language/cookbook/sql_db)，可以用下面这样的管道式语法来写：

```
full_chain = (
    RunnablePassthrough.assign(query=sql_response)
    | RunnablePassthrough.assign(
        schema=get_schema,
        response=lambda x: db.run(x["query"]),
    )
    | prompt_response
    | model
)
```
