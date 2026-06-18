import numpy as np
from turbovec import IdMapIndex

# 维度 1536（对齐 OpenAI text-embedding-3-small），4-bit 量化
index = IdMapIndex(dim=1536, bit_width=4)

# 3 条向量，配上 3 个业务侧的 uint64 ID
docs = np.random.randn(3, 1536).astype(np.float32)
index.add_with_ids(docs, np.array([1001, 1002, 1003], dtype=np.uint64))

print(len(index))   # 3

query = np.random.randn(1, 1536).astype(np.float32)

scores, ids = index.search(query, k=10)   # 返回的是你的 uint64 外部 ID

print(ids[0])       # 命中的 ID
print(scores[0])    # 对应的相似度分数

index.remove(1002)                         # 按 ID 删除，O(1)
print(1002 in index)                       # False，支持成员判断

index.write("my_index.tvim")

loaded = IdMapIndex.load("my_index.tvim")
scores, ids = index.search(query, k=10)   # 返回的是你的 uint64 外部 ID

print(ids[0])       # 命中的 ID
print(scores[0])    # 对应的相似度分数
