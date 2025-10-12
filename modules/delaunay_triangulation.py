import numpy as np
from scipy.spatial import Delaunay
from scipy.interpolate import griddata

def build_delaunay_triangulation(x, y, z):

    points_2d = np.column_stack((x, y))
    triangulation = Delaunay(points_2d)
    triangles = triangulation.simplices
    
    print(f"Created {len(triangles)} triangles from {len(points_2d)} points")

    return triangulation, triangles, len(triangles)


def optimize_with_steiner_points(x, y, z, triangulation):

    # Get original points
    original_points = np.column_stack((x, y))
    original_z = np.array(z)

    # Get all edges from triangulation
    triangles = triangulation.simplices
    edges = set()

    # Extract unique edges from all triangles
    for triangle in triangles:
        for i in range(3):
            edge = tuple(sorted([triangle[i], triangle[(i + 1) % 3]]))
            edges.add(edge)

    print(f"Found {len(edges)} unique edges in triangulation")

    # Calculate Steiner points (midpoints of edges)
    steiner_points = []
    steiner_z = []

    for edge in edges:
        p1_idx, p2_idx = edge

        # Midpoint coordinates
        mid_x = (x[p1_idx] + x[p2_idx]) / 2
        mid_y = (y[p1_idx] + y[p2_idx]) / 2

        # Interpolate elevation at midpoint
        # Use linear interpolation between the two edge endpoints
        mid_z = (z[p1_idx] + z[p2_idx]) / 2

        steiner_points.append([mid_x, mid_y])
        steiner_z.append(mid_z)

    steiner_points = np.array(steiner_points)
    steiner_z = np.array(steiner_z)
    steiner_count = len(steiner_points)

    print(f"Generated {steiner_count} Steiner points at edge midpoints")

    # Combine original points with Steiner points
    all_points = np.vstack([original_points, steiner_points])
    all_z = np.concatenate([original_z, steiner_z])

    # Create new triangulation with all points
    new_triangulation = Delaunay(all_points)
    new_triangles = new_triangulation.simplices

    # Extract coordinates for return
    new_x = all_points[:, 0]
    new_y = all_points[:, 1]
    new_z = all_z

    print(f"Optimized triangulation: {len(new_triangles)} triangles from {len(all_points)} points")
    print(f"Improvement: +{len(new_triangles) - len(triangles)} triangles, +{steiner_count} points")

    return new_triangulation, new_triangles, new_x, new_y, new_z, steiner_count