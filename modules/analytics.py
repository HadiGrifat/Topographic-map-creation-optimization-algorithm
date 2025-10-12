import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection

def calculate_triangle_fatness(points, triangles):
    fatness_ratios = []
    inradii = []
    circumradii = []
    areas = []

    for triangle in triangles:
        # Get triangle vertices
        p1, p2, p3 = points[triangle]

        # Calculate side lengths
        a = np.linalg.norm(p2 - p3)  # opposite to p1
        b = np.linalg.norm(p1 - p3)  # opposite to p2
        c = np.linalg.norm(p1 - p2)  # opposite to p3

        # Calculate area using cross product
        area = 0.5 * abs(np.cross(p2 - p1, p3 - p1))
        areas.append(area)

        # Calculate inradius: r = Area / semiperimeter
        semiperimeter = (a + b + c) / 2
        inradius = area / semiperimeter if semiperimeter > 0 else 0
        inradii.append(inradius)

        # Calculate circumradius: R = (abc) / (4 * Area)
        circumradius = (a * b * c) / (4 * area) if area > 0 else float('inf')
        circumradii.append(circumradius)

        # Calculate fatness ratio: r/R
        fatness = inradius / circumradius if circumradius > 0 and circumradius != float('inf') else 0
        fatness_ratios.append(fatness)

    fatness_ratios = np.array(fatness_ratios)

    # Generate statistics
    triangle_stats = {
        'total_triangles': len(triangles),
        'mean_fatness': np.mean(fatness_ratios),
        'median_fatness': np.median(fatness_ratios),
        'min_fatness': np.min(fatness_ratios),
        'max_fatness': np.max(fatness_ratios),
        'std_fatness': np.std(fatness_ratios),
        'fat_triangles_count': np.sum(fatness_ratios >= 0.5),  # Good quality threshold
        'skinny_triangles_count': np.sum(fatness_ratios < 0.3),  # Poor quality threshold
        'fat_percentage': (np.sum(fatness_ratios >= 0.5) / len(fatness_ratios)) * 100,
        'skinny_percentage': (np.sum(fatness_ratios < 0.3) / len(fatness_ratios)) * 100,
        'mean_area': np.mean(areas),
        'mean_inradius': np.mean(inradii),
        'mean_circumradius': np.mean(circumradii)
    }

    return fatness_ratios, triangle_stats

def visualize_triangle_fatness(points, triangles, fatness_ratios, title="Triangle Fatness Analysis"):

    fig, ax = plt.subplots(figsize=(12, 10))

    # Create custom colormap: red (skinny) -> yellow (moderate) -> green (fat)
    colors = ['red', 'orange', 'yellow', 'lightgreen', 'green']
    n_bins = 100
    cmap = LinearSegmentedColormap.from_list('fatness', colors, N=n_bins)

    # Create triangle patches
    triangle_patches = []
    for triangle in triangles:
        triangle_coords = points[triangle]
        triangle_patch = Polygon(triangle_coords, closed=True)
        triangle_patches.append(triangle_patch)

    # Create patch collection with fatness-based coloring
    patch_collection = PatchCollection(triangle_patches, cmap=cmap, alpha=0.8)
    patch_collection.set_array(fatness_ratios)
    patch_collection.set_clim(0, 1)  # Fatness ratio range [0, 1]

    # Add patches to plot
    ax.add_collection(patch_collection)

    # Add colorbar
    cbar = plt.colorbar(patch_collection, ax=ax)
    cbar.set_label('Fatness Ratio (r/R)', fontsize=12)

    # Plot original points
    ax.scatter(points[:, 0], points[:, 1], c='black', s=10, alpha=0.6, zorder=5)

    # Set plot properties
    ax.set_xlim(points[:, 0].min() - 10, points[:, 0].max() + 10)
    ax.set_ylim(points[:, 1].min() - 10, points[:, 1].max() + 10)
    ax.set_aspect('equal')
    ax.set_xlabel('X (m)', fontsize=12)
    ax.set_ylabel('Y (m)', fontsize=12)
    ax.set_title(title, fontsize=14)

    # Add quality legend
    ax.text(0.02, 0.98, 'Quality Guide:\nGreen: Fat (r/R ≥ 0.5)\nYellow: Moderate\nRed: Skinny (r/R < 0.3)',
            transform=ax.transAxes, fontsize=10, verticalalignment='top',
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

    plt.tight_layout()
    plt.show()

def print_fatness_report(triangle_stats):
    print("\nDelaunay Triangulation Quality Report")
    print("="*35)

    print(f"Total triangles: {triangle_stats['total_triangles']}")
    print(f"  Min fatness: {triangle_stats['min_fatness']:.3f}")
    print(f"  Max fatness: {triangle_stats['max_fatness']:.3f}")
    print()

    print(f"  Fat triangles (r/R ≥ 0.5): {triangle_stats['fat_triangles_count']} ({triangle_stats['fat_percentage']:.1f}%)")
    print(f"  Skinny triangles (r/R < 0.3): {triangle_stats['skinny_triangles_count']} ({triangle_stats['skinny_percentage']:.1f}%)")
    print()

    # Quality assessment
    if triangle_stats['fat_percentage'] >= 80:
        quality_grade = "EXCELLENT"
    elif triangle_stats['fat_percentage'] >= 60:
        quality_grade = "GOOD"
    elif triangle_stats['fat_percentage'] >= 40:
        quality_grade = "FAIR"
    else:
        quality_grade = "POOR"

    print(f"Overall Mesh Fatness Quality: {quality_grade}")
    print("="*35)

def analyze_triangulation_quality(triangulation, points):
    
    triangles = triangulation.simplices

    # Calculate fatness metrics
    fatness_ratios, triangle_stats = calculate_triangle_fatness(points, triangles)

    # Print analysis report
    print_fatness_report(triangle_stats)

    # Create visualization
    visualize_triangle_fatness(points, triangles, fatness_ratios)