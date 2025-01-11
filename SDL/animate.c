#include "animate.h"
#include "config.h"
#include "draw.h"
#include "handle.h"
#include "newcursor.h"
#include <SDL2/SDL.h>



// ======================================================
// ANIMATION FUNCTIONS
// ======================================================
//
// This section contains functions responsible for animating multiple Cursor objects.
// Each animation function defines a unique type of motion or behavior for the cursors.
// These animations allow dynamic movement and interaction with the shapes on the screen.
//
// Functions in this section:
// - animateDrawingsnail: Moves cursors in a spiral motion around a central point.
// - animateDrawingbond: Bounces cursors off the edges of the screen.
// - animateDrawingrotation2: Continuously rotates cursors while maintaining their positions.
// - animateDrawing: Animates cursors by dynamically rendering their shapes at specific positions.



// Function to animate cursors in a spiral motion.
//
// This function creates multiple Cursor objects, each representing a distinct shape
// (line, square, circle, etc.), and animates them in a spiral-like motion around a
// central point. The animation is continuous and interactive, allowing users to select,
// move, zoom, rotate, or delete cursors dynamically.
//
// Parameters:
// - SDL_Renderer* renderer: The SDL renderer used to draw and animate the cursors.
//
// Logic:
// 1. **Cursor Initialization**:
//    - Six Cursor objects are created with unique colors, shapes, and initial positions.
//    - These cursors are stored in an array for efficient management.
// 2. **Base Position and Angle Initialization**:
//    - Each cursor is assigned a base position (`base_x`, `base_y`) and an initial angle
//      for its spiral motion.
//    - Angles are distributed evenly among the cursors to create a balanced animation.
// 3. **Animation Loop**:
//    - The program enters a continuous loop to animate and render the cursors.
//    - Each cursor's position is updated dynamically based on its angle and radius to
//      create the spiral effect.
// 4. **User Interactions**:
//    - **Selection**: Cursors can be selected by clicking within their boundaries.
//    - **Movement**: Selected cursors can be dragged using the mouse.
//    - **Zooming**: The mouse wheel adjusts the size of the selected cursor.
//    - **Rotation**: Keyboard keys rotate the selected cursor clockwise or counterclockwise.
//    - **Deletion**: The `DELETE` key removes the selected cursor.
// 5. **Rendering and Display**:
//    - Cursors are rendered based on their updated attributes (position, scale, visibility).
//    - The screen is updated continuously to display the animations.
//
// Notes:
// - The animation loop runs until the user exits the program via an `SDL_QUIT` event.
// - Interactions like selection or movement temporarily pause the animation for the
//   selected cursor.
//
// Example Usage:
// animateDrawingsnail(renderer); // Starts the spiral animation for multiple cursors.
void animateDrawingsnail(SDL_Renderer* renderer) {
    // Step 1: Define Cursor objects, each representing a unique type of shape.
    Cursor c1 = createCursor(200, 200, (SDL_Color){255, 255, 0, 255}, 7, 1);  // Line
    Cursor c2 = createCursor(400, 300, (SDL_Color){0, 255, 255, 255}, 13, 1);  // Square
    Cursor c3 = createCursor(600, 400, (SDL_Color){255, 0, 0, 255}, 20, 1);    // Filled square
    Cursor c4 = createCursor(200, 400, (SDL_Color){0, 255, 0, 255}, 17, 1);    // Circle
    Cursor c5 = createCursor(400, 500, (SDL_Color){255, 165, 0, 255}, 30, 1);  // Filled circle
    Cursor c6 = createCursor(600, 200, (SDL_Color){128, 0, 128, 255}, 28, 1);  // Arc

    // Step 2: Store pointers to the Cursor objects in an array for management.
    Cursor* cursors[] = {&c1, &c2, &c3, &c4, &c5, &c6};
    int num_cursors = sizeof(cursors) / sizeof(cursors[0]); // Total number of cursors.

    // Step 3: Initialize base positions for animation.
    int base_x[num_cursors];
    int base_y[num_cursors];
    for (int i = 0; i < num_cursors; i++) {
        base_x[i] = cursors[i]->x; // Set the base x-position.
        base_y[i] = cursors[i]->y; // Set the base y-position.
    }

    // Step 4: Initialize angles for each cursor to distribute them evenly.
    double angles[num_cursors];
    for (int i = 0; i < num_cursors; i++) {
        angles[i] = i * (2 * M_PI / num_cursors); // Distribute cursors evenly in a circle.
    }

    // Step 5: Define animation parameters.
    int radius = 50; // Radius for circular motion.
    int running = 1; // Flag to control the main loop.
    int is_moving = 0; // Flag to indicate if a cursor is being moved.
    SDL_Event event;

    // Step 6: Main animation loop.
    while (running) {
        // Process user events.
        while (SDL_PollEvent(&event)) {
            switch (event.type) {
                case SDL_QUIT:
                    running = 0; // Exit the loop on quit event.
                    break;

                case SDL_MOUSEBUTTONDOWN: // Handle mouse button press.
                    if (event.button.button == SDL_BUTTON_LEFT) {
                        handleSelection(event.button.x, event.button.y, cursors, num_cursors); // Select a cursor.
                        is_moving = selected_cursor != NULL; // Enable movement if a cursor is selected.
                    }
                    break;

                case SDL_MOUSEBUTTONUP: // Handle mouse button release.
                    if (event.button.button == SDL_BUTTON_LEFT) {
                        is_moving = 0; // Stop movement.
                        if (selected_cursor) {
                            // Update base position for the selected cursor.
                            for (int i = 0; i < num_cursors; i++) {
                                if (cursors[i] == selected_cursor) {
                                    base_x[i] = selected_cursor->x;
                                    base_y[i] = selected_cursor->y;
                                    break;
                                }
                            }
                        }
                    }
                    break;

                case SDL_MOUSEMOTION: // Handle cursor movement.
                    if (is_moving && selected_cursor) {
                        handleMovement(event.motion.x, event.motion.y); // Move the selected cursor.
                    }
                    break;

                case SDL_MOUSEWHEEL: // Handle zoom.
                    if (selected_cursor) {
                        handleZoom(event.wheel.y > 0); // Zoom in or out based on the wheel direction.
                    }
                    break;

                case SDL_KEYDOWN: // Handle keyboard input.
                    if (selected_cursor) {
                        if (event.key.keysym.sym == SDLK_r) { // Rotate clockwise.
                            applyRotationToCursor(selected_cursor, 15);
                        } else if (event.key.keysym.sym == SDLK_e) { // Rotate counterclockwise.
                            applyRotationToCursor(selected_cursor, -15);
                        } else if (event.key.keysym.sym == SDLK_DELETE) { // Delete the selected cursor.
                            handleDeletion();
                        }
                    }
                    break;

                default:
                    break;
            }
        }

        // Step 7: Clear the screen.
        SDL_SetRenderDrawColor(renderer, 0, 0, 0, 255);
        SDL_RenderClear(renderer);

        // Step 8: Update and render each cursor.
        for (int i = 0; i < num_cursors; i++) {
            if (cursors[i]->visible) {
                // Calculate the animated position using polar coordinates.
                int anim_x = base_x[i] + radius * cos(angles[i]);
                int anim_y = base_y[i] + radius * sin(angles[i]);

                // Rotate the cursor.
                rotateCursor(cursors[i], 10);

                // Update position if the cursor is not being moved.
                if (!is_moving || cursors[i] != selected_cursor) {
                    cursors[i]->x = anim_x;
                    cursors[i]->y = anim_y;
                }
            }
            // Increment the angle for the next frame.
            angles[i] += 0.05;
        }

        // Step 9: Draw each cursor on the screen.
        drawLine(renderer, &c1, 100);
        drawSquare(renderer, &c2, 50);
        drawFilledSquare(renderer, &c3, 50);
        drawCircle(renderer, &c4, 40);
        drawFilledCircle(renderer, &c5, 40);
        drawArc(renderer, &c6, 50, 0, 180);

        // Step 10: Present the updated frame.
        SDL_RenderPresent(renderer);
        SDL_Delay(50); // Control animation speed.
    }
}


