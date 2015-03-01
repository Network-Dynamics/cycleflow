import networkx as nx
import numpy.linalg as linalg
from scipy.sparse.linalg import spsolve as solve
from scipy.sparse import csr_matrix 

def dF_with_distance(G, src_a=None, src_b=None):
        allnodes=G.nodes()

        shortest_pathlengths_ordered=[nx.single_source_shortest_path_length(G, src_a)[node] for node in allnodes]

        source_vector=csr_matrix((G.number_of_nodes(),1))        
        src_a_ind=allnodes.index(src_a)
        source_vector[src_a_ind]=1
       
        if src_b:
                src_b_ind=allnodes.index(src_b) if src_b else None
                source_vector[src_b_ind]=-1

                        
        return shortest_pathlengths_ordered,solve(G.loopy_laplacian(), source_vector)



        
