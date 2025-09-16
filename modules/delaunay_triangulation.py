import numpy as np
from scipy.spatial import Delaunay

def build_delaunay_triangulation(x, y, z):
    """
    Create Delaunay triangulation from 2D coordinates
    
    Args:
        x, y: Arrays of coordinate positions (meters)
        z: Array of elevation values (meters)
    
    Returns:
        triangulation: Delaunay triangulation object
        triangles: Array of triangle indices
        num_triangles: Number of triangles created
    """
    points_2d = np.column_stack((x, y))
    triangulation = Delaunay(points_2d)
    triangles = triangulation.simplices
    
    print(f"Created {len(triangles)} triangles from {len(points_2d)} points")
    
    return triangulation, triangles, len(triangles)