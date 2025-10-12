from modules.menu_system import get_user_choices
from modules.pipeline_controller import run_pipeline
import os

def clear_terminal():
    """Clears the terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear') # cls for Windows, clear for Unix

def main():
    """Main entry point - coordinates UI and mapping logic"""
    while True:
        clear_terminal()
        # Get user choices from UI
        method, data_source, is_multiple, grid_size, vertical_exaggeration, interpolation_method, norm_mode, vmax = get_user_choices()

        if method is None:
            print("Goodbye!")
            break

        # Run the selected method
        success = run_pipeline(method, data_source, is_multiple, grid_size, vertical_exaggeration,
                             interpolation_method, norm_mode, vmax)
        if success:
            print("\nAnalysis Completed!")
        else:
            print("\nCritical Failure")

        # Ask if user wants to continue
        print("\n" + "="*50)
        continue_choice = input("Would you like to run another analysis? (y/n): ").strip().lower()
        if continue_choice not in ['y', 'yes']:
            print("Goodbye!")
            break

if __name__ == "__main__":
    main()