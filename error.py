from tokeniser import *
from parser import *
from state import global_state

#Grammar rules error 

# Function to handle syntax errors during parsing.
#
# This function is invoked by the parser when it encounters a syntax error.
# It identifies the erroneous line and provides detailed suggestions for correcting
# common mistakes based on the unexpected token or keyword.
#
# Parameters:
# - p: A yacc parsing object representing the current parsing state and error token.
#
# Logic:
# 1. If the error token `p` is not `None`:
#    - Extracts the line number and content of the line containing the error using helper functions.
#    - Writes a syntax error message with the problematic token and line details to the standard error stream.
#    - Analyzes the token value (`p.value`) or its presence in the line to suggest corrections for specific keywords,
#      such as "move," "draw," "cursor," "if," and more.
#      - Provides usage examples for each keyword to help the user correct their code.
# 2. If the error token `p` is `None`:
#    - Indicates a syntax error due to an unexpected end of the input file.
# 3. Sets `global_state.has_errors` to `True` to signal that an error occurred.
#
# Notes:
# - The function relies on `find_error_line`, `data`, `line_offsets`, and `global_state`.
# - Detailed suggestions for common language constructs, such as statements, loops, and conditions,
#   aim to improve the user's understanding of the language syntax.
#
# Example Usage:
# When parsing a program with errors, this function provides feedback like:
# Syntax error on line 5: unexpected element 'move'.
# Suggested correction: check the complete structure of the 'move' statement.
# Usage:
# - 'move <id_cursor> by <number>'.

