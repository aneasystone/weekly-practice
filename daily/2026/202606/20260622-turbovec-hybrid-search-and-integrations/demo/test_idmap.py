import numpy as np
from turbovec import IdMapIndex

index = IdMapIndex(dim=1536, bit_width=4)

docs = np.random.randn(3, 1536).astype(np.float32)
index.add_with_ids(docs, np.array([1001, 1002, 1003], dtype=np.uint64))

query = np.random.randn(1, 1536).astype(np.float32)

scores, ids = index.search(query, k=10)   # 返回的是你的 uint64 外部 ID
print(ids)
index.remove(1002)                         # 按 ID 删除，O(1)

assert 1002 not in index                   # 被删的 ID 已经不在
assert 1003 in index                       # 其余 ID 照旧，__contains__ 语法糖
scores, ids = index.search(query, k=10)    # 仍可正常检索，结果里不会再出现 1002
print(ids)
