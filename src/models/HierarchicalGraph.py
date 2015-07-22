import networkx as nx
import numpy as np

class HierarchicalGraph(nx.Graph):
    def __init__(self, maxdepth, depth, weights="mult", compute_dual=False):
        self.size=2**(maxdepth-1)+1 #The lattice size
        self.graph=self._hierarchical(maxdepth, depth, weights)        
        
        if compute_dual:
            self.dual_graph=self.get_dual_graph()
        
    def get_dual_graph(self):
        """
        Creates the *loopy* dual graph
        """
        H=nx.MultiGraph()
        
        #This takes care of everything except the self loops and the right/top edges
        for x in range(self.size-2):
            for y in range(self.size-2):
                newnode=(x+0.5, y+0.5)
                H.add_edge((x+0.5,y+0.5),(x+1.5,y+0.5),weight=self.graph[(x+1,y)][(x+1,y+1)]['weight'])
                H.add_edge((x+0.5,y+0.5),(x+0.5,y+1.5),weight=self.graph[(x,y+1)][(x+1,y+1)]['weight'])
                
        for x in range(0, self.size-1):
            y=x
            #left self loops
            H.add_edge((0.5,y+0.5), (0.5,y+0.5), weight=self.graph[(0,y)][(0,y+1)]['weight'])
            
            #right self loops
            H.add_edge((self.size-1.5,y+0.5), (self.size-1.5,y+0.5), weight=self.graph[(self.size-1,y)][(self.size-1,y+1)]['weight'])
            
            #bottom self loops
            H.add_edge((x+0.5,0.5), (x+0.5,0.5), weight=self.graph[(x,0)][(x+1,0)]['weight'])
            
            #top self loops
            H.add_edge((x+0.5,self.size-1.5), (x+0.5,self.size-1.5), weight=self.graph[(x,self.size-1)][(x+1,self.size-1)]['weight'])
            
        for x in range(self.size-2):
            y=x
            #top edge
            H.add_edge((x+0.5,self.size-1.5), (x+1.5,self.size-1.5), weight=self.graph[(x+1,self.size-1)][(x+1,self.size-2)]['weight'])
            
            #right edge
            H.add_edge((self.size-1.5,y+0.5), (self.size-1.5,y+1.5), weight=self.graph[(self.size-2,y+1)][(self.size-1,y+1)]['weight'])

        assert(H.number_of_edges()==self.graph.number_of_edges())
        return H        
            
    def _hierarchical(self,maxdepth, depth, weights="mult"):
        """ 
        Creates a hierarchical network with depth number of hierarchy level
        """ 
        assert(depth<maxdepth)
        size=2**(maxdepth-1)+1
         
        G=nx.grid_2d_graph(size, size)
         
        stepsize=2**(maxdepth-depth-1)
         
        baseweight=1
        weight=baseweight
        d=1 
         
        for u,v in G.edges():
            G[u][v]['weight']=weight
            G[v][u]['weight']=weight
             
         
        while d<=depth:
            #Build up the weights, thinnest first
            for coord in range(0,size, stepsize):
                for other in range(size-1):
                    G[(coord, other)][(coord, other+1)]['weight']=weight
                    G[(coord, other+1)][(coord, other)]['weight']=weight
                     
                    G[(other, coord)][(other+1, coord)]['weight']=weight
                    G[(other+1, coord)][(other, coord)]['weight']=weight
     
     
            if weights=='mult':
                weight*=2
            else:
                weight+=baseweight
                 
            stepsize*=2
            d+=1
        return G
