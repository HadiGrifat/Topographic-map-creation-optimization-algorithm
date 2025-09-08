"""
Standalone Delaunay Triangulation Test
Just loads GPS data and shows 3D triangular mesh - no pipeline integration
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import numpy as np
from scipy.spatial import Delaunay
import matplotlib.pyplot as plt
from modules.data_processing import load_gpx_data, coord_transform, normalize_elevation

def create_and_show_triangulation():
    """Simple function to create and display Delaunay triangulation"""
    
    print("Loading GPS data...")
    # Load GPS data from one of the files
    gps_file = 'Data/Track2_24_4_2025.gpx'
    lats, lons, alts = load_gpx_data(gps_file)
    
    print(f"Loaded {len(lats)} GPS points from {gps_file}")
    
    # Process the data (same as we do for interpolation)
    alts = normalize_elevation(alts)
    x, y = coord_transform(lats, lons)
    z = np.array(alts)
    
    print(f"Data ranges:")
    print(f"  X: {min(x):.1f} to {max(x):.1f} m")
    print(f"  Y: {min(y):.1f} to {max(y):.1f} m")
    print(f"  Z: {min(z):.1f} to {max(z):.1f} m")
    
    # Create 2D points for triangulation (x, y coordinates only)
    points_2d = np.column_stack((x, y))
    
    print(f"Creating Delaunay triangulation...")
    # This is the core - create triangulation
    triangulation = Delaunay(points_2d)
    triangles = triangulation.simplices  # Array of triangle indices
    
    print(f"Created {len(triangles)} triangles from {len(points_2d)} points")
    
    # Show 3D visualization
    print("Displaying 3D triangular mesh...")
    
    fig = plt.figure(figsize=(14, 10))
    ax = fig.add_subplot(111, projection='3d')
    
    # Plot triangular surface
    surface = ax.plot_trisurf(x, y, z, triangles=triangles, 
                             cmap='terrain', alpha=0.8, 
                             linewidth=0.1, antialiased=True)
    
    # Add color bar for elevation
    fig.colorbar(surface, label='Elevation (m)', shrink=0.6)
    
    # Show original GPS points as red dots
    ax.scatter(x, y, z, c='red', s=8, alpha=0.6, label='GPS Points')
    
    # Labels and title
    ax.set_xlabel('X (meters)')
    ax.set_ylabel('Y (meters)')
    ax.set_zlabel('Elevation (meters)')
    ax.set_title(f'Delaunay Triangulation - 3D Mesh\\n{len(triangles)} triangles from {len(points_2d)} GPS points')
    
    # Set viewing angle
    ax.view_init(elev=30, azim=45)
    
    plt.tight_layout()
    plt.show()
    
    # Also show wireframe version
    print("Displaying wireframe mesh...")
    
    fig2 = plt.figure(figsize=(14, 10))
    ax2 = fig2.add_subplot(111, projection='3d')
    
    # Plot wireframe (just the triangle edges)
    ax2.plot_trisurf(x, y, z, triangles=triangles, 
                    color='lightblue', alpha=0.3,
                    edgecolor='black', linewidth=0.5)
    
    # Show GPS points
    ax2.scatter(x, y, z, c='red', s=10, alpha=0.8, label='GPS Points')
    
    ax2.set_xlabel('X (meters)')
    ax2.set_ylabel('Y (meters)')
    ax2.set_zlabel('Elevation (meters)')
    ax2.set_title('Delaunay Triangulation - Wireframe View\\nShowing triangle connections')
    ax2.view_init(elev=30, azim=45)
    
    plt.tight_layout()
    plt.show()
    
    return triangulation, len(triangles)

if __name__ == "__main__":
    print("=== Standalone Delaunay Triangulation Test ===")
    print("This script will:")
    print("1. Load GPS data from a file")
    print("2. Create Delaunay triangulation")
    print("3. Show 3D triangular mesh")
    print("4. Show wireframe view")
    print()
    
    try:
        triangulation, num_triangles = create_and_show_triangulation()
        print(f"\\nSUCCESS! Created and displayed triangulation with {num_triangles} triangles")
        print("You should see two 3D plots:")
        print("  1. Colored surface showing elevation")
        print("  2. Wireframe showing triangle structure")
        
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()