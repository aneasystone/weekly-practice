from pydantic import BaseModel, Field

class Student(BaseModel):
    name: str = Field(description="学生姓名")
    age: int = Field(description="学生年龄")
    gender: str = Field(description="学生性别")
    grade: int = Field(description="学生年级")
    school: str = Field(description="学生学校")

class StudentList(BaseModel):
    students: list[Student] = Field(description="学生列表")

from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
llm_with_structure = llm.with_structured_output(StudentList)
structured_output = llm_with_structure.invoke("随机生成5条学生信息")

print(structured_output)
