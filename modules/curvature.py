import numpy as np
import matplotlib.pyplot as plt
from matplotlib.tri import Triangulation
from scipy.spatial import Voronoi
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
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

    # Set level for contourf
    levels = 50

    # Apply different normalization modes
    if norm_mode == 'normal':
        plt.contourf(xi, yi, curvature_interpolated, levels=levels, cmap='turbo')
        plt.colorbar(label="Curvature (radians)")
        title_suffix = ""

    elif norm_mode == 'log':
        curvature_log = np.log1p(curvature_interpolated)
        plt.contourf(xi, yi, curvature_log, levels=levels, cmap='turbo')
        plt.colorbar(label="Log Curvature (radians)")
        title_suffix = " (Log Scale)"

    elif norm_mode == 'percentile':
        vmin = np.percentile(curvature_interpolated, 5)
        vmax_calc = np.percentile(curvature_interpolated, 95)
        plt.contourf(xi, yi, curvature_interpolated, levels=levels, cmap='turbo',
                    vmin=vmin, vmax=vmax_calc)
        plt.colorbar(label="Curvature (radians, 5-95 percentile)")
        title_suffix = " (Percentile Norm)"

    elif norm_mode == 'clip':
        if vmax is None:
            vmax = 1.0
        plt.contourf(xi, yi, curvature_interpolated, levels=levels, cmap='turbo',
                    vmin=0, vmax=vmax)
        plt.colorbar(label=f"Curvature (radians, capped at {vmax})")
        title_suffix = f" (Clipped at {vmax})"
    else:
        # Default to normal if unknown mode
        plt.contourf(xi, yi, curvature_interpolated, levels=levels, cmap='YlOrRd')
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

def visualize_curvature_triangular_mesh(x, y, vertex_curvatures, triangles, norm_mode='normal', vmax=None):

    # Create matplotlib triangulation object
    tri = Triangulation(x, y, triangles)

    # Calculate face colors: average curvature of 3 vertices per triangle
    # Handle NaN values by using nanmean
    face_colors = np.nanmean(vertex_curvatures[triangles], axis=1)

    plt.figure(figsize=(12, 10))

    # Apply different normalization modes
    title_suffix = ""

    if norm_mode == 'normal':
        # Direct values
        tcf = plt.tripcolor(tri, facecolors=face_colors, cmap='turbo',
                           edgecolors='black', linewidth=0.1, alpha=0.9)
        plt.colorbar(tcf, label="Curvature (radians)")

    elif norm_mode == 'log':
        # Logarithmic scale
        face_colors_log = np.log1p(face_colors)
        tcf = plt.tripcolor(tri, facecolors=face_colors_log, cmap='turbo',
                           edgecolors='black', linewidth=0.1, alpha=0.9)
        plt.colorbar(tcf, label="Log Curvature (radians)")
        title_suffix = " (Log Scale)"

    elif norm_mode == 'percentile':
        # Clip to percentile range
        vmin = np.nanpercentile(face_colors, 5)
        vmax_calc = np.nanpercentile(face_colors, 95)
        tcf = plt.tripcolor(tri, facecolors=face_colors, cmap='turbo',
                           edgecolors='black', linewidth=0.1, alpha=0.9,
                           vmin=vmin, vmax=vmax_calc)
        plt.colorbar(tcf, label="Curvature (radians, 5-95 percentile)")
        title_suffix = " (Percentile Norm)"

    elif norm_mode == 'clip':
        # Clip maximum value
        if vmax is None:
            vmax = 1.0
        tcf = plt.tripcolor(tri, facecolors=face_colors, cmap='turbo',
                           edgecolors='black', linewidth=0.1, alpha=0.9,
                           vmin=0, vmax=vmax)
        plt.colorbar(tcf, label=f"Curvature (radians, capped at {vmax})")
        title_suffix = f" (Clipped at {vmax})"
    else:
        # Default
        tcf = plt.tripcolor(tri, facecolors=face_colors, cmap='turbo',
                           edgecolors='black', linewidth=0.1, alpha=0.9)
        plt.colorbar(tcf, label="Curvature (radians)")

    plt.title(f"Curvature - Triangular Mesh{title_suffix}")
    plt.xlabel("X (m)")
    plt.ylabel("Y (m)")
    plt.axis('equal')
    plt.tight_layout()
    plt.show()

