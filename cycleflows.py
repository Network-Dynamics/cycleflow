from warnings import warn
import networkx as nx

from numpy import asarray, empty, where, squeeze, prod
import scipy.sparse as sparse 
from scipy.sparse.construct import eye as speye
from scipy.sparse import isspmatrix_csc, isspmatrix_csr, isspmatrix, \
        SparseEfficiencyWarning, csc_matrix

from scipy.sparse.linalg import factorized

def spsolve(A, b, permc_spec=None, use_umfpack=False):
	"""Solve the sparse linear system Ax=b, where b is a matrix.

	Parameters
	----------
	A : ndarray or sparse matrix
		The square matrix A will be converted into CSC or CSR form
	b : ndarray or sparse matrix
		The matrix or vector representing the right hand side of the equation.
		If a vector, b.size must
	permc_spec : str, optional
		How to permute the columns of the matrix for sparsity preservation.
		(default: 'COLAMD')

		- ``NATURAL``: natural ordering.
		- ``MMD_ATA``: minimum degree ordering on the structure of A^T A.
		- ``MMD_AT_PLUS_A``: minimum degree ordering on the structure of A^T+A.
		- ``COLAMD``: approximate minimum degree column ordering
	use_umfpack : bool (optional)
		if True (default) then use umfpack for the solution.  This is
		only referenced if b is a vector.

	Returns
	-------
	x : ndarray or sparse matrix
		the solution of the sparse linear equation.
		If b is a vector, then x is a vector of size A.shape[1]
		If b is a matrix, then x is a matrix of size (A.shape[1], b.shape[1])

	Notes
	-----
	For solving the matrix expression AX = B, this solver assumes the resulting
	matrix X is sparse, as is often the case for very sparse inputs.  If the
	resulting X is dense, the construction of this sparse result will be
	relatively expensive.  In that case, consider converting A to a dense
	matrix and using scipy.linalg.solve or its variants.
	"""
	if not (isspmatrix_csc(A) or isspmatrix_csr(A)):
		A = csc_matrix(A)
		warn('spsolve requires A be CSC or CSR matrix format', SparseEfficiencyWarning)

	# b.size gives a different answer for dense vs sparse:
	# use prod(b.shape)

	if isspmatrix(b) and not (isspmatrix_csc(b) or isspmatrix_csr(b)):
		b = csc_matrix(b)
		warn('solve requires b be CSC or CSR matrix format',
			 SparseEfficiencyWarning)
	if b.ndim != 2:
		raise ValueError("b must be either a vector or a matrix")

	A.sort_indices()
	A = A.asfptype()  # upcast to a floating point format

	# validate input shapes
	M, N = A.shape
	if (M != N):
		raise ValueError("matrix must be square (has shape %s)" % ((M, N),))

	if M != b.shape[0]:
		raise ValueError("matrix - rhs dimension mismatch (%s - %s)"
						 % (A.shape, b.shape[0]))


	Afactsolve = factorized(A)
	tempj = empty(M, dtype=int)
	x = A.__class__(b.shape)
	for j in range(b.shape[1]):
		xj = Afactsolve(squeeze(b[:, j].toarray()))
		w = where(xj != 0.0)[0]
		tempj.fill(j)
		x = x + A.__class__((xj[w], (w, tempj[:len(w)])),
							shape=b.shape, dtype=A.dtype)
	return x



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
	Ainv = spsolve(A, I)
	return Ainv



def dF_with_distance(G, src_a=None, src_b=None):
	allnodes=G.nodes()
	Lg=spinv(sparse.csc_matrix(G.loopy_laplacian()))
	
	if src_b:
		return [(nx.shortest_path_length(G, source=src_a, target=node) , Lg[allnodes.index(node), allnodes.index(src_a)] -Lg[allnodes.index(node), allnodes.index(src_b)]) for node in allnodes]
	else:
		return [(nx.shortest_path_length(G, source=src_a, target=node) , Lg[allnodes.index(node), allnodes.index(src_a)]) for node in allnodes]



	
