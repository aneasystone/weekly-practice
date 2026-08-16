from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen3-0.6B")

for text in ["合肥今天天气怎么样", "How is the weather in Hefei today"]:
    ids = tokenizer.encode(text)
    # tokenize() 返回的是字节级 BPE 的内部表示，直接打印会显示成「乱码」；
    # 对每个 token id 做 decode 才能还原成可读的文本片段
    tokens = [tokenizer.decode([i]) for i in ids]
    print(len(tokens), tokens)
