import itertools

import networkx as nx
import matplotlib.pyplot as plt
import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt
from networkx.utils import not_implemented_for

import variable
import easy_graph
import cost
import chinese_postman




import numpy as np
from sklearn.cluster import KMeans

# Convertir les coordonnées des quartiers en array pour K-means
quartiers_coords = np.array(list(easy_graph.quartiers.values()))

# Nombre de clusters (à ajuster selon les besoins)
n_clusters = 4

# Appliquer K-means
kmeans = KMeans(n_clusters=n_clusters, random_state=42)
kmeans.fit(quartiers_coords)
labels = kmeans.labels_

# Afficher les clusters
for i in range(n_clusters):
    cluster_points = quartiers_coords[labels == i]
    plt.scatter(cluster_points[:, 1], cluster_points[:, 0], label=f'Cluster {i+1}')

# Afficher les centres des clusters
cluster_centers = kmeans.cluster_centers_
plt.scatter(cluster_centers[:, 1], cluster_centers[:, 0], s=200, c='red', label='Centres des clusters')

plt.title('Clustering des quartiers de Montréal')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.legend()
plt.show()
# ----------------------------------------------------------------------------------------------------------------------
# Trouver la centrale pour chaque cluster
centrales = {}
for i in range(n_clusters):
    cluster_points = quartiers_coords[labels == i]
    center = cluster_centers[i]
    distances = np.linalg.norm(cluster_points - center, axis=1)
    central_index = np.argmin(distances)
    centrale_quartier = list(easy_graph.quartiers.keys())[labels.tolist().index(i)]
    centrales[f'Cluster {i+1}'] = centrale_quartier

print("Centrales des clusters:", centrales)

# ----------------------------------------------------------------------------------------------------------------------
def create_subgraph(G, quartiers, labels, cluster_label):
    subgraph = nx.Graph()
    cluster_nodes = [quartier for quartier, label in zip(quartiers.keys(), labels) if label == cluster_label]
    for node in cluster_nodes:
        subgraph.add_node(node, pos=G.nodes[node]['pos'])
    for u, v in itertools.combinations(cluster_nodes, 2):
        if G.has_edge(u, v):
            subgraph.add_edge(u, v, weight=G[u][v]['weight'])
    return subgraph

# Créer et dessiner les sous-graphes
G = easy_graph.G

from geopy.distance import geodesic


def make_graph_eulerian(G):
    # Identifier les sommets de degré impair
    odd_degree_nodes = [v for v, d in G.degree() if d % 2 == 1]
    #print(f"Sommets de degré impair : {odd_degree_nodes}")

    while odd_degree_nodes:
        u = odd_degree_nodes.pop()
        for v in G.nodes():
            if v != u and not G.has_edge(u, v):
                distance = geodesic(G.nodes[u]['pos'], G.nodes[v]['pos']).kilometers
                G.add_edge(u, v, weight=distance)
                print(f"Ajout de l'arête entre {u} et {v} avec une distance de {distance} km")
                break

    return G


# Fonction pour rendre le graphe eulérien
def make_graph_eulerian2(G):
    # Identifier les sommets de degré impair
    odd_degree_nodes = [v for v, d in G.degree() if d % 2 == 1]
    #print(f"Sommets de degré impair : {odd_degree_nodes}")

    # Créer un sous-graphe des sommets de degré impair
    odd_subgraph = nx.Graph()
    for u, v in itertools.combinations(odd_degree_nodes, 2):
        distance = geodesic(G.nodes[u]['pos'], G.nodes[v]['pos']).kilometers
        odd_subgraph.add_edge(u, v, weight=distance)

    # Trouver le matching minimum pour les sommets impairs
    matching = nx.algorithms.matching.min_weight_matching(odd_subgraph, weight='weight')
    #print(f"Matching trouvé : {matching}")

    # Ajouter les arêtes correspondantes pour équilibrer les degrés
    for u, v in matching:
        path = nx.shortest_path(G, u, v, weight='weight')
        for i in range(len(path) - 1):
            G.remove_edge(path[i], path[i + 1])

    return G

subgraphs = []
for i in range(n_clusters):
    subgraph = create_subgraph(G, easy_graph.quartiers, labels, i)
    odd_degree_nodes = [v for v, d in subgraph.degree() if d % 2 == 1]
    #print(f"Sommets de degré impair A : {odd_degree_nodes}")
    subgraph = make_graph_eulerian(subgraph)
    odd_degree_nodes = [v for v, d in subgraph.degree() if d % 2 == 1]
    if odd_degree_nodes != []:
        subgraph = make_graph_eulerian2(subgraph)
    subgraphs.append(subgraph)

    # Circuit eulérien
    eulerian_circuit = list(nx.eulerian_circuit(subgraph))
    total_distance = sum(subgraph[u][v]['weight'] for u, v in eulerian_circuit)

    # Afficher le circuit eulérien
    print(f"Circuit eulérien pour le Cluster {i+1}:")
    for edge in eulerian_circuit:
        print(f"{edge[0]} -> {edge[1]}")
    print(f"Distance totale pour le Cluster {i+1}: {total_distance:.2f} km")

for i, subgraph in enumerate(subgraphs):
    pos = {quartier: (coords[1], coords[0]) for quartier, coords in easy_graph.quartiers.items()}
    eulerian_circuit = list(nx.eulerian_circuit(subgraph))
    edge_list = [(u, v) for u, v in eulerian_circuit]

    plt.figure()
    nx.draw_networkx_nodes(subgraph, pos, node_color='skyblue', node_size=700, alpha=0.8)
    nx.draw_networkx_edges(subgraph, pos, edgelist=edge_list, width=2, edge_color='blue')
    nx.draw_networkx_labels(subgraph, pos, font_size=10, font_family='sans-serif')
    plt.title(f'Itinéraire de déneigement pour Cluster {i + 1}')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.show()



from networkx.algorithms.shortest_paths.astar import astar_path

def heuristic(u, v):
    coords_u = G.nodes[u]['pos']
    coords_v = G.nodes[v]['pos']
    return geodesic(coords_u, coords_v).kilometers

for i, subgraph in enumerate(subgraphs):
    centrale = centrales[f'Cluster {i+1}']
    eulerian_circuit = list(nx.eulerian_circuit(subgraph))

    # Calcul du chemin A* entre la centrale et le premier point du circuit
    start_point = eulerian_circuit[0][0]
    path_to_start = astar_path(G, centrale, start_point, heuristic=heuristic)

    # Chemin complet de la déneigeuse
    complete_path = path_to_start
    for u, v in eulerian_circuit:
        path_segment = astar_path(G, u, v, heuristic=heuristic)
        complete_path.extend(path_segment[1:])

    # Calculer la distance totale
    total_distance = sum(G[u][v]['weight'] for u, v in zip(complete_path[:-1], complete_path[1:]))

    print(f"Chemin complet pour le Cluster {i+1}: {complete_path}")
    print(f"Distance totale pour le Cluster {i+1} avec A*: {total_distance:.2f} km")

    # Afficher le chemin
    edge_list = [(u, v) for u, v in zip(complete_path[:-1], complete_path[1:])]
    plt.figure()
    nx.draw_networkx_nodes(G, pos, node_color='skyblue', node_size=700, alpha=0.8)
    nx.draw_networkx_edges(G, pos, edgelist=edge_list, width=2, edge_color='red')
    nx.draw_networkx_labels(G, pos, font_size=10, font_family='sans-serif')
    plt.title(f'Chemin optimisé pour Cluster {i+1}')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.show()

