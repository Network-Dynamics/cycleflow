

import networkx as nx
import numpy as np
import numpy.linalg as linalg
from scipy.linalg import solve



def central_two_nodes(VG):
    """
    choose two central nodes of the voronoi planar graph
    """

    if not VG.with_coords:
        raise TypeError("coordinate information not found, cannot continue")
    
    allnodes=VG.graph.nodes()

    node_pos=np.array([list(VG.graph.node[n]['pos']) for n in allnodes])
    dists_from_center=np.linalg.norm(node_pos-0.5, axis=1)
    
    centmost=allnodes[np.argmin(dists_from_center)]
    next_centmost=np.random.choice(nx.neighbors(VG.graph,centmost))

    return centmost, next_centmost



def cycle_distances(VG, src_a, src_b):
    """
    compute the cycle distances of all the other edges, given a source
    """

    G=VG.graph
    H=VG.dual_graph

    cycle_distance_from_c1=nx.single_source_shortest_path_length(H, G[src_a][src_b]['cycle1'])
    
    
    reslist=[]

    if 'cycle2' in G[src_a][src_b].keys():
        cycle_distance_from_c2=nx.single_source_shortest_path_length(H, G[src_a][src_b]['cycle2'])
        for u,v in G.edges():
            if 'cycle2' in G[u][v].keys():
                reslist.append(min(cycle_distance_from_c1[G[u][v]['cycle1']],cycle_distance_from_c1[G[u][v]['cycle2']],cycle_distance_from_c2[G[u][v]['cycle1']],cycle_distance_from_c2[G[u][v]['cycle2']]))
            else:
                reslist.append(min(cycle_distance_from_c1[G[u][v]['cycle1']],cycle_distance_from_c2[G[u][v]['cycle1']]))

    else:
        for u,v in G.edges():
            if 'cycle2' in G[u][v].keys():
                reslist.append(min(cycle_distance_from_c1[G[u][v]['cycle1']],cycle_distance_from_c1[G[u][v]['cycle2']]))
            else:
                reslist.append(cycle_distance_from_c1[G[u][v]['cycle1']])
        
    return reslist


def edge_distances(VG, src_a, src_b):
    """
    compute the shortest path distances of all the other edges, given a source
    """

    G=VG.graph
    shortest_distance_dict=nx.single_source_shortest_path_length(G, src_a)
    return [min(shortest_distance_dict[u], shortest_distance_dict[v]) for u,v in G.edges()]



def dF(VG, src_a=None, src_b=None, dk=10e-1):
    """
    given a source, computes the change in node potentials when the respective edge
    is perturbed by amount dk. It is computed by the equation:

    $(L+\delta L)\delta\phi = -\delta L\phi$
    """
    
    allnodes=VG.graph.nodes()
    numnodes=len(allnodes)

    src_a_idx=allnodes.index(src_a)
    src_b_idx=allnodes.index(src_b)
    
    try:
        edge_todamage_idx=VG.graph.edges().index((src_a, src_b))
    except:
        edge_todamage_idx=VG.graph.edges().index((src_b, src_a))
 
    L=VG.laplacian()
    M_inc=np.asarray(nx.incidence_matrix(VG.graph, oriented=True))
    Pvec=np.random.rand(numnodes)       #Randomly choosing some Power vector
    
#    print(L.shape, Pvec.shape) 
    pot_orig=np.insert(solve(L[1:,1:], Pvec[1:]),0,0)
    flow_orig=np.dot(M_inc.T, pot_orig)
    initial_flow_damaged_edge=flow_orig[edge_todamage_idx]


    L[src_a_idx, src_b_idx]+=dk
    L[src_b_idx, src_a_idx]+=dk
    L[src_a_idx, src_a_idx]-=dk
    L[src_b_idx, src_b_idx]-=dk
    M_inc[:, edge_todamage_idx]*=(1-dk)

    pot_new=np.insert(solve(L[1:,1:], Pvec[1:]),0,0)
    flow_new=np.dot(M_inc.T, pot_new)   #There's a bug, M_inc should also be changed at the perturbed edge

    return flow_new-flow_orig, initial_flow_damaged_edge

def dF_approx(VG, src_a=None, src_b=None, dk=10e-1):
    L=VG.loopy_laplacian()
    G=VG.graph
     
    allnodes=VG.dual_graph.nodes()
    rhs=np.zeros(L.shape[0])
        
    src_cycle1=G[src_a][src_b]['cycle1']
    src_cycle2=G[src_a][src_b]['cycle2']
    

    rhs[allnodes.index(src_cycle1)]=dk
    rhs[allnodes.index(src_cycle2)]=-dk
    print(rhs)    

    cfs=solve(L, rhs)   #the cycleflows in each loop
    
    res=[]

    for u,v in VG.graph.edges():
        r=cfs[allnodes.index(VG.graph[u][v]['cycle1'])]
        try:
            r-=cfs[allnodes.index(VG.graph[u][v]['cycle2'])]
        except KeyError:
            pass
        res.append(r)    
     
    return res

def dF_with_distance(VG, src_a=None, src_b=None, dk=10e-1):

    if not src_a:
        raise TypeError("src_a must be specified")
    

    return edge_distances(VG, src_a, src_b), cycle_distances(VG, src_a, src_b), dF(VG, src_a=src_a, src_b=src_b,dk=dk)[0]


def dF_various_cycle_dist(VG, dk=10e-3):
    dFsdict={}

    G=VG.graph
    H=VG.dual_graph

    for key in range(nx.diameter(H)+1):
        dFsdict[key]=([],[])


    for u,v in G.edges():
        cycle_dists=cycle_distances(VG, u,v)
        Dfs, F0=dF(VG, src_a=u, src_b=v, dk=dk)

        for cd, df in zip(cycle_dists, Dfs):
            dFsdict[cd][0].append(F0)
            dFsdict[cd][1].append(df)

    return dFsdict
