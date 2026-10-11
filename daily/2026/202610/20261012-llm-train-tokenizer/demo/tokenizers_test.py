english = [
    "The quick brown fox jumps over the lazy dog.",
    "The tokenizer is trained on the training corpus.",
    "Training a tokenizer is the first step of training a language model.",
    "Large language models are trained on massive amounts of text data.",
    "The trainer merges the most frequent pairs of tokens.",
]
chinese = [
    "大模型训练需要高质量的数据。",
    "训练分词器是训练模型的第一步。",
]

# 英文重复 200 次、中文只重复 5 次，模拟英文为主的语料
corpus = english * 200 + chinese * 5

from tokenizers import Tokenizer
from tokenizers.models import BPE
from tokenizers.trainers import BpeTrainer
from tokenizers import pre_tokenizers, decoders

# 1. 新建一个空的分词器，底层算法选 BPE
tokenizer = Tokenizer(BPE())

# 2. 预分词器：先把文本按空格切成粗块，BPE 只在块内做合并
tokenizer.pre_tokenizer = pre_tokenizers.ByteLevel(add_prefix_space=False)
tokenizer.decoder = decoders.ByteLevel()

# 3. 训练器：设置词表大小和特殊 token
trainer = BpeTrainer(
    vocab_size=150,
    min_frequency=2,
    special_tokens=["<|endoftext|>", "<|im_start|>", "<|im_end|>"],
)

# 4. 训练并保存
tokenizer.train_from_iterator(corpus, trainer=trainer)
tokenizer.save("my-tokenizer.json")

print("词表大小:", tokenizer.get_vocab_size())

# 检查
vocab = tokenizer.get_vocab()
items = sorted(vocab.items(), key=lambda kv: kv[1])

print("--- 词表头部 ---")
for token, idx in items[:10]:
    print(idx, repr(token))

print("--- 词表尾部 ---")
for token, idx in items[-5:]:
    print(idx, repr(token))

# 测试
text = "Training a tokenizer is the first step. 大模型训练"
enc = tokenizer.encode(text)
print([tokenizer.decode([i]) for i in enc.ids])
print("token 数:", len(enc.tokens))
