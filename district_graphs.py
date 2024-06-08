import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt

districts = [
    "Outremont, Montréal, Québec, Canada",
    "Verdun, Montréal, Québec, Canada",
    "Anjou, Montréal, Québec, Canada",
    "Rivière-des-Prairies-Pointe-aux-Trembles, Montréal, Québec, Canada",
    "Le Plateau-Mont-Royal, Montréal, Québec, Canada"
]

#returns a list of directed graphs that represent the map of each district
#in the input list
def load_districts(districts):
    district_graphs = {}
    count = 1
    l = len(districts)
    for district in districts:
        print("loading graph " + str(count) + " of " + str(l))
        count += 1
        # Extract the graph for the current district
        G = ox.graph_from_place(district, network_type='drive')
        # Store the graph in the dictionary
        district_graphs[district] = G
    return district_graphs

#draws the map from a district graph
def draw_district(G):
    pos = {node: (data['x'], data['y']) for node, data in G.nodes(data=True)}
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
    plt.title("Road Network")
    plt.show()

graphs = load_districts(districts)
for G in districts:
    draw_district(graphs[G])
