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

def create_contour_plot(xi, yi, zi, x_gps=None, y_gps=None, z_gps=None):
    # Plot contours                       
    plt.contourf(xi, yi, zi, cmap='terrain')
    plt.colorbar(label="Elevation (m)")
    # addong elevation labels to contour lines
    contour_lines = plt.contour(xi, yi, zi, colors='black', linewidths=0.5)
    plt.clabel(contour_lines, inline=True, fontsize=4, fmt='%0.0f m')
    # if z_gps is given, plot map with points colored by elevation, if not by color red
    if z_gps==None:
        z="red"
    else:
        z = z_gps
    if x_gps is not None and y_gps is not None: # scattering the gps data points
        scatter = plt.scatter(x_gps, y_gps,
                              #c= "red",
                              c=z,
                              s=5,
                              alpha=0.8
                              )
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
        showscale=True,
        contours=dict( # make contour lines show up on mesh
            z=dict(
                show=True,
                usecolormap=False,
                #color="red", # contour lines color, default = black
                highlightcolor="red", # highlight color
                project_z=False, # project on xy plane
                width=3, # width if lines
                size=2, # spacing, every x meters
                start=0, # start lines at elevation x
                end=35 # end lines at elevation x
            )
        )
    )
    # adding gps data to the 3d mesh
    if x_gps is not None and y_gps is not None and z_gps is not None:
        gps_points = go.Scatter3d(
            x = x_gps,
            y = y_gps,
            z = z_gps,
            mode = "markers",
            marker=dict(
                size=3,
                color="red",
                symbol="circle"
            ),
            name='GPS Sample Points'
        )
        fig = go.Figure(data=[surface, gps_points])
    else:
        fig = go.Figure(data=[surface]) # create figure
        
    fig.update_layout(  # set up the scene for the figure create a line above, layout settings
        title = '3D Topographic Contour Map',
        scene = dict(
            xaxis_title = 'X (m)',
            yaxis_title = 'Y (m)',
            zaxis_title = 'Elevation (m)',
            camera = dict(
                eye = dict(x=0, y=-1.5, z=0.5), # starting orientation looking north (negative y)
                # alternatives: x=1, y=1, z=0.8 isometric view
                # x=0, y=0, z=2 top down view
                up = dict(x=0, y=0, z=1) # z axis looking up
            )),
            # adding a rest button for orientation
        updatemenus = [dict( # create interactive UI element
            type = "buttons", # type of UI element wanted
            buttons = [dict(label="Reset View", #label: text that appear on button
                            method="relayout", # what action is done when button is pressed, relayout changes plot layout/styling
                            args=["scene.camera", # what specificaly to change
                                    dict(eye=dict(x=0, y=-1.5, z=0.5))])]
        )]
    )
    fig.show()