def p_error(p):
    
    if p:

        line_number, line_content = find_error_line(data, line_offsets, p.lexpos)
        
        sys.stderr.write(f"Syntax error on line {line_number}: unexpected element '{p.value}'.\n")

        if p.value == "move" or "move" in line_content:
            sys.stderr.write("Suggested correction: check the complete structure of the 'move' statement.\n")
            sys.stderr.write("Usage :\n")
            sys.stderr.write("- 'move <id_cursor> by <number>'.\n")
        if p.value == "by" or "by" in line_content:
            sys.stderr.write("Suggested correction: ensure 'by' is part of a complete 'move' or 'rotate' statement.\n")
            sys.stderr.write("Usage :\n")
            sys.stderr.write("- 'move <id_cursor> by <number>'.\n")
            sys.stderr.write("Or :\n")
            sys.stderr.write("- 'rotate <id_cursor> by <angle>'.\n")
        if p.value == "draw" or "draw" in line_content:
            sys.stderr.write("Suggested correction: check the complete structure of the 'draw' statement.\n")
            sys.stderr.write("Usage :\n")
            sys.stderr.write("- 'draw (<form>, <size>) with <cursor>'.\n")
            sys.stderr.write("Forms: circle | square | line | filledcircle | filledsquare | arc.\n")
            sys.stderr.write("Warning, 'arc' has a different usage.: \n")
            sys.stderr.write("- 'draw (arc, <size>, <start angle>, <end angle>) with <cursor>'.\n")
        if p.value == "cursor" or "cursor" in line_content:
            sys.stderr.write("Suggested correction: check the complete structure of the 'create cursor' statement.\n")
            sys.stderr.write("Usage :\n")
            sys.stderr.write("- '<id_cursor> equal create cursor at (<number or id_number>, <number or id_number>) with (<number or id_number>, <number or id_number>, <number or id_number>, <number or id_number>, <number or id_number>, <number or id_number>)'.\n")
        if p.value == "create" or "create" in line_content:
            sys.stderr.write("Suggested correction: check the complete structure of the 'create cursor' statement.\n")
            sys.stderr.write("Usage :\n")
            sys.stderr.write("- '<id_cursor> equal create cursor at (<number or id_number>, <number or id_number>) with (<number or id_number>, <number or id_number>, <number or id_number>, <number or id_number>, <number or id_number>, <number or id_number>)'.\n")
        if p.value == "with" or "with" in line_content:
            sys.stderr.write("Suggested correction: check the complete structure of the 'create cursor' or 'draw' statement.\n")
            sys.stderr.write("Usage :\n")
            sys.stderr.write("- '<id_cursor> equal create cursor at (<number or id_number>, <number or id_number>) with (<number or id_number>, <number or id_number>, <number or id_number>, <number or id_number>, <number or id_number>, <number or id_number>)'.\n")
            sys.stderr.write("Or :\n")
            sys.stderr.write("- 'draw (<form>, <size>) with <cursor>'.\n")
            sys.stderr.write("Forms: circle | square | line | filledcircle | filledsquare | arc.\n")
            sys.stderr.write("Warning, 'arc' has a different usage.: \n")
            sys.stderr.write("- 'draw (arc, <size>, <start angle>, <end angle>) with <cursor>'.\n")
        if p.value == "if" or "if" in line_content:
            sys.stderr.write("Suggested correction: check the complete structure of the condition statement.\n")
            sys.stderr.write("Two possibilities :\n")
            sys.stderr.write("- 'if <conditon> then <program> end\n")
            sys.stderr.write("- 'if condition then program else program end'\n")
        if p.value == "for" or "for" in line_content:
            sys.stderr.write("Suggested correction: check the complete structure of the loop statement.\n")
            sys.stderr.write("Usage :\n")
            sys.stderr.write("- 'for <condition> in (<start>,<end>) do <program> end'\n")
        if p.value == "mode" or "mode" in line_content:
            sys.stderr.write("Suggested correction: check the complete structure of the animation mode.\n")
            sys.stderr.write("Usage :\n")
            sys.stderr.write("- 'mode <animation>'\n")
            sys.stderr.write("Animations: snail | bounce | disco")
        if p.value == "rotate" or "rotate" in line_content:
            sys.stderr.write("Suggested correction: check the complete structure of the 'rotate' statement.\n")
            sys.stderr.write("Usage :\n")
            sys.stderr.write("- 'rotate <id_cursor> by <angle>'.\n")
        if p.value == "then" or "then" in line_content:
            sys.stderr.write("Suggested correction: check the complete structure of the condition statement.\n")
            sys.stderr.write("Two possibilities :\n")
            sys.stderr.write("- 'if <conditon> then <program> end\n")
            sys.stderr.write("- 'if condition then program else program end'\n")
        if p.value == "else" or "else" in line_content:
            sys.stderr.write("Suggested correction: check the complete structure of the condition statement.\n")
            sys.stderr.write("Usage:\n")
            sys.stderr.write("- 'if condition then program else program end'\n")
        if p.value == "while" or "while" in line_content:
            sys.stderr.write("Suggested correction: check the complete structure of the 'while' statement.\n")
            sys.stderr.write("Usage:\n")
            sys.stderr.write("- 'while <condition> do <program> end'.\n")
        if p.value == "do" or "do" in line_content:
            sys.stderr.write("Suggested correction: ensure 'do' is part of a complete 'for' or 'while' statement.\n")
            sys.stderr.write("- 'for <condition> in (<start>,<end>) do <program> end'\n")
            sys.stderr.write("Or:\n")
            sys.stderr.write("- 'while <condition> do <program> end'.\n")
        if p.value == "set" or "set" in line_content:
            sys.stderr.write("Suggested correction: ensure 'set' is part of a complete 'set thickness' statement.\n")
            sys.stderr.write("Usage:\n")
            sys.stderr.write("set <cursor> thickness at <number or id_number>")
        if p.value == "thickness" or "thickness" in line_content:
            sys.stderr.write("Suggested correction: ensure 'thickness' is part of a complete 'set thickness' statement.\n")
            sys.stderr.write("Usage:\n")
            sys.stderr.write("set <cursor> thickness at <number or id_number>")
        if p.value == "at" or "at" in line_content:
            sys.stderr.write("Suggested correction: ensure 'at' is part of a complete 'set thickness' or 'create cursor' statement.\n")
            sys.stderr.write("Usage:\n")
            sys.stderr.write("set <cursor> thickness at <number or id_number>")
            sys.stderr.write("Or:\n")
            sys.stderr.write("- '<id_cursor> equal create cursor at (<number or id_number>, <number or id_number>) with (<number or id_number>, <number or id_number>, <number or id_number>, <number or id_number>, <number or id_number>, <number or id_number>)'.\n")
        if p.value == "end" or "end" in line_content:
            sys.stderr.write("Suggested correction: ensure 'end' is part of a complete 'for', 'if' or 'while' statement.\n")
            sys.stderr.write("Usage:\n")
            sys.stderr.write("- 'for <condition> in (<start>,<end>) do <program> end'\n")
            sys.stderr.write("Or:\n")
            sys.stderr.write("- 'if <conditon> then <program> end\n") 
            sys.stderr.write("- 'if condition then program else program end'\n")
            sys.stderr.write("Or:\n")
            sys.stderr.write("- 'while <condition> do <program> end'.\n")
        if p.value == "in" or "in" in line_content:
            sys.stderr.write("Suggested correction: ensure 'in' is part of a complete 'for' statement.\n")
            sys.stderr.write("- 'for <condition> in (<start>,<end>) do <program> end'\n")
    else :
        sys.stderr.write("Syntax error: unexpected end of file\n")
    global_state.has_errors = True


