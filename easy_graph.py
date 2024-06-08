import networkx as nx
import matplotlib.pyplot as plt
from geopy.distance import geodesic

# Liste des quartiers de Montréal avec coordonnées géographiques
quartiers = {
    'Plateau-Mont-Royal': (45.5260, -73.5770),
    'Outremont': (45.5176, -73.6047),
    'Ville-Marie': (45.5087, -73.554),
    'Rosemont–La Petite-Patrie': (45.5418, -73.603),
    'Côte-des-Neiges–Notre-Dame-de-Grâce': (45.4879, -73.6405),
    'Hochelaga-Maisonneuve': (45.5552, -73.5396),
    'Verdun': (45.4600, -73.5670),
    'Villeray–Saint-Michel–Parc-Extension': (45.5518, -73.6129),
    'Mercier–Hochelaga-Maisonneuve': (45.5809, -73.5447),
    'Saint-Laurent': (45.5095, -73.6864),
    'Lachine': (45.4310, -73.6754),
    'Lasalle': (45.4310, -73.6180),
    'Ahuntsic-Cartierville': (45.5562, -73.6664),
    'Saint-Léonard': (45.5807, -73.6091),
    'Anjou': (45.6059, -73.5634),
    'Mont-Royal': (45.5184, -73.6458),
    'Pointe-aux-Trembles': (45.6481, -73.5046)
}

# Création d'un graphe
G = nx.Graph()

# Ajout des quartiers comme nœuds avec leurs coordonnées
for quartier, coords in quartiers.items():
    G.add_node(quartier, pos=coords)

# Ajout des arêtes avec la distance comme poids
for quartier1, coords1 in quartiers.items():
    for quartier2, coords2 in quartiers.items():
        if quartier1 != quartier2:
            distance = geodesic(coords1, coords2).kilometers
            G.add_edge(quartier1, quartier2, weight=distance)

# Dessiner le graphe
pos = {quartier: (coords[1], coords[0]) for quartier, coords in quartiers.items()}  # Inverser les coordonnées pour Matplotlib
edges = G.edges(data=True)

# Récupérer les poids pour la largeur des arêtes
weights = [edge[2]['weight'] for edge in edges]
norm_weights = [weight / max(weights) for weight in weights]  # Normaliser les poids pour la largeur des arêtes

# Configurer les largeurs d'arête
edge_widths = [weight * 3 for weight in norm_weights]  # Multiplier pour mieux visualiser

# Afficher les nœuds
nx.draw_networkx_nodes(G, pos, node_color='skyblue', node_size=700, alpha=0.8)

# Afficher les arêtes
nx.draw_networkx_edges(G, pos, width=edge_widths, edge_color=norm_weights, edge_cmap=plt.cm.Blues)

# Afficher les étiquettes
nx.draw_networkx_labels(G, pos, font_size=10, font_family='sans-serif')


