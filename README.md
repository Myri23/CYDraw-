# README


## Project Overview

This project provides a graphical programming environment for creating and manipulating visual elements through a custom scripting language. The project integrates various components for tokenizing, parsing, and executing the scripts, culminating in rendering animations and drawings with SDL2.


## Features

- **Custom Scripting Language :** Use commands like `move`, `draw`, and `rotate` to create and animate visuals.
- **Lexer and Parser :** Tokenizes and parses the script to validate syntax and generate executable instructions from scripts.
- **C Code Generation :** Converts script instructions into C code compatible with SDL2 for execution.
- **Animation Modes :** Supports different animation styles, including snail, bounce, and disco.
- **Interactive GUI :** A graphical interface (`Draw++`) for script editing, error correction, and execution.
- **Modular Design :** Comprehensive support for cursor manipulation, drawing functions, and animations with reusable components.


## File Descriptions

### Python Modules
#### `ide.py`
Provides the graphical user interface for editing and managing scripts. Key features include:
- File management (open, save, create new).
- Syntax highlighting and error correction.
- Integration with the lexer and parser for validation.
- Execution of scripts with results displayed in a dedicated area.

#### `tokeniser.py`
Defines the lexer for tokenizing the custom scripting language. Key features include:
- Token definitions for language constructs like `move`, `draw`, and `rotate`.
- Error detection and correction for invalid tokens.

#### `parser.py`
Implements a grammar for parsing scripts and generating actions. Key features include:
- Context-free grammar for validating script structure.
- Generation of deferred execution instructions.

#### `error.py`
Manages error reporting during parsing and execution. Key features include:
- Detailed error messages with suggestions for corrections.
- Tracks global error state.

#### `state.py`
Defines a global state manager for sharing state across modules. Key features include:
- Tracks errors by using a an error global state variable
- Ensures consistency in shared data.

#### `generationCode.py`
Generates C code from parsed scripts. Key features include:
- Categorizes instructions for cursor management, drawing, and animation.
- Writes an SDL2-compatible C program for rendering and animations.

#### `CompilerExecuter.py`
Handles the compilation and execution of generated C code. Key features include:
- Compiles C code with `gcc`.
- Executes the generated binary.
- Manages errors during compilation and execution.

#### `main.py`
Coordinates the entire workflow from tokenizing and parsing to execution. Key features include:
- Parses input scripts and checks for errors.
- Executes valid instructions and generates C code.
- Compiles and runs the generated C program.

### SDL2 Files
#### `animate.c` and `animate.h`
Contain the logic for various animation modes:
- `animateDrawingsnail`: Circular animation with distributed cursors.
- `animateDrawingbond`: Bouncing cursors with directional changes.
- `animateRotation2`: Rotational animation of shapes.

#### `config.h`
Defines constants and configuration settings for the SDL2 application.

#### `draw.c` and `draw.h`
Implement drawing functions for shapes like circles, squares, lines, arcs, and filled shapes. These functions are used to render graphical elements based on script instructions.

#### `handle.c` and `handle.h`
Provide event handling mechanisms for user interactions such as:
- Mouse clicks and movements.
- Zooming and rotating shapes.
- Deleting or modifying elements interactively.

#### `newcursor.c` and `newcursor.h`
Define the structure and properties of cursors, including:
- Position and visibility management.
- Integration with SDL2 for rendering.
- Support for custom shapes and colors.

#### `generated_code.c`
The output file generated from scripts. Contains all instructions for cursor management, drawing, and animations.


## Installation

### Prerequisites
   - **Python 3.8** or higher
   - **GCC compiler** 
   - **SDL2 development libraries :** Required to draw shapes, handle animations, and display graphics in a window.
   - **Customtkinter :** A library for modern graphical user interfaces (GUI) in Python.
   - **Tkinter libraries :** Required for building traditional GUI elements.
   - **PLY libraries :** A Python implementation of Lex and Yacc for parsing.

###  Setup Instructions
1. Clone the repositery 
   ```bash
   git clone https://github.com/Myri23/draw-.git
   cd draw-
   ```
# 
 
2. System Package Updates
Update the system packages to ensure you have the latest version :
   ```bash
   sudo apt-get update 
   ```

3. Set up a Python Virtual Environment in the folder containing the project's files
A virtual environment isolates the project's dependencies to prevent conflicts with other Python projects.
Install the Python module to create virtual environments :
   ```bash
  sudo apt install python3.12-venv
   ```
Create a virtual environment dedicated to the Draw++ project :
 ```bash
   python3 -m venv myenv
   ```
Activate the virtual environment :
   ```bash
   source myenv/bin/activate
   ```

4. Install Required Libraries
   - User Interface
Install Custom Tkinter, an essential library for the user interface :
 ```bash
   pip install customtkinter
   ```
Install Tkinter, required for managing graphical components of the interface :
   ```bash
   sudo apt-get install python3-tkinter
   ```
   - Lexical and Syntax Analysis
Install PLY (Python Lex-Yacc), used for analysing and interpreting the grammar of Draw ++ :
   ```bash
   pip install ply
   ```
   - SDL2 Graphics Libraries
