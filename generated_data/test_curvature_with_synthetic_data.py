"""
Test curvature analysis with synthetic test data

This script allows you to easily test the curvature calculation
on synthetic test datasets with known geometric properties.
"""

import sys
from pathlib import Path

# Add parent directory to path to import modules
sys.path.insert(0, str(Path(__file__).parent.parent))

import numpy as np
from modules.data_processing import load_csv_meter_data
from modules.curvature import compute_curvature
from scipy.spatial import Delaunay


def list_test_files():
    """List all available test files"""
    # Get test_data directory relative to this script's location
    script_dir = Path(__file__).parent
    test_dir = script_dir / "test_data"
    if not test_dir.exists():
        print("Error: test_data directory not found!")
        print("Run 'python generate_test_gps_data.py' first to generate test data.")
        return []

    test_files = sorted(test_dir.glob("*.csv"))
    return test_files


def display_test_menu():
    """Display available test files and let user choose"""
    test_files = list_test_files()

    if not test_files:
        return None

    print("\n" + "="*65)
    print("SYNTHETIC GPS TEST DATA - CURVATURE ANALYSIS")
    print("="*65)
    print("\nAvailable test datasets:\n")

    for i, filepath in enumerate(test_files, 1):
        filename = filepath.stem.replace("test_", "").replace("_", " ").title()
        print(f"  {i}. {filename}")

    print("\n" + "-"*65)
    return test_files


def get_test_description(filename):
    """Return description of what to expect from each test case"""
    descriptions = {
        "test_flat_plane": "A perfectly flat horizontal surface. Should produce zero or near-zero curvature at all interior vertices.",

        "test_tilted_plane": "A tilted plane with constant slope. Should also produce zero curvature (plane is flat, just sloped).",

        "test_dome": "A Gaussian dome/hill shape. Should produce positive curvature, highest at the peak, decreasing toward edges.",

        "test_valley": "An inverted dome (bowl/valley). Should show curvature pattern matching the valley shape.",

        "test_ridge": "A linear ridge running through the center. Should show high curvature along the ridge line, lower elsewhere.",

        "test_saddle": "A saddle point (hyperbolic paraboloid). Should show interesting curvature behavior - positive curvature in one direction, different in the perpendicular direction.",

        "test_sine_wave": "A sinusoidal wave terrain. Should show alternating high/low curvature at peaks and troughs.",

        "test_pyramid": "A pyramid with a sharp peak. Should show very high curvature at the apex, near-zero on the flat faces.",

        "test_random_terrain": "Smoothly varying random terrain. Should show variable curvature across different regions.",

        "test_step_terrain": "Stepped terrain with flat terraces. Should show high curvature at step edges, zero curvature on flat terraces."
    }

    return descriptions.get(filename, "No description available.")


def run_curvature_analysis(csv_file, norm_mode='normal', vmax=None):
    """
    Run curvature analysis on a test file

    Args:
        csv_file: Path to CSV file with meter coordinates
        norm_mode: 'normal', 'log', 'percentile', or 'clip'
        vmax: Maximum value for 'clip' mode
    """
    print("\n" + "="*70)
    print("RUNNING CURVATURE ANALYSIS")
    print("="*70)

    print(f"\nTest file: {csv_file}")
    print(f"Normalization mode: {norm_mode}")
    if norm_mode == 'clip' and vmax is not None:
        print(f"Clip max value: {vmax}")

    # Get expected behavior
    filename = Path(csv_file).stem
    print(f"\n{'-'*70}")
    print("EXPECTED BEHAVIOR:")
    print(f"{'-'*70}")
    print(get_test_description(filename))
    print(f"{'-'*70}")

    # Load CSV data directly
    print("\n[1/3] Loading CSV data (meter coordinates)...")
    x, y, z = load_csv_meter_data(str(csv_file))
    print(f"      Loaded {len(x)} vertices")
    print(f"      X range: [{np.min(x):.2f}, {np.max(x):.2f}] m")
    print(f"      Y range: [{np.min(y):.2f}, {np.max(y):.2f}] m")
    print(f"      Z range: [{np.min(z):.2f}, {np.max(z):.2f}] m")

    # Build Delaunay triangulation
    print("\n[2/3] Building Delaunay triangulation...")
    points_2d = np.column_stack((x, y))
    triangulation = Delaunay(points_2d)
    print(f"      Created {len(triangulation.simplices)} triangles from {len(points_2d)} vertices")

    # Compute vertex curvature
    print("\n[3/3] Computing vertex curvature...")
    points_3d = np.column_stack((x, y, z))

    compute_curvature(points_3d, triangulation.simplices,
                     norm_mode=norm_mode,
                     vmax=vmax)

    print("\n" + "="*70)
    print("ANALYSIS COMPLETE")
    print("="*70)


def main():
    """Main interactive menu"""

    # Display menu
    test_files = display_test_menu()
    if not test_files:
        return

    while True:
        try:
            choice = input("\nEnter test number (or 'q' to quit): ").strip()

            if choice.lower() == 'q':
                print("Exiting...")
                break

            test_idx = int(choice) - 1
            if 0 <= test_idx < len(test_files):
                selected_file = test_files[test_idx]

                # Ask for analysis options
                print("\nAnalysis options:")
                print("  Normalization: 'normal', 'log', 'percentile', or 'clip'")

                norm = input("Normalization mode [normal]: ").strip() or 'normal'

                vmax = None
                if norm == 'clip':
                    vmax_input = input("Clip max value [1.0]: ").strip()
                    vmax = float(vmax_input) if vmax_input else 1.0

                # Run analysis
                run_curvature_analysis(selected_file, norm, vmax)

                # Ask if user wants to test another
                again = input("\nTest another dataset? (y/n): ").strip().lower()
                if again != 'y':
                    break
            else:
                print(f"Invalid choice. Please enter a number between 1 and {len(test_files)}.")

        except ValueError:
            print("Invalid input. Please enter a number.")
        except KeyboardInterrupt:
            print("\n\nExiting...")
            break
        except Exception as e:
            print(f"\nError: {e}")
            import traceback
            traceback.print_exc()


if __name__ == "__main__":
    main()
