import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from pathlib import Path
from typing import Dict, List, Any

def write_parquet_example():
    """示例：创建DataFrame并写入Parquet文件"""
    
    # 创建示例数据
    data = {
        'id': [1, 2, 3, 4, 5],
        'name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve'],
        'age': [25, 30, 35, 28, 32],
        'city': ['New York', 'London', 'Paris', 'Tokyo', 'Berlin'],
        'salary': [50000.0, 60000.0, 70000.0, 55000.0, 65000.0]
    }
    
    # 创建DataFrame
    df = pd.DataFrame(data)
    
    # 写入Parquet文件
    output_path = Path('sample_data.parquet')
    df.to_parquet(output_path, engine='pyarrow')
    
    print(f"数据已写入到: {output_path}")
    print(f"数据形状: {df.shape}")
    print(f"数据预览:\n{df.head()}")
    
    return output_path

def read_parquet_example(file_path: str):
    """示例：读取Parquet文件"""
    
    # 方法1：使用pandas读取
    df_pandas = pd.read_parquet(file_path, engine='pyarrow')
    print(f"\n使用pandas读取的数据:\n{df_pandas}")
    
    # 方法2：使用pyarrow直接读取
    table = pq.read_table(file_path)
    print(f"\n使用pyarrow读取的表格信息:\n{table}")
    
    # 获取schema信息
    print(f"\nSchema信息:")
    for field in table.schema:
        print(f"  {field.name}: {field.type}")
    
    # 转换为pandas DataFrame
    df_arrow = table.to_pandas()
    print(f"\n从Arrow表格转换的DataFrame:\n{df_arrow}")
    
    return df_pandas

def read_parquet_with_filter(file_path: str):
    """示例：读取Parquet文件并进行过滤"""
    
    # 读取特定列
    df = pd.read_parquet(file_path, columns=['name', 'age', 'city'])
    print(f"\n读取特定列:\n{df}")
    
    # 读取并进行过滤
    df = pd.read_parquet(file_path)
    filtered_df = df[df['age'] > 30]
    print(f"\n年龄大于30的记录:\n{filtered_df}")
    
    return filtered_df

def write_multiple_partitions():
    """示例：创建分区Parquet文件"""
    
    # 创建更多示例数据
    data = {
        'id': range(1, 11),
        'name': [f'Person_{i}' for i in range(1, 11)],
        'department': ['IT', 'HR', 'Finance', 'IT', 'HR', 'Finance', 'IT', 'HR', 'Finance', 'IT'],
        'salary': [50000 + i * 1000 for i in range(10)],
        'year': [2023] * 5 + [2024] * 5
    }
    
    df = pd.DataFrame(data)
    
    # 按部门分区写入
    output_dir = Path('partitioned_data')
    output_dir.mkdir(exist_ok=True)
    
    for dept in df['department'].unique():
        dept_df = df[df['department'] == dept]
        dept_path = output_dir / f'department={dept}'
        dept_path.mkdir(exist_ok=True)
        dept_df.to_parquet(dept_path / 'data.parquet', engine='pyarrow')
    
    print(f"分区数据已写入到: {output_dir}")
    return output_dir

def read_parquet_metadata(file_path: str):
    """示例：读取Parquet文件的元数据"""
    
    # 读取文件元数据
    table = pq.read_table(file_path)
    
    print(f"\nParquet文件元数据:")
    print(f"行数: {table.num_rows}")
    print(f"列数: {table.num_columns}")
    print(f"Schema: {table.schema}")
    
    # 读取文件统计信息
    metadata = pq.read_metadata(file_path)
    print(f"\n文件统计信息:")
    print(f"创建时间: {metadata.created_by}")
    print(f"行组数量: {metadata.num_row_groups}")
    
    return table

df = read_parquet_example("../ragtest/output/community_reports.parquet")

if __name__ == "__main__x":
    # 运行示例
    print("=== Parquet文件读写示例 ===")
    
    # 1. 写入Parquet文件
    parquet_file = write_parquet_example()
    
    # 2. 读取Parquet文件
    df = read_parquet_example(parquet_file)
    
    # 3. 过滤读取
    filtered_df = read_parquet_with_filter(parquet_file)
    
    # 4. 读取元数据
    table = read_parquet_metadata(parquet_file)
    
    # 5. 创建分区文件
    partitioned_dir = write_multiple_partitions()
    
    print("\n=== 示例完成 ===")