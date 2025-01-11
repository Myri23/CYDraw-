from tokeniser import *
from state import global_state


# ----------------------------------------
# Definition of the PLY grammar (parser)
# ----------------------------------------

# Function to parse a program structure consisting of one or more statements.

# This function defines the grammar rules for parsing a program in a context-free grammar.
# The program can either consist of a single statement or multiple statements recursively.
# It constructs a list representation of the parsed program for further processing.

# Parameters:
# - p: A yacc parsing object containing tokens and their hierarchy.

# Logic:
# 1. Checks the length of p:
#    - If p has a length of 2, it represents a single statement. Assigns p[1] as the program (base case).
#    - If p has a length greater than 2, it represents a statement followed by another program.
#      Combines p[1] (the statement) with p[2] (the rest of the program) into a list (recursive case).
# 2. Assigns the constructed program structure to p[0].

# Notes:
# - The function leverages the parsing context `p` provided by the yacc parser.
# - Recursive definitions allow the program to parse sequences of statements seamlessly.

# Example Usage:
# When parsing "statement1; statement2;", the function builds a list structure like:
# ['statement1', 'statement2']

def p_program(p):
    '''program : statement
               | statement program'''
    if len(p) == 2:  # Base case: a single statement
        p[0] = [p[1]]
    else:  # Recursive case: a statement followed by a program
        p[0] = [p[1]] + p[2]

# Detects if the value is a number and assigns it directly
def p_number_or_id_number(p):
    'number_or_id : number'
    p[0] = p[1]

# Detects if the value is a variable containing a number and assigns its value.
def p_number_or_id_id(p):
    'number_or_id : id_number'
    p[0] = p[1]


# Function to parse and handle assignment statements with addition.

# This function processes statements of the form `<variable> = <variable> + <number>`.
# It defines the parsing logic and dynamically creates a function to execute the
# corresponding operation during runtime.

# Parameters:
# - p: A yacc parsing object containing tokens and parsing state.

# Logic:
# 1. Extracts the variable name to be assigned, the source variable to be added, and the increment value.
# 2. Defines a nested function `assign_expression_p` to perform the addition operation:
#    - Retrieves the value of the source variable from `variables_number` (or assumes 0 if it doesn't exist).
#    - Adds the increment to the source variable's value and assigns it to the target variable.
# 3. Assigns the nested function to `p[0]` so it can be executed later during runtime.

# Notes:
# - This function assumes the existence of a global `variables_number` dictionary to store variable values.
# - If the source variable does not exist in `variables_number`, its value is treated as 0.
# - The nested function structure allows deferred execution of the assignment logic.

# Example Usage:
# Input: `x = y + 5`
# Parsing generates a function that performs:
# `variables_number["x"] = variables_number.get("y", 0) + 5`

def p_statement_assign_expression_plus(p): 
    'statement : id_number equal id_number plus number'
    variable_name = p[1]
    source_variable = p[3]
    increment = p[5] 


    def assign_expression_p(variable_name=variable_name, source_variable=source_variable, increment=increment):
        variables_number[variable_name] = variables_number.get(source_variable, 0) + increment

    
    p[0] = assign_expression_p


# Function to parse and handle assignment statements with subtraction.

# This function processes statements of the form `<variable> = <variable> - <number>`.
# It defines the parsing logic and dynamically creates a function to execute the
# corresponding operation during runtime.

# Parameters:
# - p: A yacc parsing object containing tokens and parsing state.

# Logic:
# 1. Extracts the variable name to be assigned, the source variable to subtract from, and the decrement value.
# 2. Defines a nested function `assign_expression` to perform the subtraction operation:
#    - Retrieves the value of the source variable from `variables_number` (or assumes 0 if it doesn't exist).
#    - Subtracts the decrement value from the source variable's value and assigns it to the target variable.
# 3. Assigns the nested function to `p[0]` so it can be executed later during runtime.

# Notes:
# - This function assumes the existence of a global `variables_number` dictionary to store variable values.
# - If the source variable does not exist in `variables_number`, its value is treated as 0.
# - The nested function structure allows deferred execution of the assignment logic.

# Example Usage:
# Input: `x = y - 5`
# Parsing generates a function that performs:
# `variables_number["x"] = variables_number.get("y", 0) - 5`

