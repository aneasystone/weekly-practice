from textblob import TextBlob

# 创建 TextBlob 对象
text = "Apple Inc, founded by Steve Jobs, develops innovative iPhone technology in California."
blob = TextBlob(text)

# 1. 分词
print("分词结果：")
print(blob.words)
# 输出：['Apple', 'Inc', 'founded', 'by', 'Steve', 'Jobs', 'develops', 'innovative', 'iPhone', 'technology', 'in', 'California']

# 2. 句子分割
print("\n句子分割：")
for sentence in blob.sentences:
    print(f"- {sentence}")
# 输出：- Apple Inc, founded by Steve Jobs, develops innovative iPhone technology in California.

# 3. 词性标注
print("\n词性标注：")
for word, pos in blob.tags:
    print(f"{word:12} {pos}")
# 输出：
# Apple        NNP
# Inc          NNP  
# founded      VBN
# by           IN
# Steve        NNP
# ...

# 4. 名词短语
# Attempted to load corpora/brown
print("\n名词短语：")
for noun in blob.noun_phrases:
    print(f"- {noun}")
# 输出：
# - apple inc
# - steve jobs
# - innovative iphone technology
# - california
