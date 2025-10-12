import numpy as np
import matplotlib.pyplot as plt
from .interpolation import create_grid, interpolate_elevation

def visualize_curvature_heatmap(x, y, vertex_curvatures, grid_size=50, method='cubic',
                                norm_mode='normal', vmax=None):
    # Create interpolation grid
    xi, yi = create_grid(x, y, grid_size)

    # Interpolate curvature values onto the grid
    curvature_interpolated = interpolate_elevation(
        x, y, vertex_curvatures,
        xi, yi,
        method=method
    )

    # Create the heatmap visualization
    plt.figure(figsize=(12, 10))

    # Apply different normalization modes
    if norm_mode == 'normal':
        plt.contourf(xi, yi, curvature_interpolated, levels=20, cmap='YlOrRd')
        plt.colorbar(label="Curvature (radians)")
        title_suffix = ""

    elif norm_mode == 'log':
        curvature_log = np.log1p(curvature_interpolated)
        plt.contourf(xi, yi, curvature_log, levels=20, cmap='YlOrRd')
        plt.colorbar(label="Log Curvature (radians)")
        title_suffix = " (Log Scale)"

    elif norm_mode == 'percentile':
        vmin = np.percentile(curvature_interpolated, 5)
        vmax_calc = np.percentile(curvature_interpolated, 95)
        plt.contourf(xi, yi, curvature_interpolated, levels=20, cmap='YlOrRd',
                    vmin=vmin, vmax=vmax_calc)
        plt.colorbar(label="Curvature (radians, 5-95 percentile)")
        title_suffix = " (Percentile Norm)"

    elif norm_mode == 'clip':
        if vmax is None:
            vmax = 1.0
        plt.contourf(xi, yi, curvature_interpolated, levels=20, cmap='YlOrRd',
                    vmin=0, vmax=vmax)
        plt.colorbar(label=f"Curvature (radians, capped at {vmax})")
        title_suffix = f" (Clipped at {vmax})"
    else:
        # Default to normal if unknown mode
        plt.contourf(xi, yi, curvature_interpolated, levels=20, cmap='YlOrRd')
        plt.colorbar(label="Curvature (radians)")
        title_suffix = ""

    # Optional: Add contour lines for reference
    plt.contour(xi, yi, curvature_interpolated,
                colors='black', linewidths=0.3, alpha=0.3)

    # Overlay GPS points as small dots
    plt.scatter(x, y, c='black', s=10, alpha=0.5, edgecolors='white', linewidths=0.5)

    plt.title(f"Curvature Heatmap{title_suffix}")
    plt.xlabel("X (m)")
    plt.ylabel("Y (m)")
    plt.axis('equal')
    plt.tight_layout()
    plt.show()

def visualize_vertex_labels(points, vertex_curvatures=None):

    _, ax = plt.subplots(figsize=(14, 12))

    x = points[:, 0]
    y = points[:, 1]

    # Plot vertices
    if vertex_curvatures is not None:
        # Color by curvature if provided
        ax.scatter(x, y, c=vertex_curvatures, cmap='YlOrRd',
                  s=100, alpha=0.7, edgecolors='black', linewidths=1, zorder=3)
    else:
        # Just plot as black dots
        ax.scatter(x, y, c='black', s=100, alpha=0.7, edgecolors='white',
                  linewidths=1, zorder=3)

    # Add vertex labels
    for i in range(len(points)):
        ax.annotate(str(i), (x[i], y[i]),
                   fontsize=8, ha='center', va='center',
                   color='blue', weight='bold',
                   bbox=dict(boxstyle='round,pad=0.3', facecolor='white',
                            edgecolor='blue', alpha=0.7))

    ax.set_xlim(x.min() - 20, x.max() + 20)
    ax.set_ylim(y.min() - 20, y.max() + 20)
    ax.set_aspect('equal')
    ax.set_xlabel('X (m)', fontsize=12)
    ax.set_ylabel('Y (m)', fontsize=12)
    ax.set_title("Vertex Labels and Positions", fontsize=14)
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.show()

