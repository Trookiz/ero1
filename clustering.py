import itertools

import networkx as nx
import numpy as np
from matplotlib import pyplot as plt
from sklearn.cluster import KMeans
import easy_graph

# Convertir les coordonnées des quartiers en array pour K-means
quartiers_coords = np.array(list(easy_graph.quartiers.values()))

# Nombre de clusters (à ajuster selon les besoins)
n_clusters = 4

# Appliquer K-means
kmeans = KMeans(n_clusters=n_clusters, random_state=42)
kmeans.fit(quartiers_coords)
labels = kmeans.labels_

centrales = {}
def clustering():
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

    # Trouver la centrale pour chaque cluster
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