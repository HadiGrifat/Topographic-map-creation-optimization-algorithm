"""
Pipeline Controller - handles all business logic for running mapping pipelines
"""
from .mapping_pipeline import MappingPipeline

def run_pipeline(method, data_source, is_multiple):
    """Execute a mapping pipeline with the specified method and data"""
    if data_source is None:
        print("No data source selected.")
        return False
        
    print(f"\nRunning {method} interpolation...")
    print("=" * 50)
    
    try:
        # Create and configure pipeline
        pipeline = MappingPipeline()
        pipeline.load_data(data_source, is_multiple)
        pipeline.preprocess_data()
        
        # Visualization and processing
        pipeline.visualize_3d_original()
        pipeline.create_interpolation_grid(grid_size=20)
        pipeline.interpolate_data(method=method)
        pipeline.visualize_contour_2d()
        pipeline.visualize_contour_3d()
        
        print(f"\n{method} interpolation completed successfully!")
        return True
        
    except NotImplementedError as e:
        print(f"\nError: {method} method not implemented yet!")
        print("Available methods: linear")
        return False
    except Exception as e:
        print(f"\nError running pipeline: {e}")
        return False

def get_available_methods():
    """Return list of available interpolation methods"""
    return [
        ('linear', 'Linear Interpolation'),
        ('delaunay', 'Delaunay Triangulation (experimental)')
    ]