def visualize_curvature_voronoi(x, y, vertex_curvatures, norm_mode='normal', vmax=None):

    # Create Voronoi diagram
    points_2d = np.column_stack([x, y])
    vor = Voronoi(points_2d)

    plt.figure(figsize=(12, 10))

    # Determine color normalization based on mode
    if norm_mode == 'log':
        # Use log scale
        curvatures_for_norm = np.log1p(vertex_curvatures)
        curvatures_for_norm = curvatures_for_norm[~np.isnan(curvatures_for_norm)]
        title_suffix = " (Log Scale)"
    elif norm_mode == 'percentile':
        # Use percentile clipping
        curvatures_for_norm = vertex_curvatures[~np.isnan(vertex_curvatures)]
        vmin_norm = np.nanpercentile(curvatures_for_norm, 5)
        vmax_norm = np.nanpercentile(curvatures_for_norm, 95)
        title_suffix = " (Percentile Norm)"
    elif norm_mode == 'clip':
        # Clip maximum
        if vmax is None:
            vmax = 1.0
        curvatures_for_norm = vertex_curvatures[~np.isnan(vertex_curvatures)]
        vmin_norm = 0
        vmax_norm = vmax
        title_suffix = f" (Clipped at {vmax})"
    else:
        # Normal mode
        curvatures_for_norm = vertex_curvatures[~np.isnan(vertex_curvatures)]
        title_suffix = ""

    # Set up normalization
    if norm_mode == 'percentile':
        from matplotlib.colors import Normalize
        norm = Normalize(vmin=vmin_norm, vmax=vmax_norm)
    elif norm_mode == 'clip':
        from matplotlib.colors import Normalize
        norm = Normalize(vmin=vmin_norm, vmax=vmax_norm)
    else:
        from matplotlib.colors import Normalize
        norm = Normalize(vmin=curvatures_for_norm.min(), vmax=curvatures_for_norm.max())

    cmap = plt.cm.turbo

    # Plot each Voronoi region
    for point_idx, region_idx in enumerate(vor.point_region):
        region = vor.regions[region_idx]

        # Skip invalid regions
        if not region or -1 in region:
            continue

        # Get polygon vertices
        polygon_vertices = [vor.vertices[i] for i in region]

        # Get curvature value for this vertex
        curv_value = vertex_curvatures[point_idx]

        # Skip NaN values (boundary vertices)
        if np.isnan(curv_value):
            continue

        # Apply normalization mode
        if norm_mode == 'log':
            curv_for_color = np.log1p(curv_value)
        else:
            curv_for_color = curv_value

        # Get color
        color = cmap(norm(curv_for_color))

        # Draw polygon
        polygon = Polygon(polygon_vertices, facecolor=color, edgecolor='black', linewidth=0.5, alpha=0.9)
        plt.gca().add_patch(polygon)

    # Overlay vertex points
    plt.scatter(x, y, c='black', s=15, alpha=0.6, edgecolors='white', linewidths=0.5, zorder=3)

    # Set up colorbar with explicit ax parameter
    ax = plt.gca()
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])
    if norm_mode == 'log':
        plt.colorbar(sm, ax=ax, label="Log Curvature (radians)")
    elif norm_mode == 'percentile':
        plt.colorbar(sm, ax=ax, label="Curvature (radians, 5-95 percentile)")
    elif norm_mode == 'clip':
        plt.colorbar(sm, ax=ax, label=f"Curvature (radians, capped at {vmax})")
    else:
        plt.colorbar(sm, ax=ax, label="Curvature (radians)")

    plt.title(f"Curvature - Voronoi Diagram{title_suffix}")
    plt.xlabel("X (m)")
    plt.ylabel("Y (m)")

    # Set limits based on data
    margin = 0.05 * (x.max() - x.min())
    plt.xlim(x.min() - margin, x.max() + margin)
    plt.ylim(y.min() - margin, y.max() + margin)

    # Use adjustable='box' to avoid warning when combining with manual limits
    plt.gca().set_aspect('equal', adjustable='box')

    plt.tight_layout()
    plt.show()

