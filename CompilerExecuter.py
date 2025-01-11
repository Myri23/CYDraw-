from subprocess import *
import sys

# Function to compile and run a C program.
#
# This function compiles a set of C source files into an executable binary using the GCC compiler
# and runs the generated executable. It manages the compilation and execution process within
# a specified directory containing the required SDL2 library and other dependencies.
#
# Parameters:
# - None.
#
# Logic:
# 1. Defines the source files and the output binary name.
# 2. Constructs a GCC command for compilation with the required libraries.
# 3. Executes the compilation command in the specified directory (`sdl_directory`).
# 4. Runs the compiled binary upon successful compilation.
# 5. Handles errors during compilation or execution by capturing and displaying error messages.
#
# Notes:
# - The function uses the `run` function from the `subprocess` module for system commands.
# - The `cwd` parameter specifies the directory where commands are executed.
# - Errors during the process are caught and printed for debugging purposes.
#
# Example Usage:
# compile_and_run_c()  # Compiles and runs the C program with the specified source files.
def compile_and_run_c():
    source_files = ["generated_code.c", "draw.c", "handle.c", "newcursor.c"] # List of source files to compile.
    binary_file = "exe"  # Name of the output executable file.
    sdl_directory = "./SDL" # Directory containing SDL library and related files.
    
    try:

        # Step 1: Construct the compilation command using GCC.
        compile_command = ["gcc", "-o", binary_file] + source_files + ["-lSDL2", "-lm"]
        print(f"Compilation of the generated code ...")

        # Step 2: Execute the compilation command in the specified directory.
        run(compile_command, check=True, capture_output=True, cwd=sdl_directory)        
        print("Compilation successful!")
        
        # Step 3: Run the compiled binary.
        print(f"Executing the code ...")
        run(f"./{binary_file}", shell=True, check=True,cwd=sdl_directory)
        print("Execution successful!")
        
    except CalledProcessError as e:
        # Step 4: Handle compilation or execution errors and print the error message.
        print("Error during compilation or execution:")
        print(e.stderr.decode())
        
    except Exception as e:
        # Step 5: Handle unexpected errors and display the error message.
        print("An unexpected error occurred:", e)
