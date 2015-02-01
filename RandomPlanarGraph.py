import networkx as nx
import numpy as np

class RandomPlanarGraph(nx.Graph):
	def __init__(self, n, p_merge):
		G=nx.grid_2d_graph(n,n)
		self.gridsize=n
		nx.Graph.__init__(self,G)
		for node in self.nodes():
			if np.random.random()<p_merge:
				neighbors=self.neighbors(node)
				
				merge_with=neighbors[np.random.randint(len(neighbors))]
				neighbors.remove(merge_with)
				
				for other_neighbor in neighbors:
					self.add_edge(merge_with, other_neighbor)
				self.remove_node(node)



	def choose_2_central_nodes(self):
		N=self.number_of_nodes()
		dists_from_cents=np.array([[n,np.abs(n[0]-N/2)+np.abs(n[1]-N/2)] for n in self.nodes()])
		centralmost=dists_from_cents[np.argmin(dists_from_cents[:,1])][0]
		other=nx.neighbors(self, centralmost)[0]
    		return centralmost, other


	def _is_global_extremum(self, x,lst):
		return (x==max(lst)) or (x==min(lst))
	
	
	  
	def loopy_degree(self, degrees):
		allnodes=self.nodes()

		ldegrees=degrees

		coordarray=np.array(self.nodes()).T

		for x in xrange(self.gridsize):
			col=coordarray[1][coordarray[0]==x]
			colmax=(x,max(col))
			colmin=(x,min(col))
			ldegrees[allnodes.index(colmax)]+=1			
			ldegrees[allnodes.index(colmin)]+=1			


		for y in xrange(self.gridsize):
			col=coordarray[0][coordarray[1]==y]
			colmax=(max(col),y)
			colmin=(min(col),y)
			ldegrees[allnodes.index(colmax)]+=1			
			ldegrees[allnodes.index(colmin)]+=1			
			
			
		return ldegrees
			
	
	def loopy_laplacian(self):
		adj_mat=np.array(nx.adjacency_matrix(self))
		degrees=np.sum(adj_mat, axis=0)
		loopy_degrees=self.loopy_degree(degrees)
		
		loopy_lapl=np.diag(loopy_degrees)-adj_mat
		
		return loopy_lapl