def visualize_3d_elevation_colored_by_curvature(points, triangles, vertex_curvatures, norm_mode='normal', vmax=None):
    """
    3D surface showing ELEVATION as height, colored by CURVATURE values.
    This shows WHERE on the terrain (high/low elevation) curvature occurs.
    """
    x = points[:, 0]
    y = points[:, 1]
    z = points[:, 2]  # Elevation

    # Create triangulation
    tri = Triangulation(x, y, triangles)

    # Set up figure
    fig = plt.figure(figsize=(14, 10))
    ax = fig.add_subplot(111, projection='3d')

    # Determine color normalization based on curvature
    curvature_clean = vertex_curvatures[~np.isnan(vertex_curvatures)]

    if norm_mode == 'log':
        curv_for_color = np.log1p(vertex_curvatures)
        curv_for_color[np.isnan(curv_for_color)] = 0
        vmin_norm = np.log1p(curvature_clean.min())
        vmax_norm = np.log1p(curvature_clean.max())
        title_suffix = " (Log Scale Curvature)"
        cbar_label = "Log Curvature (radians)"
    elif norm_mode == 'percentile':
        vmin_norm = np.nanpercentile(vertex_curvatures, 5)
        vmax_norm = np.nanpercentile(vertex_curvatures, 95)
        curv_for_color = vertex_curvatures.copy()
        curv_for_color[np.isnan(curv_for_color)] = vmin_norm
        title_suffix = " (Percentile Curvature)"
        cbar_label = "Curvature (radians, 5-95 percentile)"
    elif norm_mode == 'clip':
        if vmax is None:
            vmax = 1.0
        vmin_norm = 0
        vmax_norm = vmax
        curv_for_color = vertex_curvatures.copy()
        curv_for_color[np.isnan(curv_for_color)] = 0
        title_suffix = f" (Clipped Curvature at {vmax})"
        cbar_label = f"Curvature (radians, capped at {vmax})"
    else:
        vmin_norm = curvature_clean.min()
        vmax_norm = curvature_clean.max()
        curv_for_color = vertex_curvatures.copy()
        curv_for_color[np.isnan(curv_for_color)] = 0
        title_suffix = ""
        cbar_label = "Curvature (radians)"

    # Create the 3D surface plot
    # Z = elevation (actual terrain height)
    # facecolors = curvature (showing where terrain curves)

    # Create a ScalarMappable for the colorbar (since plot_trisurf doesn't handle this well)
    from matplotlib.colors import Normalize
    norm = Normalize(vmin=vmin_norm, vmax=vmax_norm)

    # Calculate face colors: average curvature of 3 vertices per triangle
    # plot_trisurf needs face colors (one per triangle) not vertex colors
    face_curvatures = np.array([np.nanmean([curv_for_color[t[0]], curv_for_color[t[1]], curv_for_color[t[2]]])
                                 for t in triangles])

    surf = ax.plot_trisurf(tri, z,
                          cmap='jet',  # Rainbow colormap for curvature
                          edgecolor='black',
                          linewidth=0.1,
                          alpha=0.9)

    # Map curvature values to colors (use face colors, not vertex colors)
    surf.set_array(face_curvatures)
    surf.set_clim(vmin_norm, vmax_norm)

    # Labels and colorbar
    ax.set_xlabel('X (m)', fontsize=10)
    ax.set_ylabel('Y (m)', fontsize=10)
    ax.set_zlabel('Elevation (m)', fontsize=10)
    ax.set_title(f'3D Terrain: Elevation (height) colored by Curvature{title_suffix}',
                 fontsize=12, fontweight='bold')

    # Create colorbar using ScalarMappable
    sm = cm.ScalarMappable(cmap='jet', norm=norm)
    sm.set_array([])
    cbar = fig.colorbar(sm, ax=ax, shrink=0.5, aspect=5, pad=0.1)
    cbar.set_label(cbar_label, rotation=270, labelpad=15)

    plt.tight_layout()
    plt.show()

