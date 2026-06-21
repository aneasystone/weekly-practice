import numpy as np
from turbovec import TurboQuantIndex

idx = TurboQuantIndex(dim=1536, bit_width=4)
vectors = np.random.randn(6, 1536).astype(np.float32)
idx.add(vectors)

print(len(idx))   # 6

moved_from = idx.swap_remove(2) # 槽位 5 的向量补到槽位 2
print(moved_from) # 5
