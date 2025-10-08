"""
Test file for vertex curvature analysis
"""
import numpy as np
from modules.mapping_pipeline import MappingPipeline
from modules.curvature import compute_curvature

def main():
    print("="*80)
    print("CURVATURE ANALYSIS TEST")
    print("="*80)

    pipeline = MappingPipeline()

    # load GPS data
    print("\n[1/4] Loading GPS data...")
    gpx_file = 'Data/Track2_24_4_2025.gpx'
    pipeline.load_data(gpx_file, is_multiple=False)

    # preprocess data (normalize elevation and transform coordinates)
    print("\n[2/4] Preprocessing data...")
    pipeline.preprocess_data()

    # Build Delaunay triangulation mesh
    print("\n[3/4] Building Delaunay triangulation...")
    pipeline.create_triangulation()
    print(f"      Created {pipeline.num_triangles} triangles from {len(pipeline.points_2d)} vertices")

    # compute vertex curvature
    print("\n[4/4] Computing vertex curvature...")
    # Create 3D points array (x, y, z) to capture elevation
    points_3d = np.column_stack((pipeline.x, pipeline.y, pipeline.z))

    compute_curvature(points_3d, pipeline.triangulation.simplices)

    print("\n" + "="*80)
    print("CURVATURE ANALYSIS COMPLETE")
    print("="*80)

if __name__ == "__main__":
    main()
