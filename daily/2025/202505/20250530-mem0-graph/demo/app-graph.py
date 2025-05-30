from mem0 import Memory

config = {
    "graph_store": {
        "provider": "neo4j",
        "config": {
            "url": "neo4j://localhost:7687",
            "username": "neo4j",
            "password": "password"
        }
    }
}

memory = Memory.from_config(config)

memory.add("Hi, my name is Desmond.", user_id="desmond")
memory.add("I have a sister.", user_id="desmond")
memory.add("Her name is Jesica.", user_id="desmond")
memory.add("She has a dog.", user_id="desmond")

# import json
# results = memory.search(query="Who am I?", user_id="desmond", limit=3)
# print(json.dumps(results, indent=2, ensure_ascii=False))