# Function to handle syntax errors in movement-related statements.
#
# This function defines grammar rules for identifying invalid `move` statements
# and provides detailed error messages with suggested corrections for specific issues.
#
# Parameters:
# - p: A yacc parsing object containing tokens and parsing state.
#
# Logic:
# 1. Matches the input with various patterns of invalid `move` statements.
# 2. Identifies specific error cases:
#    - Case 1: Incomplete `move` command (missing arguments).
#    - Case 2: Command with a number but missing `id_cursor`.
#    - Case 3: Command with `id_cursor` but missing `by <number>`.
#    - Case 4: Command with `id_cursor by` but missing the number.
#    - Case 5: Commands where the order of components is incorrect.
# 3. For each case, writes an appropriate syntax error message to the standard error stream.
# 4. Provides usage examples for the correct `move` command format.
# 5. Marks the global state as having errors to indicate that parsing failed.
#
# Notes:
# - Relies on helper functions like `find_line` and `resolve_value` to determine error details.
# - The correct usage of the `move` command is emphasized in each error message.
#
# Example Usage:
# For an incorrect command like `move 10`, this function outputs:
# Syntax error on line 5: 'id_cursor' missing before the number '10'.
# Suggested correction: 'move <id_cursor> by 10'.

def p_statement_movement_errors(p):
    '''
    statement : move
              | move number_or_id 
              | move id_cursor
              | move id_cursor by
              | id_cursor by move number_or_id
              | by id_cursor move number_or_id
              | move by id_cursor number_or_id
              | number_or_id by move id_cursor
              | by number_or_id move id_cursor
              | id_cursor move by number_or_id
    '''
    
    line_number = find_line(line_offsets, p.lexpos(1))

    # Case 1 : Incomplete `move` command (no argument)
    if len(p) == 2 and p[1] == 'move':
        sys.stderr.write(f"Syntax error on line {line_number}: 'id_cursor' and 'by <number>' missing after 'move'.\n")
        sys.stderr.write("Suggested correction: check the complete structure of the 'draw' statement.\n")
        sys.stderr.write("Usage :\n")
        sys.stderr.write("- 'move <id_cursor> by <number>'.\n")
        global_state.has_errors = True

    # Case2 : Command with a number but without`id_cursor`
    elif len(p) == 3 and p[1] == 'move' and (isinstance(p[2], (int)) or isinstance(p[2], (str))):
        number = resolve_value(p[2])
        sys.stderr.write(f"Syntax error on line {line_number}: 'id_cursor' missing before the number '{number}'.\n")
        sys.stderr.write(f"Suggested correction: 'move <id_cursor> by {p[2]}'.\n")
        global_state.has_errors = True

    # Case 3 : Command with `id_cursor` but without `by <number>`
    elif len(p) == 3 and p[1] == 'move':
        sys.stderr.write(f"Syntax error on line {line_number}: 'by <number>' missing after 'move {p[2]}'.\n")
        sys.stderr.write(f"Suggested correction: 'move {p[2]} by <number>'.\n")
        global_state.has_errors = True

    # Case 4 : Command with `id_cursor by` but without `number`
    elif len(p) == 4 and p[1] == 'move' and p[3] == 'by':
        sys.stderr.write(f"Syntax error on line {line_number}: missing number after 'by' in 'move {p[2]} by'.\n")
        sys.stderr.write(f"Suggested correction: 'move {p[2]} by <number>'.\n")
        global_state.has_errors = True

    # Case 5 : Command out of order
    elif len(p) == 5 and (
        (p[1] == 'id_cursor' and p[2] == 'by' and p[3] == 'move') or
        (p[1] == 'by' and p[2] == 'id_cursor' and p[3] == 'move') or
        (p[1] == 'move' and p[2] == 'by' and p[3] == 'id_cursor') or
        (p[1] == 'number_or_id' and p[2] == 'by' and p[3] == 'move') or
        (p[1] == 'by' and p[2] == 'number_or_id' and p[3] == 'move') or
        (p[1] == 'id_cursor' and p[2] == 'move' and p[3] == 'by')
    ):
        
        sys.stderr.write(f"Syntax error on line {line_number}: command in an incorrect order '{' '.join(str(x) for x in p[1:])}'.\n")
        sys.stderr.write(f"Suggested correction: 'move <id_cursor> by <number>'.\n")
        global_state.has_errors = True


