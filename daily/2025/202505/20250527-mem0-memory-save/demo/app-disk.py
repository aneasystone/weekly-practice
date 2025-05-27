from openai import OpenAI
from mem0 import Memory

openai_client = OpenAI()

config = {
    "vector_store": {
        "provider": "qdrant",
        "config": {
            "path": "/tmp/qdrant_data",
            "on_disk": True
        }
    },
}

memory = Memory.from_config(config)

def chat_with_memories(message: str, user_id: str = "default_user") -> str:
    
    # 检索相关记忆
    relevant_memories = memory.search(query=message, user_id=user_id, limit=3)
    memories_str = "\n".join(f"- {entry['memory']}" for entry in relevant_memories["results"])

    # 生成助手回复
    system_prompt = f"你是我的私人助理，请根据我的记忆回答我的问题。\n我的记忆：\n{memories_str}"
    # print('--------------------------------')
    # print(system_prompt)
    # print('--------------------------------')
    messages = [{"role": "system", "content": system_prompt}, {"role": "user", "content": message}]
    response = openai_client.chat.completions.create(model="gpt-4o-mini", messages=messages)
    assistant_response = response.choices[0].message.content

    # 从对话中创建新记忆
    messages.append({"role": "assistant", "content": assistant_response})
    memory.add(messages, user_id=user_id)

    return assistant_response

def main():
    while True:
        user_input = input("用户：").strip()
        if user_input.lower() == 'exit':
            print("再见！")
            break
        print(f"系统：{chat_with_memories(user_input, "zhangsan")}")

if __name__ == "__main__":
    main()