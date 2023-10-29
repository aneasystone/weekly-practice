from database import qa

schema = """CREATE TABLE IF NOT EXISTS `students`(
   `id` INT UNSIGNED AUTO_INCREMENT,
   `no` VARCHAR(100) NOT NULL,
   `name` VARCHAR(100) NOT NULL,
   `sex` INT NULL COMMENT '1表示男生，2表示女生',
   `birthday` DATE NULL,
   PRIMARY KEY ( `id` )
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE utf8_general_ci;
"""

question = "王可可的学号是多少？"
answer = qa(schema=schema, question=question)
print(answer)

# 王可可的学号是202301030004。

# question = "班上一共有多少个男生？"
# answer = qa(schema=schema, question=question)
# print(answer)

# 班上一共有 6 个男生。

# question = "班上一共有多少个男生，多少个女生？"
# answer = qa(schema=schema, question=question)
# print(answer)

# 班上一共有 6 个男生，4 个女生。

# question = "王可可今年多大？"
# answer = qa(schema=schema, question=question)
# print(answer)

# 王可可今年 8 岁。

# question = "王可可和孙然谁的年龄大？"
# answer = qa(schema=schema, question=question)
# print(answer)

# 孙然的年龄比王可可大。
