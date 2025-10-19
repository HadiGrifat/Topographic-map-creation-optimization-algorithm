"""
Visualize all synthetic test terrains in a grid layout

This script creates a quick visual overview of all test datasets
to help understand their geometry before running curvature analysis.
"""

import sys
from pathlib import Path

# Add parent directory to path to import modules
sys.path.insert(0, str(Path(__file__).parent.parent))

import numpy as np
import matplotlib.pyplot as plt
from modules.data_processing import load_csv_meter_data
from matplotlib import cm


def load_and_process_test_file(filepath):
    """Load and process a test CSV file with meter coordinates"""
    x, y, z = load_csv_meter_data(filepath)
    return x, y, z


def visualize_all_terrains():
    """Create a grid visualization of all test terrains"""
    # Get test_data directory relative to this script's location
    script_dir = Path(__file__).parent
    test_dir = script_dir / "test_data"
    test_files = sorted(test_dir.glob("*.csv"))

    if not test_files:
        print("Error: No test files found in test_data/")
        print("Run 'python generate_test_gps_data.py' first.")
        return

    # Calculate grid layout
    n_files = len(test_files)
    n_cols = 3
    n_rows = (n_files + n_cols - 1) // n_cols

    fig = plt.figure(figsize=(18, 6 * n_rows))

    for idx, filepath in enumerate(test_files, 1):
        try:
            # Load data
            x, y, z = load_and_process_test_file(filepath)

            # Create subplot
            ax = fig.add_subplot(n_rows, n_cols, idx, projection='3d')

            # Create surface plot
            # Reshape data if it's a grid (assume square grid)
            n_points = len(x)
            grid_size = int(np.sqrt(n_points))

            if grid_size * grid_size == n_points:
                # Perfect square - reshape for surface plot
                # Data was generated in row-major order (i for rows, j for columns)
                # where x=j*spacing and y=i*spacing
                # Need to transpose to match matplotlib's expectation
                X = x.reshape(grid_size, grid_size).T
                Y = y.reshape(grid_size, grid_size).T
                Z = z.reshape(grid_size, grid_size).T

                surf = ax.plot_surface(X, Y, Z,
                                      cmap='terrain',
                                      edgecolor='black',
                                      linewidth=0.2,
                                      alpha=0.9)
            else:
                # Not a perfect square - use scatter plot
                surf = ax.scatter(x, y, z, c=z, cmap='terrain', s=20)

            # Set labels and title
            filename = filepath.stem.replace("test_", "").replace("_", " ").title()
            ax.set_title(filename, fontsize=12, fontweight='bold')
            ax.set_xlabel('X (m)', fontsize=8)
            ax.set_ylabel('Y (m)', fontsize=8)
            ax.set_zlabel('Elevation (m)', fontsize=8)

            # Adjust viewing angle for better visualization
            ax.view_init(elev=25, azim=45)

        except Exception as e:
            print(f"Error processing {filepath.name}: {e}")
            continue

    plt.tight_layout()
    plt.suptitle("Synthetic Test Terrains - 3D Overview",
                fontsize=16, fontweight='bold', y=1.001)
    plt.show()


def visualize_terrain_2d_heatmaps():
    """Create 2D heatmap view of all terrains"""
    # Get test_data directory relative to this script's location
    script_dir = Path(__file__).parent
    test_dir = script_dir / "test_data"
    test_files = sorted(test_dir.glob("*.csv"))

    if not test_files:
        print("Error: No test files found in test_data/")
        return

    n_files = len(test_files)
    n_cols = 5
    n_rows = (n_files + n_cols - 1) // n_cols

    fig, axes = plt.subplots(n_rows, n_cols, figsize=(20, 4 * n_rows))
    axes = axes.flatten() if n_files > 1 else [axes]

    for idx, filepath in enumerate(test_files):
        try:
            x, y, z = load_and_process_test_file(filepath)

            ax = axes[idx]

            # Scatter plot colored by elevation
            scatter = ax.scatter(x, y, c=z, cmap='terrain', s=50, edgecolors='black', linewidths=0.5)
            plt.colorbar(scatter, ax=ax, label='Elevation (m)')

            filename = filepath.stem.replace("test_", "").replace("_", " ").title()
            ax.set_title(filename, fontsize=10, fontweight='bold')
            ax.set_xlabel('X (m)', fontsize=8)
            ax.set_ylabel('Y (m)', fontsize=8)
            ax.set_aspect('equal')
            ax.grid(True, alpha=0.3)

        except Exception as e:
            print(f"Error processing {filepath.name}: {e}")
            continue

    # Hide unused subplots
    for idx in range(len(test_files), len(axes)):
        axes[idx].set_visible(False)

    plt.tight_layout()
    plt.suptitle("Synthetic Test Terrains - 2D Elevation Maps",
                fontsize=16, fontweight='bold', y=1.001)
    plt.show()


def main():
    """Main menu"""
    print("="*60)
    print("TERRAIN VISUALIZATION TOOL")
    print("="*60)
    print("\nVisualization options:")
    print("  1. 3D surface plots (all terrains)")
    print("  2. 2D elevation heatmaps (all terrains)")
    print("  3. Both")

    choice = input("\nEnter choice (1/2/3) [3]: ").strip() or '3'

    if choice in ['1', '3']:
        print("\nGenerating 3D visualizations...")
        visualize_all_terrains()

    if choice in ['2', '3']:
        print("\nGenerating 2D visualizations...")
        visualize_terrain_2d_heatmaps()

    print("\nVisualization complete!")


if __name__ == "__main__":
    main()
