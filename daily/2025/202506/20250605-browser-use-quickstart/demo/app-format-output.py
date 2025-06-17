from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
llm = ChatOpenAI(model="gpt-4.1-mini")

from typing import List
from pydantic import BaseModel

class Book(BaseModel):
    book_title: str          # 书名
    author: str              # 作者
    brief_introduction: str  # 简介
    score: float             # 评分

class Books(BaseModel):
    books: List[Book]

from browser_use import Controller

controller = Controller(output_model=Books)

from browser_use import Agent
async def main():
    agent = Agent(
        task="进入豆瓣读书，搜索关于大模型相关的书籍，获取排名前三的书籍详情",
        llm=llm,
        controller=controller
    )
    history = await agent.run()
    result = history.final_result()
    if result:
        parsed: Books = Books.model_validate_json(result)
        for book in parsed.books:
            print('\n--------------------------------')
            print(f'书名:     {book.book_title}')
            print(f'作者:     {book.author}')
            print(f'简介:     {book.brief_introduction}')
            print(f'评分:     {book.score}')

import asyncio
asyncio.run(main())