# Function to handle syntax errors in 'draw' statements.
#
# This function identifies syntax errors in various forms of the 'draw' statement, 
# including general drawing commands and specific cases like 'arc'. 
# It provides detailed error messages and suggestions for corrections.
#
# Parameters:
# - p: A yacc parsing object containing tokens and parsing state.
#
# Logic:
# 1. Matches the input against several patterns of invalid 'draw' statements.
# 2. Identifies specific error cases:
#    - Missing or incorrect components such as parentheses, form, size, or cursor.
#    - Specific issues with 'arc' commands, like missing or invalid size, angles, or cursor.
# 3. For each case, writes an appropriate error message with suggestions for corrections.
# 4. Marks the global state as having errors to indicate that parsing failed.
#
# Notes:
# - Relies on helper functions like `find_line` to determine the line number where the error occurred.
# - The correct usage of the 'draw' statement is emphasized in each error message.
# - Provides different correction messages depending on whether the issue is with general forms or 'arc'.
#
# Example Usage:
# For an invalid command like `draw (circle, ) with cursor1`, this function outputs:
# Syntax error on line 5: invalid or missing size for 'circle'.
# Suggested correction: check the complete structure of the 'draw' instruction.
# Usage:
# - 'draw (<form>, <size>) with <cursor>'.
# Forms: circle | square | line | filledcircle | filledsquare | arc.

