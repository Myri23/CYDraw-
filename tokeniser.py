from ply.lex import *
from ply.yacc import *
import sys
from difflib import get_close_matches
from state import global_state

# Handling the input file from command-line arguments.
#
# This script processes an input file provided as a command-line argument. It verifies the
# correct usage, checks if the file exists, and reads its contents for further processing.
#
# Logic:
# 1. Verifies that exactly one argument is passed (the file path).
#    - If not, prints usage instructions and exits with an error code.
# 2. Attempts to open and read the specified file.
#    - If the file does not exist, prints an error message and exits with a different error code.
#
# Notes:
# - The script expects to be run as `python main.py <file>` where `<file>` is the path to the input file.
# - Error codes:
#   - `1`: Incorrect usage (missing or extra arguments).
#   - `2`: File not found.
#
# Example Usage:
# - Correct: `python main.py input.txt`
# - Incorrect: `python main.py` or `python main.py input.txt extra_arg`
if len(sys.argv) != 2:
    sys.stderr.write("Usage: python main.py <file>") # Inform the user of the correct usage.
    sys.exit(1) # Exit with an error code for incorrect usage.

file_path = sys.argv[1] # Retrieve the file path from command-line arguments.
try:
    # Attempt to open and read the specified file.
    with open(file_path, "r") as file:
        data = file.read() # Read the file's content into the `data` variable.
except FileNotFoundError:
    # Handle the case where the file does not exist.
    sys.stderr.write(f"Error: file '{file_path}' not found.") # Inform the user of the missing file.
    sys.exit(2) # Exit with an error code for a missing file.



# Functions for managing and analyzing lines in a text.
#
# These functions provide utilities to retrieve line information, including error-specific lines,
# line offsets, and line numbers based on character positions.
#
# Functions:
# 1. `find_error_line(data, line_offsets, pos)`: Retrieves the line containing an error based on a position.
# 2. `count_lines(data)`: Calculates and returns offsets for all lines in a given text.
# 3. `find_line(line_offsets, lexpos)`: Finds the line number corresponding to a specific character position.
#
# Parameters:
# - `data` (str): The input text to analyze.
# - `line_offsets` (list): A list of cumulative offsets for each line in the text.
# - `pos` (int): The character position to locate in the text.
# - `lexpos` (int): The character position for which the line number is needed.
#
# Logic:
# 1. `find_error_line`:
#    - Splits the text into lines and iterates to find the line containing the specified position.
#    - Returns the line number and content of the line containing the position.
# 2. `count_lines`:
#    - Computes cumulative offsets for each line and returns a list of offsets.
#    - Includes line endings in the offset calculations.
# 3. `find_line`:
#    - Compares a character position (`lexpos`) against the line offsets to determine the corresponding line number.
#
# Notes:
# - These functions are helpful for debugging or analyzing errors in textual data.
# - `find_error_line` and `find_line` depend on accurate offsets calculated by `count_lines`.
#
# Example Usage:
# text = "Line 1\nLine 2\nLine 3"
# offsets = count_lines(text)
# line_number, line_content = find_error_line(text, offsets, 10)  # Finds the line for position 10.
# line_num = find_line(offsets, 10)  # Finds the line number for position 10.

def find_error_line(data, line_offsets, pos):
    """
    Retrieve the specific line containing an error.

    Parameters:
    - data (str): The input text to analyze.
    - line_offsets (list): Precomputed list of line offsets in the text.
    - pos (int): The character position to locate in the text.

    Returns:
    - tuple: A tuple containing:
        - The line number (int) containing the error.
        - The content of the line (str) containing the error.
    """
    lines = data.splitlines()
    line_number = 0
    line_number = line_number
    line_offsets = line_offsets
    current_pos = 0
    
    for i, line in enumerate(lines):
        line_length = len(line) + 1  
        if current_pos <= pos < current_pos + line_length:
            return i + 1, line.strip()
        current_pos += line_length
    
    return len(lines), ""

def count_lines(data):
    """
    Calculate and return offsets for all lines in the text.

    Parameters:
    - data (str): The input text to analyze.

    Returns:
    - list: A list of cumulative offsets for each line in the text.
    """
    line_offsets = [0]
    current_offset = 0
    for line in data.splitlines(keepends=True):
        current_offset += len(line) + 1
        line_offsets.append(current_offset)
    return line_offsets

