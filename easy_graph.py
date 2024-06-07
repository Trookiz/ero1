import networkx as nx

# Graph Creation :  example on a little data's amount
# Random GPS points
points_of_interest = {
    'Point A': (45.5017, -73.5673),  # Coordinates de Montréal
    'Point B': (45.5588, -73.5515),  # Other point
    'Point C': (45.5091, -73.5735),  # Another point again
}

# Create an empty graph
G_drones = nx.Graph()

# Add nodes
for point, coords in points_of_interest.items():
    G_drones.add_node(point, pos=coords)

# Add edges
G_drones.add_edge('Point A', 'Point B', weight=10)
G_drones.add_edge('Point B', 'Point C', weight=20)
G_drones.add_edge('Point A', 'Point C', weight=15)

# Get point's position for visualization
pos = nx.get_node_attributes(G_drones, 'pos')