def p_statement_drawing_not_arc_error(p):
    '''statement : draw 
                 | draw error
                 | draw lp form rp
                 | draw lp error rp error
                 | draw lp error rp with error
                 | draw lp error rp with id_cursor
                 | draw lp form comma error rp with id_cursor
                 | draw lp form comma number_or_id rp error
                 | draw lp form comma number_or_id error with id_cursor
                 | draw lp arc comma error comma number_or_id comma number_or_id rp with id_cursor
                 | draw lp arc comma number_or_id comma error comma number_or_id rp with id_cursor
                 | draw lp arc comma number_or_id comma number_or_id comma error rp with id_cursor
                 | draw lp arc comma number_or_id comma number_or_id comma number_or_id rp error
                 | draw lp error error error rp with id_cursor
                 | draw lp form comma error error rp with id_cursor
                 | draw lp form error rp error id_cursor'''
    
    line_number = find_line(line_offsets, p.lexpos(1))

    # Handling multiple cases
    if len(p) >= 6 and 'error' in p:
        sys.stderr.write(f"Syntax error on line {line_number}: 'draw' statement is incorrect or incomplete.\n")
        sys.stderr.write("Suggested correction: check the complete structure of the 'draw' instruction.\n")
        sys.stderr.write("Usage :\n")
        sys.stderr.write("- 'draw (<form>, <size>) with <curseur>'.\n")
        sys.stderr.write("Forms: circle | square | line | filledcircle | filledsquare | arc.\n")
        sys.stderr.write("Warning, 'arc' has a different usage. \n")
        sys.stderr.write("- 'draw (arc, <size>, <start angle>, <end angle>) with <curseur>'.\n")
        return
    
    if len(p) <= 6 and p[1] == 'draw':
        sys.stderr.write(f"Syntax error on line {line_number}: 'draw' statement is incorrect or incomplete.\n")
        sys.stderr.write("Suggested correction: check the complete structure of the 'draw' instruction.\n")
        sys.stderr.write("Usage :\n")
        sys.stderr.write("- 'draw (<form>, <size>) with <curseur>'.\n")
        sys.stderr.write("Forms: circle | square | line | filledcircle | filledsquare | arc.\n")
        sys.stderr.write("Warning, 'arc' has a different usage. \n")
        sys.stderr.write("- 'draw (arc, <size>, <start angle>, <end angle>) with <curseur>'.\n")
        return


    # General case
    if len(p) >= 6 and p[3] == 'error':
        sys.stderr.write(f"Syntax error on line {line_number}: incorrect or missing element after 'draw'.\n")
        sys.stderr.write("Suggested correction: check the complete structure of the 'draw' instruction.\n")
        sys.stderr.write("Usage :\n")
        sys.stderr.write("- 'draw (<form>, <size>) with <curseur>'.\n")
        sys.stderr.write("Forms: circle | square | line | filledcircle | filledsquare | arc.\n")
        sys.stderr.write("Warning, 'arc' has a different usage. \n")
        sys.stderr.write("- 'draw (arc, <size>, <start angle>, <end angle>) with <curseur>'.\n")

    elif len(p) >= 8 and p[5] == 'error':
        sys.stderr.write(f"Syntax error on line {line_number}: invalid or missing size for '{p[3]}'.\n")
        sys.stderr.write("Suggested correction: check the complete structure of the 'draw' instruction.\n")
        sys.stderr.write("Usage :\n")
        sys.stderr.write("- 'draw (<form>, <size>) with <curseur>'.\n")

    elif len(p) >= 8 and p[6] == 'error':
        sys.stderr.write(f"Syntax error on line {line_number}: incorrect syntax before 'with'.\n")
        sys.stderr.write("Suggested correction: check the complete structure of the 'draw' instruction.\n")
        sys.stderr.write("Usage :\n")
        sys.stderr.write("- 'draw (<form>, <size>) with <curseur>'.\n")

    elif len(p) >= 8 and p[7] == 'error':
        sys.stderr.write(f"Syntax error on line {line_number}: missing or invalid cursor after 'with'.\n")
        sys.stderr.write("Suggested correction: check the complete structure of the 'draw' instruction.\n")
        sys.stderr.write("Usage :\n")
        sys.stderr.write("- 'draw (<form>, <size>) with <curseur>'.\n")

    # Specific case for arc
    if len(p) == 10 and p[5] == 'error':
        sys.stderr.write(f"Syntax error on line {line_number}: invalid or missing size after 'arc'.\n")
        sys.stderr.write("Suggested correction: check the complete structure of the 'draw arc' instruction.\n")
        sys.stderr.write("Usage :\n")
        sys.stderr.write("- 'draw (arc, <size>, <start angle>, <end angle>) with <curseur>'.\n")

    elif len(p) == 10 and p[7] == 'error':
        sys.stderr.write(f"Syntax error on line {line_number}: invalid or missing start angle after the size.\n")
        sys.stderr.write("Suggested correction: check the complete structure of the 'draw arc' instruction.\n")
        sys.stderr.write("Usage :\n")
        sys.stderr.write("- 'draw (arc, <size>, <start angle>, <end angle>) with <curseur>'.\n")

    elif len(p) == 10 and p[9] == 'error':
        sys.stderr.write(f"Syntax error on line {line_number}: invalid or missing end angle after the start angle.\n")
        sys.stderr.write("Suggested correction: check the complete structure of the 'draw arc' instruction.\n")
        sys.stderr.write("Usage :\n")
        sys.stderr.write("- 'draw (arc, <size>, <start angle>, <end angle>) with <curseur>'.\n")

    elif len(p) == 12 and p[12] == 'error':
        sys.stderr.write(f"Syntax error on line {line_number}: invalid or missing cursor after 'with'.\n")
        sys.stderr.write("Suggested correction: check the complete structure of the 'draw arc' instruction.\n")
        sys.stderr.write("Usage :\n")
        sys.stderr.write("- 'draw (arc, <size>, <start angle>, <end angle>) with <curseur>'.\n")

    global_state.has_errors = True