def find_line(line_offsets, lexpos):
    """
    Find the line number corresponding to a specific character position.

    Parameters:
    - line_offsets (list): Precomputed list of line offsets in the text.
    - lexpos (int): The character position to locate in the text.

    Returns:
    - int: The line number containing the character position.
    """
    for i, offset in enumerate(line_offsets):
        if lexpos < offset:
            return i + 1
    return len(line_offsets)

line_offsets = count_lines(data)


# Variable for Error detection
global_state.has_errors = False

# For the c code instructions
parsed_data_c = []

# Table of keywords
reserved = {
    'move': 'move',
    'draw': 'draw',
    'create': 'create',
    'cursor': 'cursor',
    'at': 'at',
    'with': 'with',
    'set': 'set',
    'thickness':'thickness',
    'color': 'color',
    'if': 'if',
    'then': 'then',
    'else': 'else',
    'while': 'while',
    'end': 'end',
    'for': 'for',
    'do': 'do',
    'in': 'in',
    'by': 'by',
    'rotate': 'rotate',
    'mode': 'mode',
    # Forms
    'circle': 'form',
    'filledcircle':'form',
    'square': 'form',
    'filledsquare':'form',
    'line': 'form',
    'arc':'arc',
    # animation mode
    'snail': 'animation',
    'bounce':'animation',
    'disco':'animation',
}

# Tokens list
tokens = (
    'number', 'comma', 'equal', 'id_cursor', 'id_number','plus','minus','greater','less', 
    'dividedby', 'modulo', 'times', 'form', 'lp', 'rp'
) + tuple(reserved.values())

# Regular expressions for simple tokens
t_equal = r'=' 
t_greater = r'>'
t_less = r'<'
t_comma = r','
t_plus = r'\+'
t_minus = r'\-'
t_times = r'\*'
t_dividedby = r'\/'
t_modulo = r'\%'
t_lp = r'\('
t_rp = r'\)'

# Ignore spaces and tabs
t_ignore = ' \t'

# To ignore empty or blank lines
t_ignore_comment = r'\#.*'

# Table of defined variables
variables_cursor = []
variables_number = {}

# Handles newlines and updates line number
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Token for numbers
def t_number(t):
    r'\d+'
    t.value = int(t.value) # Convert token to an integer
    return t

# Function to correct an incorrect keyword.
#
# This function attempts to find the closest match for a given word in a list of valid keywords.
# It uses a similarity algorithm to suggest a correction based on a predefined threshold.
#
# Parameters:
# - word (str): The word to be corrected.
# - word_list (list): A list of valid keywords to compare against.
#
# Logic:
# 1. Uses the `get_close_matches` function from the `difflib` module to find the closest match.
# 2. Returns the closest match if it meets the similarity threshold; otherwise, returns `None`.
#
# Notes:
# - The similarity threshold is defined by the `cutoff` parameter, set to 0.8 (80% similarity).
# - If no close match is found, the function gracefully handles it by returning `None`.
#
# Example Usage:
# keywords = ["for", "while", "if", "else", "return"]
# corrected_word = correct_keyword("fo", keywords)  # Returns "for" if similarity is above the cutoff.
# corrected_word = correct_keyword("loop", keywords)  # Returns None if no match is found.
def correct_keyword(word, word_list):
    close_matches = get_close_matches(word, word_list, n=1, cutoff=0.8)
    return close_matches[0] if close_matches else None

# Function to identify cursor variables, determine the type of other variables, and handle errors for unknown variables.
#
# This function is part of a lexer and is responsible for identifying tokens that represent
# variables, determining their type (e.g., cursor, number, or reserved keyword), and handling errors
# when the variable is unrecognized.
#
# Parameters:
# - t: A token object from the lexer containing the value and position of the current token.
#
# Logic:
# 1. Matches identifiers against reserved keywords.
# 2. Checks if the identifier is a known cursor or number variable.
# 3. For unknown variables:
#    - Analyzes the context after an `=` to determine if it represents a new cursor or number.
#    - If valid, assigns the correct type and appends it to the appropriate list.
#    - Otherwise, searches for a similar keyword and suggests corrections.
# 4. Handles lexical errors by displaying error messages with suggestions and marking the error state.
#
# Notes:
# - This function modifies global variables like `variables_cursor` and `global_state`.
# - Error messages include line numbers and suggestions for user correction.
#
# Example Usage:
# - As part of a lexer, this function is automatically called when the token regex matches.
# - Example: `t_id_cursor(t)` processes an identifier to determine if it's a cursor, number, or unknown variable.

