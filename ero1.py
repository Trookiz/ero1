import itertools
import networkx as nx
import matplotlib.pyplot as plt
import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt
from networkx.utils import not_implemented_for

import parcours
import variable
import easy_graph
import cost
import chinese_postman
import numpy as np
from sklearn.cluster import KMeans
import clustering

# Créer et dessiner les sous-graphes
G = nx.Graph()
G = easy_graph.create_map(G)
easy_graph.draw_map(G)

drone_distance = chinese_postman.draw_and_define(G)
clustering.clustering()
parcours.sub_clustering(G, drone_distance)