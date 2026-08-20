from transformers import AutoTokenizer

# 加载 Qwen3-0.6B 的分词器
tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen3-0.6B")

# 词表就是一个「token 文本 → id」的大字典
vocab = tokenizer.get_vocab()
print(len(vocab))

# 按 id 排序，看看队头和队尾
vocab_by_id = sorted(vocab.items(), key=lambda kv: kv[1])
print(dict(vocab_by_id[:10]))
print(dict(vocab_by_id[-3:]))

# print(vocab['Hello'])
# print(vocab['ä½łå¥½'])

print(tokenizer.convert_ids_to_tokens(108386))
print(tokenizer.tokenize("你好"))

# │ 文本 → token（词表 key 形式） │ tokenizer.tokenize()              │ "你好" → ['ä½łå¥½'] │
# ├───────────────────────────────┼───────────────────────────────────┼─────────────────────┤
# │ 文本 → id                     │ tokenizer.encode()                │ "你好" → [108386]   │
# ├───────────────────────────────┼───────────────────────────────────┼─────────────────────┤
# │ token → id                    │ tokenizer.convert_tokens_to_ids() │ 'ä½łå¥½' → 108386   │
# ├───────────────────────────────┼───────────────────────────────────┼─────────────────────┤
# │ id → token                    │ tokenizer.convert_ids_to_tokens() │ 108386 → 'ä½łå¥½'   │
# ├───────────────────────────────┼───────────────────────────────────┼─────────────────────┤
# │ id → 文本                     │ tokenizer.decode()                │ [108386] → '你好'   │
