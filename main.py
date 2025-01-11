from parser import *
from generationCode import *
from CompilerExecuter import *
from tokeniser import *
from error import *
from state import global_state


# Main function to parse input data, execute parsed instructions, and generate/compile C code.
#
# This function coordinates the parsing of input data, handles potential errors, executes valid
# instructions, and generates a C program based on the parsed data for further compilation and execution.
#
# Parameters:
# - None.
#
# Logic:
# 1. Initializes a parser instance using the yacc() function.
# 2. Parses the input data using the provided lexer with error tracking enabled.
# 3. Checks for errors in the global state:
#    - If errors are detected, exits the program with a status code of 1.
# 4. Processes the parsed data:
#    - Iterates through each statement in the parsed output.
#    - If a statement is executable (callable), it executes the statement directly.
#    - If a statement is invalid, writes an error message to the standard error stream and exits with status 1.
# 5. Calls external helper functions to:
#    - Generate a C file from the parsed data.
#    - Compile and execute the generated C program.
#
# Notes:
# - The function assumes the presence of global variables like `data`, `lexer`, `global_state`, and `parsed_data_c`.
# - Error handling ensures that invalid instructions are flagged and prevent further execution.
# - The `generate_c_code` and `compile_and_run_c` functions must be implemented separately to complete the workflow.
#
# Example Usage:
# This function is intended to be the entry point of a script. When executed, it parses and processes
# the input data, then generates and runs the corresponding C program.

def main():

    parser = yacc()
    parsed_data = parser.parse(data, lexer=lexer, tracking=True)
    

    if global_state.has_errors:
        sys.exit(1) 


    if parsed_data:
        for statement in parsed_data:
            if callable(statement):  # Check if the instruction is executable
                statement()  # Execution of instructions
            else:
                sys.stderr.write("Invalid instruction detected :", statement) 
                sys.exit(1) 
    # Générer le fichier C
    generate_c_code(parsed_data_c)
    compile_and_run_c()
    
    display_variables() # Checks the state of the variables after execution


# Entry point for the script execution.
#
# This block ensures that the `main()` function is called only when the script
# is executed directly, and not when it is imported as a module.
#
# Logic:
# 1. Checks if the script is being run as the main program by verifying the `__name__` variable.
# 2. Calls the `main()` function to execute the primary workflow of the script.
#
# Notes:
# - This construct allows the script to function as both a standalone program and an importable module.
#
# Example Usage:
# Run the script directly from the command line to trigger the `main()` function:
# python script_name.py
if __name__ == "__main__":
    main()