def visualize_3d_dual_comparison(points, triangles, vertex_curvatures, norm_mode='normal', vmax=None):
    """
    Side-by-side 3D comparison with synchronized rotation.
    Left: Elevation surface (colored by elevation)
    Right: Curvature surface (colored by curvature, Z = curvature magnitude)
    """
    x = points[:, 0]
    y = points[:, 1]
    z = points[:, 2]  # Elevation

    # Create triangulation
    tri = Triangulation(x, y, triangles)

    # Prepare curvature for Z-axis on right plot
    curvature_clean = vertex_curvatures.copy()
    curvature_clean[np.isnan(curvature_clean)] = 0  # Replace NaN with 0 for visualization

    # Set up figure with two 3D subplots
    fig = plt.figure(figsize=(18, 8))

    # Left plot: Elevation
    ax1 = fig.add_subplot(121, projection='3d')
    surf1 = ax1.plot_trisurf(tri, z,
                            cmap='terrain',  # Terrain colormap for elevation
                            edgecolor='black',
                            linewidth=0.1,
                            alpha=0.9)
    surf1.set_array(z)

    ax1.set_xlabel('X (m)', fontsize=10)
    ax1.set_ylabel('Y (m)', fontsize=10)
    ax1.set_zlabel('Elevation (m)', fontsize=10)
    ax1.set_title('Terrain Elevation', fontsize=12, fontweight='bold')

    # Create colorbar using ScalarMappable for elevation
    from matplotlib.colors import Normalize
    norm_elev = Normalize(vmin=z.min(), vmax=z.max())
    sm1 = cm.ScalarMappable(cmap='terrain', norm=norm_elev)
    sm1.set_array([])
    cbar1 = fig.colorbar(sm1, ax=ax1, shrink=0.5, aspect=5, pad=0.1)
    cbar1.set_label('Elevation (m)', rotation=270, labelpad=15)

    # Right plot: Curvature as height
    ax2 = fig.add_subplot(122, projection='3d')

    # Determine curvature normalization
    if norm_mode == 'log':
        curv_display = np.log1p(curvature_clean)
        vmin_norm = curv_display.min()
        vmax_norm = curv_display.max()
        title_suffix = " (Log Scale)"
        cbar_label = "Log Curvature"
    elif norm_mode == 'percentile':
        vmin_norm = np.nanpercentile(vertex_curvatures, 5)
        vmax_norm = np.nanpercentile(vertex_curvatures, 95)
        curv_display = curvature_clean
        title_suffix = " (Percentile)"
        cbar_label = "Curvature (radians, 5-95%)"
    elif norm_mode == 'clip':
        if vmax is None:
            vmax = 1.0
        curv_display = np.clip(curvature_clean, 0, vmax)
        vmin_norm = 0
        vmax_norm = vmax
        title_suffix = f" (Clipped at {vmax})"
        cbar_label = f"Curvature (capped at {vmax})"
    else:
        curv_display = curvature_clean
        vmin_norm = curv_display.min()
        vmax_norm = curv_display.max()
        title_suffix = ""
        cbar_label = "Curvature (radians)"

    # Calculate face colors for curvature plot
    face_curvatures = np.array([np.nanmean([curv_display[t[0]], curv_display[t[1]], curv_display[t[2]]])
                                 for t in triangles])

    surf2 = ax2.plot_trisurf(tri, curv_display,  # Z = curvature magnitude
                            cmap='jet',  # Rainbow colormap
                            edgecolor='black',
                            linewidth=0.1,
                            alpha=0.9)
    surf2.set_array(face_curvatures)

    ax2.set_xlabel('X (m)', fontsize=10)
    ax2.set_ylabel('Y (m)', fontsize=10)
    ax2.set_zlabel('Curvature (radians)', fontsize=10)
    ax2.set_title(f'Terrain Curvature{title_suffix}', fontsize=12, fontweight='bold')

    # Create colorbar using ScalarMappable for curvature
    norm_curv = Normalize(vmin=vmin_norm, vmax=vmax_norm)
    sm2 = cm.ScalarMappable(cmap='jet', norm=norm_curv)
    sm2.set_array([])
    cbar2 = fig.colorbar(sm2, ax=ax2, shrink=0.5, aspect=5, pad=0.1)
    cbar2.set_label(cbar_label, rotation=270, labelpad=15)

    # Synchronize viewing angles
    def on_move(event):
        if event.inaxes == ax1:
            ax2.view_init(elev=ax1.elev, azim=ax1.azim)
        elif event.inaxes == ax2:
            ax1.view_init(elev=ax2.elev, azim=ax2.azim)
        fig.canvas.draw_idle()

    fig.canvas.mpl_connect('motion_notify_event', on_move)

    plt.tight_layout()
    plt.show()

