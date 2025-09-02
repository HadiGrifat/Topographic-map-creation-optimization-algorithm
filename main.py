import numpy as np
from modules.data_processing import load_gpx_data, normalize_elevation, coord_transform
from modules.visualization import plot_3D, create_contour_plot, create_3d_contour
from modules.interpolation import create_grid, interpolate_elevation

def main():
# Step 1: Load data
    lats, lons, alts = load_gpx_data('Data/Track2_24_4_2025.gpx')
    print(f"Number of GPS points: {len(lats)}") # print number of gps samples

    # Step 2: Normalize elevation
    alts = normalize_elevation(alts)
    print(f"Elevation range: {np.min(alts):.1f} to {np.max(alts):.1f} meters") # print total elevation change

    # Step 3: Create 3D plot
    plot_3D(lats, lons, alts)

    # Step 4: Transform coordinates
    x, y = coord_transform(lats, lons)
    z = np.array(alts)

    # Step 5: Create interpolation grid
    grid_size = 20
    xi, yi = create_grid(x, y, grid_size)
    print(f"Grid size: {grid_size}x{grid_size} = {grid_size**2} interpolated points") # number of grid points

    # Step 6: Interpolate elevation
    zi = interpolate_elevation(x, y, z, xi, yi)
    print(f"Interpolated elevation range: {np.nanmin(zi):.1f} to {np.nanmax(zi):.1f} meters") # interpolation elevation range

    # Step 7: Create contour plot
    create_contour_plot(xi, yi, zi)
    create_3d_contour(xi, yi, zi)

if __name__=="__main__":
    main()
