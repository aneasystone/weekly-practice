import asyncio

from dbgpt.core.awel import DAG, MapOperator, InputOperator, SimpleCallDataInputSource

with DAG("awel_hello_world") as dag:
    input_task = InputOperator(input_source=SimpleCallDataInputSource())
    task = MapOperator(map_function=lambda x: print(f"Hello, {x}!"))
    input_task >> task

asyncio.run(task.call(call_data="world"))
