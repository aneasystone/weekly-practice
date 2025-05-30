import json
from mem0 import Memory
memory = Memory()

memory.add("我叫张三，我今年20岁，我住在上海，我喜欢吃辣", user_id="zhangsan")

results = memory.search(query="我叫什么？", user_id="zhangsan", limit=3)
print(json.dumps(results, indent=2, ensure_ascii=False))
