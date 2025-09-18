"""
Menu system for mapping project - handles ONLY user interface logic
"""
import os

def get_available_gpx_files():
    """Scan Data folder for all .gpx files"""
    data_folder = 'Data'
    try:
        all_files = os.listdir(data_folder)
        gpx_files = [f for f in all_files if f.endswith('.gpx')]
        return [os.path.join(data_folder, f) for f in gpx_files]
    except FileNotFoundError:
        print(f"Error: {data_folder} folder not found!")
        return []

def choose_single_file():
    """Let user choose from all available GPX files"""
    gpx_files = get_available_gpx_files()
    
    if not gpx_files:
        print("No GPX files found in Data folder!")
        return None
        
    print(f"\nAvailable GPX files ({len(gpx_files)} found):")
    for i, file_path in enumerate(gpx_files, 1):
        filename = os.path.basename(file_path)  # Show just filename, not full path
        print(f"{i}. {filename}")
    
    while True:
        try:
            choice = int(input(f"Choose file (1-{len(gpx_files)}): "))
            if 1 <= choice <= len(gpx_files):
                return gpx_files[choice - 1]
            else:
                print(f"Please enter a number between 1 and {len(gpx_files)}")
        except ValueError:
            print("Please enter a valid number")

def choose_multiple_files():
    """Let user select multiple GPX files"""
    gpx_files = get_available_gpx_files()
    
    if not gpx_files:
        return []
        
    print(f"\nAvailable GPX files ({len(gpx_files)} found):")
    for i, file_path in enumerate(gpx_files, 1):
        filename = os.path.basename(file_path)
        print(f"{i}. {filename}")
    
    print(f"{len(gpx_files) + 1}. Select all files")
    
    while True:
        choice_input = input(f"Enter file numbers separated by commas (e.g., 1,3,5) or {len(gpx_files) + 1} for all: ").strip()
        
        if choice_input == str(len(gpx_files) + 1):
            return gpx_files
            
        try:
            choices = [int(x.strip()) for x in choice_input.split(',')]
            selected_files = []
            
            for choice in choices:
                if 1 <= choice <= len(gpx_files):
                    selected_files.append(gpx_files[choice - 1])
                else:
                    print(f"Invalid choice: {choice}")
                    break
            else:  # This runs if the loop completed without break
                return selected_files
                
        except ValueError:
            print("Please enter valid numbers separated by commas")

def choose_data_source():
    """Let user choose which files to process"""
    print("\nData Source Selection:")
    print("=" * 30)
    print("1. Single file")
    print("2. Multiple files")
    
    while True:
        choice = input("Choose data source (1-2): ").strip()
        
        if choice == '1':
            selected_file = choose_single_file()
            if selected_file:
                return selected_file, False
            else:
                return None, False
        elif choice == '2':
            selected_files = choose_multiple_files()
            if selected_files:
                return selected_files, True
            else:
                return None, True
        else:
            print("Invalid choice. Please enter 1 or 2.")

def choose_interpolation_method():
    """Let user choose specific interpolation method"""
    print("\nInterpolation Methods:")
    print("=" * 30)
    print("1. Linear Interpolation")
    print("2. Cubic Interpolation")
    print("3. Nearest Value Interpolation")

    while True:
        try:
            choice = int(input("\nSelect interpolation method (1-3): "))
            if choice == 1:
                return 'linear'
            elif choice == 2:
                return 'cubic'
            elif choice == 3:
                return 'nearest'
            else:
                print("Please enter a number between 1 and 3")
        except ValueError:
            print("Please enter a valid number")

def choose_delaunay_option():
    """Let user choose between mesh creation, analytics, or optimized solution for Delaunay triangulation"""
    print("\nDelaunay Triangulation Options:")
    print("=" * 40)
    print("1. Create Mesh (3D visualization)")
    print("2. Triangle Analytics (quality analysis)")
    print("3. Optimized Solution (Steiner points)")

    while True:
        try:
            choice = int(input("\nSelect option (1-3): "))
            if choice == 1:
                return 'delaunay_mesh'
            elif choice == 2:
                return 'delaunay_analytics'
            elif choice == 3:
                return 'delaunay_optimized'
            else:
                print("Please enter a number between 1 and 3")
        except ValueError:
            print("Please enter a valid number")

def choose_method():
    """Let user choose mapping method"""
    print("\nMethod Selection:")
    print("=" * 30)
    print("1. Interpolation")
    print("2. Delaunay Triangulation")
    print("3. Exit")

    while True:
        try:
            choice = int(input("\nSelect option (1-3): "))
            if choice == 1:
                # Show interpolation submenu
                return choose_interpolation_method()
            elif choice == 2:
                # Show Delaunay submenu
                return choose_delaunay_option()
            elif choice == 3:
                return None  # Exit
            else:
                print("Please enter a number between 1 and 3")
        except ValueError:
            print("Please enter a valid number")

def get_grid_size():
    """Get desired grid size from user"""
    while True:
        try:
            grid_size = int(input("\nEnter desired grid size (e.g., 20 for 20x20 grid): "))
            if grid_size > 0:
                return grid_size
            else:
                print("Grid size must be a positive number")
        except ValueError:
            print("Please enter a valid number")

def get_vertical_exaggeration():
    """Get vertical exaggeration factor from user"""
    print("\nVertical Exaggeration Settings:")
    print("=" * 35)
    print("• 1.0 = True scale (may appear flat)")
    print("• 3.0 = Realistic view (recommended)")
    print("• >10 = Dramatic exaggeration")
    
    while True:
        try:
            exaggeration = float(input("\nEnter vertical exaggeration factor (default: 3.0): ") or "3.0")
            if exaggeration > 0:
                return exaggeration
            else:
                print("Vertical exaggeration must be a positive number")
        except ValueError:
            print("Please enter a valid number")

def get_user_choices():
    """Get all user choices and return them"""
    print("Mapping Project - Interactive Pipeline")
    print("=" * 45)
    
    # Get method choice
    method = choose_method()
    
    if method is None:
        return None, None, None, None, None
    
    # Get data source
    data_source, is_multiple = choose_data_source()
    
    # Get grid size for interpolation methods only
    if method in ['linear', 'cubic', 'nearest']:
        grid_size = get_grid_size()
    else:
        grid_size = None  # Not needed for non-interpolation methods
    
    # Get vertical exaggeration for all 3D visualizations
    vertical_exaggeration = get_vertical_exaggeration()
    
    return method, data_source, is_multiple, grid_size, vertical_exaggeration