from langchain.llms import OpenAI

llm = OpenAI(temperature=0.9)

prompt = """Based on the table schema below, write a SQL query that would answer the user's question:

CREATE TABLE IF NOT EXISTS `students`(
   `id` INT UNSIGNED AUTO_INCREMENT,
   `no` VARCHAR(100) NOT NULL,
   `name` VARCHAR(100) NOT NULL,
   `sex` INT NULL,
   `birthday` DATE NULL,
   PRIMARY KEY ( `id` )
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE utf8_general_ci;

Question: 王可可的学号是多少？
SQL Query:"""

response = llm.predict(prompt)
print(response)

# SELECT no FROM students WHERE name = '王可可';