def p_statement_assign_expression_minus(p): 
    'statement : id_number equal id_number minus number'
    variable_name = p[1]
    source_variable = p[3]
    increment = p[5] 

 
    def assign_expression(variable_name=variable_name, source_variable=source_variable, increment=increment):  
            variables_number[variable_name] = variables_number.get(source_variable, 0) - increment

    
    p[0] = assign_expression


# Function to parse and handle assignment statements with multiplication.

# This function processes statements of the form `<variable> = <variable> * <number>`.
# It defines the parsing logic and dynamically creates a function to execute the
# corresponding operation during runtime.

# Parameters:
# - p: A yacc parsing object containing tokens and parsing state.

# Logic:
# 1. Extracts the variable name to be assigned, the source variable to multiply, and the multiplier value.
# 2. Defines a nested function `assign_expression` to perform the multiplication operation:
#    - Retrieves the value of the source variable from `variables_number` (or assumes 0 if it doesn't exist).
#    - Multiplies the source variable's value by the multiplier and assigns the result to the target variable.
# 3. Assigns the nested function to `p[0]` so it can be executed later during runtime.

# Notes:
# - This function assumes the existence of a global `variables_number` dictionary to store variable values.
# - If the source variable does not exist in `variables_number`, its value is treated as 0.
# - The nested function structure allows deferred execution of the assignment logic.

# Example Usage:
# Input: `x = y * 5`
# Parsing generates a function that performs:
# `variables_number["x"] = variables_number.get("y", 0) * 5`

def p_statement_assign_expression_times(p): 
    'statement : id_number equal id_number times number'
    variable_name = p[1]
    source_variable = p[3]
    increment = p[5] 
 
    def assign_expression(variable_name=variable_name, source_variable=source_variable, increment=increment):  
            variables_number[variable_name] = variables_number.get(source_variable, 0) * increment

    
    p[0] = assign_expression


# Function to parse and handle assignment statements with division.

# This function processes statements of the form `<variable> = <variable> / <number>`.
# It defines the parsing logic, validates the divisor to prevent division by zero,
# and dynamically creates a function to execute the corresponding operation during runtime.

# Parameters:
# - p: A yacc parsing object containing tokens and parsing state.

# Logic:
# 1. Extracts the variable name to be assigned, the source variable to divide, and the divisor value.
# 2. Checks if the divisor (increment) is zero:
#    - If the divisor is zero, writes an error message to the standard error stream,
#      sets the global error state, and skips further processing.
# 3. Defines a nested function `assign_expression` to perform the division operation:
#    - Retrieves the value of the source variable from `variables_number` (or assumes 0 if it doesn't exist).
#    - Divides the source variable's value by the divisor and assigns the result to the target variable.
# 4. Assigns the nested function to `p[0]` so it can be executed later during runtime.

# Notes:
# - This function assumes the existence of a global `variables_number` dictionary to store variable values.
# - If the source variable does not exist in `variables_number`, its value is treated as 0.
# - Division by zero is explicitly checked and handled to prevent runtime errors.
# - The nested function structure allows deferred execution of the assignment logic.

# Example Usage:
# Input: `x = y / 5`
# Parsing generates a function that performs:
# `variables_number["x"] = variables_number.get("y", 0) / 5`

def p_statement_assign_expression_dividedby(p): 
    'statement : id_number equal id_number dividedby number'
    variable_name = p[1]
    source_variable = p[3]
    increment = p[5] 
    
    if increment == 0:
        sys.stderr.write("Error: You can't divide by 0")
        global_state.has_errors = True
    else :
 
        def assign_expression(variable_name=variable_name, source_variable=source_variable, increment=increment): 
            variables_number[variable_name] = variables_number.get(source_variable, 0) / increment

    
        p[0] = assign_expression


# Function to parse and handle assignment statements with modulo operation.

# This function processes statements of the form `<variable> = <variable> % <number>`.
# It defines the parsing logic, validates the divisor to prevent modulo by zero,
# and dynamically creates a function to execute the corresponding operation during runtime.

# Parameters:
# - p: A yacc parsing object containing tokens and parsing state.

