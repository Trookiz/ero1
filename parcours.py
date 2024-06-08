import networkx as nx
from geopy.distance import geodesic
from matplotlib import pyplot as plt
from networkx import astar_path

import chinese_postman
import clustering
import cost
import easy_graph
from algo import make_graph_eulerian, make_graph_eulerian2

subgraphs = []

def sub_clustering(G, drone_distance):
    for i in range(clustering.n_clusters):
        subgraph = clustering.create_subgraph(G, easy_graph.quartiers, clustering.labels, i)
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
        print(f"Circuit eulérien pour la Centrale {i+1}:")
        for edge in eulerian_circuit:
            print(f"{edge[0]} -> {edge[1]}")
        print(f"Distance totale pour la Centrale {i+1}: {total_distance:.2f} km")

    for i, subgraph in enumerate(subgraphs):
        pos = {quartier: (coords[1], coords[0]) for quartier, coords in easy_graph.quartiers.items()}
        eulerian_circuit = list(nx.eulerian_circuit(subgraph))
        edge_list = [(u, v) for u, v in eulerian_circuit]

        plt.figure()
        nx.draw_networkx_nodes(subgraph, pos, node_color='skyblue', node_size=700, alpha=0.8)
        nx.draw_networkx_edges(subgraph, pos, edgelist=edge_list, width=2, edge_color='blue')
        nx.draw_networkx_labels(subgraph, pos, font_size=10, font_family='sans-serif')
        plt.title(f'Itinéraire de déneigement pour Centrale {i + 1}')
        plt.xlabel('Longitude')
        plt.ylabel('Latitude')
        plt.show()

    def heuristic(u, v):
        coords_u = G.nodes[u]['pos']
        coords_v = G.nodes[v]['pos']
        return geodesic(coords_u, coords_v).kilometers

    def centralisation(G):
        cout = cost.calculate_cost_drone(1, drone_distance)
        for i, subgraph in enumerate(subgraphs):
            centrale = clustering.centrales[f'Cluster {i + 1}']
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
            cout += cost.calculate_cost_type_one(1, total_distance, 4)
            print("cout : " + str(cout))
            print(cost.calculate_cost_total(1, drone_distance, total_distance, 0))

            print(f"Chemin complet pour la Centrale {i + 1}: {complete_path}")
            print(f"Distance totale pour la Centrale {i + 1} avec A*: {total_distance:.2f} km")

            # Afficher le chemin
            edge_list = [(u, v) for u, v in zip(complete_path[:-1], complete_path[1:])]
            plt.figure()
            nx.draw_networkx_nodes(G, pos, node_color='skyblue', node_size=700, alpha=0.8)
            nx.draw_networkx_edges(G, pos, edgelist=edge_list, width=2, edge_color='red')
            nx.draw_networkx_labels(G, pos, font_size=10, font_family='sans-serif')
            plt.title(f'Chemin optimisé pour Centrale {i + 1}')
            plt.xlabel('Longitude')
            plt.ylabel('Latitude')
            plt.show()

    centralisation(G)

