import pandas as pd
from pathlib import Path

def write_parquet_example(filepath):
    """写入示例数据"""
    
    # 创建示例数据
    data = {
        'id': [1, 2, 3, 4, 5],
        'name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve'],
        'age': [25, 30, 35, 28, 32],
        'city': ['New York', 'London', 'Paris', 'Tokyo', 'Berlin'],
        'salary': [50000.0, 60000.0, 70000.0, 55000.0, 65000.0]
    }
    
    # 创建 DataFrame
    df = pd.DataFrame(data)
    
    # 写入 Parquet 文件
    output_path = Path(filepath)
    df.to_parquet(output_path, engine='pyarrow')
    
    print(f"数据已写入到: {output_path}")
    print(f"数据形状: {df.shape}")
    print(f"数据预览:\n{df.head()}")
    
    return output_path

def read_parquet_example(file_path: str):
    """读取示例文件"""
    
    # 读取完整数据
    df = pd.read_parquet(file_path, engine='pyarrow')
    print(f"\n读取完整数据:\n{df}")
    
    # 读取特定列
    df = pd.read_parquet(file_path, columns=['name', 'age', 'city'])
    print(f"\n读取特定列:\n{df}")
    
    return df

if __name__ == "__main__":
    
    # 1. 写入 Parquet 文件
    parquet_file = write_parquet_example('sample_data.parquet')
    
    # 2. 读取 Parquet 文件
    df = read_parquet_example('sample_data.parquet')
