import networkx as nx
import numpy as np

class RandomPlanarGraph(nx.Graph):
	def __init__(self, n, p_merge):
		G=nx.grid_2d_graph(n,n)
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
	
	
	  
	def get_boundary(self):
		allnodes=self.nodes()
		boundarynodes=[]
		boundarynodes+=[node for node in allnodes if self._is_global_extremum(node[0], [anynode[0] for anynode in allnodes if anynode[1]==node[1]])]
		boundarynodes+=[node for node in allnodes if self._is_global_extremum(node[1], [anynode[1] for anynode in allnodes if anynode[0]==node[0]])]
		
		return set(boundarynodes)
		
	
	def loopy_laplacian(self):
		adj_mat=np.array(nx.adjacency_matrix(self))
		diagterms=np.sum(adj_mat, axis=0)
	
		allnodes=self.nodes()
	
		boundarynodes=self.get_boundary()

		diagterms[[allnodes.index(node) for node in boundarynodes]]+=1
		loopy_lapl=np.diag(diagterms)-adj_mat
		
		return loopy_lapl



