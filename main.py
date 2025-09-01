import numpy as np
from data_proccessing import load_gpx_data, normalize_elevation, coord_transform
from visualization import plot_3D, create_contour_plot
from interpolation import create_grid, interpolate_elevation

def main():
# Step 1: Load data
    lats, lons, alts = load_gpx_data('Data/Track2_24_4_2025.gpx')

    # Step 2: Normalize elevation
    alts = normalize_elevation(alts)

    # Step 3: Create 3D plot
    plot_3D(lats, lons, alts)

    # Step 4: Transform coordinates
    x, y = coord_transform(lats, lons)
    z = np.array(alts)

    # Step 5: Create interpolation grid
    xi, yi = create_grid(x, y, 200)

    # Step 6: Interpolate elevation
    zi = interpolate_elevation(x, y, z, xi, yi)

    # Step 7: Create contour plot
    create_contour_plot(xi, yi, zi)

if __name__=="__main__":
    main()
