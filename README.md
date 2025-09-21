# Topographic Mapping Project

A comprehensive GPS data processing and topographic mapping system that implements advanced geometric algorithms for creating accurate terrain models from GPS survey data.

## Overview

This project transforms raw GPS data (.gpx files) into high-quality topographic maps using multiple interpolation methods and advanced Delaunay triangulation techniques.

### Key Features

- **Multiple Interpolation Methods**: Linear, cubic, and nearest-neighbor interpolation
- **Delaunay Triangulation**: Advanced mesh generation with quality analysis
- **Triangle Quality Assessment**: Fat triangulation analysis with visual feedback
- **Steiner Point Optimization**: Mesh refinement for improved accuracy
- **3D Visualization**: Interactive terrain models with customizable vertical exaggeration
- **Coordinate System Handling**: Automatic GPS to UTM coordinate transformation
- **Batch Processing**: Support for multiple GPX files

## Quick Start

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Mapping_Project
   ```

2. **Install dependencies**
   ```bash
   pip install numpy scipy matplotlib plotly os gpxpy pyproj
   ```

3. **Add your GPS data**
   - Place your `.gpx` files in the `Data/` folder
   - The system automatically detects and lists available files

4. **Run the application**
   ```bash
   python main.py
   ```

### Basic Usage

1. **Select your mapping method**:
   - `linear`, `cubic`, `nearest` - Interpolation-based mapping
   - `delaunay_mesh` - 3D triangular mesh visualization
   - `delaunay_analytics` - Geometric quality analysis
   - `delaunay_optimized` - Steiner point mesh refinement

2. **Choose your data source**:
   - Single GPX file or multiple files
   - System automatically lists available files in `Data/` folder

3. **Configure parameters**:
   - Grid size for interpolation (default: 20x20)
   - Vertical exaggeration for 3D plots (default: 3x)

## Project Structure

```
Mapping_Project/
├── main.py                     # Application entry point
├── README.md                   # Documentation
│
├── modules/                    # Core functionality
│   ├── menu_system.py         # User interface logic
│   ├── pipeline_controller.py # Workflow orchestration
│   ├── mapping_pipeline.py    # Main processing pipeline
│   ├── data_processing.py     # GPX loading and preprocessing
│   ├── interpolation.py       # Grid-based interpolation methods
│   ├── delaunay_triangulation.py # Triangulation algorithms
│   ├── analytics.py           # Geometric quality analysis
│   └── visualization.py       # 3D plotting and visualization
│
├── Data/                       # GPS data files (.gpx format)
├── Results/                    # Generated maps and analysis
└── legacy and testing/         # Archive and test files
```

## Technical Features

### Interpolation Methods

- **Linear Interpolation**: Fast, suitable for smooth terrain
- **Cubic Interpolation**: Higher accuracy for complex surfaces
- **Nearest Neighbor**: Preserves original data values

### Delaunay Triangulation

- **Quality Analysis**: Fat triangulation metrics (inradius/circumradius ratios)
- **Mesh Optimization**: Steiner point insertion at edge midpoints
- **Visual Assessment**: Color-coded triangle quality visualization

### Coordinate Systems

- **Input**: GPS coordinates (WGS84 latitude/longitude)
- **Processing**: UTM projection for metric calculations
- **Output**: Maintains spatial accuracy for survey applications

## Output Examples

### Interpolation Results
- **2D Contour Maps**: Elevation contours with GPS point overlay
- **3D Surface Plots**: Terrain visualization with customizable viewing angles
- **Statistical Reports**: Elevation ranges, interpolation accuracy metrics

### Triangulation Analysis
- **Mesh Visualization**: 3D triangular surface representation
- **Quality Assessment**: Triangle fatness analysis with color coding
- **Wireframe Views**: Structural mesh examination
- **Optimization Results**: Before/after Steiner point improvement

## Mathematical Foundation

This project implements algorithms based on research in geometric sampling theory:

- **Curvature-based sampling density**: Terrain complexity drives point requirements
- **Fat triangulation theory**: Quality metrics prevent numerical instability
- **Delaunay mesh properties**: Optimal angle bounds and surface approximation
- **Steiner point optimization**: Strategic point placement for mesh improvement


## Configuration

### Grid Parameters
- Adjust `grid_size` parameter (default: 20) for interpolation resolution
- Higher values = more detail, longer processing time but also oversmoothing

### Visualization Options
- `vertical_exaggeration`: Enhance terrain features (default: 3x)
added as initally matplotlib would stretch the z axis as the z delta 
would be smaller than the y,x delta and hence we would get exaggerated relif, hence
we fixed that by adding the ability to change the aspect ratio
- Multiple plot types: scatter, contour, surface, wireframe

### Data Processing
- Automatic elevation normalization (minimum = 0 meters)
- Coordinate transformation with proper UTM zone detection
- Multi-file processing for large survey areas

## Requirements and dependencies

- **Python**: 3.8 or higher
- **Core Libraries**:
  - `numpy` - Numerical computations
  - `scipy` - Scientific algorithms (Delaunay triangulation)
  - `matplotlib` - 2D plotting and visualization
  - `plotly` - Interactive 3D plots (optional)

## Troubleshooting

### Common Issues

**"No GPX files found"**
- Ensure `.gpx` files are in the `Data/` folder
- Check file extensions (must be `.gpx`, not `.GPX`)

## Contributing

This is an academic research project Done by Hadi Grifat

## References

- Saucan, E., Appleboim, E., Zeevi, Y.Y. (2008). "Sampling and Reconstruction of Surfaces and Higher Dimensional Manifolds"
- Boissonnat, J.D., Oudot, S. (2006). "Provably Good Sampling and Meshing of Lipschitz Surfaces"
- Classical Delaunay triangulation theory and applications
---