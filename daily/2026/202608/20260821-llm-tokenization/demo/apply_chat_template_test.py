from transformers import AutoTokenizer

# 加载 Qwen3-0.6B 的分词器
tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen3-0.6B")

messages = [
    {"role": "system", "content": "你是一个有帮助的助手。"},
    {"role": "user", "content": "什么是分词？"},
]
text = tokenizer.apply_chat_template(
    messages, tokenize=False, add_generation_prompt=True
)
print(text)
