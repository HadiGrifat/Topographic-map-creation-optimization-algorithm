"""
Generate synthetic test data for curvature analysis

This script creates CSV files with various terrain patterns to test
the curvature calculation algorithm with known geometric properties.

Data is stored directly in meter coordinates (x, y, z) without any
GPS coordinate conversion to avoid transformation artifacts.
"""

import numpy as np
from pathlib import Path


def save_terrain_data(x_meters, y_meters, elevations, filename, track_name="Test Track"):
    """
    Save terrain data directly in meter coordinates (x, y, z)

    Args:
        x_meters: Array of X coordinates in meters
        y_meters: Array of Y coordinates in meters
        elevations: Array of elevation values in meters
        filename: Output CSV filename
        track_name: Name for the terrain dataset
    """
    # Convert lists to numpy arrays for easier computation
    x_meters = np.array(x_meters)
    y_meters = np.array(y_meters)
    elevations = np.array(elevations)

    # Save as CSV file with x, y, z columns
    data = np.column_stack((x_meters, y_meters, elevations))

    # Write to file with header
    with open(filename, 'w') as f:
        f.write(f"# {track_name}\n")
        f.write("# X(m), Y(m), Z(m)\n")
        np.savetxt(f, data, delimiter=',', fmt='%.6f')

    print(f"Created: {filename}")
    print(f"  Points: {len(x_meters)}")
    print(f"  X range: [{min(x_meters):.2f}, {max(x_meters):.2f}] m")
    print(f"  Y range: [{min(y_meters):.2f}, {max(y_meters):.2f}] m")
    print(f"  Elevation range: [{min(elevations):.2f}, {max(elevations):.2f}] m")


def generate_flat_plane(output_dir):
    """
    Generate a flat plane - should produce zero or near-zero curvature everywhere
    """
    print("\n=== Generating Flat Plane ===")

    # Create a 10x10 grid with 5m spacing in meter coordinates
    spacing_meters = 5.0
    grid_size = 10

    x_coords = []
    y_coords = []
    elevations = []

    for i in range(grid_size):
        for j in range(grid_size):
            x_coords.append(j * spacing_meters)  # X increases with column
            y_coords.append(i * spacing_meters)  # Y increases with row
            elevations.append(100.0)  # Constant elevation - perfectly flat

    filename = output_dir / "test_flat_plane.csv"
    save_terrain_data(x_coords, y_coords, elevations, filename, "Flat Plane")
    print("Expected: Zero curvature at all interior vertices\n")


def generate_tilted_plane(output_dir):
    """
    Generate a tilted plane - should also produce zero curvature (flat, just sloped)
    """
    print("\n=== Generating Tilted Plane ===")

    spacing_meters = 5.0
    grid_size = 10

    x_coords = []
    y_coords = []
    elevations = []

    # Add a slope: elevation increases by 2m per grid step in y direction
    for i in range(grid_size):
        for j in range(grid_size):
            x_coords.append(j * spacing_meters)
            y_coords.append(i * spacing_meters)
            elevations.append(100.0 + 2.0 * i)  # Linear slope

    filename = output_dir / "test_tilted_plane.csv"
    save_terrain_data(x_coords, y_coords, elevations, filename, "Tilted Plane")
    print("Expected: Zero curvature (plane is flat, just tilted)\n")


def generate_dome(output_dir):
    """
    Generate a dome/hill shape - should produce uniform positive curvature
    """
    print("\n=== Generating Dome/Hill ===")

    spacing_meters = 3.0
    grid_size = 15

    x_coords = []
    y_coords = []
    elevations = []

    # Dome: elevation based on distance from center
    center_i = grid_size / 2.0
    center_j = grid_size / 2.0
    dome_height = 20.0  # Peak height above base
    dome_radius = grid_size / 2.0

    for i in range(grid_size):
        for j in range(grid_size):
            # Distance from center
            dist = np.sqrt((i - center_i)**2 + (j - center_j)**2)

            # Gaussian dome shape
            elevation = 100.0 + dome_height * np.exp(-(dist**2) / (2 * (dome_radius/2)**2))

            x_coords.append(j * spacing_meters)
            y_coords.append(i * spacing_meters)
            elevations.append(elevation)

    filename = output_dir / "test_dome.csv"
    save_terrain_data(x_coords, y_coords, elevations, filename, "Dome/Hill")
    print("Expected: Positive curvature, highest at peak, lower at edges\n")


