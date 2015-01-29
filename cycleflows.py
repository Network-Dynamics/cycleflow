import networkx as nx
import scipy.sparse as sparse 
import scipy.sparse.linalg as spalg
from scipy.sparse.construct import eye as speye

def spinv(A):
	"""
	Compute the inverse of a sparse matrix

	.. versionadded:: 0.12.0

	Parameters
	----------
	A : (M,M) ndarray or sparse matrix
	    square matrix to be inverted

	Returns
	-------
	Ainv : (M,M) ndarray or sparse matrix
	    inverse of `A`

	Notes
	-----
	This computes the sparse inverse of `A`.  If the inverse of `A` is expected
	to be non-sparse, it will likely be faster to convert `A` to dense and use
	scipy.linalg.inv.

	"""
	I = speye(A.shape[0], A.shape[1], dtype=A.dtype, format=A.format)
	Ainv = spalg.spsolve(A, I)
	return Ainv



def dF_with_distance(G, src_a=None, src_b=None):
	allnodes=G.nodes()
	Lg=spinv(sparse.csc_matrix(G.loopy_laplacian()))
	
	if src_b:
		return [(nx.shortest_path_length(G, source=src_a, target=node) , Lg[allnodes.index(node), allnodes.index(src_a)] -Lg[allnodes.index(node), allnodes.index(src_b)]) for node in allnodes]
	else:
		return [(nx.shortest_path_length(G, source=src_a, target=node) , Lg[allnodes.index(node), allnodes.index(src_a)]) for node in allnodes]



	
