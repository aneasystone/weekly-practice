from tokenizers import Tokenizer, models, trainers, pre_tokenizers, decoders

# 从字节级 BPE 开始，保证任何字符都能被编码
tokenizer = Tokenizer(models.BPE())
tokenizer.pre_tokenizer = pre_tokenizers.ByteLevel(add_prefix_space=False)

trainer = trainers.BpeTrainer(
    vocab_size=2048,
    special_tokens=["<|endoftext|>", "<|user|>", "<|bot|>"],
)
tokenizer.train(["toy_corpus.txt"], trainer)
tokenizer.save("mini_tokenizer.json")

tokenizer = Tokenizer.from_file("mini_tokenizer.json")
# 字节级 BPE 要配上对应的解码器，不然中文解码出来是乱码
tokenizer.decoder = decoders.ByteLevel()
ids = tokenizer.encode("小明喜欢编程").ids
print("vocab size:", tokenizer.get_vocab_size())
print("ids:", ids)
print("decode:", tokenizer.decode(ids))
