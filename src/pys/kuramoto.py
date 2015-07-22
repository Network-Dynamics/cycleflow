import numpy as np
from scipy.integrate import odeint 
import networkx as nx









def kuramoto_ode(th,t, M_I,M_I_w, P):
	"""
	th: theta, array with size=nnodes
	t: time
	M_I: unweighted oriented incidence matrix
	M_I_W: weighted oriented incidence matrix
	P: Power production at each node
	"""
	return P-np.dot(M_I_w, np.sin(np.dot(M_I.T, th)))



def integrate_for(large_time, thetas, tol=10e-5, args=None):
             th_start, th_end=odeint(kuramoto_ode, thetas, t=[0, large_time], args=args)

             not_converged=np.linalg.norm(kuramoto_ode(th_end, large_time, *args))>tol
             return not_converged, th_end
                        


        


def try_find_fps(ntry,M,Mw, P, tmax=200, tol=10e-4):
	"""
	ntry: number of initial conditions that will be tried to reach a fixed point
	tol: the odesolver ends when the norm of the vector at different stages get less than this
	"""


        assert(M.shape[0]==P.shape[0])  #The way it's supposed to be done...
        

        size=P.shape[0]
	
	#trying to detect if converged
	#the individual oscillators, if decoupled, will accelerate with constant torque P_j. 
	#therefore, in time t, starting from 0, it will reach angular vel 0.5P_j t**2.
	#let's assume 10*sqrt(2/P) is a reasonable time for them to complete multiple full 2*pi oscillations

	large_time=10*np.sqrt(2.0/np.max(P))
      
        for ntry in xrange(ntry):
                initguess=np.random.uniform(0,np.pi/2, size)
	        
                thetas=initguess
                t=0
                not_converged=True

                while t<tmax and not_converged:
                    not_converged, thetas=integrate_for(large_time, thetas, tol=tol,args=(M,Mw,P))
                    t+=large_time

                if not_converged==False:
                    return thetas, {'initguess':initguess}
   


