import matplotlib.pyplot as plt
import plotly.graph_objects as go

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

def create_3d_contour(xi, yi, zi, x_gps=None, y_gps=None, z_gps=None):
    surface = go.Surface( # create mesh surface from 3d data, x,y are 2d grids and z give elevation
        x = xi,           # data at each intersection
        y = yi,
        z= zi,
        colorscale='earth',
        showscale=True
    )
    fig = go.Figure(data=[surface]) # create gifure
    fig.update_layout(  # set up the scene for the figure create a line above, layout settings
        title = '3D Topographic Contour Map',
        scene = dict(
            xaxis_title = 'X (m)',
            yaxis_title = 'Y (m)',
            zaxis_title = 'Elevation (m)'
        )
    )
    fig.show()