// Function to animate cursors bouncing off screen edges.
//
// This function animates multiple Cursor objects, each moving in straight lines.
// When a cursor collides with the edge of the screen, it bounces back in the opposite direction.
// Each cursor moves independently, and user interactions like selection, movement, zooming,
// rotation, and deletion are supported.
//
// Parameters:
// - SDL_Renderer* renderer: The SDL renderer used to draw and animate the cursors.
//
// Logic:
// 1. **Cursor Initialization**:
//    - Several Cursor objects are created with unique colors, shapes, and initial positions.
//    - These cursors are stored in an array for efficient management.
// 2. **Velocity Initialization**:
//    - Each cursor is assigned an independent velocity (`dx`, `dy`) for movement in both
//      horizontal and vertical directions.
// 3. **Animation Loop**:
//    - The program enters a continuous loop to animate and render the cursors.
//    - Each cursor's position is updated dynamically based on its velocity.
//    - If a cursor collides with a screen edge, its velocity in the corresponding direction is inverted.
// 4. **User Interactions**:
//    - **Selection**: Cursors can be selected by clicking within their boundaries.
//    - **Movement**: Selected cursors can be dragged using the mouse.
//    - **Zooming**: The mouse wheel adjusts the size of the selected cursor.
//    - **Rotation**: Keyboard keys rotate the selected cursor clockwise or counterclockwise.
//    - **Deletion**: The `DELETE` key removes the selected cursor.
// 5. **Rendering and Display**:
//    - Cursors are rendered based on their updated attributes (position, scale, visibility).
//    - The screen is updated continuously to display the animations.
//
// Notes:
// - The animation loop runs until the user exits the program via an `SDL_QUIT` event.
// - Interactions like selection or movement temporarily pause the animation for the
//   selected cursor.
//
// Example Usage:
// animateDrawingbond(renderer); // Starts the bouncing animation for multiple cursors.
void animateDrawingbond(SDL_Renderer* renderer) {
    // Step 1: Define Cursor objects, each representing a unique type of shape.
    // These cursors are initialized with different colors, sizes, and positions.
    Cursor c1 =     createCursor(200, 200, (SDL_Color){255, 255, 0, 255}, 7, 1);  
    Cursor c2 =     createCursor(400, 300, (SDL_Color){0, 255, 255, 255}, 13, 1);  
    Cursor c3 =     createCursor(600, 400, (SDL_Color){255, 0, 0, 255}, 20, 1);    
    Cursor c4 =     createCursor(200, 400, (SDL_Color){0, 255, 0, 255}, 17, 1);   
    Cursor c5 =     createCursor(400, 500, (SDL_Color){255, 165, 0, 255}, 30, 1); 
    Cursor c6 =     createCursor(600, 200, (SDL_Color){128, 0, 128, 255}, 28, 1);  
    
    // Step 2: Store pointers to all cursors in an array for easy management.
    Cursor* cursors[] = {&c1, &c2, &c3, &c4, &c5, &c6};
    int num_cursors = sizeof(cursors) / sizeof(cursors[0]);

    // Step 3: Initialize velocity arrays for each cursor.
    // Each cursor is assigned initial x and y velocities (dx, dy) for movement.
    int dx[num_cursors]; // Velocity in the x-direction.
    int dy[num_cursors]; // Velocity in the y-direction.
    for (int i = 0; i < num_cursors; i++) {
        dx[i] = (i % 2 == 0) ? 5 : -5;  // Alternate directions for x.
        dy[i] = (i % 2 == 0) ? 5 : -5;  // Alternate directions for y.
    }

    // Step 4: Main loop control variable.
    int running = 1;
    SDL_Event event;

    // Step 5: Main animation loop.
    while (running) {
        // Step 5.1: Handle SDL events (e.g., quit, mouse, keyboard).
        while (SDL_PollEvent(&event)) {
            switch (event.type) {
                case SDL_QUIT: // Exit the loop on quit event.
                    running = 0;
                    break;
                case SDL_MOUSEBUTTONDOWN: // Handle left mouse button press.
                    if (event.button.button == SDL_BUTTON_LEFT) {
                        // Check if a cursor is selected based on the mouse click position.
                        handleSelection(event.button.x, event.button.y, cursors, num_cursors);
                    }
                    break;
                case SDL_MOUSEMOTION: // Handle mouse movement.
                    if (event.motion.state & SDL_BUTTON_LMASK) {
                        // Move the selected cursor based on mouse coordinates.
                        handleMovement(event.motion.x, event.motion.y);
                    }
                    break;
                case SDL_MOUSEWHEEL: // Handle mouse wheel input.
                    // Zoom in or out on the selected cursor.
                    handleZoom(event.wheel.y > 0);
                    break;
                case SDL_KEYDOWN: // Handle keyboard input.
                    if (event.key.keysym.sym == SDLK_r) {
                        // Rotate the selected cursor clockwise by 15 degrees.
                        applyRotationToCursor(selected_cursor, 15);
                    }
                    if (event.key.keysym.sym == SDLK_e) {
                        // Rotate the selected cursor counterclockwise by 15 degrees.
                        applyRotationToCursor(selected_cursor, -15);
                    }
                    if (event.key.keysym.sym == SDLK_DELETE) {
                        // Delete the selected cursor.
                        handleDeletion();
                    }
                    break;
                default:
                    break;
            }
        }

        // Step 6: Clear the screen.
        SDL_SetRenderDrawColor(renderer, 0, 0, 0, 255); // Black background.
        SDL_RenderClear(renderer);

        // Step 7: Update cursor positions and handle bouncing.
        for (int i = 0; i < num_cursors; i++) {
            if (cursors[i]->visible) {
                // Check for collisions with the screen edges.
                // Reverse velocity if the cursor hits an edge.
                if (cursors[i]->x <= 0 || cursors[i]->x >= SCREEN_WIDTH) dx[i] = -dx[i];
                if (cursors[i]->y <= 0 || cursors[i]->y >= SCREEN_HEIGHT) dy[i] = -dy[i];

                // Update the position of the cursor based on its velocity.
                cursors[i]->x += dx[i];
                cursors[i]->y += dy[i];

                // Appliquer une rotation au curseur
                rotateCursor(cursors[i], 10);
            }
        }

        // Step 8: Render all cursors on the screen.
        // Each cursor is drawn based on its shape and attributes.
        drawLine(renderer, &c1, 100); // Draw a line.
        drawSquare(renderer, &c2, 50); // Draw a square.
        drawFilledSquare(renderer, &c3, 50); // Draw a filled square.
        drawCircle(renderer, &c4, 40); // Draw a circle.
        drawFilledCircle(renderer, &c5, 40); // Draw a filled circle.
        drawArc(renderer, &c6, 50, 0, 180); // Draw an arc.

        // Step 9: Present the updated frame.
        SDL_RenderPresent(renderer);

        // Step 10: Delay to control the animation speed.
        SDL_Delay(100);
    }
}

