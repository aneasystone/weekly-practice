import json
import orjson
import time

# 测试数据，构造大对象
data = {
    "users": [
        {"id": i, "name": f"user_{i}", "email": f"user_{i}@example.com"}
        for i in range(10000)
    ]
}

# 性能对比
def benchmark_json():
    start = time.time()
    for _ in range(10000):
        json.dumps(data)
    return time.time() - start

def benchmark_orjson():
    start = time.time()
    for _ in range(10000):
        orjson.dumps(data).decode('utf-8')
    return time.time() - start

json_time = benchmark_json()
orjson_time = benchmark_orjson()
print(f"json 耗时：{json_time}")
print(f"orjson 耗时：{orjson_time}")
print(f"orjson 比 json 快了 {json_time / orjson_time:.2f} 倍")