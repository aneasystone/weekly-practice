lines = [
    "小明是一个喜欢编程的少年。小明每天早上都会写代码。",
    "Xiaoming is a boy who loves programming. He writes code every morning.",
    "编程让小明感到快乐。Programming makes Xiaoming happy.",
    "大模型是一种会说话的程序。A large language model is a program that can talk.",
    "训练一个小模型需要数据、算力和耐心。Training a small model needs data, compute and patience.",
    "小明学会了用分词器处理文本。The tokenizer turns text into tokens.",
    " loss 下降说明模型在学习。A falling loss means the model is learning.",
    "小明的模型虽然小，但是能说话。The small model can talk.",
]

with open("toy_corpus.txt", "w", encoding="utf-8") as f:
    for i in range(4000):
        f.write(lines[i % len(lines)] + "\n")

import os
print(f"corpus size: {os.path.getsize('toy_corpus.txt') / 1024:.0f} KB")
