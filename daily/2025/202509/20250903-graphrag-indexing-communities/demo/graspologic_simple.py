import json
import networkx as nx
from graspologic.partition import hierarchical_leiden

def create_random_graph(num_nodes, edge_probability, seed):
    """生成一个随机图"""
    
    G = nx.erdos_renyi_graph(num_nodes, edge_probability, seed=seed)
    
    # 给节点加上 label 属性
    for node in G.nodes():
        G.nodes[node]['label'] = f"Node_{node}"
    
    return G

def apply_hierarchical_leiden_clustering(graph, max_cluster_size, seed):
    """调用 Leiden 层次化聚类算法"""
    
    # 层次化聚类
    community_mapping = hierarchical_leiden(
        graph, 
        max_cluster_size=max_cluster_size, 
        random_seed=seed
    )
    
    formatted_mapping = [
        {
            "node": partition.node,
            "cluster": partition.cluster,
            "parent_cluster": partition.parent_cluster,
            "level": partition.level,
            "is_final_cluster": partition.is_final_cluster
        }
        for partition in community_mapping
    ]
    print(json.dumps(formatted_mapping))
    
    # 组织聚类结果
    results = {}
    hierarchy = {}
    
    for partition in community_mapping:
        level = partition.level
        if level not in results:
            results[level] = {}    
        results[level][partition.node] = partition.cluster
        hierarchy[partition.cluster] = partition.parent_cluster if partition.parent_cluster is not None else -1
    
    return results, hierarchy

if __name__ == "__main__":
    
    # 生成一个随机图
    G = create_random_graph(num_nodes=25, edge_probability=0.2, seed=42)
    
    # 调用 Leiden 层次化聚类算法
    clustering_results, hierarchy = apply_hierarchical_leiden_clustering(
        G, max_cluster_size=8, seed=42
    )
    
    print(json.dumps(clustering_results))
    print(json.dumps(hierarchy))