import networkx as nx
import matplotlib.pyplot as plt
import easy_graph

G_drones = easy_graph.G_drones
pos = easy_graph.pos

# Application algorithm's shortest path

# Algorithm A* between 'Point A' and 'Point C' (using geographical's distance like heuristic)
# La distance géographique est la distance euclidienne pour ce petit exemple
shortest_path_astar = nx.astar_path(G_drones, 'Point A', 'Point C', heuristic=lambda u, v: nx.shortest_path_length(G_drones, u, v, weight='weight'))
shortest_path_length_astar = nx.astar_path_length(G_drones, 'Point A', 'Point C', heuristic=lambda u, v: nx.shortest_path_length(G_drones, u, v, weight='weight'))

print(f"Plus court chemin (A*) de 'Point A' à 'Point C': {shortest_path_astar}")
print(f"Longueur du plus court chemin (A*): {shortest_path_length_astar}")

# Graph analysis

# Calcul node's centrality
centrality = nx.degree_centrality(G_drones)
print(f"Centralité des nœuds: {centrality}")

# Calcul node's degree
degree = dict(G_drones.degree())
print(f"Degré des nœuds: {degree}")

# Draw  the graph
plt.figure(figsize=(8, 6))
nx.draw(G_drones, pos, with_labels=True, node_size=700, node_color='skyblue', font_size=10, font_weight='bold', edge_color='gray')
nx.draw_networkx_edge_labels(G_drones, pos, edge_labels={(u, v): d['weight'] for u, v, d in G_drones.edges(data=True)})
plt.title("Graphe des points d'application pour les drones")
plt.show()