def generate_valley(output_dir):
    """
    Generate a valley/bowl shape - should produce negative curvature concept
    (but algorithm computes absolute angle deficit, so positive values)
    """
    print("\n=== Generating Valley/Bowl ===")

    spacing_meters = 3.0
    grid_size = 15

    x_coords = []
    y_coords = []
    elevations = []

    # Valley: inverted dome
    center_i = grid_size / 2.0
    center_j = grid_size / 2.0
    valley_depth = 15.0
    valley_radius = grid_size / 2.0

    for i in range(grid_size):
        for j in range(grid_size):
            dist = np.sqrt((i - center_i)**2 + (j - center_j)**2)

            # Inverted Gaussian
            elevation = 100.0 - valley_depth * np.exp(-(dist**2) / (2 * (valley_radius/2)**2))

            x_coords.append(j * spacing_meters)
            y_coords.append(i * spacing_meters)
            elevations.append(elevation)

    filename = output_dir / "test_valley.csv"
    save_terrain_data(x_coords, y_coords, elevations, filename, "Valley/Bowl")
    print("Expected: Curvature pattern (inverted dome shape)\n")


def generate_ridge(output_dir):
    """
    Generate a ridge - high curvature along the ridge line
    """
    print("\n=== Generating Ridge ===")

    spacing_meters = 3.0
    grid_size = 15

    x_coords = []
    y_coords = []
    elevations = []

    # Ridge: elevation drops off perpendicular to center line
    center_j = grid_size / 2.0
    ridge_height = 15.0

    for i in range(grid_size):
        for j in range(grid_size):
            # Distance from center line (j direction)
            dist_from_ridge = abs(j - center_j)

            # Exponential drop-off
            elevation = 100.0 + ridge_height * np.exp(-dist_from_ridge / 2.0)

            x_coords.append(j * spacing_meters)
            y_coords.append(i * spacing_meters)
            elevations.append(elevation)

    filename = output_dir / "test_ridge.csv"
    save_terrain_data(x_coords, y_coords, elevations, filename, "Ridge")
    print("Expected: High curvature along center ridge line\n")


def generate_saddle_point(output_dir):
    """
    Generate a saddle point - interesting curvature behavior
    (positive in one direction, negative in perpendicular direction)
    """
    print("\n=== Generating Saddle Point ===")

    spacing_meters = 3.0
    grid_size = 15

    x_coords = []
    y_coords = []
    elevations = []

    center_i = grid_size / 2.0
    center_j = grid_size / 2.0
    scale = 3.0

    for i in range(grid_size):
        for j in range(grid_size):
            # Saddle function: z = x^2 - y^2
            x = (i - center_i) / scale
            y = (j - center_j) / scale

            elevation = 100.0 + (x**2 - y**2) * 5.0

            x_coords.append(j * spacing_meters)
            y_coords.append(i * spacing_meters)
            elevations.append(elevation)

    filename = output_dir / "test_saddle.csv"
    save_terrain_data(x_coords, y_coords, elevations, filename, "Saddle Point")
    print("Expected: Complex curvature pattern at saddle point\n")


def generate_sine_wave(output_dir):
    """
    Generate a sine wave terrain - periodic curvature pattern
    """
    print("\n=== Generating Sine Wave ===")

    spacing_meters = 2.0
    grid_size = 20

    x_coords = []
    y_coords = []
    elevations = []

    wavelength = grid_size / 3.0  # 3 complete waves
    amplitude = 10.0

    for i in range(grid_size):
        for j in range(grid_size):
            # Sine wave in i direction
            elevation = 100.0 + amplitude * np.sin(2 * np.pi * i / wavelength)

            x_coords.append(j * spacing_meters)
            y_coords.append(i * spacing_meters)
            elevations.append(elevation)

    filename = output_dir / "test_sine_wave.csv"
    save_terrain_data(x_coords, y_coords, elevations, filename, "Sine Wave")
    print("Expected: Alternating high/low curvature at peaks and troughs\n")


