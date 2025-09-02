"""
Demo showing how to use graspologic's hierarchical_leiden for graph clustering.
This example creates a random graph and applies hierarchical clustering.
"""

import networkx as nx
import numpy as np
from graspologic.partition import hierarchical_leiden
import matplotlib.pyplot as plt
import json

def create_random_graph(num_nodes, edge_probability, seed):
    """Create a random graph for demonstration."""
    # np.random.seed(seed)
    G = nx.erdos_renyi_graph(num_nodes, edge_probability, seed=seed)
    
    # Add some node attributes for visualization
    for node in G.nodes():
        G.nodes[node]['label'] = f"Node_{node}"
    
    # nx.write_graphml(G, "demo.graphml", encoding='utf-8')
    return G


def apply_hierarchical_leiden_clustering(graph, max_cluster_size=10, seed=42):
    """Apply hierarchical Leiden clustering to the graph."""
    print(f"Applying hierarchical Leiden clustering to graph with {len(graph.nodes)} nodes and {len(graph.edges)} edges")
    
    # Apply hierarchical clustering
    community_mapping = hierarchical_leiden(
        graph, 
        max_cluster_size=max_cluster_size, 
        random_seed=seed
    )
    print(json.dumps(community_mapping))
    print('---')
    
    # Process the results
    results = {}
    hierarchy = {}
    
    for partition in community_mapping:
        level = partition.level
        if level not in results:
            results[level] = {}
        
        results[level][partition.node] = partition.cluster
        hierarchy[partition.cluster] = partition.parent_cluster if partition.parent_cluster is not None else -1
    
    print(json.dumps(results))
    print('---')
    print(json.dumps(hierarchy))
    print('---')
    return results, hierarchy


def visualize_clusters(graph, clustering_results, level=0):
    """Visualize the graph with cluster coloring."""
    if level not in clustering_results:
        print(f"Level {level} not found in clustering results")
        return
    
    # Get cluster assignments for the specified level
    cluster_assignments = clustering_results[level]
    
    # Create color map for clusters with more distinguishable colors
    unique_clusters = set(cluster_assignments.values())
    # Remove -1 (unassigned nodes) from unique_clusters for coloring
    if -1 in unique_clusters:
        unique_clusters.remove(-1)
    
    # Use a set of highly distinguishable colors
    distinct_colors = [
        '#FF0000',  # Red
        '#0000FF',  # Blue
        '#00FF00',  # Green
        '#FFFF00',  # Yellow
        '#FF00FF',  # Magenta
        '#00FFFF',  # Cyan
        '#FF8000',  # Orange
        '#8000FF',  # Purple
        '#FF0080',  # Pink
        '#80FF00',  # Lime
        '#0080FF',  # Light Blue
        '#FF8080',  # Light Red
        '#80FF80',  # Light Green
        '#8080FF',  # Light Blue
        '#FFFF80',  # Light Yellow
        '#FF80FF',  # Light Magenta
        '#80FFFF',  # Light Cyan
        '#FFB366',  # Light Orange
        '#B366FF',  # Light Purple
        '#66FFB3',  # Mint
    ]
    
    # Use distinct colors, and if we need more, generate additional ones
    if len(unique_clusters) <= len(distinct_colors):
        colors = distinct_colors[:len(unique_clusters)]
    else:
        # Use distinct colors first, then generate additional ones
        colors = distinct_colors + list(plt.cm.Set3(np.linspace(0, 1, len(unique_clusters) - len(distinct_colors))))
    
    color_map = {cluster: colors[i] for i, cluster in enumerate(unique_clusters)}
    # Add gray color for unassigned nodes
    color_map[-1] = '#CCCCCC'  # Gray color
    
    # Set node colors based on cluster assignments
    node_colors = []
    for node in graph.nodes():
        cluster_id = cluster_assignments.get(node, -1)
        node_colors.append(color_map[cluster_id])
    
    # Draw the graph
    plt.figure(figsize=(12, 8))
    pos = nx.spring_layout(graph, seed=42)
    
    nx.draw(graph, pos, 
            node_color=node_colors, 
            node_size=500, 
            with_labels=True,
            font_size=10,
            font_weight='bold',
            edge_color='gray',
            width=1.5)
    
    plt.title(f"Graph Clustering with Hierarchical Leiden (Level {level})")
    plt.axis('off')
    plt.tight_layout()
    plt.show()


def print_clustering_info(clustering_results, hierarchy):
    """Print information about the clustering results."""
    print("\n=== Clustering Results ===")
    
    for level in sorted(clustering_results.keys()):
        clusters = clustering_results[level]
        unique_clusters = set(clusters.values())
        print(f"\nLevel {level}:")
        print(f"  Number of clusters: {len(unique_clusters)}")
        print(f"  Cluster assignments: {dict(list(clusters.items())[:5])}...")  # Show first 5
    
    print(f"\n=== Hierarchy Information ===")
    print(f"Total clusters in hierarchy: {len(hierarchy)}")
    
    # Show some hierarchy relationships
    print("Sample hierarchy relationships:")
    for i, (cluster, parent) in enumerate(hierarchy.items()):
        if i < 5:  # Show first 5
            print(f"  Cluster {cluster} -> Parent: {parent}")


def main():
    """Main function to demonstrate hierarchical Leiden clustering."""
    print("=== Graspologic Hierarchical Leiden Clustering Demo ===\n")
    
    # Create a random graph
    G = create_random_graph(num_nodes=25, edge_probability=0.2, seed=42)
    print(f"Created random graph with {len(G.nodes)} nodes and {len(G.edges)} edges")
    
    # Apply clustering
    clustering_results, hierarchy = apply_hierarchical_leiden_clustering(
        G, max_cluster_size=8, seed=42
    )
    
    # Print clustering information
    print_clustering_info(clustering_results, hierarchy)
    
    # Visualize clusters at different levels
    print("\n=== Visualization ===")
    print("Generating visualizations for different clustering levels...")
    
    available_levels = sorted(clustering_results.keys())
    for level in available_levels:
        print(f"Visualizing level {level}...")
        visualize_clusters(G, clustering_results, level)
    
    print("\nDemo completed successfully!")


if __name__ == "__main__":
    main()