// Function to animate cursors with continuous rotation.
//
// This function animates multiple Cursor objects by applying a continuous rotation
// to their shapes. The cursors remain stationary at their respective positions, and
// only their rotation angles are updated over time. User interactions such as selection,
// movement, zooming, rotation, and deletion are also supported.
//
// Parameters:
// - SDL_Renderer* renderer: The SDL renderer used to draw and animate the cursors.
//
// Logic:
// 1. **Cursor Initialization**:
//    - Several Cursor objects are created with unique colors, shapes, and initial positions.
//    - These cursors are stored in an array for efficient management.
// 2. **Animation Loop**:
//    - The program enters a continuous loop to animate and render the cursors.
//    - Each cursor's rotation angle is incremented in every frame, giving the effect
//      of continuous spinning.
// 3. **User Interactions**:
//    - **Selection**: Cursors can be selected by clicking within their boundaries.
//    - **Movement**: Selected cursors can be dragged using the mouse.
//    - **Zooming**: The mouse wheel adjusts the size of the selected cursor.
//    - **Rotation**: Keyboard keys apply additional rotation to the selected cursor.
//    - **Deletion**: The `DELETE` key removes the selected cursor.
// 4. **Rendering and Display**:
//    - Cursors are rendered based on their updated attributes (rotation angle, position, scale).
//    - The screen is updated continuously to display the animations.
//
// Notes:
// - The animation loop runs until the user exits the program via an `SDL_QUIT` event.
// - Interactions like selection or movement temporarily pause user-triggered rotations.
//
// Example Usage:
// animateRotation2(renderer); // Starts the continuous rotation animation for multiple cursors.
void animateRotation2(SDL_Renderer* renderer) {
    // Step 1: Define Cursor objects, each representing a unique type of shape.
    // These cursors are initialized with different colors, sizes, and positions.
    Cursor c1 =     createCursor(200, 200, (SDL_Color){255, 255, 0, 255}, 7, 1);  
    Cursor c2 =     createCursor(400, 300, (SDL_Color){0, 255, 255, 255}, 13, 1);  
    Cursor c3 =     createCursor(600, 400, (SDL_Color){255, 0, 0, 255}, 20, 1);    
    Cursor c4 =     createCursor(200, 400, (SDL_Color){0, 255, 0, 255}, 17, 1);   
    Cursor c5 =     createCursor(400, 500, (SDL_Color){255, 165, 0, 255}, 30, 1); 
    Cursor c6 =     createCursor(600, 200, (SDL_Color){128, 0, 128, 255}, 28, 1);

    // Step 2: Store pointers to all cursors in an array for easy management.
    Cursor* cursors[] = {&c1, &c2, &c3, &c4, &c5, &c6};
    int num_cursors = sizeof(cursors) / sizeof(cursors[0]);

    int running = 1; // Flag to control the main loop.
    SDL_Event event;

    // Step 3: Main animation loop.
    while (running) {
        // Step 3.1: Handle SDL events (e.g., quit, mouse, keyboard).
        while (SDL_PollEvent(&event)) {
            switch (event.type) {
                case SDL_QUIT: // Exit the loop on quit event.
                    running = 0;
                    break;
                case SDL_MOUSEBUTTONDOWN: // Handle left mouse button press.
                    if (event.button.button == SDL_BUTTON_LEFT) {
                        // Check if a cursor is selected based on the mouse click position.
                        handleSelection(event.button.x, event.button.y, cursors, num_cursors);
                    }
                    break;
                case SDL_MOUSEMOTION: // Handle mouse movement.
                    if (event.motion.state & SDL_BUTTON_LMASK) {
                        // Move the selected cursor based on mouse coordinates.
                        handleMovement(event.motion.x, event.motion.y);
                    }
                    break;
                case SDL_MOUSEWHEEL: // Handle mouse wheel input.
                    // Zoom in or out on the selected cursor.
                    handleZoom(event.wheel.y > 0);
                    break;
                case SDL_KEYDOWN: // Handle keyboard input.
                    if (event.key.keysym.sym == SDLK_r) {
                        // Rotate the selected cursor clockwise by 15 degrees.
                        applyRotationToCursor(selected_cursor, 15);
                    }
                    if (event.key.keysym.sym == SDLK_e) {
                        // Rotate the selected cursor counterclockwise by 15 degrees.
                        applyRotationToCursor(selected_cursor, -15);
                    }
                    if (event.key.keysym.sym == SDLK_DELETE) {
                        // Delete the selected cursor.
                        handleDeletion();
                    }
                    break;
                default:
                    break;
            }
        }

        // Step 4: Clear the screen
        SDL_SetRenderDrawColor(renderer, 0, 0, 0, 255); // Black background.
        SDL_RenderClear(renderer);

        // Step 5: Update the rotation angle for each cursor.
        for (int i = 0; i < num_cursors; i++) {
            if (cursors[i]->visible) {
                // Increment the cursor's rotation angle to create a continuous spinning effect.
                rotateCursor2(cursors[i], 10); // Rotate by 10 degrees per frame.
            }
        }

        // Step 6: Render all cursors on the screen.
        // Each cursor is drawn based on its shape and attributes.
        drawLine(renderer, &c1, 100); // Draw a line.
        drawSquare(renderer, &c2, 50); // Draw a square.
        drawFilledSquare(renderer, &c3, 50); // Draw a filled square.
        drawCircle(renderer, &c4, 40); // Draw a circle.
        drawFilledCircle(renderer, &c5, 40); // Draw a filled circle.
        drawArc(renderer, &c6, 50, 0, 180); // Draw an arc.

        // Step 7: Present the updated frame.
        SDL_RenderPresent(renderer);

        // Step 8: Delay to control the animation speed.
        SDL_Delay(100);
    }
}


