from transformers import AutoTokenizer

# 加载 Qwen3-0.6B 的分词器
tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen3-0.6B")

texts = ["我们今天来学习分词", "We are learning tokenization today", "unbelievable"]
for text in texts:
    ids = tokenizer.encode(text)
    # 逐个 decode 出 token 片段，把空格换成 ␣ 方便看
    tokens = [tokenizer.decode([i]).replace(" ", "␣") for i in ids]
    print(f'"{text}" → {len(ids)} 个 token：{" / ".join(tokens)}')
