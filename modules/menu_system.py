"""
Menu system for mapping project - handles ONLY user interface logic
"""
import os
from .pipeline_controller import get_available_methods

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

def choose_method():
    """Let user choose interpolation method"""
    methods = get_available_methods()
    
    print("\nMethod Selection:")
    print("=" * 30)
    for i, (method_key, method_name) in enumerate(methods, 1):
        print(f"{i}. {method_name}")
    print(f"{len(methods) + 1}. Method Comparison")
    print(f"{len(methods) + 2}. Exit")
    
    while True:
        try:
            choice = int(input(f"\nSelect option (1-{len(methods) + 2}): "))
            if 1 <= choice <= len(methods):
                return methods[choice - 1][0], 'single'  # Return method key and type
            elif choice == len(methods) + 1:
                return None, 'comparison'  # Special case for comparison
            elif choice == len(methods) + 2:
                return None, 'exit'
            else:
                print(f"Please enter a number between 1 and {len(methods) + 2}")
        except ValueError:
            print("Please enter a valid number")

def choose_comparison_methods():
    """Let user choose which methods to compare"""
    methods = get_available_methods()
    
    print("\nSelect methods to compare:")
    for i, (method_key, method_name) in enumerate(methods, 1):
        print(f"{i}. {method_name}")
    print(f"{len(methods) + 1}. All available methods")
    
    while True:
        choice_input = input(f"Enter method numbers separated by commas (e.g., 1,2) or {len(methods) + 1} for all: ").strip()
        
        if choice_input == str(len(methods) + 1):
            return [method_key for method_key, _ in methods]
            
        try:
            choices = [int(x.strip()) for x in choice_input.split(',')]
            selected_methods = []
            
            for choice in choices:
                if 1 <= choice <= len(methods):
                    selected_methods.append(methods[choice - 1][0])
                else:
                    print(f"Invalid choice: {choice}")
                    break
            else:  # This runs if the loop completed without break
                return selected_methods
                
        except ValueError:
            print("Please enter valid numbers separated by commas")

def get_user_choices():
    """Get all user choices and return them"""
    print("Mapping Project - Interactive Pipeline")
    print("=" * 45)
    
    # Get method choice
    method, run_type = choose_method()
    
    if run_type == 'exit':
        return None, None, None, 'exit'
    
    # Get data source
    data_source, is_multiple = choose_data_source()
    
    if run_type == 'comparison':
        # For comparison, let user choose which methods to compare
        methods_to_compare = choose_comparison_methods()
        return methods_to_compare, data_source, is_multiple, 'comparison'
    
    return method, data_source, is_multiple, 'single'