def t_id_cursor(t):
    r'[a-zA-Z][a-zA-Z0-9_]*'
    if t.value in reserved:
        t.type = reserved[t.value]
        return t
    elif t.value in variables_cursor:
        t.type = 'id_cursor'
        return t
    elif t.value in variables_number:
        t.type = 'id_number'
        return t
    else:
        # Context verification after `=`
        next_pos = t.lexer.lexpos
        lexdata = t.lexer.lexdata
        if next_pos < len(lexdata) and lexdata[next_pos:].lstrip().startswith('='):
            equals_pos = lexdata.find('=', next_pos)
            if equals_pos != -1:
                after_equals = lexdata[equals_pos + 1:].lstrip()
                if after_equals.startswith('create cursor'):
                    variables_cursor.append(t.value)  # New cursor
                    t.type = 'id_cursor'
                    return t
                elif after_equals and after_equals[0].isdigit():
                    # calling `t_id_number` in a numerical context
                    return t_id_number(t)
        # Error handling

        # Check if the word is close to an existing keyword-
        closest_match = correct_keyword(t.value, reserved.keys())
        if closest_match:
            return t_error(t)
        line_number = find_line(line_offsets, t.lexpos)
        sys.stderr.write(f"Lexical error on line {line_number}: variable '{t.value}' not recognized.\n")
        sys.stderr.write(f"Suggestion: You need to assign a value such as a cursor or a number to a variable for it to be valid.\n")
        global_state.has_errors = True
        t.lexer.skip(len(t.value))

# Function to identify number variables, determine the type of other variables, and handle errors for unknown variables.
#
# This function is part of a lexer and is responsible for identifying tokens that represent
# numeric variables, checking their type, and handling errors for unrecognized variables.
#
# Parameters:
# - t: A token object from the lexer containing the value and position of the current token.
#
# Logic:
# 1. Matches identifiers against reserved keywords.
# 2. Checks if the identifier is a known cursor or number variable.
# 3. For unknown variables:
#    - Analyzes the context after an `=` to determine if it represents a new number or cursor variable.
#    - If valid, assigns the correct type and updates the corresponding global list.
#    - Otherwise, searches for a similar keyword and suggests corrections.
# 4. Handles lexical errors by displaying error messages with suggestions and marking the error state.
#
# Notes:
# - This function modifies global variables like `variables_number` and `global_state`.
# - Error messages include line numbers and suggestions for user correction.
#
# Example Usage:
# - As part of a lexer, this function is automatically called when the token regex matches.
# - Example: `t_id_number(t)` processes an identifier to determine if it's a number, cursor, or unknown variable.
def t_id_number(t):
    r'[a-zA-Z][a-zA-Z0-9_]*'
    if t.value in reserved:
        t.type = reserved[t.value]
        return t
    elif t.value in variables_cursor:
        t.type = 'id_cursor'
        return t
    elif t.value in variables_number:
        t.type = 'id_number'
        return t
    else:
        # context verification after `=`
        next_pos = t.lexer.lexpos
        lexdata = t.lexer.lexdata
        if next_pos < len(lexdata) and lexdata[next_pos:].lstrip().startswith('='):
            equals_pos = lexdata.find('=', next_pos)
            if equals_pos != -1:
                after_equals = lexdata[equals_pos + 1:].lstrip()
                if after_equals and after_equals[0].isdigit():
                    variables_number[t.value] = None  # New numeric variable
                    t.type = 'id_number'
                    return t
                elif after_equals.startswith('create cursor'):
                    # calling `t_id_cursor` in a cursor context
                    return t_id_cursor(t)
        # errors management 

        # Check if the word is similar to an existing keyword
        closest_match = correct_keyword(t.value, reserved.keys())
        if closest_match:
            return t_error(t)
        line_number = find_line(line_offsets, t.lexpos)
        sys.stderr.write(f"Lexical error on line {line_number}: variable '{t.value}' not recognized.\n")
        sys.stderr.write(f"Suggestion: You need to assign a value such as a cursor or a number to a variable for it to be valid.\n")

        global_state.has_errors = True
        t.lexer.skip(len(t.value))