def compute_curvature(points, triangles, interpolation_method='cubic', norm_mode='normal', vmax=None):

    vertex_curvatures = []
    n_vertices = len(points)

    # vertex to triangle dicitionary
    # to map which trianges each vertex is part of
    vertex_to_triangles = {i: [] for i in range(n_vertices)}
    for triangle_id, triangle in enumerate(triangles):
        for vertex_id in triangle:
            vertex_to_triangles[vertex_id].append(triangle_id)

    # edge-to-triangle-count mapping to identify boundary edges
    # An edge is represented as a sorted tuple (v1, v2) where v1 < v2
    edge_to_triangle_count = {}
    for triangle in triangles:
        # Each triangle has 3 edges
        edges = [
            tuple(sorted([triangle[0], triangle[1]])),
            tuple(sorted([triangle[1], triangle[2]])),
            tuple(sorted([triangle[2], triangle[0]]))
        ]
        for edge in edges:
            edge_to_triangle_count[edge] = edge_to_triangle_count.get(edge, 0) + 1

    # Identify boundary edges (edges that belong to only 1 triangle)
    boundary_edges = {edge for edge, count in edge_to_triangle_count.items() if count == 1}

    # Identify boundary vertices (vertices connected to any boundary edge)
    boundary_vertices = set()
    for edge in boundary_edges:
        boundary_vertices.add(edge[0])
        boundary_vertices.add(edge[1])

    print(f"\nCurvature Analysis Report:")
    print("="*35)
    print(f"Boundary Detection:")
    print("-"*35)
    print(f"  Total edges: {len(edge_to_triangle_count)}")
    print(f"  Boundary edges: {len(boundary_edges)}")
    print(f"  Boundary vertices: {len(boundary_vertices)}")
    print(f"  Interior vertices: {n_vertices - len(boundary_vertices)}")

    for vertex_id in range(n_vertices):
        # Skip boundary vertices - assign curvature of 0
        if vertex_id in boundary_vertices:
            vertex_curvatures.append(0.0)
            continue

        connected_triangles = vertex_to_triangles[vertex_id]
        angle_sum = 0.0

        # calculate the angle at this vertex in each triangle
        for triangle_id in connected_triangles:
            triangle = triangles[triangle_id]

            # determineind which position in the triangle corresponds to our vertex
            local_idx = np.where(triangle == vertex_id)[0][0]

            # Get the three vertices (reorder so our vertex is first)
            v0 = points[triangle[local_idx]]      # Our vertex (center)
            v1 = points[triangle[(local_idx + 1) % 3]]  # Next vertex
            v2 = points[triangle[(local_idx + 2) % 3]]  # Previous vertex

            # Calculate edges from center vertex
            edge1 = v1 - v0
            edge2 = v2 - v0

            # calculating the angle using dot product
            len1 = np.linalg.norm(edge1)
            len2 = np.linalg.norm(edge2)

            if len1 > 0 and len2 > 0: # check for division by zero
                cos_angle = np.dot(edge1, edge2) / (len1 * len2)
                # force values to [-1, 1] to avoid numerical errors
                # due to python float quirks
                cos_angle = np.clip(cos_angle, -1.0, 1.0)
                angle = np.arccos(cos_angle)
                angle_sum += angle

        # calculate angle deficit k = 2pi - sum(angles)
        curvature = abs(2 * np.pi - angle_sum)
        vertex_curvatures.append(curvature)

    vertex_curvatures_array = np.array(vertex_curvatures)

    # Get interior vertices only for stats
    interior_curvatures = np.array([vertex_curvatures_array[i] for i in range(n_vertices)
                                     if i not in boundary_vertices])

    print(f"\nCurvature Statistics (Interior vertices only):")
    print("-"*35)
    if len(interior_curvatures) > 0:
        print(f"  Min curvature:    {np.min(interior_curvatures):.6f} radians")
        print(f"  Max curvature:    {np.max(interior_curvatures):.6f} radians")
        print(f"  Mean curvature:   {np.mean(interior_curvatures):.6f} radians")
        print(f"  Median curvature: {np.median(interior_curvatures):.6f} radians")
    else:
        print("  No interior vertices found!")

    # Identify vertices with highest and lowest curvature, interior only
    # filtering out boundary vertices (curvature = 0)
    interior_indices = [i for i in range(n_vertices) if i not in boundary_vertices]

    if len(interior_indices) > 0:
        interior_curvatures_with_idx = [(i, vertex_curvatures_array[i]) for i in interior_indices]
        interior_curvatures_with_idx.sort(key=lambda x: x[1])

        print(f"\n5 Interior Vertices with LOWEST curvature (flattest):")
        print("-"*35)
        for i in range(min(5, len(interior_curvatures_with_idx))):
            idx, curv = interior_curvatures_with_idx[i]
            print(f"  Vertex {idx:4d}: {curv:.6f} rad | "
                  f"Triangles: {len(vertex_to_triangles[idx]):2d} | "
                  f"Coords: ({points[idx, 0]:.2f}, {points[idx, 1]:.2f})")

        print(f"\n5 Interior Vertices with HIGHEST curvature (most curved):")
        print("-"*35)
        for i in range(min(5, len(interior_curvatures_with_idx))):
            idx, curv = interior_curvatures_with_idx[-(i+1)]
            print(f"  Vertex {idx:4d}: {curv:.6f} rad | "
                  f"Triangles: {len(vertex_to_triangles[idx]):2d} | "
                  f"Coords: ({points[idx, 0]:.2f}, {points[idx, 1]:.2f})")

    print("="*35)

    # Export detailed results to CSV file
    import csv
    output_file = "curvature_analysis_results.csv"
    try:
        with open(output_file, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Vertex_ID', 'Curvature_Radians', 'Incident_Triangles', 'Is_Boundary', 'X_Coord', 'Y_Coord'])
            for i in range(n_vertices):
                writer.writerow([
                    i,
                    f"{vertex_curvatures_array[i]:.6f}",
                    len(vertex_to_triangles[i]),
                    'Boundary' if i in boundary_vertices else 'Interior',
                    f"{points[i, 0]:.2f}",
                    f"{points[i, 1]:.2f}"
                ])
        print(f"Results exported to: {output_file}")
    except Exception as e:
        print(f"Warning: Could not export to CSV: {e}")

    # Show vertex labels visualization
    points_2d = points[:, :2] if points.shape[1] >= 2 else points
    visualize_vertex_labels(points_2d, vertex_curvatures_array)

    # Show curvature heatmap visualization
    x_coords = points[:, 0]
    y_coords = points[:, 1]
    visualize_curvature_heatmap(x_coords, y_coords, vertex_curvatures_array,
                               grid_size=50, method=interpolation_method,
                               norm_mode=norm_mode, vmax=vmax)