# Logic:
# 1. Extracts the variable name to be assigned, the source variable, and the divisor value.
# 2. Checks if the divisor (increment) is zero:
#    - If the divisor is zero, writes an error message to the standard error stream,
#      sets the global error state, and skips further processing.
# 3. Defines a nested function `assign_expression` to perform the modulo operation:
#    - Retrieves the value of the source variable from `variables_number` (or assumes 0 if it doesn't exist).
#    - Computes the modulo of the source variable's value with the divisor and assigns the result to the target variable.
# 4. Assigns the nested function to `p[0]` so it can be executed later during runtime.

# Notes:
# - This function assumes the existence of a global `variables_number` dictionary to store variable values.
# - If the source variable does not exist in `variables_number`, its value is treated as 0.
# - Modulo by zero is explicitly checked and handled to prevent runtime errors.
# - The nested function structure allows deferred execution of the assignment logic.

# Example Usage:
# Input: `x = y % 5`
# Parsing generates a function that performs:
# `variables_number["x"] = variables_number.get("y", 0) % 5`

def p_statement_assign_expression_modulo(p): 
    'statement : id_number equal id_number modulo number'
    variable_name = p[1]
    source_variable = p[3]
    increment = p[5] 

    if increment == 0 :
        sys.stderr.write("Error: '%' cannot be followed by zero")
        global_state.has_errors = True
    else: 

        def assign_expression(variable_name=variable_name, source_variable=source_variable, increment=increment):  
            variables_number[variable_name] = variables_number.get(source_variable, 0) % increment


        p[0] = assign_expression


# Function to display the current states of global variables.

# This function iterates over the global dictionaries `variables_number` and `variables_cursor`
# to display the current state of numeric variables and cursor variables in the system.

# Parameters:
# - None.

# Logic:
# 1. Iterates through `variables_number`:
#    - Prints each variable name and its associated value in the format `<variable> = <value>`.
# 2. Iterates through `variables_cursor`:
#    - Prints each cursor variable name.

# Notes:
# - Assumes the existence of global dictionaries `variables_number` and `variables_cursor`.
# - The function directly outputs the variable states to the standard output.

# Example Usage:
# If `variables_number` contains `{"x": 5, "y": 10}` and `variables_cursor` contains `["cursor1", "cursor2"]`,
# the function outputs:
# ```
# x = 5
# y = 10
# cursor1
# cursor2
# ```
 
def display_variables():
    for var, val in variables_number.items():
        print(f"{var} = {val}")
    for var in variables_cursor:
        print(f"{var}")


# Function to parse and handle simple variable assignments.

# This function processes statements of the form `<variable> = <value>`.
# It assigns the given value (or the value of another variable) to the specified variable
# and dynamically creates an action to display the assignment during runtime.

# Parameters:
# - p: A yacc parsing object containing tokens and parsing state.

# Logic:
# 1. Extracts the target variable name and the value (or another variable's value) from the parsing object.
# 2. Assigns the value to the target variable in the global `variables_number` dictionary.
# 3. Defines a nested function `assign_action` to display the assignment during runtime:
#    - Outputs a message indicating the variable name and its assigned value.
# 4. Assigns the nested function to `p[0]` for deferred execution.

# Notes:
# - This function assumes the existence of a global `variables_number` dictionary to store variable values.
# - The nested function structure allows the assignment action to be executed later during runtime.

# Example Usage:
# Input: `x = 10`
# Parsing generates a function that performs:
# `variables_number["x"] = 10` and displays: `Variable 'x' defined with the value 10`.

def p_statement_assign_number(p):
    'statement : id_number equal number_or_id'
    variable_name = p[1]
    value = p[3]
    variables_number[variable_name] = value

    def assign_action(variable_name=variable_name, value=value):    
        variable_name=variable_name
        value=value


    p[0] = assign_action