# Function to handle syntax errors in 'rotate' statements.
#
# This function identifies syntax errors in various forms of the 'rotate' statement
# and provides detailed error messages with suggestions for corrections.
#
# Parameters:
# - p: A yacc parsing object containing tokens and parsing state.
#
# Logic:
# 1. Matches the input against several patterns of invalid 'rotate' statements.
# 2. Identifies specific error cases:
#    - Case 1: Missing cursor and angle after 'rotate'.
#    - Case 2: Unexpected token after 'rotate'.
#    - Case 3: Missing angle or 'by' keyword after cursor.
#    - Case 4: Invalid cursor name.
#    - Case 5: Missing angle after 'by'.
#    - Case 6: Invalid angle value after 'by'.
#    - Case 7: Missing 'by' keyword before angle.
#    - Case 8: Components in an incorrect order.
# 3. For each case, writes an appropriate error message with suggestions for corrections.
# 4. Marks the global state as having errors to indicate that parsing failed.
#
# Notes:
# - Relies on helper functions like `find_line` to determine the line number where the error occurred.
# - Provides usage examples for the correct 'rotate' command format in each error message.
#
# Example Usage:
# For an invalid command like `rotate cursor1 90`, this function outputs:
# Syntax error on line 5: Missing 'by' keyword after cursor 'cursor1'.
# Suggested correction: Include the 'by' keyword before specifying the angle.
# Usage example: 'rotate <cursor> by <angle>'.

def p_statement_rotation_error(p):
    ''' statement : rotate 
                  | rotate error
                  | rotate id_cursor 
                  | rotate id_cursor error
                  | rotate id_cursor by 
                  | rotate id_cursor by error
                  | rotate error by error
                  | rotate id_cursor number_or_id
                  '''
    
    line_number = find_line(line_offsets, p.lexpos(1))
    # Case 1 : Incomplete 'move' command
    if len(p) == 2 and p[1] == 'rotate':
        sys.stderr.write(f"Syntax error on line {line_number}: 'id_cursor' and 'by <angle>' missing after 'rotate'.\n")
        sys.stderr.write("Suggested correction: check the complete structure of the 'rotate' statement.\n")
        sys.stderr.write("Usage :\n")
        sys.stderr.write("-'rotate <cursor> by <angle>'.\n")
        global_state.has_errors = True
    # Case 2: 'rotate error' (unexpected error token after 'rotate')
    elif len(p) == 3 and p[2] == 'error':
        sys.stderr.write(f"Syntax error on line {line_number}: Unexpected error token after 'rotate'.\n")
        sys.stderr.write("Suggested correction: Check the syntax after 'rotate'. Expected a cursor.\n")
        sys.stderr.write("Usage example: 'rotate <cursor> by <angle>'.\n")
    
    # Case 3: 'rotate id_cursor' (cursor is missing angle or 'by')
    elif len(p) == 3 and p[2] == 'id_cursor':
        sys.stderr.write(f"Syntax error on line {line_number}: Missing angle value after cursor.\n")
        sys.stderr.write("Suggested correction: After the cursor, you must specify 'by' and an angle.\n")
        sys.stderr.write("Usage example: 'rotate <cursor> by <angle>'.\n")
    
    # Case 4: 'rotate id_cursor error' (invalid cursor name)
    elif len(p) == 4 and p[3] == 'error':
        sys.stderr.write(f"Syntax error on line {line_number}: Invalid cursor name '{p[2]}'.\n")
        sys.stderr.write("Suggested correction: Ensure the cursor name is valid.\n")
        sys.stderr.write("Usage example: 'rotate <valid_cursor> by <angle>'.\n")
    
    # Case 5: 'rotate id_cursor by' (missing angle after 'by')
    elif len(p) == 4 and p[3] == 'by':
        sys.stderr.write(f"Syntax error on line {line_number}: Missing angle after 'by' for cursor '{p[2]}'.\n")
        sys.stderr.write("Suggested correction: You need to provide an angle after 'by'.\n")
        sys.stderr.write("Usage example: 'rotate <cursor> by <angle>'.\n")
    
    # Case 6: 'rotate id_cursor by error' (invalid angle after 'by')
    elif len(p) == 5 and p[4] == 'error':
        sys.stderr.write(f"Syntax error on line {line_number}: Invalid angle value for cursor '{p[2]}'.\n")
        sys.stderr.write("Suggested correction: Ensure the angle is a valid number.\n")
        sys.stderr.write("Usage example: 'rotate <cursor> by <valid_angle>'.\n")
    
    # Case 7: 'rotate id_cursor number_or_id' (missing 'by' keyword)
    elif len(p) == 4 and p[3] != 'by':
        sys.stderr.write(f"Syntax error on line {line_number}: Missing 'by' keyword after cursor '{p[2]}'.\n")
        sys.stderr.write("Suggested correction: Include the 'by' keyword before specifying the angle.\n")
        sys.stderr.write("Usage example: 'rotate <cursor> by <angle>'.\n")
    
    # Case 5: Command in the wrong order (rotate)
    elif len(p) == 5 and (
        (p[1] == 'id_cursor' and p[2] == 'by' and p[3] == 'rotate') or
        (p[1] == 'by' and p[2] == 'id_cursor' and p[3] == 'rotate') or
        (p[1] == 'rotate' and p[2] == 'by' and p[3] == 'id_cursor') or
        (p[1] == 'number_or_id' and p[2] == 'by' and p[3] == 'rotate') or
        (p[1] == 'by' and p[2] == 'number_or_id' and p[3] == 'rotate') or
        (p[1] == 'id_cursor' and p[2] == 'rotate' and p[3] == 'by')
    ):

        sys.stderr.write(f"Syntax error on line {line_number}: command in an incorrect order '{' '.join(str(x) for x in p[1:])}'.\n")
        sys.stderr.write(f"Suggested correction: 'rotate <id_cursor> by <angle>'.\n")
        global_state.has_errors = True




