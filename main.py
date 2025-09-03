#!/usr/bin/env python3
"""
Main script for running different mapping methods
"""
from mapping_pipeline import MappingPipeline

def run_linear_interpolation():
    """Run your current working method - linear interpolation"""
    print("Running Linear Interpolation Method")
    print("=" * 50)
    
    pipeline = MappingPipeline()
    pipeline.load_data('Data/Track2_24_4_2025.gpx')
    pipeline.preprocess_data()
    pipeline.visualize_3d_original()
    pipeline.create_interpolation_grid(grid_size=20)
    pipeline.interpolate_data(method='linear')
    pipeline.visualize_contour_2d()
    pipeline.visualize_contour_3d()

def run_delaunay_triangulation():
    """Placeholder for Delaunay method - you'll implement this later"""
    print("Running Delaunay Triangulation Method")
    print("=" * 50)
    
    pipeline = MappingPipeline()
    pipeline.load_data('Data/Track2_24_4_2025.gpx')
    pipeline.preprocess_data()
    pipeline.visualize_3d_original()
    pipeline.create_interpolation_grid(grid_size=20)
    
    try:
        pipeline.interpolate_data(method='delaunay')
        pipeline.visualize_contour_2d()
        pipeline.visualize_contour_3d()
    except NotImplementedError:
        print("Delaunay method not implemented yet!")

def run_multiple_files():
    """Test with multiple GPX files"""
    print("Running Multiple Files with Linear Interpolation")
    print("=" * 50)
    
    gpx_files = [
        'Data/Track2_24_4_2025.gpx',
        'Data/Track1_24_4_2025.gpx'
    ]
    
    pipeline = MappingPipeline()
    pipeline.load_data(gpx_files, is_multiple=True)
    pipeline.preprocess_data()
    pipeline.visualize_3d_original()
    pipeline.create_interpolation_grid(grid_size=25)  # Slightly bigger grid for more data
    pipeline.interpolate_data(method='linear')
    pipeline.visualize_contour_2d()
    pipeline.visualize_contour_3d()

def main():
    """Main function with method selection menu"""
    print("Mapping Project - Method Selection")
    print("=" * 40)
    print("1. Linear Interpolation (current working method)")
    print("2. Delaunay Triangulation (experimental)")
    print("3. Multiple GPX files")
    print("4. Exit")
    
    while True:
        choice = input("\nSelect method (1-4): ").strip()
        
        if choice == '1':
            run_linear_interpolation()
            break
        elif choice == '2':
            run_delaunay_triangulation()
            break
        elif choice == '3':
            run_multiple_files()
            break
        elif choice == '4':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please enter 1-4.")

if __name__ == "__main__":
    main()