# Function to parse and handle cursor movement statements.
#
# This function processes statements of the form `move <cursor> by <distance>`.
# It resolves the distance value, creates a C instruction for moving the cursor,
# and dynamically creates an action to append the instruction to the parsed data during runtime.
#
# Parameters:
# - p: A yacc parsing object containing tokens and parsing state.
#
# Logic:
# 1. Extracts the cursor identifier and the distance value from the parsing object.
# 2. Resolves the distance value using the `resolve_value` function to handle variables or constants.
# 3. Defines a nested function `move_action` to:
#    - Generate a C instruction for moving the cursor using the format:
#      `moveCursor(&<cursor_id>, <distance_value>);`
#    - Append the generated instruction to the `parsed_data_c` list.
# 4. Assigns the nested function to `p[0]` for deferred execution.
#
# Notes:
# - This function assumes the existence of a global `parsed_data_c` list to store C instructions.
# - The `resolve_value` function must handle variables and constants properly to compute the distance value.
# - The nested function structure allows deferred execution of the movement logic.
#
# Example Usage:
# Input: `move cursor1 by 10`
# Parsing generates a function that appends:
# `moveCursor(&cursor1, 10);` to `parsed_data_c`.

def p_statement_movement(p):
    '''
    statement : move id_cursor by number_or_id
    '''
    cursor_id = p[2]
    distance_value = resolve_value(p[4])

    def move_action():
        instruction_c = f"moveCursor(&{cursor_id},{distance_value});"
        parsed_data_c.append(instruction_c)
    
    p[0] = move_action


# Function to parse and handle cursor thickness changing statements.
#
# This function processes statements of the form `set <cursor> thickness at <value>`.
# It resolves the thickness value, creates a C instruction for setting the cursor's thickness,
# and dynamically creates an action to append the instruction to the parsed data during runtime.
#
# Parameters:
# - p: A yacc parsing object containing tokens and parsing state.
#
# Logic:
# 1. Extracts the cursor identifier and the thickness value from the parsing object.
# 2. Resolves the thickness value using the `resolve_value` function to handle variables or constants.
# 3. Defines a nested function `thickness_action` to:
#    - Generate a C instruction for changing the cursor's thickness using the format:
#      `setThickness(&<cursor_id>, <thickness_value>);`
#    - Append the generated instruction to the `parsed_data_c` list.
# 4. Assigns the nested function to `p[0]` for deferred execution.
#
# Notes:
# - This function assumes the existence of a global `parsed_data_c` list to store C instructions.
# - The `resolve_value` function must handle variables and constants properly to compute the thickness value.
# - The nested function structure allows deferred execution of the thickness-changing logic.
#
# Example Usage:
# Input: `set cursor1 thickness at 5`
# Parsing generates a function that appends:
# `setThickness(&cursor1, 5);` to `parsed_data_c`.

def p_statement_thickness_changing(p):
    '''
    statement : set id_cursor thickness at number_or_id
    '''
    cursor_id = p[2]
    thickness_value = resolve_value(p[5])

    def thickness_action():
        instruction_c = f"setThickness(&{cursor_id},{thickness_value});"
        parsed_data_c.append(instruction_c)
    
    p[0] = thickness_action


# Function to parse and handle cursor creation statements.

# This function processes statements of the form:
# `<cursor_id> = create cursor at (<x>, <y>) with (<r1>, <g1>, <b1>, <r2>, <g2>, <b2>, <thickness>, <visibility>)`.
# It resolves all parameters, ensures the cursor is tracked, and generates the necessary
# action to create the cursor in the parsed data.

# Parameters:
# - p: A yacc parsing object containing tokens and parsing state.

# Logic:
# 1. Extracts the cursor ID and ensures it is added to the `variables_cursor` list if not already present.
# 2. Resolves all positional and configuration parameters using the `resolve_value` function:
#    - Coordinates: `coord_x` and `coord_y`
#    - RGB color components: `rgb_1`, `rgb_2`, `rgb_3`, and `rgb_4`
#    - Thickness: `thickness`
#    - Visibility: `visibility`
# 3. These resolved parameters can be used to generate corresponding C code or handle additional logic in a later step.

# Notes:
# - This function assumes the existence of:
#   - A global `variables_cursor` list to track cursor identifiers.
#   - A `resolve_value` function to handle variables or constants for parameter resolution.
# - The actual action to append the instruction (e.g., to `parsed_data_c`) is not yet included in this function.

# Example Usage:
# Input: `cursor1 = create cursor at (10, 20) with (255, 0, 0, 0, 255, 0, 5, 1)`
# Parsing resolves the parameters and ensures `cursor1` is tracked in `variables_cursor`.

