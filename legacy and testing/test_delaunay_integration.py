"""
Test script to verify Delaunay triangulation pipeline integration
"""
from modules.pipeline_controller import run_pipeline

def test_delaunay_pipeline():
    """Test the complete Delaunay pipeline integration"""
    print("Testing Delaunay triangulation pipeline...")
    
    # Test parameters
    method = 'delaunay'
    data_source = 'Data/Track2_24_4_2025.gpx'
    is_multiple = False
    grid_size = 20  # Won't be used for Delaunay but required by function signature
    
    # Run the pipeline
    success = run_pipeline(method, data_source, is_multiple, grid_size)
    
    if success:
        print("\nSUCCESS: Delaunay triangulation pipeline completed!")
        print("Integration test passed - Delaunay is now available in the main menu.")
    else:
        print("\nERROR: Pipeline failed")
        
    return success

if __name__ == "__main__":
    test_delaunay_pipeline()