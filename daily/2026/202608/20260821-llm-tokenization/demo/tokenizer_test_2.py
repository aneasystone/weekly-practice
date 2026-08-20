from transformers import AutoTokenizer

# 加载 Qwen3-0.6B 的分词器
tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen3-0.6B")

text = "你好，world！今天的 weather 真不错 😊"

# encode：文本 → token id 序列
ids = tokenizer.encode(text)
print(ids)

# 逐个看每个 token 对应的文本片段
for i in ids:
    print(i, repr(tokenizer.decode([i])))

# decode：token id 序列 → 还原成文本
print(tokenizer.decode(ids))