def p_statement_creation_cursor(p):
    '''
    statement : id_cursor equal create cursor at lp number_or_id comma number_or_id rp with lp number_or_id comma number_or_id comma number_or_id comma number_or_id comma number_or_id comma number_or_id rp
    '''
    cursor_id = p[1]
    if cursor_id not in variables_cursor:
        variables_cursor.append(cursor_id)

    # Resolving parameters with possible mix
    coord_x = resolve_value(p[7])
    coord_y = resolve_value(p[9])
    rgb_1 = resolve_value(p[13])
    rgb_2 = resolve_value(p[15])
    rgb_3 = resolve_value(p[17])
    rgb_4 = resolve_value(p[19])
    thickness = resolve_value(p[21])
    visibility = resolve_value(p[23])

    # Action to execute
    def create_cursor_action():
        instruction_c = (
            f"Cursor {cursor_id} = createCursor({coord_x}, {coord_y}, (SDL_Color){{{rgb_1}, {rgb_2}, {rgb_3}, {rgb_4}}}, {thickness}, {visibility});"
        )
        parsed_data_c.append(instruction_c)

    p[0] = create_cursor_action


# Function to parse and handle shape drawing statements (excluding arcs).
#
# This function processes statements of the form:
# `draw (<shape>, <size>) with <cursor>`, where the shape can be a circle, square,
# line, filled square, or filled circle. It resolves the size, determines the shape type,
# and generates the corresponding C instruction for drawing.
#
# Parameters:
# - p: A yacc parsing object containing tokens and parsing state.
#
# Logic:
# 1. Extracts the shape type, size parameter, and cursor identifier from the parsing object.
# 2. Defines a nested function `draw_action_not_arc` to:
#    - Resolve the size parameter using the `resolve_value` function.
#    - Generate a C instruction for the specified shape and size using the corresponding function:
#      - `drawCircle`, `drawSquare`, `drawLine`, `drawFilledSquare`, or `drawFilledCircle`.
#    - Append the generated C instruction to the `parsed_data_c` list.
# 3. Assigns the nested function to `p[0]` for deferred execution.
#
# Notes:
# - This function assumes the existence of:
#   - A global `parsed_data_c` list to store C instructions.
#   - A `resolve_value` function to handle variables or constants for size resolution.
# - The function supports a variety of shapes, each mapped to a specific C function.
# - The nested function structure allows deferred execution of the drawing logic.
#
# Example Usage:
# Input: `draw (circle, 10) with cursor1`
# Parsing generates a function that appends:
# `drawCircle(renderer, &cursor1, 10); // Draw a circle` to `parsed_data_c`.

def p_statement_drawing_not_arc(p):
    'statement : draw lp form comma number_or_id rp with id_cursor'
    form = p[3]  # Type of shape (circle, square, line)
    size = p[5]  # Parameter associated with the shape (radius or size)
    cursor_id = p[8]  # Cursor identifier to use  
 
    def draw_action_not_arc(form=form, size=size, cursor_id=cursor_id):
        
        current_size = resolve_value(size)

        if form == 'circle':
            instruction_c = f'drawCircle(renderer, &{cursor_id}, {current_size}); // Draw a circle'
        elif form == 'square':
            current_size = resolve_value(size)
            instruction_c = f'drawSquare(renderer, &{cursor_id}, {current_size}); // Draw a square'
        elif form == 'line':
            instruction_c = f'drawLine(renderer, &{cursor_id}, {current_size}); // Draw a line'
        elif form == 'filledsquare':
            instruction_c = f'drawFilledSquare(renderer, &{cursor_id}, {current_size}); // Draw a filled square'
        elif form == 'filledcircle':
            instruction_c = f'drawFilledCircle(renderer, &{cursor_id}, {current_size}); // Draw a filled circle'
        parsed_data_c.append(instruction_c)

    p[0] = draw_action_not_arc  


