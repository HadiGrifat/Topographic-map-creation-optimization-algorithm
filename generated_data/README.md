# Generated Test Data

This folder contains synthetic test datasets and tools for validating the curvature analysis algorithm.

## Contents

- **`generate_test_gps_data.py`**: Script to generate synthetic terrain data in CSV format
- **`test_curvature_with_synthetic_data.py`**: Interactive tool to test curvature analysis on synthetic datasets
- **`visualize_test_terrains.py`**: Visualize all test terrains in 3D and 2D heatmaps
- **`test_data/`**: Directory containing generated CSV test datasets

## Usage

### Generate Test Data
```bash
python generated_data/generate_test_gps_data.py
```

This creates 10 synthetic terrain datasets with known geometric properties:
- Flat plane (zero curvature expected)
- Tilted plane (zero curvature expected)
- Dome/hill (positive curvature at peak)
- Valley/bowl (curvature pattern)
- Ridge (high curvature along ridge line)
- Saddle point (complex curvature)
- Sine wave (alternating curvature)
- Pyramid (very high curvature at apex)
- Random terrain (variable curvature)
- Step terrain (high curvature at edges)

### Test Curvature Analysis
```bash
python generated_data/test_curvature_with_synthetic_data.py
```

This runs the full curvature analysis pipeline on selected test datasets and displays:
- Curvature statistics
- Boundary vertex detection
- Multiple visualizations (triangular mesh, Voronoi diagram, distributions, profiles)

### Visualize Test Terrains
```bash
python generated_data/visualize_test_terrains.py
```

Creates 3D surface plots and 2D heatmaps of all test terrains to understand their geometry before analysis.

## Test Data Format

All test data is stored as CSV files with the format:
```
# Test Name
# X(m), Y(m), Z(m)
0.0, 0.0, 100.0
5.0, 0.0, 100.0
...
```

Data is in pure meter coordinates (no GPS transformation) to avoid coordinate artifacts.
