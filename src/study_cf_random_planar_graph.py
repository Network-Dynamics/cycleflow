import RandomPlanarGraph as rpg
import cycleflows as cf
import numpy as np

def calculate_mean_and_sd(xdata, ydata):
	"""
	arguments:
		xdata: python iterable
		ydata: python iterable
	xdata and ydata must have equal length

	returns: xpoints, means, sds
		xpoints: unique elements of xdata, in increasing order
		means: average of y data points corresponding to each element in xpoints
		sds: standard deviation of y data points corresponding to each element in xpoints
	"""
	xdata=np.array(xdata)
	ydata=np.array(ydata)
		
	xpoints=set(xdata)
	mean_at_xpoints=[]
	sd_at_xpoints=[]
		

	for x in xpoints:
		yvals_for_x=ydata[xdata==x]
		mean_at_xpoints.append(np.mean(np.abs(yvals_for_x)))
		sd_at_xpoints.append(np.sqrt(np.var(yvals_for_x)))
	
	return xpoints, mean_at_xpoints, sd_at_xpoints

def cf_decay_with_dist(size, p_rewire):
	"""
	calculates the decay of cycleflow with distance in a RAndomPlanarGraph with parameters
	size, p_rewire
	"""

	G=rpg.RandomPlanarGraph(size, p_rewire)
	a,b=G.choose_2_central_nodes()
	
	dists, cfs=cf.dF_with_distance(G, src_a=a, src_b=b)
	
	
	return calculate_mean_and_sd(dists, cfs)

if __name__=='__main__':
	import sys
	
	size=int(sys.argv[1])
	p_rewire=float(sys.argv[2])

	x, y, sds=cf_decay_with_dist(size, p_rewire)	
	
	print "#size=%d,p_rewire=%f"%(size, p_rewire)	
	print "#distances	mean_cf_decay	standard_deviation"

	for a,b,c in zip(x,y,sds):
		print a,'\t',b,'\t',c


