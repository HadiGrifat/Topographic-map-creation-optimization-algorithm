"""
Main entry point for the mapping project
Coordinates between UI (menu_system) and mapping logic (pipeline_controller)
"""
from modules.menu_system import get_user_choices
from modules.pipeline_controller import run_pipeline

def main():
    """Main entry point - coordinates UI and mapping logic"""
    while True:
        # Get user choices from UI
        method, data_source, is_multiple = get_user_choices()
        
        if method is None:
            print("Goodbye!")
            break
        
        # Run the selected method
        success = run_pipeline(method, data_source, is_multiple)
        if success:
            print("\nPipeline completed successfully!")
        else:
            print("\nPipeline failed. Please try again.")
        
        # Ask if user wants to continue
        print("\n" + "="*50)
        continue_choice = input("Would you like to run another analysis? (y/n): ").strip().lower()
        if continue_choice not in ['y', 'yes']:
            print("Goodbye!")
            break

if __name__ == "__main__":
    main()