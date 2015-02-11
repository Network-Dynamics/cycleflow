import networkx as nx
import numpy.linalg as linalg
import scipy.sparse.linalg as linalg
from scipy.sparse import csc_matrix 


def dF_with_distance(G, src_a=None, src_b=None):
	allnodes=G.nodes()
	Lg=linalg.inv(csc_matrix(G.loopy_laplacian())).toarray()

        shortest_pathlengths_ordered=[nx.single_source_shortest_path_length(G, src_a)[node] for node in allnodes]
        
        src_a_ind=allnodes.index(src_a)
        src_b_ind=allnodes.index(src_b) if src_b else None
        	
	if src_b:

                return zip(shortest_pathlengths_ordered , Lg[:,src_a_ind]-Lg[:,src_b_ind])
                
        else:
                return zip(shortest_pathlengths_ordered , Lg[:,src_a_ind])



	
