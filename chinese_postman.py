import itertools

import networkx as nx
from matplotlib import pyplot as plt

import easy_graph

# Fonction pour vérifier les degrés impairs
def get_odd_degree_nodes(G):
    return [v for v, d in G.degree() if d % 2 != 0]

# Fonction pour trouver le couplage minimum

def min_weight_matching(G, odd_nodes):
    pairs = list(itertools.combinations(odd_nodes, 2))
    pairs_weight = {(u, v): nx.shortest_path_length(G, u, v, weight='weight') for u, v in pairs}
    return nx.algorithms.matching.min_weight_matching(G, weight=lambda u, v: pairs_weight[(u, v)])

def draw_and_define(G):
    # Trouver les nœuds de degré impair
    odd_degree_nodes = get_odd_degree_nodes(G)

    # Faire correspondre les nœuds de degré impair
    matching = min_weight_matching(G, odd_degree_nodes)

    # Ajouter des arêtes en double pour équilibrer les degrés
    for u, v in matching:
        G.add_edge(u, v, weight=nx.shortest_path_length(G, u, v, weight='weight'))

    # Trouver le circuit eulérien
    eulerian_circuit = list(nx.eulerian_circuit(G))

    # Calculer la distance totale
    total_distance = sum(G[u][v]['weight'] for u, v in eulerian_circuit)

    # Afficher le circuit eulérien et la distance
    print("Circuit eulérien :")
    for edge in eulerian_circuit:
        print(f"{edge[0]} -> {edge[1]}")
    print(f"Distance totale : {total_distance:.2f} km")

    # Dessiner le graphe avec le circuit eulérien
    pos = {quartier: (coords[1], coords[0]) for quartier, coords in easy_graph.quartiers.items()}
    edge_list = [(u, v) for u, v in eulerian_circuit]
    nx.draw_networkx_nodes(G, pos, node_color='skyblue', node_size=700, alpha=0.8)
    nx.draw_networkx_edges(G, pos, edgelist=edge_list, width=2, edge_color='blue')
    nx.draw_networkx_labels(G, pos, font_size=10, font_family='sans-serif')

    plt.title('Graphe des quartiers de Montréal avec Circuit Eulérien')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.show()

    return total_distance