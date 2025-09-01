import matplotlib.pyplot as plt

def plot_3D(lats, lons, alts):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    sc = ax.scatter(lons, lats, alts, c=alts, cmap='terrain')
    ax.set_xlabel('Longitude')
    ax.set_ylabel('Latitude')
    ax.set_zlabel('Elevation (m)')
    fig.colorbar(sc, label='Elevation')
    plt.title('Topographic Map from GPX')
    plt.show()

def create_contour_plot(xi, yi, zi):
    # Plot contours                       
    plt.contourf(xi, yi, zi, cmap='terrain')
    #plt.contour(xi, yi, zi, cmap='terrain')
    plt.colorbar(label="Elevation (m)")
    plt.title("Topographic Contour Map")
    plt.xlabel("X (m)")
    plt.ylabel("Y (m)")
    plt.axis('equal')
    plt.show()