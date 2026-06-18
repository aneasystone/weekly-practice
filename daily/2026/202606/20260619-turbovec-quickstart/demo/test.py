import numpy as np
from turbovec import TurboQuantIndex

# 维度 1536（对齐 OpenAI text-embedding-3-small），4-bit 量化
index = TurboQuantIndex(dim=1536, bit_width=4)

# 假设这是一批文档向量，实际中来自 embedding 模型
vectors = np.random.randn(10000, 1536).astype(np.float32)
index.add(vectors)

# 还能继续增量添加，不需要重建
more_vectors = np.random.randn(5000, 1536).astype(np.float32)
index.add(more_vectors)

print(len(index))   # 15000

############

# 查询也要是二维的，1 条查询就是形状 (1, 1536)
query = np.random.randn(1, 1536).astype(np.float32)

# 返回 top-10 的分数和下标
scores, indices = index.search(query, k=10)

print(indices[0])   # 命中的向量下标
print(scores[0])    # 对应的相似度分数

############

index.write("my_index.tv")

loaded = TurboQuantIndex.load("my_index.tv")
scores, indices = loaded.search(query, k=10)

print(indices[0])   # 命中的向量下标
print(scores[0])    # 对应的相似度分数