def visualize_curvature_distribution(vertex_curvatures, boundary_vertices):

    # Filter out boundary vertices (NaN values)
    interior_curvatures = np.array([vertex_curvatures[i] for i in range(len(vertex_curvatures))
                                     if i not in boundary_vertices and not np.isnan(vertex_curvatures[i])])

    if len(interior_curvatures) == 0:
        print("Warning: No interior vertices to plot distribution")
        return

    fig, axes = plt.subplots(1, 2, figsize=(16, 6))

    # Histogram 1: Linear scale
    axes[0].hist(interior_curvatures, bins=50, color='steelblue', edgecolor='black', alpha=0.7)
    axes[0].axvline(np.mean(interior_curvatures), color='red', linestyle='--',
                    linewidth=2, label=f'Mean: {np.mean(interior_curvatures):.4f}')
    axes[0].axvline(np.median(interior_curvatures), color='green', linestyle='--',
                    linewidth=2, label=f'Median: {np.median(interior_curvatures):.4f}')
    axes[0].set_xlabel('Curvature (radians)', fontsize=12)
    axes[0].set_ylabel('Frequency', fontsize=12)
    axes[0].set_title('Curvature Distribution (Linear Scale)', fontsize=14, fontweight='bold')
    axes[0].legend(fontsize=10)
    axes[0].grid(True, alpha=0.3)

    # Histogram 2: Log scale (useful if distribution is skewed)
    axes[1].hist(interior_curvatures, bins=50, color='coral', edgecolor='black', alpha=0.7)
    axes[1].axvline(np.mean(interior_curvatures), color='red', linestyle='--',
                    linewidth=2, label=f'Mean: {np.mean(interior_curvatures):.4f}')
    axes[1].axvline(np.median(interior_curvatures), color='green', linestyle='--',
                    linewidth=2, label=f'Median: {np.median(interior_curvatures):.4f}')
    axes[1].set_xlabel('Curvature (radians)', fontsize=12)
    axes[1].set_ylabel('Frequency (log scale)', fontsize=12)
    axes[1].set_title('Curvature Distribution (Log Scale)', fontsize=14, fontweight='bold')
    axes[1].set_yscale('log')
    axes[1].legend(fontsize=10)
    axes[1].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.show()

def visualize_curvature_profile(vertex_curvatures, boundary_vertices):

    n_vertices = len(vertex_curvatures)
    vertex_ids = np.arange(n_vertices)

    # Separate interior and boundary vertices
    interior_mask = np.array([i not in boundary_vertices for i in range(n_vertices)])
    boundary_mask = ~interior_mask

    fig, axes = plt.subplots(figsize=(16, 10))

    # Plot 1: Curvature profile with boundary markers
    axes.plot(vertex_ids[interior_mask],
                 np.array(vertex_curvatures)[interior_mask],
                 'o-', color='steelblue', markersize=3, linewidth=0.5,
                 label='Interior vertices', alpha=0.7)
    axes.scatter(vertex_ids[boundary_mask],
                    np.zeros(np.sum(boundary_mask)),
                    c='red', marker='x', s=30,
                    label='Boundary vertices (excluded)', alpha=0.5, zorder=3)

    # Add mean line
    interior_curvatures = np.array(vertex_curvatures)[interior_mask]
    if len(interior_curvatures) > 0:
        mean_curv = np.mean(interior_curvatures[~np.isnan(interior_curvatures)])
        axes.axhline(mean_curv, color='green', linestyle='--',
                       linewidth=2, label=f'Mean: {mean_curv:.4f}', alpha=0.7)

    axes.set_xlabel('Vertex ID', fontsize=12)
    axes.set_ylabel('Curvature (radians)', fontsize=12)
    axes.set_title('Curvature Profile: All Vertices', fontsize=14, fontweight='bold')
    axes.legend(fontsize=10)
    axes.grid(True, alpha=0.3)

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
            vertex_curvatures.append(np.nan)
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

        # Count vertices with zero or near-zero curvature
        zero_threshold = 1e-6  # Consider values below this as effectively zero
        zero_curv_count = np.sum(interior_curvatures < zero_threshold)
        print(f"  Vertices with ~0 curvature: {zero_curv_count} ({100*zero_curv_count/len(interior_curvatures):.1f}%)")
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

    # Show statistical visualizations
    visualize_curvature_distribution(vertex_curvatures_array, boundary_vertices)
    visualize_curvature_profile(vertex_curvatures_array, boundary_vertices)

    # Show vertex labels visualization
    points_2d = points[:, :2] if points.shape[1] >= 2 else points
    visualize_vertex_labels(points_2d, vertex_curvatures_array)

    # curvature visualizations 
    x_coords = points[:, 0]
    y_coords = points[:, 1]

    visualize_curvature_triangular_mesh(x_coords, y_coords, vertex_curvatures_array,
                                       triangles, norm_mode=norm_mode, vmax=vmax)

    visualize_curvature_voronoi(x_coords, y_coords, vertex_curvatures_array,
                               norm_mode=norm_mode, vmax=vmax)
    '''
    # 3D comparison visualizations
    visualize_3d_elevation_colored_by_curvature(points, triangles, vertex_curvatures_array,
                                                norm_mode=norm_mode, vmax=vmax)

    visualize_3d_dual_comparison(points, triangles, vertex_curvatures_array,
                                norm_mode=norm_mode, vmax=vmax)
    '''
    # interpolation-based heatmap
    visualize_curvature_heatmap(x_coords, y_coords, vertex_curvatures_array,
                               grid_size=50, method=interpolation_method,
                               norm_mode=norm_mode, vmax=vmax)
