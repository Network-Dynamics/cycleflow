import numpy as np
import networkx as nx

def dF_with_distance(G, src_a=None, src_b=None):
	allnodes=G.nodes()
	Lg=np.linalg.pinv(G.loopy_laplacian())
	
	if src_b:
		return [(nx.shortest_path_length(G, source=src_a, target=node) , Lg[allnodes.index(node), allnodes.index(src_a)] -Lg[allnodes.index(node), allnodes.index(src_b)]) for node in allnodes]
	else:
		return [(nx.shortest_path_length(G, source=src_a, target=node) , Lg[allnodes.index(node), allnodes.index(src_a)]) for node in allnodes]



	
