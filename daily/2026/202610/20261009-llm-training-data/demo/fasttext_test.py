import fasttext

# lid.176 是 fastText 官方的语言识别模型，ftz 后缀是量化压缩版
model = fasttext.load_model("lid.176.ftz")

texts = [
    "大模型训练的数据从哪来",
    "The quick brown fox jumps over the lazy dog",
    "Bonjour le monde",
    "Common Crawl is a nonprofit that crawls the web",
]
for text in texts:
    labels, scores = model.predict(text)
    print(f"{text!r} -> {labels[0]} 分数 {scores[0]:.3f}")
