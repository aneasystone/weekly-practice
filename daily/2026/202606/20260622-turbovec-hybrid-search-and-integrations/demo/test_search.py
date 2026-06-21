import numpy as np
from turbovec import TurboQuantIndex

idx = TurboQuantIndex(dim=1536, bit_width=4)
vectors = np.random.randn(6, 1536).astype(np.float32)
idx.add(vectors)

print(len(idx))   # 6

query = np.random.randn(1, 1536).astype(np.float32)
scores, slots = idx.search(query, k=10)
print(slots)

disabled_slots = [0,1,2]
mask = np.ones(len(idx), dtype=bool)
mask[disabled_slots] = False
scores, slots = idx.search(query, k=10, mask=mask)
print(slots)

############

from turbovec import IdMapIndex

idx = IdMapIndex(dim=1536, bit_width=4)
vectors = np.random.randn(6, 1536).astype(np.float32)
idx.add_with_ids(vectors, np.array([1001, 1002, 1003, 1004, 1005, 1006], dtype=np.uint64))

allowed = np.array([1001, 1002, 1003], dtype=np.uint64)
scores, ids = idx.search(query, k=10, allowlist=allowed)
print(ids)