# Function to parse and handle arc drawing statements.
#
# This function processes statements of the form:
# `draw (arc, <size>, <start_angle>, <end_angle>) with <cursor>`.
# It resolves the size, start angle, end angle, and cursor identifier,
# and generates the corresponding C instruction for drawing the arc.
#
# Parameters:
# - p: A yacc parsing object containing tokens and parsing state.
#
# Logic:
# 1. Extracts and resolves the parameters from the parsing object:
#    - `size`: The size (e.g., radius) of the arc.
#    - `start_angle`: The starting angle of the arc in degrees.
#    - `end_angle`: The ending angle of the arc in degrees.
#    - `cursor_id`: The cursor identifier to use.
# 2. Defines a nested function `draw_action_arc` to:
#    - Generate a C instruction for drawing the arc using the format:
#      `drawArc(renderer, &<cursor_id>, <size>, <start_angle>, <end_angle>);`
#    - Append the generated instruction to the `parsed_data_c` list.
# 3. Assigns the nested function to `p[0]` for deferred execution.
#
# Notes:
# - This function assumes the existence of:
#   - A global `parsed_data_c` list to store C instructions.
#   - A `resolve_value` function to handle variables or constants for parameter resolution.
# - The nested function structure allows deferred execution of the arc drawing logic.
#
# Example Usage:
# Input: `draw (arc, 50, 0, 90) with cursor1`
# Parsing generates a function that appends:
# `drawArc(renderer, &cursor1, 50, 0, 90);` to `parsed_data_c`.

def p_statement_drawing_arc(p):
    'statement : draw lp arc comma number_or_id comma number_or_id comma number_or_id rp with id_cursor'
    size = resolve_value(p[5])
    start_angle = resolve_value(p[7])
    end_angle = resolve_value(p[9])
    cursor_id = resolve_value(p[12])
    
    def draw_action_arc():
        instruction_c = f'drawArc(renderer, &{cursor_id}, {size}, {start_angle}, {end_angle});'
        parsed_data_c.append(instruction_c)
    
    p[0] = draw_action_arc

# Function to parse and handle animation mode statements.

# This function processes statements of the form:
# `mode <animation>`, where `<animation>` specifies the type of animation to apply.
# It determines the animation type, generates the corresponding C instruction,
# and dynamically creates an action to append the instruction to the parsed data during runtime.

# Parameters:
# - p: A yacc parsing object containing tokens and parsing state.

# Logic:
# 1. Extracts the animation type from the parsing object.
# 2. Defines a nested function `animation_mode` to:
#    - Generate a C instruction for the specified animation type:
#      - `'snail'` => `animateDrawingsnail(renderer);`
#      - `'bounce'` => `animateDrawingbond(renderer);`
#      - `'disco'` => `animateRotation2(renderer);`
#    - Append the generated instruction to the `parsed_data_c` list.
# 3. Assigns the nested function to `p[0]` for deferred execution.

# Notes:
# - This function assumes the existence of a global `parsed_data_c` list to store C instructions.
# - The nested function structure allows deferred execution of the animation logic.

# Example Usage:
# Input: `mode snail`
# Parsing generates a function that appends:
# `animateDrawingsnail(renderer);` to `parsed_data_c`.

def p_statement_animation_mode(p):
    'statement : mode animation'
    animation = p[2]
    
    def animation_mode() :
        if animation == 'snail':
            instruction_c = f'animateDrawingsnail(renderer);'
        elif animation == 'bounce':
            instruction_c = f'animateDrawingbond(renderer);'
        elif animation == 'disco':
            instruction_c = f'animateRotation2(renderer);'
            
        parsed_data_c.append(instruction_c)
        
    p[0] = animation_mode

# Function to parse and handle cursor rotation statements.

# This function processes statements of the form:
# `rotate <cursor> by <angle>`, where `<cursor>` is the cursor to rotate, and `<angle>` specifies the rotation angle.
# It resolves the rotation angle, generates the corresponding C instruction,
# and dynamically creates an action to append the instruction to the parsed data during runtime.

# Parameters:
# - p: A yacc parsing object containing tokens and parsing state.

# Logic:
# 1. Extracts the cursor name and rotation angle from the parsing object.
# 2. Resolves the angle using the `resolve_value` function to handle variables or constants.
# 3. Defines a nested function `rotation_action` to:
#    - Generate a C instruction for rotating the cursor using the format:
#      `rotateCursor(&<cursor_name>, <angle>);`
#    - Append the generated instruction to the `parsed_data_c` list.
# 4. Assigns the nested function to `p[0]` for deferred execution.

# Notes:
# - This function assumes the existence of:
#   - A global `parsed_data_c` list to store C instructions.
#   - A `resolve_value` function to handle variables or constants for angle resolution.
# - The nested function structure allows deferred execution of the rotation logic.

