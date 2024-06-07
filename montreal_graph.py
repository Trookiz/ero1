# Real Montreal's coordinates

import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt

# Définir la zone d'intérêt - ici, Montréal
city_name = "Montréal, Québec, Canada"

# Extraire le graphe routier pour les véhicules motorisés
G = ox.graph_from_place(city_name, network_type='drive')

# Afficher le nombre de nœuds et d'arcs
print(f"Nombre de nœuds: {len(G.nodes)}")
print(f"Nombre d'arcs: {len(G.edges)}")

# Obtenir les positions des nœuds pour la visualisation
pos = {node: (data['x'], data['y']) for node, data in G.nodes(data=True)}

# Dessiner le graphe
plt.figure(figsize=(12, 8))
nx.draw(
    G,
    pos,
    node_size=10,          # Taille des nœuds
    node_color='blue',     # Couleur des nœuds
    edge_color='gray',     # Couleur des arêtes
    with_labels=False,     # Ne pas afficher les étiquettes
    font_size=12,
    font_color='black',
    font_weight='bold'
)

# Afficher le graphe
plt.title("Graphe routier de Montréal")
plt.show()