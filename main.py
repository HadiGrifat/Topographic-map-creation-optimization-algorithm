#!/usr/bin/env python3
"""
Main entry point for the mapping project
Coordinates between UI (menu_system) and business logic (pipeline_controller)
"""
from modules.menu_system import get_user_choices
from modules.pipeline_controller import run_pipeline, run_method_comparison

def main():
    """Main entry point - coordinates UI and business logic"""
    while True:
        # Get user choices from UI
        method_or_methods, data_source, is_multiple, run_type = get_user_choices()
        
        if run_type == 'exit':
            print("Goodbye!")
            break
        elif run_type == 'single':
            # Run single method
            success = run_pipeline(method_or_methods, data_source, is_multiple)
            if success:
                print("\nPipeline completed successfully!")
            else:
                print("\nPipeline failed. Please try again.")
        elif run_type == 'comparison':
            # Run method comparison
            results = run_method_comparison(data_source, is_multiple, method_or_methods)
            print(f"\nComparison completed. {sum(results.values())} out of {len(results)} methods succeeded.")
        
        # Ask if user wants to continue
        print("\n" + "="*50)
        continue_choice = input("Would you like to run another analysis? (y/n): ").strip().lower()
        if continue_choice not in ['y', 'yes']:
            print("Goodbye!")
            break

if __name__ == "__main__":
    main()