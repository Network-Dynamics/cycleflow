import unittest
import RandomPlanarGraph
class p_zero_TestCase(unittest.TestCase):
	def setUp(self):
		self.gridsize=10
		G=RandomPlanarGraph.RandomPlanarGraph(self.gridsize,0)
	
	def test_graph_size(self):
		assertTrue(G.number_of_nodes==self.gridsize**2 and G.number_of_edges==)