# Token for specific forms.
#
# This function identifies tokens that match specific geometric or graphical forms.
# It uses a regular expression to match predefined shapes or forms.
#
# Parameters:
# - t: A token object from the lexer containing the value of the current token.
#
# Logic:
# 1. Matches the token against the specified forms: `circle`, `square`, `line`, `filledcircle`, `arc`, `filledsquare`.
# 2. If a match is found, the token is returned as-is.
#
# Notes:
# - This function assumes that the input will match one of the specified forms.
# - It is designed to work as part of a lexer that processes graphical or geometric instructions.
#
# Example Usage:
# - As part of a lexer, this function is automatically called when the token regex matches.
# - Example: If the input contains `circle`, this function identifies it as a valid form token.
def t_form(t):
    r'circle|square|line|filledcircle|arc|filledsquare'
    return t

# Function to handle lexical errors during tokenization.
#
# This function is invoked when an unrecognized character or token is encountered by the lexer.
# It attempts to correct the error by suggesting a replacement if a close match exists.
#
# Parameters:
# - t: A token object from the lexer containing the value and position of the current token.
#
# Logic:
# 1. Retrieves the line number of the error using the token's position (`lexpos`).
# 2. Searches for a close match to the erroneous token in the list of reserved keywords using `correct_keyword`.
# 3. If a match is found:
#    - Logs the error and the suggested correction.
#    - Replaces the token value with the suggested match and assigns the correct token type.
#    - Returns the corrected token to the lexer.
# 4. If no match is found:
#    - Logs the error and indicates that no correction is available.
#    - Skips the erroneous character in the lexer.
# 5. Marks the global error state (`global_state.has_errors`) as `True`.
#
# Notes:
# - This function modifies the token in place if a correction is applied.
# - The function uses global variables `line_offsets` and `global_state` for context and error tracking.
#
# Example Usage:
# - As part of a lexer, this function is automatically called when an unrecognized token is encountered. 
def t_error(t):

    """
    Handle lexical errors and suggest corrections for unrecognized tokens.

    Parameters:
    - t: The token object containing the erroneous character or token.

    Returns:
    - The corrected token if a match is found.
    - None: If no match is found, the erroneous character is skipped.
    """

    line_number = find_line(line_offsets, t.lexpos)
    closest_match = correct_keyword(t.value, reserved.keys())
    if closest_match:
        sys.stderr.write(f"Lexical error on line {line_number}: unrecognized character '{t.value[0]}'.\n")
        sys.stderr.write(f"Suggested correction: '{t.value}' replaced with '{closest_match}'.\n")

        t.value = closest_match  # Apply the correction
        t.type = reserved.get(closest_match, 'id')

        return t
    else:
        sys.stderr.write(f"Lexical error on line {line_number}, unrecognized character '{t.value[0]}'. No correction found.\n")

    global_state.has_errors = True
    t.lexer.skip(1)

# Utility function to resolve variable values.
#
# This function resolves a variable's value, handling both defined and undefined cases.
# If the value is a string corresponding to a known numeric variable, it retrieves the value.
# If the variable is undefined, an error message is logged, and the global error state is marked.
#
# Parameters:
# - value: The value to resolve, which can be a string (variable name) or a numeric value.
#
# Logic:
# 1. Checks if the input `value` is a string and exists in the `variables_number` dictionary.
#    - If found, returns the corresponding numeric value.
# 2. If the input is a string but not defined:
#    - Logs an error message with the line number and variable name.
#    - Marks the global error state as `True`.
#    - Returns an error message indicating that the variable is undefined.
# 3. If the input is already a number, it is returned as-is.
#
# Notes:
# - This function uses global variables such as `variables_number` and `line_offsets` for context.
# - Errors are logged to `stderr`, providing suggestions to define missing variables.
#
# Example Usage:
# - `resolve_value("x")` retrieves the value of `x` from `variables_number` if defined.
# - `resolve_value(42)` returns `42` as-is.
# - If `resolve_value("y")` is called and `y` is undefined, it logs an error and returns a message.
def resolve_value(value):

    """
    Resolve the value of a variable or return the numeric value directly.

    Parameters:
    - value: The input value to resolve. Can be a variable name (str) or a number.

    Returns:
    - The numeric value if the variable is defined or the input is already a number.
    - An error message if the variable is undefined.
    """

    if isinstance(value, str) and value in variables_number:
        return variables_number[value]
    elif isinstance(value, str):  # Undefined variable

        line_number = find_line(line_offsets, value.lexpos)
        sys.stderr.write(f"Error on line '{line_number}': variable '{value}' not defined.\n Please define '{value}' as a numeric variable.")
        global_state.has_errors = True  
        return f"Error on line '{line_number}': variable '{value}' not defined.\n Please define '{value}' as a numeric variable."
    return value  # If it is a number

# Lexer construction
lexer = lex()