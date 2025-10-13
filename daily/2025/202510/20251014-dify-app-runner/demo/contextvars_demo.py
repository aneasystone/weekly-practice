import contextvars

# 创建上下文变量
user_id = contextvars.ContextVar('user_id', default=None)

# 设置值（返回Token对象，用于后续重置）
token = user_id.set(123)

# 获取值
print(user_id.get())  # 输出: 123

# 重置值（使用之前保存的Token）
user_id.reset(token)
print(user_id.get())  # 输出: None（默认值）

# 重新设置值
token = user_id.set(456)

# 在函数中使用
def func():
    print(user_id.get())  # 输出: 456

func()

# 模仿 dify 的写法

from contextlib import contextmanager

@contextmanager
def preserve_flask_contexts(context_vars: contextvars.Context):
    # Set context variables if provided
    if context_vars:
        for var, val in context_vars.items():
            var.set(val)
    yield

# 在新线程中使用

def func2(context: contextvars.Context):
    with preserve_flask_contexts(context_vars=context):
        print(user_id.get())  # 输出: 456

import threading

context = contextvars.copy_context()
worker_thread = threading.Thread(
    target=func2,
    kwargs={
        "context": context,
    },
)
worker_thread.start()

# 异步方法中使用

import asyncio

async def task1():
    user_id.set(1)
    await asyncio.sleep(0.1)
    print(f"Task1: {user_id.get()}")  # 输出: 1

async def task2():
    # user_id.set(2)
    await asyncio.sleep(0.1)
    print(f"Task2: {user_id.get()}")  # 输出: 2

async def main():
    await asyncio.gather(task1(), task2())

asyncio.run(main())