import cycleflows as cf
import unittest
import RandomPlanarGraph
import numpy as np

class size_2_p_zero_TestCase(unittest.TestCase):
	def setUp(self):
		self.G=RandomPlanarGraph.RandomPlanarGraph(2,0)
	
	def test_dF_with_distance(self):
		dfs=cf.dF_with_distance(self.G, src_a=(0,1),src_b=(0,0))

		idealresult=[(0, 0.20833333333333331),\
		(2, -0.041666666666666657),\
		(1, -0.20833333333333329),\
		(1, 0.041666666666666664)]
		

		difference_flows=np.array([elem[1] for elem in dfs])-np.array([elem[1] for elem in idealresult])

		self.assertTrue(np.linalg.norm(difference_flows)<10e-6)

if __name__ == '__main__':
	unittest.main()
	    	