# Example Usage:
# Input: `rotate cursor1 by 90`
# Parsing generates a function that appends:
# `rotateCursor(&cursor1, 90);` to `parsed_data_c`.

def p_statement_rotation(p):
    'statement : rotate id_cursor by number_or_id'

    cursor_name = p[2]
    angle = resolve_value(p[4])

    def rotation_action():
        instruction_c = f'rotateCursor(&{cursor_name},{angle});'
        parsed_data_c.append(instruction_c)
    
    p[0] = rotation_action


# Function to parse and handle conditions in statements.

# This function processes conditions of the form:
# `<variable> <operator> <value>`, where `<operator>` can be `<`, `>`, or `=`.
# It resolves the variable and value, and dynamically creates a function to evaluate the condition during runtime.
#
# Parameters:
# - p: A yacc parsing object containing tokens and parsing state.
#
# Logic:
# 1. Extracts the components of the condition from the parsing object:
#    - `variable_name`: The name of the variable to evaluate.
#    - `operator`: The comparison operator (`<`, `>`, or `=`).
#    - `value`: The numeric value to compare against.
# 2. Defines a nested function `condition` to:
#    - Evaluate the condition based on the operator:
#      - `<`: Returns `True` if the variable's value is less than the specified value.
#      - `>`: Returns `True` if the variable's value is greater than the specified value.
#      - `=`: Returns `True` if the variable's value is equal to the specified value.
#    - If the variable does not exist in `variables_number`, its value is treated as 0.
# 3. Prints the condition for debugging purposes.
# 4. Assigns the nested function to `p[0]` for deferred execution.

# Notes:
# - This function assumes the existence of a global `variables_number` dictionary to store variable values.
# - The nested function structure allows deferred execution and evaluation of the condition logic.

# Example Usage:
# Input: `x < 10`
# Parsing generates a function that evaluates:
# `variables_number.get("x", 0) < 10`
# Output: `True` or `False` based on the condition.

def p_condition(p):
    '''condition : number_or_id less number_or_id
                 | number_or_id greater number_or_id
                 | number_or_id equal number_or_id'''
    variable_name = p[1]  # Capture the variable name
    operator = p[2]       # Capture the operator (<, >, =)
    value = p[3]          # Capture the numeric value

    # Define a callable function to evaluate the condition
    def condition():
        if operator == '<':
            return variables_number.get(variable_name, 0) < value
        elif operator == '>':
            return variables_number.get(variable_name, 0) > value
        elif operator == '=':
            return variables_number.get(variable_name, 0) == value

    p[0] = condition


# Function to parse and handle conditional statements.

# This function processes conditional statements of the form:
# `if <condition> then <program> end` or 
# `if <condition> then <program> else <program> end`.
# It evaluates the condition and executes the appropriate block of statements during runtime.

# Parameters:
# - p: A yacc parsing object containing tokens and parsing state.

# Logic:
# 1. Extracts the condition function and program blocks (then/else) from the parsing object:
#    - `condition_func`: A callable function to evaluate the condition.
#    - `then_block`: A list of statements to execute if the condition is true.
#    - `else_block`: A list of statements to execute if the condition is false (optional).
# 2. Defines a nested function `condition_action` to:
#    - Evaluate the condition using `condition_func()`.
#    - Execute the `then_block` if the condition is true.
#    - If the condition is false and an `else_block` exists, execute the `else_block`.
#    - Each statement in the block is executed only if it is callable.
# 3. Assigns the nested function to `p[0]` for deferred execution.

# Notes:
# - This function assumes that program blocks are lists of callable functions.
# - The nested function structure allows deferred execution of the conditional logic.

# Example Usage:
# Input: 
# ```
# if x < 10 then
#     y = y + 1
# else
#     z = z - 1
# end
# ```
# Parsing generates a function that evaluates `x < 10` and executes the appropriate block.

