import numpy as np
from modules.data_processing import load_gpx_data, load_multiple_gpx, normalize_elevation, coord_transform
from modules.visualization import plot_3D, create_contour_plot, create_3d_contour
from modules.interpolation import create_grid, interpolate_elevation

def main():
    # Step 1: Load data
    lats, lons, alts = load_gpx_data('Data/7_4_Tech_Park.gpx')
    # combined data pipeline
    #gpx_files = [
    #    'Data/Track2_24_4_2025.gpx',
    #    'Data/Track1_24_4_2025.gpx'
    #]
    #lats, lons, alts = load_multiple_gpx(gpx_files)
    print(f"Number of GPS points: {len(lats)}") # print number of gps samples

    # Step 2: Normalize elevation
    alts = normalize_elevation(alts)
    print(f"Elevation range: {np.min(alts):.1f} to {np.max(alts):.1f} meters") # print total elevation change

    # Step 3: Create 3D plot
    plot_3D(lats, lons, alts)

    # Step 4: Transform coordinates
    x, y = coord_transform(lats, lons)
    z = np.array(alts) # alts is already a np array so we could just say z=alts but i am choosing to
    # keep it like this for ease of understanding, since alts is turned into a np array in a function

    # Step 5: Create interpolation grid
    grid_size = 20
    xi, yi = create_grid(x, y, grid_size)
    print(f"Grid size: {grid_size}x{grid_size} = {grid_size**2} interpolated points") # number of grid points

    # Step 6: Interpolate elevation
    zi = interpolate_elevation(x, y, z, xi, yi)
    print(f"Interpolated elevation range: {np.nanmin(zi):.1f} to {np.nanmax(zi):.1f} meters") # interpolation elevation range

    #print(f"GPS X range: {min(x):.1f} to {max(x):.1f}")
    #print(f"GPS Y range: {min(y):.1f} to {max(y):.1f}")
    #print(f"Grid X range: {xi.min():.1f} to {xi.max():.1f}")     
    #print(f"Grid Y range: {yi.min():.1f} to {yi.max():.1f}")     
    #print(f"Grid has NaN values: {np.isnan(zi).sum()} out of {zi.size}")
    # these prints commands where used for debugging, edges weren't rendering, so wanted
    # to see how many NaN values return

    # Step 7: Create contour plot, takes optionl arguments for gps data scattering x,y. z if we want gps points colored by elevation
    create_contour_plot(xi, yi, zi, x, y)
    # create_3d_contour take optional params of the orignal gps coord, x,y,z
    # in order to plot them on the mesh
    create_3d_contour(xi, yi, zi, x, y, z)

if __name__=="__main__":
    main()
