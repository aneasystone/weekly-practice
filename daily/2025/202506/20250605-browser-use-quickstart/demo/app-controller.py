from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
llm = ChatOpenAI(model="gpt-4.1-mini")

from browser_use import Controller, ActionResult

controller = Controller()

# @controller.action('查询某个城市的天气')
# def weather(city: str) -> ActionResult:
#   return ActionResult(
#     extracted_content=f'{city}今天的天气晴，气温28摄氏度'
#   )

# from browser_use import Agent
# async def main():
#     agent = Agent(
#         task="使用 weather 工具查下合肥的天气",
#         llm=llm,
        
#         # 自定义工具
#         controller=controller
#     )
#     result = await agent.run()
#     print(result)

class MyContext:
   
   x: int | None = 0
   y: int | None = 0
   z: int | None = 0

   def __init__(self, x, y, z) -> None:
      self.x = x
      self.y = y
      self.z = z

@controller.action('查询某个城市的天气')
def weather(city: str, context: MyContext) -> ActionResult:
  print(f"Invoking weather {context.x} {context.y} {context.z}")
  return ActionResult(
    extracted_content=f'{city}今天的天气晴，气温28摄氏度'
  )

from browser_use import Agent
async def main():
    agent = Agent(
        task="使用 weather 工具查下合肥的天气",
        llm=llm,
        
        # 自定义工具
        controller=controller,
        context=MyContext(x=1, y=2, z=3)
    )
    result = await agent.run()
    print(result)

import asyncio
asyncio.run(main())