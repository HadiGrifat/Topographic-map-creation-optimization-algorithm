import numpy as np
from .data_processing import load_gpx_data, load_multiple_gpx, normalize_elevation, coord_transform
from .visualization import plot_3D, create_contour_plot, create_3d_contour
from .interpolation import create_grid, interpolate_elevation

class MappingPipeline:
    def __init__(self):
        # Raw GPS data
        self.lats = None
        self.lons = None
        self.alts = None
        
        # Processed data
        self.x = None
        self.y = None
        self.z = None
        
        # Grid and interpolated data
        self.xi = None
        self.yi = None
        self.zi = None
        
    def load_data(self, data_source, is_multiple=False):
        """Load GPS data from single file or multiple files"""
        if is_multiple:
            self.lats, self.lons, self.alts = load_multiple_gpx(data_source)
        else:
            self.lats, self.lons, self.alts = load_gpx_data(data_source)
        print(f"Number of GPS points: {len(self.lats)}")
        
    def preprocess_data(self):
        """Normalize elevation and transform coordinates"""
        self.alts = normalize_elevation(self.alts)
        print(f"Elevation range: {np.min(self.alts):.1f} to {np.max(self.alts):.1f} meters")
        
        self.x, self.y = coord_transform(self.lats, self.lons)
        self.z = np.array(self.alts)
        
    def create_interpolation_grid(self, grid_size=20):
        """Create interpolation grid"""
        self.xi, self.yi = create_grid(self.x, self.y, grid_size)
        print(f"Grid size: {grid_size}x{grid_size} = {grid_size**2} interpolated points")
        
    def interpolate_data(self, method='linear'):
        """Interpolate elevation data using specified method"""
        if method == 'linear':
            self.zi = interpolate_elevation(self.x, self.y, self.z, self.xi, self.yi)
        elif method == 'delaunay':
            # Placeholder for future implementation
            raise NotImplementedError("Delaunay triangulation method not yet implemented")
        else:
            raise ValueError(f"Unknown interpolation method: {method}")
            
        print(f"Interpolated elevation range: {np.nanmin(self.zi):.1f} to {np.nanmax(self.zi):.1f} meters")
        
    def visualize_3d_original(self):
        """Create 3D plot of original GPS data"""
        plot_3D(self.lats, self.lons, self.alts)
        
    def visualize_contour_2d(self, show_gps_points=True):
        """Create 2D contour plot"""
        if show_gps_points:
            create_contour_plot(self.xi, self.yi, self.zi, self.x, self.y)
        else:
            create_contour_plot(self.xi, self.yi, self.zi)
            
    def visualize_contour_3d(self, show_gps_points=True):
        """Create 3D contour plot"""  
        if show_gps_points:
            create_3d_contour(self.xi, self.yi, self.zi, self.x, self.y, self.z)
        else:
            create_3d_contour(self.xi, self.yi, self.zi)