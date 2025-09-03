from mapping_pipeline import MappingPipeline

print("Testing MappingPipeline class...")
print("=" * 40)

# Create pipeline instance
pipeline = MappingPipeline()

# Test each step - this should match your current main.py exactly
print("Step 1: Loading data...")
pipeline.load_data('Data/Track2_24_4_2025.gpx')

print("\nStep 2: Preprocessing data...")
pipeline.preprocess_data()

print("\nStep 3: Creating 3D plot of original GPS data...")
pipeline.visualize_3d_original()

print("\nStep 4: Creating interpolation grid...")
pipeline.create_interpolation_grid(grid_size=20)

print("\nStep 5: Interpolating elevation data...")
pipeline.interpolate_data(method='linear')

print("\nStep 6: Creating 2D contour plot...")
pipeline.visualize_contour_2d(show_gps_points=True)

print("\nStep 7: Creating 3D contour plot...")
pipeline.visualize_contour_3d(show_gps_points=True)

print("\nPipeline test completed successfully!")
print("This should produce the same results as your original main.py")