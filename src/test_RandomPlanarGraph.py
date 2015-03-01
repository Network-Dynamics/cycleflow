import unittest
import RandomPlanarGraph
import numpy as np
import networkx as nx

class p_zero_TestCase(unittest.TestCase):
	def setUp(self):
		self.gridsize=np.random.randint(2,10)
		self.G=RandomPlanarGraph.RandomPlanarGraph(self.gridsize,0)
	
	def test_graph_size(self):
		self.assertTrue(self.G.number_of_nodes()==self.gridsize**2 and self.G.number_of_edges()==2*self.gridsize*(self.gridsize-1))

	def test_loopy_degree(self):
		adj_mat=nx.adjacency_matrix(self.G)
		degrees=np.squeeze(np.asarray(adj_mat.sum(axis=1)))

		self.assertTrue((self.G.loopy_degree(degrees)==4).all())

if __name__ == '__main__':
	unittest.main()
	    	
