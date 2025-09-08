"""
Pipeline Controller - handles all business logic for running mapping pipelines
"""
from .mapping_pipeline import MappingPipeline

def run_interpolation_pipeline(pipeline, method, grid_size):
    """Execute interpolation-specific pipeline workflow"""
    pipeline.visualize_3d_original()
    pipeline.create_interpolation_grid(grid_size=grid_size)
    pipeline.interpolate_data(method=method)
    pipeline.visualize_contour_2d()
    pipeline.visualize_contour_3d()
    print(f"\n{method} interpolation completed successfully!")

def run_delaunay_pipeline(pipeline, method):
    """Execute Delaunay triangulation-specific pipeline workflow"""
    pipeline.visualize_3d_original()
    # TODO: Add Delaunay-specific steps when implementation is ready
    # - Create triangular mesh
    # - Apply triangulation algorithm  
    # - Generate mesh-based visualizations
    raise NotImplementedError(f"{method} triangulation not yet implemented")

def run_pipeline(method, data_source, is_multiple, grid_size=20):
    """Execute a mapping pipeline with the specified method and data"""
    if data_source is None:
        print("No data source selected.")
        return False
        
    # Determine pipeline type based on method
    if method in ['linear', 'cubic', 'nearest']:
        pipeline_type = "interpolation"
    elif method == 'delaunay':
        pipeline_type = "triangulation"
    else:
        print(f"Unknown method: {method}")
        return False
        
    print(f"\nRunning {method} {pipeline_type}...")
    print("=" * 50)
    
    try:
        # Shared setup for all methods
        pipeline = MappingPipeline()
        pipeline.load_data(data_source, is_multiple)
        pipeline.preprocess_data()
        
        # Route to method-specific pipeline
        if pipeline_type == "interpolation":
            run_interpolation_pipeline(pipeline, method, grid_size)
        elif pipeline_type == "triangulation":
            run_delaunay_pipeline(pipeline, method)
            
        return True
        
    except NotImplementedError as e:
        print(f"\nError: {e}")
        print("Available methods: linear, cubic, nearest interpolation")
        return False
    except Exception as e:
        print(f"\nError running pipeline: {e}")
        return False

def get_available_methods():
    """Return list of available mapping methods"""
    return [
        ('interpolation', 'Interpolation'),
        ('delaunay', 'Delaunay Triangulation (experimental)')
    ]

def get_available_interpolations():
    """Return list of available interpolation methods"""
    return [
        ('linear', 'Linear Interpolation'),
        ('cubic', 'Cubic Interpolation'),
        ('nearest', 'Nearest Value Interpolation')
    ]