# Function to handle syntax errors in 'for' statements.
#
# This function identifies syntax errors in various forms of the 'for' loop
# and provides detailed error messages with suggestions for corrections.
#
# Parameters:
# - p: A yacc parsing object containing tokens and parsing state.
#
# Logic:
# 1. Matches the input against several patterns of invalid 'for' statements.
# 2. Identifies specific error cases:
#    - Case 1: Missing identifier after 'for'.
#    - Case 2: Missing identifier or structure after 'in'.
#    - Case 3: Missing '(' after 'in'.
#    - Case 4: Missing comma between start and end values in range.
# 3. Writes an appropriate error message with a suggestion for corrections.
# 4. Marks the global state as having errors to indicate that parsing failed.
#
# Notes:
# - Relies on helper functions like `find_line` to determine the line number where the error occurred.
# - A fallback mechanism is used to handle cases where `lexpos` is unavailable.
# - Provides a consistent correction message with the expected structure of a 'for' loop.
#
# Example Usage:
# For an invalid command like `for id_number in`, this function outputs:
# Syntax error on line 5: missing '(' after 'in'.
# Suggested correction: 'for <identifier> in (<start>, <end>) do <instruction> end'.

def p_statement_for_error(p):
    '''statement : for
                 | for in
                 | for id_number 
                 | for id_number lp
                 | for id_number in
                 | for id_number in error
                 | for id_number in lp
                 | for id_number in lp error
                 | for id_number in id_number
                 '''
   
    
    try:
        line_number = find_line(line_offsets, p.lexpos(1))
    except AttributeError:
        # Fallback if lexpos is not available
        line_number = "unknown"

    base_correction = "for <identifier> in (<start>, <end>) do <instruction> end"
    
    if len(p) == 2 and p[1] == 'for':
        sys.stderr.write(f"Syntax error on line {line_number}: missing identifier after 'for'.\n")
        sys.stderr.write(f"Suggested correction: '{base_correction}'.\n")
        
    elif len(p) == 3 and p[2] == 'in':
        sys.stderr.write(f"Syntax error on line {line_number}: missing identifier after 'for'.\n")
        sys.stderr.write(f"Suggested correction: '{base_correction}'.\n")
        
    elif len(p) == 4 and p[3] == 'lp':
        sys.stderr.write(f"Syntax error on line {line_number}: '(' missing after 'in'.\n")
        sys.stderr.write(f"Suggested correction: '{base_correction}'.\n")
        
    elif len(p) == 7 and p[6] != 'comma':
        sys.stderr.write(f"Syntax error on line {line_number}: a comma is missing.\n")
        sys.stderr.write(f"Suggested correction: '{base_correction}'.\n")
    
    global_state.has_errors = True
