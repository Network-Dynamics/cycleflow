import networkx as nx
import numpy as np
import scipy.sparse as sparse

class RandomPlanarGraph(nx.Graph):
        def __init__(self, n, p_merge):
                G=nx.grid_2d_graph(n,n)
                self.gridsize=n
                nx.Graph.__init__(self,G)

                if p_merge:
	                for node in self.nodes():
	                        if np.random.random()<p_merge:
	                                neighbors=self.neighbors(node)
	                                
	                                merge_with=neighbors[np.random.randint(len(neighbors))]
	                                neighbors.remove(merge_with)
	                                
	                                for other_neighbor in neighbors:
	                                        self.add_edge(merge_with, other_neighbor)
	                                self.remove_node(node)
	


        def choose_2_central_nodes(self):
                N=self.gridsize
                dists_from_cents=np.array([[n,np.abs(n[0]-N/2)+np.abs(n[1]-N/2)] for n in self.nodes()])
                centralmost=dists_from_cents[np.argmin(dists_from_cents[:,1])][0]
                other=nx.neighbors(self, centralmost)[0]
                return centralmost, other


        def _is_global_extremum(self, x,lst):
                return (x==max(lst)) or (x==min(lst))
        
        
          
        def loopy_degree(self):
                ldegrees=self.degree()

                coordarray_x,coordarray_y=np.array(self.nodes()).T

                for x in xrange(self.gridsize):
                        col=coordarray_y[coordarray_x==x]
                        colmax=(x,max(col))
                        colmin=(x,min(col))
                        ldegrees[colmax]+=1                        
                        ldegrees[colmin]+=1                        


                for y in xrange(self.gridsize):
                        col=coordarray_x[coordarray_y==y]
                        colmax=(max(col),y)
                        colmin=(min(col),y)
                        ldegrees[colmax]+=1                        
                        ldegrees[colmin]+=1                        
                        
                        
                return np.array([ldegrees[key] for key in self.nodes()])
                        
        
        def loopy_laplacian(self):
                adj_mat=nx.to_scipy_sparse_matrix(self,format='csr')

                loopy_degrees=self.loopy_degree()
                
                loopy_lapl=sparse.diags(loopy_degrees,0)-adj_mat
                
                return loopy_lapl