def generate_pyramid(output_dir):
    """
    Generate a pyramid - sharp peak with high curvature at apex
    """
    print("\n=== Generating Pyramid ===")

    spacing_meters = 3.0
    grid_size = 15

    x_coords = []
    y_coords = []
    elevations = []

    center_i = grid_size / 2.0
    center_j = grid_size / 2.0
    pyramid_height = 25.0

    for i in range(grid_size):
        for j in range(grid_size):
            # Distance from center (L1 norm for pyramid shape)
            dist = abs(i - center_i) + abs(j - center_j)
            max_dist = grid_size

            # Linear decrease from peak
            elevation = 100.0 + pyramid_height * max(0, 1 - dist / max_dist)

            x_coords.append(j * spacing_meters)
            y_coords.append(i * spacing_meters)
            elevations.append(elevation)

    filename = output_dir / "test_pyramid.csv"
    save_terrain_data(x_coords, y_coords, elevations, filename, "Pyramid")
    print("Expected: Very high curvature at apex, zero on flat faces\n")


def generate_random_terrain(output_dir):
    """
    Generate random terrain with varying curvature
    """
    print("\n=== Generating Random Terrain ===")

    spacing_meters = 4.0
    grid_size = 12

    x_coords = []
    y_coords = []
    elevations = []

    # Use Perlin-like noise (simplified with random + smoothing)
    np.random.seed(42)  # Reproducible random terrain

    # Generate random base heights
    base_elevations = np.random.uniform(90, 110, (grid_size, grid_size))

    # Smooth with a simple gaussian filter
    from scipy.ndimage import gaussian_filter
    smoothed = gaussian_filter(base_elevations, sigma=1.5)

    for i in range(grid_size):
        for j in range(grid_size):
            x_coords.append(j * spacing_meters)
            y_coords.append(i * spacing_meters)
            elevations.append(smoothed[i, j])

    filename = output_dir / "test_random_terrain.csv"
    save_terrain_data(x_coords, y_coords, elevations, filename, "Random Terrain")
    print("Expected: Variable curvature across the terrain\n")


def generate_step_terrain(output_dir):
    """
    Generate step/terrace terrain - to test algorithm on discontinuities
    """
    print("\n=== Generating Step Terrain ===")

    spacing_meters = 3.0
    grid_size = 15

    x_coords = []
    y_coords = []
    elevations = []

    # Create 3 terraces
    for i in range(grid_size):
        for j in range(grid_size):
            # Step function based on i
            if i < 5:
                elevation = 100.0
            elif i < 10:
                elevation = 110.0
            else:
                elevation = 120.0

            x_coords.append(j * spacing_meters)
            y_coords.append(i * spacing_meters)
            elevations.append(elevation)

    filename = output_dir / "test_step_terrain.csv"
    save_terrain_data(x_coords, y_coords, elevations, filename, "Step Terrain")
    print("Expected: High curvature at step edges, zero on flat terraces\n")


def main():
    """
    Generate all test datasets
    """
    print("="*60)
    print("GPS TEST DATA GENERATOR FOR CURVATURE ANALYSIS")
    print("="*60)

    # Create output directory relative to this script's location
    script_dir = Path(__file__).parent
    output_dir = script_dir / "test_data"
    output_dir.mkdir(exist_ok=True)
    print(f"\nOutput directory: {output_dir.absolute()}\n")

    # Generate all test cases
    generate_flat_plane(output_dir)
    generate_tilted_plane(output_dir)
    generate_dome(output_dir)
    generate_valley(output_dir)
    generate_ridge(output_dir)
    generate_saddle_point(output_dir)
    generate_sine_wave(output_dir)
    generate_pyramid(output_dir)
    generate_random_terrain(output_dir)
    generate_step_terrain(output_dir)

    print("="*60)
    print("ALL TEST DATASETS GENERATED SUCCESSFULLY!")
    print("="*60)
    print(f"\nYou can now test these files using your curvature analysis pipeline.")
    print(f"Each test case has known geometric properties to validate results.\n")


if __name__ == "__main__":
    main()
