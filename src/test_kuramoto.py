import unittest
import kuramoto
import numpy as np

class TestKuramoto(unittest.TestCase):
	def test_find_fps(self):
		M=np.array([1,-1]).T
		tol=10e-4
		fp, details=kuramoto.try_find_fps(1,M,M, np.array([0.5,-0.5]), tmax=200, tol=tol)
		self.assertTrue(np.abs(np.sin(fp[1]-fp[0]))-0.50<tol)


if __name__=='__main__':
	unittest.main()



