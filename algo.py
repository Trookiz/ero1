import itertools

import networkx as nx
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