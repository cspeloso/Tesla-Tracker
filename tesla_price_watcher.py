import subprocess
import sys
import os

def run_main_script():
    # Define the path to the main.py script
    main_script_path = os.path.join(os.path.dirname(__file__), 'Classes', 'main.py')

    # Run the main.py script and stream the output to the console
    process = subprocess.Popen([sys.executable, main_script_path], stdout=sys.stdout, stderr=sys.stderr)

    process.communicate()  # Wait for the process to complete

if __name__ == "__main__":
    run_main_script()