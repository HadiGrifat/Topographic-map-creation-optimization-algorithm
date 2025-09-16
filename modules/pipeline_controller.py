"""
Pipeline Controller - handles all business logic for running mapping pipelines
"""
from .mapping_pipeline import MappingPipeline
from .analytics import analyze_triangulation_quality

def run_interpolation_pipeline(pipeline, method, grid_size, vertical_exaggeration):
    """Execute interpolation-specific pipeline workflow"""
    pipeline.visualize_3d_original()
    pipeline.create_interpolation_grid(grid_size=grid_size)
    pipeline.interpolate_data(method=method)
    pipeline.visualize_contour_2d()
    pipeline.visualize_contour_3d(vertical_exaggeration=vertical_exaggeration)
    print(f"\n{method} interpolation completed successfully!")

def run_delaunay_mesh_pipeline(pipeline, method, vertical_exaggeration):
    """Execute Delaunay triangulation mesh creation workflow"""
    pipeline.visualize_3d_original()
    pipeline.create_triangulation()
    pipeline.visualize_triangular_mesh(vertical_exaggeration=vertical_exaggeration)
    pipeline.visualize_wireframe(vertical_exaggeration=vertical_exaggeration)
    print(f"\n{method} mesh creation completed successfully!")

def run_delaunay_analytics_pipeline(pipeline, method, vertical_exaggeration):
    """Execute Delaunay triangulation analytics workflow"""
    pipeline.visualize_3d_original()
    pipeline.create_triangulation()

    # Perform triangle quality analysis
    triangulation = pipeline.triangulation
    points_2d = pipeline.points_2d
    print("\nPerforming triangle quality analysis...")
    fatness_ratios, triangle_stats = analyze_triangulation_quality(triangulation, points_2d)
    print(f"\n{method} analytics completed successfully!")

def run_pipeline(method, data_source, is_multiple, grid_size=20, vertical_exaggeration=3):
    """Execute a mapping pipeline with the specified method and data"""
    if data_source is None:
        print("No data source selected.")
        return False
        
    # Determine pipeline type based on method
    if method in ['linear', 'cubic', 'nearest']:
        pipeline_type = "interpolation"
    elif method == 'delaunay_mesh':
        pipeline_type = "delaunay_mesh"
    elif method == 'delaunay_analytics':
        pipeline_type = "delaunay_analytics"
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
            run_interpolation_pipeline(pipeline, method, grid_size, vertical_exaggeration)
        elif pipeline_type == "delaunay_mesh":
            run_delaunay_mesh_pipeline(pipeline, method, vertical_exaggeration)
        elif pipeline_type == "delaunay_analytics":
            run_delaunay_analytics_pipeline(pipeline, method, vertical_exaggeration)
            
        return True
        
    except NotImplementedError as e:
        print(f"\nError: {e}")
        print("Available methods: linear, cubic, nearest interpolation")
        return False
    except Exception as e:
        print(f"\nError running pipeline: {e}")
        return False


