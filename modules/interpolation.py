import numpy as np
from scipy.interpolate import griddata

def create_grid(x, y, grid_size):
    xi = np.linspace(min(x), max(x), grid_size)
    yi = np.linspace(min(y), max(y), grid_size)
    xi, yi = np.meshgrid(xi, yi)
    return xi, yi

def interpolate_elevation(x, y, z, xi, yi, method='linear'):
    x = np.array(x, dtype=float)
    y = np.array(y, dtype=float)
    z = np.array(z, dtype=float)
    zi = griddata((x, y), z, (xi, yi), method=method) 
    # nearest: Assigns the value of the nearest known data point
    # Cubic: Performs cubic interpolation over a triangle mesh
    # linear: Interpolates within triangles formed by your data points
    return zi