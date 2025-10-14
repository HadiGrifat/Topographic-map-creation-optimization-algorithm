# Topographic Mapping Project

A GPS data processing and topographic mapping system that implements advanced geometric algorithms for creating terrain models from GPS survey data as well as run analytical report to determine the health and quality of the terrain models.

## Overview

This project transforms raw GPS data (.gpx files) into topographic maps using multiple interpolation methods and advanced Delaunay triangulation techniques.
In addition we use several analytical method to determine the quality of mapping process such as triangle fatness measure and curvature measure around the mesh vertices, a.k.a the GPS data points.



## Problems and Troubleshooting
# Cubic interpolation option not working in the curvature analytics path
likely due to the fact the scipy's interpolate function can not handle NaN values, which
we assign to boudnary vertices.
Not solved yet, possible solution:
- just don't use cubic options
- assigns 0 values to boundary vertices, which we did first. problem 0 curvature values implies flat area
- more complicated solution such as interpolating boundary curvature from nearby inner vertices
- calulcate the max angle for a each boundary vertex and calculate normalized curvature

# Percentile cutoff for curvature heatmap not working

## Contributing

This is an academic research project Done by Hadi Grifat

## References

1. **BoissonnatI.pdf** - Boissonnat, J.D., Oudot, S. "Provably Good Sampling and Meshing of Lipschitz Surfaces"
2. **DonohoOnMnfds.pdf** - Donoho, D.L. "Manifolds and Learning"
3. **JMIV-JournalVersion.pdf** - Saucan, E., Appleboim, E., Zeevi, Y.Y. "Sampling and Reconstruction of Surfaces and Higher Dimensional Manifolds" (Journal of Mathematical Imaging and Vision)
4. **LetcherSampling.pdf** - Letcher, A. "Sampling Theory for Surfaces"
5. **STSIP_JournalVersion.pdf** - "Sampling Theory for Signals and Images Processing" (Journal Version)
6. **UnCertaintySurvey.pdf** - Survey on Uncertainty in Geometric Computations
