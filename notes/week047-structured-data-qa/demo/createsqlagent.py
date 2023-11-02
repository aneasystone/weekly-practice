from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.sql_database import SQLDatabase
from langchain.llms.openai import OpenAI

db = SQLDatabase.from_uri("mysql+pymysql://root:123456@192.168.1.45:3306/demo?charset=utf8")
toolkit = SQLDatabaseToolkit(db=db, llm=OpenAI(temperature=0))

from langchain.agents import create_sql_agent
from langchain.agents.agent_types import AgentType

agent_executor = create_sql_agent(
    llm=OpenAI(temperature=0),
    toolkit=toolkit,
    verbose=True,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
)

response = agent_executor.run("班上一共有多少个女生？")
print(response)
