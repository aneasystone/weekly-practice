from database import text_to_sql

schema = """CREATE TABLE IF NOT EXISTS `students`(
   `id` INT UNSIGNED AUTO_INCREMENT,
   `no` VARCHAR(100) NOT NULL,
   `name` VARCHAR(100) NOT NULL,
   `sex` INT NULL,
   `birthday` DATE NULL,
   PRIMARY KEY ( `id` )
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE utf8_general_ci;
"""

question = "王可可的学号是多少？"
sql = text_to_sql(schema=schema, question=question)
print(sql)

# SELECT no FROM students WHERE name = '王可可';

question = "班上一共有多少个男生？"
sql = text_to_sql(schema=schema, question=question)
print(sql)

# SELECT COUNT(*) FROM students WHERE sex=1;

question = "班上一共有多少个男生，多少个女生？"
sql = text_to_sql(schema=schema, question=question)
print(sql)

# SELECT 
#     SUM(CASE WHEN sex = 0 THEN 1 ELSE 0 END) AS "女生",
#     SUM(CASE WHEN sex = 1 THEN 1 ELSE 0 END) AS "男生"
# FROM students;

question = "王可可今年多大？"
sql = text_to_sql(schema=schema, question=question)
print(sql)

# SELECT YEAR(CURRENT_DATE) - YEAR(birthday) FROM students WHERE NAME='王可可';

question = "王可可和孙然谁的年龄大？"
sql = text_to_sql(schema=schema, question=question)
print(sql)

# SELECT NAME, YEAR(CURDATE())-YEAR(birthday) AS age
# FROM students
# WHERE NAME IN ("王可可", "孙然")
# ORDER BY age DESC LIMIT 1;
