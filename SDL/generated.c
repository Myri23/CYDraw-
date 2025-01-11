#include "config.h"
#include "draw.h"
#include "handle.h"
#include "newcursor.h"

void animateDrawingsnail(SDL_Renderer* renderer) {
Cursor c = createCursor(200, 200, (SDL_Color){255, 0, 0, 255}, 10, 1);

Cursor* cursors[] = {
    &c
};

    // Movement and rotation instructions

    int num_cursors = sizeof(cursors) / sizeof(cursors[0]);

    // Base positions for animation
    int base_x[num_cursors];
    int base_y[num_cursors];
    for (int i = 0; i < num_cursors; i++) {
        base_x[i] = cursors[i]->x;
        base_y[i] = cursors[i]->y;
    }

    double angles[num_cursors]; // Angles for each cursor
    for (int i = 0; i < num_cursors; i++) {
        angles[i] = i * (2 * M_PI / num_cursors); // Distribute cursors evenly
    }

    int radius = 50; // Radius for animation
    int running = 1;
    int is_moving = 0; // Indicator for movement
    SDL_Event event;

    while (running) {
        while (SDL_PollEvent(&event)) {
            switch (event.type) {
                case SDL_QUIT:
                    running = 0;
                    break;

                case SDL_MOUSEBUTTONDOWN:
                    if (event.button.button == SDL_BUTTON_LEFT) {
                        handleSelection(event.button.x, event.button.y, cursors, num_cursors);
                        if (selected_cursor) {
                            is_moving = 1; // Activate movement mode
                        } else {
                            is_moving = 0; // No cursor selected
                        }
                    }
                    break;

                case SDL_MOUSEBUTTONUP:
                    if (event.button.button == SDL_BUTTON_LEFT) {
                        is_moving = 0; // Stop movement

                        // Update base positions for the selected cursor
                        if (selected_cursor) {
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

                case SDL_MOUSEMOTION:
                    if (is_moving && selected_cursor) {
                        handleMovement(event.motion.x, event.motion.y);
                    }
                    break;

                case SDL_MOUSEWHEEL:
                    if (selected_cursor) { // Only zoom if a cursor is selected
                        handleZoom(event.wheel.y > 0);
                    }
                    break;

                case SDL_KEYDOWN:
                    if (selected_cursor) { // Ensure actions only apply to a selected cursor
                        if (event.key.keysym.sym == SDLK_r) { // Rotate clockwise
                            applyRotationToCursor(selected_cursor, 15);
                        }
                        if (event.key.keysym.sym == SDLK_e) { // Rotate counterclockwise
                            applyRotationToCursor(selected_cursor, -15);
                        }
                        if (event.key.keysym.sym == SDLK_DELETE) { // Delete the selected shape
                            handleDeletion();
                        }
                    }
                    break;

                default:
                    break;
            }
        }

        SDL_SetRenderDrawColor(renderer, 0, 0, 0, 255);
        SDL_RenderClear(renderer);

        // Animation and display of cursors
        for (int i = 0; i < num_cursors; i++) {
            if (cursors[i]->visible) {
                // Calculate the animated position
                int anim_x = base_x[i] + radius * cos(angles[i]);
                int anim_y = base_y[i] + radius * sin(angles[i]);

                // Rotate the shape
                rotateCursor(cursors[i], 10);

                // Update animated position only if not being moved
                if (!is_moving || cursors[i] != selected_cursor) {
                    cursors[i]->x = anim_x;
                    cursors[i]->y = anim_y;
                }
            }
            // Advance the angle for animation
            angles[i] += 0.05;
        }
        // Drawing instructions
drawSquare(renderer, &c, 20); // Draw a square
drawSquare(renderer, &c, 40); // Draw a square
drawSquare(renderer, &c, 60); // Draw a square
drawSquare(renderer, &c, 80); // Draw a square
drawSquare(renderer, &c, 100); // Draw a square
drawSquare(renderer, &c, 120); // Draw a square
drawCircle(renderer, &c, 120); // Draw a circle

        SDL_RenderPresent(renderer);
        SDL_Delay(50);
    }
}

void animateDrawingbond(SDL_Renderer* renderer) {
Cursor c = createCursor(200, 200, (SDL_Color){255, 0, 0, 255}, 10, 1);

Cursor* cursors[] = {
    &c
};

    // Movement instructions and rotation instructions

    int num_cursors = sizeof(cursors) / sizeof(cursors[0]);

    // Initialize individual speeds for each cursor
    int dx[num_cursors];
    int dy[num_cursors];
    for (int i = 0; i < num_cursors; i++) {
        dx[i] = (i % 2 == 0) ? 5 : -5;  // Alternating initial direction
        dy[i] = (i % 2 == 0) ? 5 : -5;
    }

    int running = 1;
    SDL_Event event;

    while (running) {
        while (SDL_PollEvent(&event)) {
            switch (event.type) {
                case SDL_QUIT:
                    running = 0;
                    break;
                case SDL_MOUSEBUTTONDOWN:
                    if (event.button.button == SDL_BUTTON_LEFT) {
                        handleSelection(event.button.x, event.button.y, cursors, num_cursors);
                    }
                    break;
                case SDL_MOUSEMOTION:
                    if (event.motion.state & SDL_BUTTON_LMASK) {
                        handleMovement(event.motion.x, event.motion.y);
                    }
                    break;
                case SDL_MOUSEWHEEL:
                    handleZoom(event.wheel.y > 0);
                    break;
                case SDL_KEYDOWN:
                    if (event.key.keysym.sym == SDLK_r) {
                        applyRotationToCursor(selected_cursor, 15);
                    }
                    if (event.key.keysym.sym == SDLK_e) {
                        applyRotationToCursor(selected_cursor, -15);
                    }
                    if (event.key.keysym.sym == SDLK_DELETE) {
                        handleDeletion();
                    }
                    break;
                default:
                    break;
            }
        }

        SDL_SetRenderDrawColor(renderer, 0, 0, 0, 255);
        SDL_RenderClear(renderer);

        for (int i = 0; i < num_cursors; i++) {
            if (cursors[i]->visible) {
                if (cursors[i]->x <= 0 || cursors[i]->x >= SCREEN_WIDTH) dx[i] = -dx[i];
                if (cursors[i]->y <= 0 || cursors[i]->y >= SCREEN_HEIGHT) dy[i] = -dy[i];

                cursors[i]->x += dx[i];
                cursors[i]->y += dy[i];

                rotateCursor(cursors[i], 10);
           }
       }
        // Drawing instructions
        drawSquare(renderer, &c, 20); // Draw a square;
        drawSquare(renderer, &c, 40); // Draw a square;
        drawSquare(renderer, &c, 60); // Draw a square;
        drawSquare(renderer, &c, 80); // Draw a square;
        drawSquare(renderer, &c, 100); // Draw a square;
        drawSquare(renderer, &c, 120); // Draw a square;
        drawCircle(renderer, &c, 120); // Draw a circle;

        SDL_RenderPresent(renderer);
        SDL_Delay(100);
        }
    }


void animateRotation2(SDL_Renderer* renderer) {
    // Defining cursors with different drawing types
Cursor c = createCursor(200, 200, (SDL_Color){255, 0, 0, 255}, 10, 1);

Cursor* cursors[] = {
    &c
};

    // movement and rotation instructions

    int num_cursors = sizeof(cursors) / sizeof(cursors[0]);

    int running = 1;
    SDL_Event event;

    while (running) {
        while (SDL_PollEvent(&event)) {
            switch (event.type) {
                case SDL_QUIT:
                    running = 0;
                    break;
                case SDL_MOUSEBUTTONDOWN:
                    if (event.button.button == SDL_BUTTON_LEFT) {
                        handleSelection(event.button.x, event.button.y, cursors, num_cursors);
                    }
                    break;
                case SDL_MOUSEMOTION:
                    if (event.motion.state & SDL_BUTTON_LMASK) {
                        handleMovement(event.motion.x, event.motion.y);
                    }
                    break;
                case SDL_MOUSEWHEEL:
                    handleZoom(event.wheel.y > 0);
                    break;
                case SDL_KEYDOWN:
                    if (event.key.keysym.sym == SDLK_r) {
                        applyRotationToCursor(selected_cursor, 15);
                    }
                    if (event.key.keysym.sym == SDLK_e) {
                        applyRotationToCursor(selected_cursor, -15);
                    }
                    if (event.key.keysym.sym == SDLK_DELETE) {
                        handleDeletion();
                    }
                    break;
                default:
                    break;
            }
        }

        // Clear the screen
        SDL_SetRenderDrawColor(renderer, 0, 0, 0, 255);
        SDL_RenderClear(renderer);

        // Draw the shapes in rotation
        for (int i = 0; i < num_cursors; i++) {
            if (cursors[i]->visible) {
                rotateCursor2(cursors[i], 10); // Specific rotation for animateRotation2

            }
        }
        // Drawing instructions 
        drawSquare(renderer, &c, 20); // Draw a square;
        drawSquare(renderer, &c, 40); // Draw a square;
        drawSquare(renderer, &c, 60); // Draw a square;
        drawSquare(renderer, &c, 80); // Draw a square;
        drawSquare(renderer, &c, 100); // Draw a square;
        drawSquare(renderer, &c, 120); // Draw a square;
        drawCircle(renderer, &c, 120); // Draw a circle;

        SDL_RenderPresent(renderer);
        SDL_Delay(100);
    }
}

void animateDrawing(SDL_Renderer* renderer) {
Cursor c = createCursor(200, 200, (SDL_Color){255, 0, 0, 255}, 10, 1);

Cursor* cursors[] = {
    &c
};

    // movement and rotation instructions 

    int num_cursors = sizeof(cursors) / sizeof(cursors[0]);

    int running = 1;
    while (running) {
        SDL_Event event;
        while (SDL_PollEvent(&event)) {
            switch (event.type) {
                case SDL_QUIT:
                    running = 0;
                    break;
                case SDL_MOUSEBUTTONDOWN:
                    if (event.button.button == SDL_BUTTON_LEFT) {
                        handleSelection(event.button.x, event.button.y, cursors, num_cursors);
                    }
                    break;
                case SDL_MOUSEMOTION:
                    if (event.motion.state & SDL_BUTTON_LMASK) {
                        handleMovement(event.motion.x, event.motion.y);
                    }
                    break;
                case SDL_MOUSEWHEEL:
                    handleZoom(event.wheel.y > 0);
                    break;
                case SDL_KEYDOWN:
                    if (event.key.keysym.sym == SDLK_r) { // Rotate clockwise when 'R' is pressed.
                        applyRotationToCursor(selected_cursor, 15);
                    }
                    if (event.key.keysym.sym == SDLK_e) { // Rotate counterclockwise when 'E' is pressed.
                        applyRotationToCursor(selected_cursor, -15);
                    }
                    if (event.key.keysym.sym == SDLK_DELETE) { // Delete the selected shape.
                        handleDeletion();
                    }
                    break;
                default:
                    break;
            }
        }

        // Clear the screen
        SDL_SetRenderDrawColor(renderer, 0, 0, 0, 255);
        SDL_RenderClear(renderer);

        // Drawing instructions
        drawSquare(renderer, &c, 20); // Draw a square;
        drawSquare(renderer, &c, 40); // Draw a square;
        drawSquare(renderer, &c, 60); // Draw a square;
        drawSquare(renderer, &c, 80); // Draw a square;
        drawSquare(renderer, &c, 100); // Draw a square;
        drawSquare(renderer, &c, 120); // Draw a square;
        drawCircle(renderer, &c, 120); // Draw a circle;

        SDL_RenderPresent(renderer);
    }
}

int main() {

    // Initialize SDL
    if (SDL_Init(SDL_INIT_VIDEO) != 0) {
        printf("SDL initialization error : %s\n", SDL_GetError());
        return 1;
    }

    SDL_Window* window = SDL_CreateWindow("SDL Cursor Drawing", SDL_WINDOWPOS_CENTERED, SDL_WINDOWPOS_CENTERED, SCREEN_WIDTH, SCREEN_HEIGHT, SDL_WINDOW_SHOWN);
    if (!window) {
        printf("window creation error : %s\n", SDL_GetError());
        SDL_Quit();
        return 1;
    }

    SDL_Renderer* renderer = SDL_CreateRenderer(window, -1, SDL_RENDERER_ACCELERATED);
    if (!renderer) {
        SDL_DestroyWindow(window);
        printf("Renderer creation error : %s\n", SDL_GetError());
        SDL_Quit();
        return 1;
    }

    // Animation mode
      animateDrawing(renderer);    // Clean up and exit
    SDL_DestroyRenderer(renderer);
    SDL_DestroyWindow(window);
    SDL_Quit();

    return 0;
}
