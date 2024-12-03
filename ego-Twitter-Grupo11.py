import networkx as nx

# Load the dataset
file_path = "twitter_combined.txt"  
G = nx.read_edgelist(file_path)

# Subset the graph based on degree threshold
degree_threshold = 50
subset_nodes = [node for node, degree in dict(G.degree()).items() if degree > degree_threshold]
subset_G = G.subgraph(subset_nodes)

# Compute metrics for the subset
subset_metrics = {
    "Nodes": subset_G.number_of_nodes(),
    "Edges": subset_G.number_of_edges(),
    "Nodes in largest WCC": len(max(nx.connected_components(subset_G), key=len)),
    "Edges in largest WCC": subset_G.subgraph(max(nx.connected_components(subset_G), key=len)).number_of_edges(),
    "Average clustering coefficient": nx.average_clustering(subset_G),
    "Number of triangles": sum(nx.triangles(subset_G).values()) // 3,
    "Fraction of closed triangles": nx.transitivity(subset_G),
    "Diameter": nx.diameter(subset_G) if nx.is_connected(subset_G) else "Graph not connected",
    "90-percentile effective diameter": nx.diameter(subset_G) * 0.9 if nx.is_connected(subset_G) else "N/A",
}

# Output the subset metrics
print("Subset Metrics:")
for key, value in subset_metrics.items():
    print(f"{key}: {value}")

# Add comparison logic here if needed, comparing with manually-entered full dataset values
full_dataset_metrics = {
    "Nodes": 81306,
    "Edges": 1768149,
    "Nodes in largest WCC": 81306,
    "Edges in largest WCC": 1768149,
    "Average clustering coefficient": 0.5653,
    "Number of triangles": 13082506,
    "Fraction of closed triangles": 0.06415,
    "Diameter": 7,
    "90-percentile effective diameter": 4.5,
}

print("\nComparison with Full Dataset:")
for key in full_dataset_metrics:
    subset_value = subset_metrics.get(key, "N/A")
    full_value = full_dataset_metrics[key]
    print(f"{key}: Subset = {subset_value}, Full Dataset = {full_value}")