// Function to dynamically render and display multiple cursors.
//
// This function animates multiple Cursor objects by rendering their shapes dynamically
// at specific positions. The cursors do not move or rotate automatically but can be
// interacted with by the user for actions like selection, movement, zooming, rotation,
// and deletion.
//
// Parameters:
// - SDL_Renderer* renderer: The SDL renderer used to draw and display the cursors.
//
// Logic:
// 1. **Cursor Initialization**:
//    - Several Cursor objects are created with unique colors, shapes, and initial positions.
//    - These cursors are stored in an array for efficient management.
// 2. **User Interactions**:
//    - **Selection**: Cursors can be selected by clicking within their boundaries.
//    - **Movement**: Selected cursors can be dragged using the mouse.
//    - **Zooming**: The mouse wheel adjusts the size of the selected cursor.
//    - **Rotation**: Keyboard keys apply rotation to the selected cursor.
//    - **Deletion**: The `DELETE` key removes the selected cursor.
// 3. **Rendering and Display**:
//    - Cursors are rendered based on their attributes (position, scale, visibility, angle).
//    - The screen is updated continuously to display the cursors.
//
// Notes:
// - The animation loop runs until the user exits the program via an `SDL_QUIT` event.
// - The function provides a foundation for interactive rendering without automated motion.
//
// Example Usage:
// animateDrawing(renderer); // Starts rendering multiple cursors dynamically.
void animateDrawing(SDL_Renderer* renderer) {
    // Step 1: Define Cursor objects, each representing a unique type of shape.
    // These cursors are initialized with different colors, sizes, and positions.
    Cursor c1 =     createCursor(200, 200, (SDL_Color){255, 255, 0, 255}, 7, 1);  
    Cursor c2 =     createCursor(400, 300, (SDL_Color){0, 255, 255, 255}, 13, 1);
    Cursor c3 =     createCursor(600, 400, (SDL_Color){255, 0, 0, 255}, 20, 1);    
    Cursor c4 =     createCursor(200, 400, (SDL_Color){0, 255, 0, 255}, 17, 1);   
    Cursor c5 =     createCursor(400, 500, (SDL_Color){255, 165, 0, 255}, 30, 1); 
    Cursor c6 =     createCursor(600, 200, (SDL_Color){128, 0, 128, 255}, 28, 1);  
    
    // Step 2: Store pointers to all cursors in an array for easy management.
    Cursor* cursors[] = {&c1, &c2, &c3, &c4, &c5, &c6};

    int num_cursors = sizeof(cursors) / sizeof(cursors[0]); 

    int running = 1; // Flag to control the main loop.
    SDL_Event event;

    // Step 3: Main rendering and interaction loop.
    while (running) {
        // Step 3.1: Handle SDL events (e.g., quit, mouse, keyboard).
        while (SDL_PollEvent(&event)) {
            switch (event.type) {
                case SDL_QUIT: // Exit the loop on quit event.
                    running = 0; 
                    break;

                case SDL_MOUSEBUTTONDOWN: // Handle left mouse button press.
                    if (event.button.button == SDL_BUTTON_LEFT) {
                        // Check if a cursor is selected based on the mouse click position.
                        handleSelection(event.button.x, event.button.y, cursors, num_cursors); // Select a shape.
                    }
                    break;

                case SDL_MOUSEMOTION: // Handle mouse movement.
                    if (event.motion.state & SDL_BUTTON_LMASK) {
                        // Move the selected cursor based on mouse coordinates.
                        handleMovement(event.motion.x, event.motion.y);
                    }
                    break;

                case SDL_MOUSEWHEEL: // Handle mouse wheel input.
                    // Zoom in or out on the selected cursor.
                    handleZoom(event.wheel.y > 0); 
                    break;

                case SDL_KEYDOWN: // Handle keyboard input.
                    if (event.key.keysym.sym == SDLK_r) { 
                        // Rotate the selected cursor clockwise by 15 degrees.
                        applyRotationToCursor(selected_cursor, 15);
                    }
                    if (event.key.keysym.sym == SDLK_e) { 
                        // Rotate the selected cursor counterclockwise by 15 degrees.
                        applyRotationToCursor(selected_cursor, -15);
                    }
                    if (event.key.keysym.sym == SDLK_DELETE) { 
                        // Delete the selected cursor.
                        handleDeletion();
                    }
                    break;

                default:
                    break;
            }
        }

        // Step 4: Clear the screen.
        SDL_SetRenderDrawColor(renderer, 0, 0, 0, 255); // Black background.
        SDL_RenderClear(renderer);

        // Step 5: Render all cursors on the screen.
        // Each cursor is drawn based on its shape and attributes.
        drawLine(renderer, &c1, 100); // Draw a line.
        drawSquare(renderer, &c2, 50); // Draw a square.
        drawFilledSquare(renderer, &c3, 50); // Draw a filled square.
        drawCircle(renderer, &c4, 40); // Draw a circle.
        drawFilledCircle(renderer, &c5, 40); // Draw a filled circle.
        drawArc(renderer, &c6, 50, 0, 180); // Draw an arc.

        // Step 6: Present the updated frame.
        SDL_RenderPresent(renderer);

        // Step 7: Delay to control the rendering speed.
        SDL_Delay(50);
    }
}