def p_statement_condition(p):
    '''statement : if condition then program end
                 | if condition then program else program end'''
    
    condition_func = p[2]  # Retrieve the condition function

    if len(p) == 6:  # Case without else
        then_block = p[4]
        def condition_action():
            if condition_func():  # Explicite call to the function to evaluate the condition

                for statement in then_block:
                    if callable(statement):
                        statement()


    else:  # Case with else
        then_block = p[4]
        else_block = p[6]
        def condition_action():
            if condition_func():  # Explicite call to the function to evaluate the condition

                for statement in then_block:
                    if callable(statement):
                        statement()
            else:

                for statement in else_block:
                    if callable(statement):
                        statement()

    p[0] = condition_action


# Function to parse and handle 'for' loop statements.

# This function processes statements of the form:
# `for <variable> in (<start>, <end>) do <program> end`.
# It resolves the start and end values, executes the loop body for each iteration,
# and dynamically creates a function to handle the loop execution during runtime.

# Parameters:
# - p: A yacc parsing object containing tokens and parsing state.

# Logic:
# 1. Extracts the loop variable, range boundaries (start and end), and the loop body from the parsing object.
# 2. Resolves the start and end values using the `resolve_value` function.
# 3. Prints debugging information to indicate the start and progress of the loop.
# 4. Defines a nested function `execute_loop` to:
#    - Iterate over the range [start, end] (inclusive).
#    - Assign the current iteration value to the loop variable in `variables_number`.
#    - Execute each statement in the loop body for the current iteration.
#    - Print debugging information for each iteration and upon loop completion.
# 5. Assigns the nested function to `p[0]` for deferred execution.

# Notes:
# - This function assumes the existence of:
#   - A global `variables_number` dictionary to store variable values.
#   - A `resolve_value` function to handle variables or constants for range resolution.
#   - A loop body (`program`) that is a list of callable functions.
# - The nested function structure allows deferred execution of the loop logic.

# Example Usage:
# Input:
# ```
# for i in (1, 5) do
#     print(i)
# end
# ```
# Parsing generates a function that executes the loop and prints:
# ```
# Beginning of the loop for: i from 1 to 5
# Iteration 1: Start executing the instructions.
# Iteration 2: Start executing the instructions.
# ...
# Fin de la boucle for
# ```

def p_statement_loop(p):
    'statement : for id_number in lp number_or_id comma number_or_id rp do program end'
    loop_var = p[2]
    start, end, body = resolve_value(p[5]), resolve_value(p[7]), p[10]

    for i in range(start, end + 1):
        variables_number[loop_var] = i

        for stmt in body:
            stmt()
 
    def execute_loop():

        for i in range(start, end + 1):
            variables_number[loop_var] = i

            for stmt in body:
                stmt()

    p[0] = execute_loop


# Function to parse and handle 'while' loop statements.
#
# This function processes statements of the form:
# `while <condition> do <program> end`.
# It evaluates the condition, and as long as the condition evaluates to `True`,
# it executes the loop body. The loop terminates when the condition becomes `False`.
#
# Parameters:
# - p: A yacc parsing object containing tokens and parsing state.
#
# Logic:
# 1. Extracts the condition function and loop body from the parsing object:
#    - `condition`: A callable function that evaluates the loop condition.
#    - `body`: A list of statements to execute for each iteration.
# 2. Defines a nested function `execute_while` to:
#    - Continuously evaluate the condition using `condition()`.
#    - If the condition is `True`, execute each statement in the loop body.
#    - If the condition is `False`, exit the loop.
# 3. Prints debugging information to indicate the start, progress, and termination of the loop.
# 4. Assigns the nested function to `p[0]` for deferred execution.
#
# Notes:
# - This function assumes the existence of:
#   - A `condition` function that evaluates the condition logic.
#   - A loop body (`program`) that is a list of callable functions.
# - The nested function structure allows deferred execution of the loop logic.
#
# Example Usage:
# Input:
# ```
# while x < 5 do
#     print(x)
#     x = x + 1
# end
# ```
# Parsing generates a function that continuously checks `x < 5` and executes the loop body until `x >= 5`.

def p_statement_while(p):
    'statement : while condition do program end'
    
    condition, body = p[2], p[4]  # Correct order of condition and body

    def execute_while():
        
        #Executes the while loop. The loop checks the condition and iterates over the body
        #until the condition returns False.
        

        while True:
            if not condition():  # Check the condition

                break  # Exit the loop if the condition is False
            else:

                for stmt in body:  # Execute each statement in the body
                    stmt()

    # Store the function for later execution
    p[0] = execute_while



