# Function to generate C code from a parsed program.
#
# This function takes a parsed representation of a program and generates a C file (`generated_code.c`)
# that includes animation and drawing logic. The function categorizes instructions, defines cursor-related
# structures, and writes SDL2-compatible C code.
#
# Parameters:
# - parsed_program: A list of strings representing the parsed lines of the program.
#
# Logic:
# 1. Categorizes instructions into creation, movement, rotation, thickness, drawing, and animation commands.
# 2. Extracts cursor names and creates a table for managing cursors.
# 3. Writes a C file with:
#    - Header inclusions for required modules.
#    - Cursor creation, movement, and drawing instructions.
#    - Animation modes for different behaviors.
#    - A `main` function to initialize SDL, run animations, and clean up resources.
#
# Notes:
# - The function supports various animation modes (e.g., `animateDrawingsnail`, `animateDrawingbond`).
# - Cursor operations like movement, rotation, and zoom are implemented for interactivity.
# - Default fallback behavior uses the `animateDrawing` function if no specific mode is set.
# - Generated code assumes an SDL2 environment with necessary dependencies.
#
# Example Usage:
# parsed_program = [
#     "createCursor = cursor1",
#     "drawCircle(cursor1, 50, 50, 20)",
#     "animateDrawingsnail"
# ]
# generate_c_code(parsed_program)
def generate_c_code(parsed_program):
    cursor_creation_instructions = []
    movement_and_rotation_and_thickness_instructions = []
    drawing_instructions = []
    current_animation_mode = None  # Will contain the last animation mode instruction
    cursor_names = []

    for line in parsed_program:
        if "createCursor" in line:
            parts = line.split("=", 1)
            cursor_name = parts[0].strip().split()[-1]  # Takes the last word before the "="
            cursor_creation_instructions.append(line)
            cursor_names.append(cursor_name)
        elif "moveCursor" in line or "rotateCursor" in line or "setThickness" in line:
            movement_and_rotation_and_thickness_instructions.append(line)
        elif "drawCircle" in line or "drawSquare" in line or "drawLine" in line or "drawArc" in line or "drawFilledCircle" in line or "drawFilledSquare" in line:
            drawing_instructions.append(line)
        elif "animateDrawingsnail" in line or "animateDrawingbond" in line or "animateRotation2" in line:
            current_animation_mode = line  # Replaces the previous mode

    cursor_table_declaration = f"Cursor* cursors[] = {{\n    " + ",\n    ".join(f"&{name}" for name in cursor_names) + "\n};"

    with open("./SDL/generated_code.c", "w") as f:
        f.write('#include "config.h"\n')
        f.write('#include "draw.h"\n')
        f.write('#include "handle.h"\n')
        f.write('#include "newcursor.h"\n\n')

        # Writing the bounce mode


        f.write('void animateDrawingsnail(SDL_Renderer* renderer) {\n')
        
        # Add instructions for creation cursor
        for line in cursor_creation_instructions:
            f.write(f"{line}\n")
        f.write("\n")

        # Add the cursor table
        f.write(f"{cursor_table_declaration}\n\n")

        # Adding rotation/movement instructions
        f.write('    // Movement and rotation instructions\n')
        for line in movement_and_rotation_and_thickness_instructions:
            f.write(f'    {line}\n')
        f.write('\n')
        
        f.write('    int num_cursors = sizeof(cursors) / sizeof(cursors[0]);\n\n')
        f.write('    // Base positions for animation\n')
        f.write('    int base_x[num_cursors];\n')
        f.write('    int base_y[num_cursors];\n')
        f.write('    for (int i = 0; i < num_cursors; i++) {\n')
        f.write('        base_x[i] = cursors[i]->x;\n')
        f.write('        base_y[i] = cursors[i]->y;\n')
        f.write('    }\n\n')
        f.write('    double angles[num_cursors]; // Angles for each cursor\n')
        f.write('    for (int i = 0; i < num_cursors; i++) {\n')
        f.write('        angles[i] = i * (2 * M_PI / num_cursors); // Distribute cursors evenly\n')
        f.write('    }\n\n')
        f.write('    int radius = 50; // Radius for animation\n')
        f.write('    int running = 1;\n')
        f.write('    int is_moving = 0; // Indicator for movement\n')
        f.write('    SDL_Event event;\n\n')
        f.write('    while (running) {\n')
        f.write('        while (SDL_PollEvent(&event)) {\n')
        f.write('            switch (event.type) {\n')
        f.write('                case SDL_QUIT:\n')
        f.write('                    running = 0;\n')
        f.write('                    break;\n\n')
        f.write('                case SDL_MOUSEBUTTONDOWN:\n')
        f.write('                    if (event.button.button == SDL_BUTTON_LEFT) {\n')
        f.write('                        handleSelection(event.button.x, event.button.y, cursors, num_cursors);\n')
        f.write('                        if (selected_cursor) {\n')
        f.write('                            is_moving = 1; // Activate movement mode\n')
        f.write('                        } else {\n')
        f.write('                            is_moving = 0; // No cursor selected\n')
        f.write('                        }\n')
        f.write('                    }\n')
        f.write('                    break;\n\n')

        f.write('                case SDL_MOUSEBUTTONUP:\n')
        f.write('                    if (event.button.button == SDL_BUTTON_LEFT) {\n')
        f.write('                        is_moving = 0; // Stop movement\n\n')
        f.write('                        // Update base positions for the selected cursor\n')
        f.write('                        if (selected_cursor) {\n')
        f.write('                            for (int i = 0; i < num_cursors; i++) {\n')
        f.write('                                if (cursors[i] == selected_cursor) {\n')
        f.write('                                    base_x[i] = selected_cursor->x;\n')
        f.write('                                    base_y[i] = selected_cursor->y;\n')
        f.write('                                    break;\n')
        f.write('                                }\n')
        f.write('                            }\n')
        f.write('                        }\n')
        f.write('                    }\n')
        f.write('                    break;\n\n')

        f.write('                case SDL_MOUSEMOTION:\n')
        f.write('                    if (is_moving && selected_cursor) {\n')
        f.write('                        handleMovement(event.motion.x, event.motion.y);\n')
        f.write('                    }\n')
        f.write('                    break;\n\n')

        f.write('                case SDL_MOUSEWHEEL:\n')
        f.write('                    if (selected_cursor) { // Only zoom if a cursor is selected\n')
        f.write('                        handleZoom(event.wheel.y > 0);\n')
        f.write('                    }\n')
        f.write('                    break;\n\n')

        f.write('                case SDL_KEYDOWN:\n')
        f.write('                    if (selected_cursor) { // Ensure actions only apply to a selected cursor\n')
        f.write('                        if (event.key.keysym.sym == SDLK_r) { // Rotate clockwise\n')
        f.write('                            applyRotationToCursor(selected_cursor, 15);\n')
        f.write('                        }\n')
        f.write('                        if (event.key.keysym.sym == SDLK_e) { // Rotate counterclockwise\n')
        f.write('                            applyRotationToCursor(selected_cursor, -15);\n')
        f.write('                        }\n')
        f.write('                        if (event.key.keysym.sym == SDLK_DELETE) { // Delete the selected shape\n')
        f.write('                            handleDeletion();\n')
        f.write('                        }\n')
        f.write('                    }\n')
        f.write('                    break;\n\n')

        f.write('                default:\n')
        f.write('                    break;\n')
        f.write('            }\n')
        f.write('        }\n\n')

        f.write('        SDL_SetRenderDrawColor(renderer, 0, 0, 0, 255);\n')
        f.write('        SDL_RenderClear(renderer);\n\n')

        f.write('        // Animation and display of cursors\n')
        f.write('        for (int i = 0; i < num_cursors; i++) {\n')
        f.write('            if (cursors[i]->visible) {\n')
        f.write('                // Calculate the animated position\n')
        f.write('                int anim_x = base_x[i] + radius * cos(angles[i]);\n')
        f.write('                int anim_y = base_y[i] + radius * sin(angles[i]);\n\n')

        f.write('                // Rotate the shape\n')
        f.write('                rotateCursor(cursors[i], 10);\n\n')

        f.write('                // Update animated position only if not being moved\n')
        f.write('                if (!is_moving || cursors[i] != selected_cursor) {\n')
        f.write('                    cursors[i]->x = anim_x;\n')
        f.write('                    cursors[i]->y = anim_y;\n')
        f.write('                }\n')
        f.write('            }\n')
        f.write('            // Advance the angle for animation\n')
        f.write('            angles[i] += 0.05;\n')
        f.write('        }\n')

        for line in drawing_instructions:
            f.write(f'{line}\n')
        f.write('\n')

        f.write('        SDL_RenderPresent(renderer);\n')
        f.write('        SDL_Delay(50);\n')
        f.write('    }\n')
        f.write('}\n\n')






        # Writing the bounce mode

        f.write('void animateDrawingbond(SDL_Renderer* renderer) {\n')
        
        #Add the cursor creation instructions
        for line in cursor_creation_instructions:
            f.write(f"{line}\n")
        f.write("\n")

        # Add the cursor table
        f.write(f"{cursor_table_declaration}\n\n")

        #Adding rotation/movement instructions
        f.write('    // Movement instructions and rotation instructions\n')
        for line in movement_and_rotation_and_thickness_instructions:
            f.write(f'    {line};\n')
        f.write('\n')

        f.write('    int num_cursors = sizeof(cursors) / sizeof(cursors[0]);\n\n')
        f.write('    // Initialize individual speeds for each cursor\n')
        f.write('    int dx[num_cursors];\n')
        f.write('    int dy[num_cursors];\n')
        f.write('    for (int i = 0; i < num_cursors; i++) {\n')
        f.write('        dx[i] = (i % 2 == 0) ? 5 : -5;  // Alternating initial direction\n')
        f.write('        dy[i] = (i % 2 == 0) ? 5 : -5;\n')
        f.write('    }\n\n')
        f.write('    int running = 1;\n')
        f.write('    SDL_Event event;\n\n')
        f.write('    while (running) {\n')
        f.write('        while (SDL_PollEvent(&event)) {\n')
        f.write('            switch (event.type) {\n')
        f.write('                case SDL_QUIT:\n')
        f.write('                    running = 0;\n')
        f.write('                    break;\n')
        f.write('                case SDL_MOUSEBUTTONDOWN:\n')
        f.write('                    if (event.button.button == SDL_BUTTON_LEFT) {\n')
        f.write('                        handleSelection(event.button.x, event.button.y, cursors, num_cursors);\n')
        f.write('                    }\n')
        f.write('                    break;\n')
        f.write('                case SDL_MOUSEMOTION:\n')
        f.write('                    if (event.motion.state & SDL_BUTTON_LMASK) {\n')
        f.write('                        handleMovement(event.motion.x, event.motion.y);\n')
        f.write('                    }\n')
        f.write('                    break;\n')
        f.write('                case SDL_MOUSEWHEEL:\n')
        f.write('                    handleZoom(event.wheel.y > 0);\n')
        f.write('                    break;\n')
        f.write('                case SDL_KEYDOWN:\n')
        f.write('                    if (event.key.keysym.sym == SDLK_r) {\n')
        f.write('                        applyRotationToCursor(selected_cursor, 15);\n')
        f.write('                    }\n')
        f.write('                    if (event.key.keysym.sym == SDLK_e) {\n')
        f.write('                        applyRotationToCursor(selected_cursor, -15);\n')
        f.write('                    }\n')
        f.write('                    if (event.key.keysym.sym == SDLK_DELETE) {\n')
        f.write('                        handleDeletion();\n')
        f.write('                    }\n')
        f.write('                    break;\n')
        f.write('                default:\n')
        f.write('                    break;\n')
        f.write('            }\n')
        f.write('        }\n\n')
        f.write('        SDL_SetRenderDrawColor(renderer, 0, 0, 0, 255);\n')
        f.write('        SDL_RenderClear(renderer);\n\n')
        f.write('        for (int i = 0; i < num_cursors; i++) {\n')
        f.write('            if (cursors[i]->visible) {\n')
        f.write('                if (cursors[i]->x <= 0 || cursors[i]->x >= SCREEN_WIDTH) dx[i] = -dx[i];\n')
        f.write('                if (cursors[i]->y <= 0 || cursors[i]->y >= SCREEN_HEIGHT) dy[i] = -dy[i];\n\n')
        f.write('                cursors[i]->x += dx[i];\n')
        f.write('                cursors[i]->y += dy[i];\n\n')
        f.write('                rotateCursor(cursors[i], 10);\n')
        f.write('           }\n')
        f.write('       }\n')
        
        f.write('        // Drawing instructions\n')
        for line in drawing_instructions:
            f.write(f'        {line};\n')
        f.write('\n')

    
        f.write('        SDL_RenderPresent(renderer);\n')
        f.write('        SDL_Delay(100);\n')
        f.write('        }\n')
        f.write('    }\n\n\n')






        # Adding function Rotation2

        f.write('void animateRotation2(SDL_Renderer* renderer) {\n')
        f.write('    // Defining cursors with different drawing types\n')
        
        # adding instructions cursor creation
        for line in cursor_creation_instructions:
            f.write(f"{line}\n")
        f.write("\n")

        # Adding cursor table
        f.write(f"{cursor_table_declaration}\n\n")

        #Adding rotation / movement instructions
        f.write('    // movement and rotation instructions\n')
        for line in movement_and_rotation_and_thickness_instructions:
            f.write(f'    {line}\n')
        f.write('\n')

        f.write('    int num_cursors = sizeof(cursors) / sizeof(cursors[0]);\n\n')
        f.write('    int running = 1;\n')
        f.write('    SDL_Event event;\n\n')
        f.write('    while (running) {\n')
        f.write('        while (SDL_PollEvent(&event)) {\n')
        f.write('            switch (event.type) {\n')
        f.write('                case SDL_QUIT:\n')
        f.write('                    running = 0;\n')
        f.write('                    break;\n')
        f.write('                case SDL_MOUSEBUTTONDOWN:\n')
        f.write('                    if (event.button.button == SDL_BUTTON_LEFT) {\n')
        f.write('                        handleSelection(event.button.x, event.button.y, cursors, num_cursors);\n')
        f.write('                    }\n')
        f.write('                    break;\n')
        f.write('                case SDL_MOUSEMOTION:\n')
        f.write('                    if (event.motion.state & SDL_BUTTON_LMASK) {\n')
        f.write('                        handleMovement(event.motion.x, event.motion.y);\n')
        f.write('                    }\n')
        f.write('                    break;\n')
        f.write('                case SDL_MOUSEWHEEL:\n')
        f.write('                    handleZoom(event.wheel.y > 0);\n')
        f.write('                    break;\n')
        f.write('                case SDL_KEYDOWN:\n')
        f.write('                    if (event.key.keysym.sym == SDLK_r) {\n')
        f.write('                        applyRotationToCursor(selected_cursor, 15);\n')
        f.write('                    }\n')
        f.write('                    if (event.key.keysym.sym == SDLK_e) {\n')
        f.write('                        applyRotationToCursor(selected_cursor, -15);\n')
        f.write('                    }\n')
        f.write('                    if (event.key.keysym.sym == SDLK_DELETE) {\n')
        f.write('                        handleDeletion();\n')
        f.write('                    }\n')
        f.write('                    break;\n')
        f.write('                default:\n')
        f.write('                    break;\n')
        f.write('            }\n')
        f.write('        }\n\n')
        f.write('        // Clear the screen\n')
        f.write('        SDL_SetRenderDrawColor(renderer, 0, 0, 0, 255);\n')
        f.write('        SDL_RenderClear(renderer);\n\n')
        f.write('        // Draw the shapes in rotation\n')
        f.write('        for (int i = 0; i < num_cursors; i++) {\n')
        f.write('            if (cursors[i]->visible) {\n')
        f.write('                rotateCursor2(cursors[i], 10); // Specific rotation for animateRotation2\n\n')
        f.write('            }\n')
        f.write('        }\n')

        f.write('        // Drawing instructions \n')
        for line in drawing_instructions:
            f.write(f'        {line};\n')
        f.write('\n')

        f.write('        SDL_RenderPresent(renderer);\n')
        f.write('        SDL_Delay(100);\n')
        f.write('    }\n')
        f.write('}\n\n')  






        # Addind function animateDrawing
        f.write('void animateDrawing(SDL_Renderer* renderer) {\n')

        #adding functions cursor rotation
        for line in cursor_creation_instructions:
            f.write(f"{line}\n")
        f.write("\n")

        # Adding the cursor table
        f.write(f"{cursor_table_declaration}\n\n")

        #Adding rotation/movement instructions
        f.write('    // movement and rotation instructions \n')
        for line in movement_and_rotation_and_thickness_instructions:
            f.write(f'    {line}\n')
        f.write('\n')

        f.write('    int num_cursors = sizeof(cursors) / sizeof(cursors[0]);\n\n')

        f.write('    int running = 1;\n')
        f.write('    while (running) {\n')
        f.write('        SDL_Event event;\n')
        f.write('        while (SDL_PollEvent(&event)) {\n')
        f.write('            switch (event.type) {\n')
        f.write('                case SDL_QUIT:\n')
        f.write('                    running = 0;\n')
        f.write('                    break;\n')
        f.write('                case SDL_MOUSEBUTTONDOWN:\n')
        f.write('                    if (event.button.button == SDL_BUTTON_LEFT) {\n')
        f.write('                        handleSelection(event.button.x, event.button.y, cursors, num_cursors);\n')
        f.write('                    }\n')
        f.write('                    break;\n')
        f.write('                case SDL_MOUSEMOTION:\n')
        f.write('                    if (event.motion.state & SDL_BUTTON_LMASK) {\n')
        f.write('                        handleMovement(event.motion.x, event.motion.y);\n')
        f.write('                    }\n')
        f.write('                    break;\n')
        f.write('                case SDL_MOUSEWHEEL:\n')
        f.write('                    handleZoom(event.wheel.y > 0);\n')
        f.write('                    break;\n')
        f.write('                case SDL_KEYDOWN:\n')
        f.write('                    if (event.key.keysym.sym == SDLK_r) { // Rotate clockwise when \'R\' is pressed.\n')
        f.write('                        applyRotationToCursor(selected_cursor, 15);\n')
        f.write('                    }\n')
        f.write('                    if (event.key.keysym.sym == SDLK_e) { // Rotate counterclockwise when \'E\' is pressed.\n')
        f.write('                        applyRotationToCursor(selected_cursor, -15);\n')
        f.write('                    }\n')
        f.write('                    if (event.key.keysym.sym == SDLK_DELETE) { // Delete the selected shape.\n')
        f.write('                        handleDeletion();\n')
        f.write('                    }\n')
        f.write('                    break;\n')
        f.write('                default:\n')
        f.write('                    break;\n')
        f.write('            }\n')
        f.write('        }\n\n')

        f.write('        // Clear the screen\n')
        f.write('        SDL_SetRenderDrawColor(renderer, 0, 0, 0, 255);\n')
        f.write('        SDL_RenderClear(renderer);\n\n')

        f.write('        // Drawing instructions\n')
        for line in drawing_instructions:
            f.write(f'        {line};\n')
        f.write('\n')

        f.write('        SDL_RenderPresent(renderer);\n')
        f.write('    }\n')
        f.write('}\n\n')

        # Adding the main
        f.write('int main() {\n\n')
        f.write('    // Initialize SDL\n')
        f.write('    if (SDL_Init(SDL_INIT_VIDEO) != 0) {\n')
        f.write('        printf("SDL initialization error : %s\\n", SDL_GetError());\n')
        f.write('        return 1;\n')
        f.write('    }\n\n')

        f.write('    SDL_Window* window = SDL_CreateWindow("SDL Cursor Drawing", SDL_WINDOWPOS_CENTERED, SDL_WINDOWPOS_CENTERED, SCREEN_WIDTH, SCREEN_HEIGHT, SDL_WINDOW_SHOWN);\n')
        f.write('    if (!window) {\n')
        f.write('        printf("window creation error : %s\\n", SDL_GetError());\n')
        f.write('        SDL_Quit();\n')
        f.write('        return 1;\n')
        f.write('    }\n\n')

        f.write('    SDL_Renderer* renderer = SDL_CreateRenderer(window, -1, SDL_RENDERER_ACCELERATED);\n')
        f.write('    if (!renderer) {\n')
        f.write('        SDL_DestroyWindow(window);\n')
        f.write('        printf("Renderer creation error : %s\\n", SDL_GetError());\n')
        f.write('        SDL_Quit();\n')
        f.write('        return 1;\n')
        f.write('    }\n\n')

        # Adding animation mode
        f.write('    // Animation mode\n')
        if current_animation_mode:
            f.write(f"    {current_animation_mode}\n\n")
        else:
            f.write(f"      animateDrawing(renderer);")


        f.write('    // Clean up and exit\n')
        f.write('    SDL_DestroyRenderer(renderer);\n')
        f.write('    SDL_DestroyWindow(window);\n')
        f.write('    SDL_Quit();\n\n')

        f.write('    return 0;\n')
        f.write('}\n')
