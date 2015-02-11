import RandomPlanarGraph as rpg
G=rpg.RandomPlanarGraph(100,0)
L=G.loopy_laplacian()

def benchmark_numpy():
	import numpy as np
	return np.linalg.inv(L)

def benchmark_sparse():
	import scipy.sparse as sp
	import scipy.sparse.linalg as linalg
	
	return linalg.inv(L)
