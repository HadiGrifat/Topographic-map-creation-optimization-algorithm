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

# def create_3d_contour(xi, yi, zi, x_gps=None, y_gps=None, z_gps=None):
#     surface = go.Surface( # create mesh surface from 3d data, x,y are 2d grids and z give elevation
#         x = xi,           # data at each intersection
#         y = yi,
#         z= zi,
#         colorscale='earth',
#         showscale=True,
#         contours=dict( # make contour lines show up on mesh
#             z=dict(
#                 show=True,
#                 usecolormap=False,
#                 #color="red", # contour lines color, default = black
#                 highlightcolor="red", # highlight color
#                 project_z=False, # project on xy plane
#                 width=3, # width if lines
#                 size=2, # spacing, every x meters
#                 start=0, # start lines at elevation x
#                 end=35 # end lines at elevation x
#             )
#         )
#     )
#     # adding gps data to the 3d mesh
#     if x_gps is not None and y_gps is not None and z_gps is not None:
#         gps_points = go.Scatter3d(
#             x = x_gps,
#             y = y_gps,
#             z = z_gps,
#             mode = "markers",
#             marker=dict(
#                 size=3,
#                 color="red",
#                 symbol="circle"
#             ),
#             name='GPS Sample Points'
#         )
#         fig = go.Figure(data=[surface, gps_points])
#     else:
#         fig = go.Figure(data=[surface]) # create figure
#         
#     fig.update_layout(  # set up the scene for the figure create a line above, layout settings
#         title = '3D Topographic Contour Map',
#         scene = dict(
#             xaxis_title = 'X (m)',
#             yaxis_title = 'Y (m)',
#             zaxis_title = 'Elevation (m)',
#             camera = dict(
#                 eye = dict(x=0, y=-1.5, z=0.5), # starting orientation looking north (negative y)
#                 # alternatives: x=1, y=1, z=0.8 isometric view
#                 # x=0, y=0, z=2 top down view
#                 up = dict(x=0, y=0, z=1) # z axis looking up
#             )),
#             # adding a rest button for orientation
#         updatemenus = [dict( # create interactive UI element
#             type = "buttons", # type of UI element wanted
#             buttons = [dict(label="Reset View", #label: text that appear on button
#                             method="relayout", # what action is done when button is pressed, relayout changes plot layout/styling
#                             args=["scene.camera", # what specificaly to change
#                                     dict(eye=dict(x=0, y=-1.5, z=0.5))])]
#         )]
#     )
#     fig.show()

def create_3d_contour(xi, yi, zi, x_gps=None, y_gps=None, z_gps=None):
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    # Create 3D surface plot with contours
    surface = ax.plot_surface(xi, yi, zi, 
                             cmap='terrain', 
                             alpha=0.8,
                             linewidth=0.1, 
                             antialiased=True,
                             rstride=1, cstride=1)
    
    # Add contour lines projected on the surface
    contour_lines = ax.contour(xi, yi, zi, 
                              levels=10, 
                              colors='black', 
                              linewidths=0.5,
                              alpha=0.7)
    
    # Add color bar
    fig.colorbar(surface, label='Elevation (m)', shrink=0.6)
    
    # Add GPS points if provided
    if x_gps is not None and y_gps is not None and z_gps is not None:
        ax.scatter(x_gps, y_gps, z_gps, 
                  c='red', s=10, alpha=0.8, 
                  label='GPS Sample Points')
        ax.legend()
    
    # Labels and title
    ax.set_xlabel('X (m)')
    ax.set_ylabel('Y (m)')
    ax.set_zlabel('Elevation (m)')
    ax.set_title('3D Topographic Contour Map')
    
    # Set viewing angle similar to Plotly
    ax.view_init(elev=20, azim=45)
    
    plt.tight_layout()
    plt.show()

def visualize_triangular_mesh(x, y, z, triangles, title_suffix=""):
    """
    Display 3D triangular mesh with colored surface
    
    Args:
        x, y, z: Coordinate and elevation arrays
        triangles: Triangle indices from triangulation
        title_suffix: Additional text for plot title
    """
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
    ax.set_title(f'Delaunay Triangulation - 3D Mesh{title_suffix}\n{len(triangles)} triangles from {len(x)} GPS points')
    
    # Set viewing angle
    ax.view_init(elev=30, azim=45)
    
    # Set proper aspect ratio - prevent unrealistic vertical exaggeration
    # Use 3x vertical exaggeration for better visibility while keeping realistic proportions
    x_range = max(x) - min(x)
    y_range = max(y) - min(y) 
    z_range = max(z) - min(z)
    vertical_exaggeration = 3
    ax.set_box_aspect([x_range, y_range, z_range * vertical_exaggeration])
    
    plt.tight_layout()
    plt.show()

def visualize_wireframe(x, y, z, triangles, title_suffix=""):
    """
    Display wireframe view showing triangle structure
    
    Args:
        x, y, z: Coordinate and elevation arrays  
        triangles: Triangle indices from triangulation
        title_suffix: Additional text for plot title
    """
    fig = plt.figure(figsize=(14, 10))
    ax = fig.add_subplot(111, projection='3d')
    
    # Plot wireframe (just the triangle edges)
    ax.plot_trisurf(x, y, z, triangles=triangles, 
                   color='lightblue', alpha=0.3,
                   edgecolor='black', linewidth=0.5)
    
    # Show GPS points
    ax.scatter(x, y, z, c='red', s=10, alpha=0.8, label='GPS Points')
    
    ax.set_xlabel('X (meters)')
    ax.set_ylabel('Y (meters)')
    ax.set_zlabel('Elevation (meters)')
    ax.set_title(f'Delaunay Triangulation - Wireframe View{title_suffix}\nShowing triangle connections')
    ax.view_init(elev=30, azim=45)
    
    # Set proper aspect ratio - prevent unrealistic vertical exaggeration
    # Use 3x vertical exaggeration for better visibility while keeping realistic proportions
    x_range = max(x) - min(x)
    y_range = max(y) - min(y) 
    z_range = max(z) - min(z)
    vertical_exaggeration = 3
    ax.set_box_aspect([x_range, y_range, z_range * vertical_exaggeration])
    
    plt.tight_layout()
    plt.show()