Install SDL2 libraries to handle graphical features like drawing and animations : 
   ```bash
   sudo apt-get install libsdl2-2.0-0 libsdl2-dbg libsdl2-dev libsdl2-image-2.0-0 libsdl2-image-dbg libsdl2-image-dev
   ```

5. Verify Installed Libraries
To ensure all required libraries have been installed correctly, use the following command :
```bash
   pip list
   ```


## Usage

### GUI Mode 
1. Activate the virtual environment in the project's folder with the command: source myenv/bin/activate 
2. Run the GUI:
   ```python3 ide.py
   ```
3. Use the GUI to create or open a `dpp` file.
4. Edit and execute your script directly in the interface.

### Grammar

Assign expression plus, Usage: "<id_number> = <id_number> + <number>" 
Assign expression plus, Example: x = x + 1 

Assign expression minus, Usage: "<id_number> = <id_number> - <number>"
Assign expression minus, Example: x = x - 1 

Assign expression times, Usage: "<id_number> = <id_number> * <number>" 
Assign expression times, Example: x = x * 1

Assign expression dividedby, Usage: "<id_number> = <id_number> / <number>" 
Assign expression dividedby, Example: x = x / 1  

Assign expression modulo, Usage: "<id_number> = <id_number> % <number>" 
Assign expression modulo, Example: x = x % 1  

Assign a number to a variable, Usage: "<id_number> equal <number_or_id_number>"
Assign a number to a variable, Example: x = 10 Example: x = y

Create a cursor, Usage: "<id_cursor> equal create cursor at (<number_or_id_number>, <number_or_id_number>) with (<number_or_id_number>, <number_or_id_number>, <number_or_id_number>, <number_or_id_number>, <number_or_id_number>, <number_or_id_number>)"
Create a cursor, Explanation: id_cursor = create cursor at (x, y) with (r, g, b, a, thickness, visibility)
Create a cursor, Example: cursor4 = create cursor at (200, 450) with (255, 0, 0, 255, 1, 1) 

Set a new thickness to a cursor, Usage: "set <id_cursor> thickness at <number_or_id_number>"
Set a new thickness to a cursor, Example: set c thickness at 20

If condition, Usage: "if <condition> then <program> fi" or "if <condition> then <program> else <program> fi"
If condition, Example:"if x < 20 then draw (circle, 50) with cursor4 fi" or "if i = 10 then draw (circle, 50) with cursor4 else draw (square, 50) with cursor2 fi"

For loop, Usage: "for <id_cursor> in (start, end) do <program> rof"
For loop, Example : for i in (0, 20) do draw (square, 50) with cursor2 rof

While loop Usage: "while <condition> do <program> end"
While loop Example : while x > 40 do draw (arc, x, 0, 180) with cursor2 end

Rotation, Usage: rotate <id_cursor> by <number_or_id>
Rotation, Example: rotate cursor1 by 20

Movement, Usage: move <id_cursor> by <number_or_id>
Movement, Example: move cursor1 by 40


Forms (without arcs), Usage: draw (<form>, <number_or_id>) with <id_cursor>
Forms (without arcs), Explanation: draw (form, size) with <id_cursor>
Forms (without arcs), Example: draw (circle, 50) with cursor7

Form arc, Usage: draw (arc, <number_or_id>, <number_or_id>, <number_or_id>) with <id_cursor>
Form arc, Explanation: draw (arc, size, start_angle, end_angle) with <id_cursor>
Form arc, Explanation: draw (arc, 50, 30, 120) with cursor1

- Available forms : `circle`, `square`, `line`, `filledcircle`, `filledsquare`, `arc`.


Selecting an animation mode, Usage : mode <animation>
Selecting an animation mode, Example : mode disco
Available animations : `disco`, `snail`, `bounce`.


- A simple condition can be used to perform comparisons. Those are the available conditions :
<number_or_id> < <number_or_id> : less than
<number_or_id> > <number_or_id> : greater than
<number_or_id> = <number_or_id> : equal to

- Add a comment with '#' :
Example: #This is a comment.
The comment will automatically ignore the rest of the line after #

### Examples
```
# Create a red cursor
cursor1 = create cursor at (50, 50) with (255, 0, 0, 255, 0, 0, 5, 1)

# Draw a circle
draw (circle, 20) with cursor1

# Move and rotate
move cursor1 by 50
rotate cursor1 by 45

#Function to animate
mode snail
```

## Script Reference

### Basic commands
- `create cursor` : Initialize a new cursor
- `draw` : Create shapes (circle, square, line)
- `move` : Reposition cursor
- `rotate` : Change cursor orientation
- `mode` : Set animation style

### Cursor properties
- Position (x, y)
- Color (R, G, B, A)
- Thickness (int)
- Visibility (0 or 1)

### Animation Modes
- snail : Circular rotation + motion
- bounce : Rebounding movement
- disco : circular movements

## Acknowledgments
- SDL2 library for graphics and rendering.
- Python's PLY library for lexer and parser implementation.
- Customtkinter for the GUI.
- Tkinter for the GUI and basic widgets.

