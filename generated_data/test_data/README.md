# Synthetic GPS Test Data for Curvature Analysis

This directory contains synthetic GPS test datasets designed to validate the curvature calculation algorithm with known geometric properties.

## Quick Start

1. **Generate test data** (if not already done):
   ```bash
   python generate_test_gps_data.py
   ```

2. **Run tests**:
   ```bash
   python test_curvature_with_synthetic_data.py
   ```

## Test Datasets

### 1. Flat Plane (`test_flat_plane.gpx`)
- **Description**: Perfectly flat horizontal surface
- **Expected Result**: Zero or near-zero curvature at all interior vertices
- **Use Case**: Validates that algorithm correctly identifies flat regions
- **Grid**: 10×10 points, 5m spacing
- **Elevation**: Constant at 100m

### 2. Tilted Plane (`test_tilted_plane.gpx`)
- **Description**: Planar surface with constant slope
- **Expected Result**: Zero curvature (plane is flat despite being tilted)
- **Use Case**: Tests that algorithm distinguishes between slope and curvature
- **Grid**: 10×10 points, 5m spacing
- **Elevation**: Linear gradient (100-118m)

### 3. Dome/Hill (`test_dome.gpx`)
- **Description**: Gaussian dome shape (hill)
- **Expected Result**: Positive curvature, highest at peak, decreasing toward edges
- **Use Case**: Tests detection of convex surfaces
- **Grid**: 15×15 points, 3m spacing
- **Elevation**: Gaussian distribution (100-120m)

### 4. Valley/Bowl (`test_valley.gpx`)
- **Description**: Inverted dome (valley or bowl shape)
- **Expected Result**: Curvature pattern matching valley geometry
- **Use Case**: Tests detection of concave surfaces
- **Grid**: 15×15 points, 3m spacing
- **Elevation**: Inverted Gaussian (85-100m)

### 5. Ridge (`test_ridge.gpx`)
- **Description**: Linear ridge running through center
- **Expected Result**: High curvature along ridge line, lower elsewhere
- **Use Case**: Tests directional curvature detection
- **Grid**: 15×15 points, 3m spacing
- **Elevation**: Exponential drop-off from center line (100-112m)

### 6. Saddle Point (`test_saddle.gpx`)
- **Description**: Hyperbolic paraboloid (saddle shape)
- **Expected Result**: Complex curvature pattern - different curvature in different directions
- **Use Case**: Tests algorithm on surfaces with mixed curvature
- **Grid**: 15×15 points, 3m spacing
- **Elevation**: z = x² - y² function (69-131m)

### 7. Sine Wave (`test_sine_wave.gpx`)
- **Description**: Sinusoidal wave terrain
- **Expected Result**: Alternating high/low curvature at peaks and troughs
- **Use Case**: Tests periodic curvature patterns
- **Grid**: 20×20 points, 2m spacing
- **Elevation**: Sine wave pattern (90-110m)

### 8. Pyramid (`test_pyramid.gpx`)
- **Description**: Pyramid with sharp peak
- **Expected Result**: Very high curvature at apex, near-zero on flat faces
- **Use Case**: Tests algorithm on sharp features
- **Grid**: 15×15 points, 3m spacing
- **Elevation**: Linear decrease from center (100-123m)

### 9. Random Terrain (`test_random_terrain.gpx`)
- **Description**: Smoothly varying random terrain
- **Expected Result**: Variable curvature across different regions
- **Use Case**: Tests algorithm on realistic irregular terrain
- **Grid**: 12×12 points, 4m spacing
- **Elevation**: Smoothed random values (97-103m)

### 10. Step Terrain (`test_step_terrain.gpx`)
- **Description**: Terraced landscape with flat steps
- **Expected Result**: High curvature at step edges, zero on flat terraces
- **Use Case**: Tests algorithm on discontinuities and sharp transitions
- **Grid**: 15×15 points, 3m spacing
- **Elevation**: Three distinct levels (100, 110, 120m)

## Validation Strategy

For each test case:

1. **Visual Inspection**: Check that curvature heatmaps match expected patterns
2. **Statistical Analysis**: Verify curvature statistics (mean, min, max) align with geometry
3. **Boundary Handling**: Ensure boundary vertices are correctly identified and handled
4. **Extreme Cases**: Test both zero-curvature (planes) and high-curvature (pyramid apex) cases

## Known Limitations

- **Cubic Interpolation**: May fail on datasets with NaN boundary values. Use 'linear' interpolation for more robust results.
- **Percentile Normalization**: Feature noted as not working correctly in main README
- **Coordinate System**: All datasets use approximate coordinates around (31°N, 35°E) - Lebanon/Middle East region

## Customization

To create custom test datasets:

1. Edit `generate_test_gps_data.py`
2. Add new generator functions following existing patterns
3. Call your function in `main()`
4. Regenerate test data

## Analysis Options

When running tests with `test_curvature_with_synthetic_data.py`:

- **Interpolation Methods**:
  - `linear`: Recommended, more robust
  - `cubic`: Smoother but may fail with NaN boundaries

- **Normalization Modes**:
  - `normal`: Direct curvature values
  - `log`: Logarithmic scale (useful for wide ranges)
  - `percentile`: Clip to 5-95 percentile range
  - `clip`: Manually set maximum value

## File Format

All test files are standard GPX format with:
- Track points with latitude, longitude, elevation
- Timestamps (synthetic, for GPX validity)
- Proper GPX XML structure

## Output

Test results include:
- Curvature statistics (min, max, mean, median)
- Boundary vertex identification
- CSV export (`curvature_analysis_results.csv`)
- Multiple visualizations:
  - Curvature distribution histograms
  - Curvature profile by vertex
  - Vertex label map
  - Triangular mesh visualization
  - Voronoi diagram
  - Interpolated heatmap

## Tips

- Start with **Flat Plane** and **Tilted Plane** to validate zero-curvature detection
- Use **Dome** and **Valley** to verify basic curvature detection
- Test **Pyramid** to ensure algorithm handles sharp features
- Use **Random Terrain** for realistic scenario testing
- Compare results across different normalization modes to understand data range
