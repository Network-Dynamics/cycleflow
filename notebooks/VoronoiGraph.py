from scipy.spatial import Voronoi
import numpy as np
import networkx as nx


class VoronoiPlanarGraph():
    """
    add docs here
    """
    def __init__(self, size):
        vor=self.__gen_voronoi(size)
        self.graph=self.__voronoi_graph(vor)
        self.dual_graph=self.__voronoi_loopy_dual(vor)
        
    def __gen_voronoi(self, size):
        """
        Generate a voronoi tessalation with `size` seed points in the unit cube
        """
        points=np.random.rand(size,2)
        return Voronoi(points)
    
    
    def __voronoi_graph(self, vor, with_coords=True):
        """
        Create a planar graph and it's loopy dual from a voronoi tessalation
        """
        G=nx.Graph()
    
        #We select all the voronoi ridges that doesn't stretch to infinity
        for ridge in vor.ridge_vertices:
            if -1 not in ridge: 
                G.add_edge(*ridge)
    
        if with_coords:
            for node in G.nodes():
                G.node[node]['pos']=tuple(vor.vertices[node])
    
        return G
    
    
    def __voronoi_loopy_dual(self, vor, with_coords=True):
        H=nx.MultiGraph()
        
        points_with_bounded_regions=[]
        for idx, pt in enumerate(vor.points):
            region=vor.regions[vor.point_region[idx]]
            
            if region and (-1 not in region):
                points_with_bounded_regions.append(idx)
    
    
    
        for pt1,pt2 in vor.ridge_points:
            if pt1 in points_with_bounded_regions:
                if pt2 in points_with_bounded_regions:
                    H.add_edge(pt1,pt2)
                else:
                    H.add_edge(pt1,pt1)
            elif pt2 in points_with_bounded_regions:
                H.add_edge(pt2,pt2)
            else:
                pass
        if with_coords:
            for node in H.nodes():
                H.node[node]['pos']=tuple(vor.points[node])
    
        return H
    
