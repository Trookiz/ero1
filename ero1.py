import networkx as nx
import matplotlib.pyplot as plt
import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt
import variable
import easy_graph
import a_star
import cost
#import montreal_graph

# Exemple d'utilisation
days = 1  # Durée de l'opération en jours
hours_type_one = 8  # Nombre d'heures pour les véhicules de type 1 par jour
hours_type_two = a_star.shortest_path_length_astar  * variable.distance_type_two_price # Nombre d'heures pour les véhicules de type 2 par jour
distance_drone = a_star.shortest_path_length_astar  # Distance parcourue par les drones

costs = cost.calculate_cost(days, hours_type_one, hours_type_two, distance_drone)

print(costs)

########################################################################################################################

import networkx as nx
from networkx.algorithms.matching import max_weight_matching
from itertools import combinations

def chinese_postman(G):
    # Convertir le graphe en undirected pour vérifier la connexité
    if not nx.is_connected(G.to_undirected()):
        raise nx.NetworkXError("Le graphe doit être connexe.")

    # Trouver les sommets de degré impair
    odd_degree_nodes = [v for v, d in G.degree() if d % 2 != 0]

    # Si tous les sommets ont un degré pair, le graphe est déjà Eulerien
    if len(odd_degree_nodes) == 0:
        eulerian_cycle = list(nx.eulerian_circuit(G, source=0))
        distance = sum(G[u][v]['length'] for u, v in eulerian_cycle)
        return eulerian_cycle, distance

    # Créer un graphe complet pondéré des sommets de degré impair
    odd_graph = nx.Graph()
    for u, v in combinations(odd_degree_nodes, 2):
        length = nx.shortest_path_length(G, source=u, target=v, weight='length')
        odd_graph.add_edge(u, v, weight=-length)  # Utiliser -length pour trouver le matching minimum

    # Trouver le plus court appariement parfait
    matching = max_weight_matching(odd_graph, maxcardinality=True, weight='weight')

    # Créer une copie du graphe pour le parcours sans modifier le graphe original
    G_aug = G.copy()

    # Ajouter les chemins correspondant aux arêtes du matching au graphe original
    for u, v in matching:
        path = nx.shortest_path(G, source=u, target=v, weight='length')
        for i in range(len(path) - 1):
            if G_aug.has_edge(path[i], path[i+1]):
                edge_data = G_aug.get_edge_data(path[i], path[i+1])
                edge_data['count'] = edge_data.get('count', 1) + 1
                G_aug.add_edge(path[i], path[i+1], **{str(k): v for k, v in edge_data.items()})
            else:
                G_aug.add_edge(path[i], path[i+1], length=G[path[i]][path[i+1]]['length'], count=1)

    # Trouver le circuit Eulerien sur le graphe modifié
    eulerian_path = []
    edge_count = {}

    for u, v, d in G_aug.edges(data=True):
        if isinstance(d, dict):
            edge_count[(u, v)] = edge_count[(v, u)] = d.get('count', 1)
        else:
            edge_count[(u, v)] = edge_count[(v, u)] = 1

    def find_eulerian_cycle(v):
        stack = [v]
        path = []
        total_length = 0
        while stack:
            u = stack[-1]
            for neighbor in list(G_aug.neighbors(u)):
                if edge_count[(u, neighbor)] > 0:
                    stack.append(neighbor)
                    edge_count[(u, neighbor)] -= 1
                    edge_count[(neighbor, u)] -= 1
                    total_length += G_aug[u][neighbor]['length']
                    break
            else:
                path.append(stack.pop())
        return path, total_length

    start_node = odd_degree_nodes[0] if odd_degree_nodes else list(G.nodes())[0]
    eulerian_path, total_distance = find_eulerian_cycle(start_node)

    return eulerian_path, total_distance

# Charger le graphe fourni
G = easy_graph.G_drones

# Convertir les attributs 'length' en nombres flottants
for u, v, data in G.edges(data=True):
    if 'length' in data:
        data['length'] = float(data['length'])
    else:
        data['length'] = 1.0  # Assignez une valeur par défaut si l'attribut 'length' est manquant

# Trouver le circuit Eulerien le plus court en repassant sur des arêtes
try:
    eulerian_cycle, total_distance = chinese_postman(G)
    print("Cycle eulérien le plus court:", eulerian_cycle)
    print("Distance totale du cycle eulérien:", total_distance)
except nx.NetworkXError as e:
    print(e)