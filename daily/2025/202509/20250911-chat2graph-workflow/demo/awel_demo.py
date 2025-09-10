import asyncio

from dbgpt.core.awel import DAG, MapOperator

with DAG("awel_hello_world") as dag:
    task = MapOperator(map_function=lambda x: print(f"Hello, {x}!"))

asyncio.run(task.call(call_data="world"))