/* int main() {
    // Step 1: Initialize SDL and create a window and renderer.
    if (SDL_Init(SDL_INIT_VIDEO) != 0) {
        // Check if SDL failed to initialize and print an error message if it did.
        printf("SDL_Init Error: %s\n", SDL_GetError());
        return 1;
    }

    // Create an SDL window with the title "Animation Window".
    SDL_Window* win = SDL_CreateWindow("Animation Window", 100, 100, 800, 600, SDL_WINDOW_SHOWN);
    if (win == NULL) {
        // If the window creation fails, print an error message and quit SDL.
        printf("SDL_CreateWindow Error: %s\n", SDL_GetError());
        SDL_Quit();
        return 1;
    }

    // Create an SDL renderer for the window.
    SDL_Renderer* renderer = SDL_CreateRenderer(win, -1, SDL_RENDERER_ACCELERATED | SDL_RENDERER_PRESENTVSYNC);
    if (renderer == NULL) {
        // If the renderer creation fails, print an error message, destroy the window, and quit SDL.
        SDL_DestroyWindow(win);
        printf("SDL_CreateRenderer Error: %s\n", SDL_GetError());
        SDL_Quit();
        return 1;
    }

    animateDrawingsnail(renderer);

    // Step 4: Cleanup SDL resources and exit the program.
    SDL_DestroyRenderer(renderer); // Destroy the renderer.
    SDL_DestroyWindow(win);        // Destroy the window.
    SDL_Quit();                    // Quit SDL.
    return 0; // Return 0 to indicate successful execution.
} */