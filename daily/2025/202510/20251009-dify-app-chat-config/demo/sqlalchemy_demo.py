from sqlalchemy import create_engine, select, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 创建基类
Base = declarative_base()

# 定义数据模型（映射到数据库表）
class User(Base):
    __tablename__ = 'users'  # 表名
    
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    age = Column(Integer)

# 创建数据库引擎（SQLite 数据库）
engine = create_engine('sqlite:///example.db')

# 创建所有表（根据定义的模型）
Base.metadata.create_all(engine)

# 创建会话工厂
Session = sessionmaker(bind=engine)
session = Session()

# 添加数据
new_user = User(name='Alice', age=30)
session.add(new_user)
new_user = User(name='Bob', age=31)
session.add(new_user)
session.commit()

# 查询数据
users = session.query(User).all()
for user in users:
    print(f"ID: {user.id}, Name: {user.name}, Age: {user.age}")

# 查询数据（新语法）
stmt = select(User).where(
    User.name == "Alice",
)
user = session.scalar(stmt)
print(f"ID: {user.id}, Name: {user.name}, Age: {user.age}")

# 关闭会话
session.close()