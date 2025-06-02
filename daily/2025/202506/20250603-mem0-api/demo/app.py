from mem0 import MemoryClient

client = MemoryClient(
    host="http://localhost:8888",
    api_key="xxx",
)

result = client.add("你好，我叫张三", user_id="zhangsan")
print(result)

related_memories = client.search("我是谁？", user_id="zhangsan")
print(related_memories)