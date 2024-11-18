# File path: twitter_analysis_optimized.py

import networkx as nx
import matplotlib.pyplot as plt
from collections import Counter
import random

# Load a sampled dataset
def load_sampled_twitter_data(file_path, sample_edges=100000):
    G = nx.Graph()
    with open(file_path, 'r') as f:
        for i, line in enumerate(f):
            if i >= sample_edges:
                break  # Stop reading after reaching the sample size
            edge = line.strip().split()
            if len(edge) == 2:
                G.add_edge(edge[0], edge[1])
    return G

# Create subset of the graph
def create_graph_subset(G, degree_threshold=50):
    # Filter nodes based on degree threshold
    nodes_subset = [node for node, degree in dict(G.degree()).items() if degree > degree_threshold]
    subset_G = G.subgraph(nodes_subset)
    return subset_G

# Approximate analysis of graph statistics
def analyze_graph_approx(G):
    stats = {
        "num_nodes": G.number_of_nodes(),
        "num_edges": G.number_of_edges(),
        "average_clustering_coefficient": nx.average_clustering(G),
        "approx_diameter": nx.approximation.diameter(G) if nx.is_connected(G) else "Graph not connected",
        "largest_connected_component_size": len(max(nx.connected_components(G), key=len)),
        "degree_distribution": Counter(dict(G.degree()).values()),
    }
    return stats

# Visualize degree distribution
def plot_degree_distribution(degree_distribution, title="Degree Distribution"):
    degrees = list(degree_distribution.keys())
    counts = list(degree_distribution.values())
    plt.figure(figsize=(8, 6))
    plt.bar(degrees, counts, width=0.80, color='b')
    plt.title(title)
    plt.xlabel("Degree")
    plt.ylabel("Frequency")
    plt.show()

# Main function
def main():
    # File path
    file_path = 'twitter_combined.txt'
    sample_size = 100000  # Number of edges to sample
    degree_threshold = 50  # Subset criteria
    
    # Load a sampled dataset
    print(f"Loading a sample of {sample_size} edges from the dataset...")
    G = load_sampled_twitter_data(file_path, sample_edges=sample_size)
    print(f"Sampled graph loaded: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")
    
    # Create subset
    print(f"Creating a subset of nodes with degree > {degree_threshold}...")
    subset_G = create_graph_subset(G, degree_threshold=degree_threshold)
    print(f"Subset created: {subset_G.number_of_nodes()} nodes, {subset_G.number_of_edges()} edges")
    
    # Analyze sampled graph and subset
    print("Analyzing sampled graph...")
    sampled_graph_stats = analyze_graph_approx(G)
    print("Analyzing subset graph...")
    subset_graph_stats = analyze_graph_approx(subset_G)
    
    # Print stats
    print("Sampled Graph Stats:", sampled_graph_stats)
    print("Subset Graph Stats:", subset_graph_stats)
    
    # Visualize degree distribution
    plot_degree_distribution(sampled_graph_stats["degree_distribution"], "Sampled Graph Degree Distribution")
    plot_degree_distribution(subset_graph_stats["degree_distribution"], "Subset Graph Degree Distribution")

if __name__ == "__main__":
    main()
