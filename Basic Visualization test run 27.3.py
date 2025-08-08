import gpxpy
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from scipy.interpolate import griddata
from pyproj import Transformer
import pandas as pd

with open('Data/Track2_24_4_2025.gpx', 'r') as f:
    gpx = gpxpy.parse(f)

lats, lons, alts = [], [], []
for track in gpx.tracks:
    for segment in track.segments:
        for point in segment.points:
            lats.append(point.latitude)
            lons.append(point.longitude)
            alts.append(point.elevation)

'''   # If Data in CSV format...
df = pd.read_csv('') # load CSV data
lats = df['lat'].to_numpy() # extracting data from CSV file
lons = df['lon'].to_numpy()
alts = df['alt'].to_numpy()
'''

alts -= np.min(alts) # normalizing elevation so min(alts) = 0

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
sc = ax.scatter(lons, lats, alts, c=alts, cmap='terrain')
ax.set_xlabel('Longitude')
ax.set_ylabel('Latitude')
ax.set_zlabel('Elevation (m)')
fig.colorbar(sc, label='Elevation')
plt.title('Topographic Map from GPX')
plt.show()

transformer = Transformer.from_crs("epsg:4326", "epsg:32636", always_xy=True) # tranforming latitude and longitude from degree into meters for projection
x, y = transformer.transform(lons, lats)
z = np.array(alts)

# creating grid for interpolation
xi = np.linspace(min(x), max(x), 200)
yi = np.linspace(min(y), max(y), 200)
xi, yi = np.meshgrid(xi, yi)

# interpolating elevation at grid points
x = np.array(x, dtype=float)
y = np.array(y, dtype=float)
z = np.array(z, dtype=float)
zi = griddata((x, y), z, (xi, yi), method='linear')    # nearest: Assigns the value of the nearest known data point
                                                        # Cubic: Performs cubic interpolation over a triangle mesh
# Plot contours                                         # linear: Interpolates within triangles formed by your data points
plt.contourf(xi, yi, zi, cmap='terrain')
#plt.contour(xi, yi, zi, cmap='terrain')
plt.colorbar(label="Elevation (m)")
plt.title("Topographic Contour Map")
plt.xlabel("X (m)")
plt.ylabel("Y (m)")
plt.axis('equal')
plt.show()


'''
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

sc = ax.scatter(lons, lats, alts, c=alts, cmap='terrain', s=20)
ax.set_xlabel("Longitude")
ax.set_ylabel("Latitude")
ax.set_zlabel("Altitude (m)")
plt.title("Topographic Sample Points")
fig.colorbar(sc, label="Elevation")
plt.show()'
'''