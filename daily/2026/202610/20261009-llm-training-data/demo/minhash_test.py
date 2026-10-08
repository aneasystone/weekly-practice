from datasketch import MinHash, MinHashLSH

docs = [
    "the quick brown fox jumps over the lazy dog",
    "the quick brown fox jumps over the lazy cat",   # 与第 1 条只差一个词
    "a completely different sentence about cooking",
    "the quick brown fox jumps over the lazy dog",   # 与第 1 条完全相同
]

def to_minhash(text):
    m = MinHash(num_perm=128)
    for word in text.split():
        m.update(word.encode("utf8"))
    return m

lsh = MinHashLSH(threshold=0.5, num_perm=128)
for i, doc in enumerate(docs):
    lsh.insert(f"doc{i}", to_minhash(doc))

# 查询与 doc0 相似的文档
result = lsh.query(to_minhash(docs[0]))
print("与 doc0 相似的文档:", result)
