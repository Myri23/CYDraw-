#include "draw.h"
#include "config.h"
#include <math.h>
#include <SDL2/SDL.h>


// ======================================================
// DRAW FUNCTIONS
// ======================================================

// This section contains functions responsible for rendering different shapes
// (lines, squares, circles, arcs, etc.) on the screen. These shapes are drawn
// based on the attributes of the `Cursor` object, such as position, scale, color,
// thickness, and rotation.
//
// Functions in this section:
// - drawLine: Draws a straight line with configurable thickness and rotation.
// - drawSquare: Draws the outline of a square with configurable size, thickness, and rotation.
// - drawFilledSquare: Draws a filled square centered at the cursor's position.
// - drawCircle: Draws the outline of a circle with configurable thickness.
// - drawFilledCircle: Draws a filled circle centered at the cursor's position.
// - drawArc: Draws a partial circle (arc) with configurable start and end angles.


// Function to draw a line with a specified Cursor object.
//
// This function draws a line starting from the cursor's position (`x`, `y`)
// in the direction of its current angle. The length of the line and its
// thickness are determined by the cursor's attributes.
//
// Parameters:
// - SDL_Renderer* renderer: The SDL renderer used to draw the line.
// - Cursor* cursor: A pointer to the Cursor object, which provides the position,
//   angle, color, and thickness for the line.
// - int length: The length of the line to be drawn, scaled by the cursor's scale.
//
// Notes:
// - The line respects the `angle` attribute of the cursor, allowing it to be drawn
//   at any orientation.
// - The `thickness` attribute is used to draw parallel lines, simulating a thicker line.
//
// Example Usage:
// Cursor cursor = createCursor(300, 300, {0, 255, 0, 255}, 5, 1);
// drawLine(renderer, &cursor, 100); // Draws a 100-pixel green line with 5-pixel thickness.
void drawLine(SDL_Renderer* renderer, Cursor* cursor, int length) {
    if(cursor->visible){
        int scaled_length = (int)(length * cursor->scale);  // Adjust line length based on the cursor's scale.
        float rad_angle = cursor->angle * M_PI / 180.0;     // Convert the angle to radians.

        // Starting position of the line.
        int x_start = cursor->x;
        int y_start = cursor->y;

        // Ending position of the line, calculated using the angle and length.
        int x_end = x_start + scaled_length * cos(rad_angle);
        int y_end = y_start + scaled_length * sin(rad_angle);

        // Set the drawing color based on the cursor's RGBA values.
        SDL_SetRenderDrawColor(renderer, cursor->color.r, cursor->color.g, cursor->color.b, cursor->color.a);

        // Draw parallel lines to simulate thickness.
        for (int offset = -cursor->thickness / 2; offset <= cursor->thickness / 2; offset++) {
            SDL_RenderDrawLine(renderer,
                x_start + offset * cos(rad_angle + M_PI / 2),  // Offset the start point perpendicularly.
                y_start + offset * sin(rad_angle + M_PI / 2),  // Offset the start point perpendicularly.
                x_end + offset * cos(rad_angle + M_PI / 2),    // Offset the end point perpendicularly.
                y_end + offset * sin(rad_angle + M_PI / 2)     // Offset the end point perpendicularly.
            );
        }
    }
}


// Function to draw a square using a Cursor object.
//
// This function draws a square centered at the cursor's current position (`x`, `y`).
// The square's size is determined by the `size` parameter, scaled by the cursor's `scale` attribute.
// It also respects the cursor's `angle` for rotation and uses its `color` and `thickness` attributes
// to define the appearance of the square.
//
// Parameters:
// - SDL_Renderer* renderer: The SDL renderer used to draw the square.
// - Cursor* cursor: A pointer to the Cursor object that provides position, rotation angle,
//   color, thickness, and scaling factor for the square.
// - int size: The side length of the square before scaling.
//
// Implementation Details:
// - The square is defined by its four corners, calculated relative to the cursor's center (`x`, `y`).
// - Each corner is rotated around the cursor's center using the cursor's `angle`.
// - The square's thickness is simulated by drawing multiple lines around its edges.
// - The color of the square is set using `SDL_SetRenderDrawColor`.
//
// Notes:
// - The square's rotation is calculated using trigonometric functions (`cos` and `sin`).
// - Ensure the `cursor->angle` is in degrees, as the function converts it to radians.
//
// Example Usage:
// Cursor cursor = createCursor(300, 300, {255, 0, 0, 255}, 5, 1);
// drawSquare(renderer, &cursor, 50); // Draws a rotated red square with 50-pixel sides.
void drawSquare(SDL_Renderer* renderer, Cursor* cursor, int size) {
    if(cursor->visible){
        int scaled_size = (int)(size * cursor->scale);  // Adjust size based on the cursor's scale.
        int half_size = scaled_size / 2;

        // Define the initial corners of the square relative to the center (no rotation yet).
        int x1 = -half_size, y1 = -half_size; // Top-left corner
        int x2 = half_size, y2 = -half_size;  // Top-right corner
        int x3 = half_size, y3 = half_size;   // Bottom-right corner
        int x4 = -half_size, y4 = half_size;  // Bottom-left corner

        // Apply rotation and draw the square with thickness.
        for (int offset = 0; offset < cursor->thickness; offset++) {
            float rad_angle = cursor->angle * M_PI / 180.0; // Convert angle to radians.

            // Rotate each corner of the square around the cursor's center.
            int rotated_x1 = (int)(x1 * cos(rad_angle) - y1 * sin(rad_angle)) + cursor->x - offset;
            int rotated_y1 = (int)(x1 * sin(rad_angle) + y1 * cos(rad_angle)) + cursor->y - offset;

            int rotated_x2 = (int)(x2 * cos(rad_angle) - y2 * sin(rad_angle)) + cursor->x + offset;
            int rotated_y2 = (int)(x2 * sin(rad_angle) + y2 * cos(rad_angle)) + cursor->y - offset;

            int rotated_x3 = (int)(x3 * cos(rad_angle) - y3 * sin(rad_angle)) + cursor->x + offset;
            int rotated_y3 = (int)(x3 * sin(rad_angle) + y3 * cos(rad_angle)) + cursor->y + offset;

            int rotated_x4 = (int)(x4 * cos(rad_angle) - y4 * sin(rad_angle)) + cursor->x - offset;
            int rotated_y4 = (int)(x4 * sin(rad_angle) + y4 * cos(rad_angle)) + cursor->y + offset;

            // Set the color for drawing.
            SDL_SetRenderDrawColor(renderer, cursor->color.r, cursor->color.g, cursor->color.b, cursor->color.a);

            // Draw the four edges of the square.
            SDL_RenderDrawLine(renderer, rotated_x1, rotated_y1, rotated_x2, rotated_y2); // Top edge
            SDL_RenderDrawLine(renderer, rotated_x2, rotated_y2, rotated_x3, rotated_y3); // Right edge
            SDL_RenderDrawLine(renderer, rotated_x3, rotated_y3, rotated_x4, rotated_y4); // Bottom edge
            SDL_RenderDrawLine(renderer, rotated_x4, rotated_y4, rotated_x1, rotated_y1); // Left edge
        }
    }
}


// Function to draw a filled square using a Cursor object.
//
// This function draws a filled square centered at the cursor's current position (`x`, `y`).
// The square's size is determined by the `size` parameter, scaled by the cursor's `scale` attribute.
// It respects the cursor's `angle` for rotation and uses its `color` and `thickness` attributes
// to define the appearance of the square.
//
// Parameters:
// - SDL_Renderer* renderer: The SDL renderer used to draw the filled square.
// - Cursor* cursor: A pointer to the Cursor object that provides position, rotation angle,
//   color, thickness, and scaling factor for the square.
// - int size: The side length of the square before scaling.
//
// Implementation Details:
// - The square is drawn by filling in each pixel within its bounds, rotated around the cursor's center.
// - Each pixel is rotated individually using the cursor's `angle` to account for rotation.
// - The color is set using `SDL_SetRenderDrawColor`.
//
// Notes:
// - The rotation is calculated using trigonometric functions (`cos` and `sin`).
// - Ensure the `cursor->angle` is in degrees, as it is converted to radians for calculations.
//
// Example Usage:
// Cursor cursor = createCursor(300, 300, {0, 255, 0, 255}, 5, 1);
// drawFilledSquare(renderer, &cursor, 50); // Draws a filled green square with 50-pixel sides.
void drawFilledSquare(SDL_Renderer* renderer, Cursor* cursor, int size) {
    if(cursor->visible){
        int scaled_size = (int)(size * cursor->scale);  // Adjust size based on the cursor's scale.
        int half_size = scaled_size / 2;
        float rad_angle = cursor->angle * M_PI / 180.0; // Convert the angle to radians.

        // Set the color for the filled square.
        SDL_SetRenderDrawColor(renderer, cursor->color.r, cursor->color.g, cursor->color.b, cursor->color.a);

        // Loop through all pixels within the bounds of the square.
        for (int y = -half_size - cursor->thickness / 2; y <= half_size + cursor->thickness / 2; y++) {
            for (int x = -half_size - cursor->thickness / 2; x <= half_size + cursor->thickness / 2; x++) {
                // Rotate the pixel around the center of the square.
                int rotated_x = (int)(x * cos(rad_angle) - y * sin(rad_angle));
                int rotated_y = (int)(x * sin(rad_angle) + y * cos(rad_angle));

                // Draw the rotated pixel at the cursor's position.
                SDL_RenderDrawPoint(renderer, cursor->x + rotated_x, cursor->y + rotated_y);
            }
        }
    }
}


// Function to draw a circle using a Cursor object.
//
// This function draws the outline of a circle centered at the cursor's current position (`x`, `y`).
// The circle's radius is determined by the `radius` parameter, scaled by the cursor's `scale` attribute.
// The function respects the cursor's `color` and `thickness` attributes for the appearance of the circle.
//
// Parameters:
// - SDL_Renderer* renderer: The SDL renderer used to draw the circle.
// - Cursor* cursor: A pointer to the Cursor object that provides position, color,
//   thickness, and scaling factor for the circle.
// - int radius: The radius of the circle before scaling.
//
// Implementation Details:
// - The circle's points are calculated using the parametric equations of a circle:
//     x = r * cos(angle)
//     y = r * sin(angle)
// - Multiple concentric circles are drawn to simulate the thickness.
// - The `color` is set using `SDL_SetRenderDrawColor`.
//
// Notes:
// - Ensure the `cursor->thickness` is positive; otherwise, no circle will be drawn.
// - This function does not consider rotation, as circles are invariant to rotation.
//
// Example Usage:
// Cursor cursor = createCursor(300, 300, {0, 0, 255, 255}, 5, 1);
// drawCircle(renderer, &cursor, 50); // Draws a blue circle with a 50-pixel radius and 5-pixel thickness.
void drawCircle(SDL_Renderer* renderer, Cursor* cursor, int radius) {
    if(cursor->visible){
        int scaled_radius = (int)(radius * cursor->scale); // Adjust radius based on the cursor's scale.

        // Set the color for the circle's outline.
        SDL_SetRenderDrawColor(renderer, cursor->color.r, cursor->color.g, cursor->color.b, cursor->color.a);

        // Loop through each layer of thickness.
        for (int offset = 0; offset < cursor->thickness; offset++) {
            // Loop through 360 degrees to calculate and draw the circle points.
            for (int angle = 0; angle < 360; angle++) {
                int x = cursor->x + (scaled_radius + offset) * cos(angle * M_PI / 180.0); // x-coordinate of the point
                int y = cursor->y + (scaled_radius + offset) * sin(angle * M_PI / 180.0); // y-coordinate of the point
                SDL_RenderDrawPoint(renderer, x, y); // Draw the point on the renderer
            }
        }
    }
}


// Function to draw a filled circle using a Cursor object.
//
// This function draws a filled circle centered at the cursor's current position (`x`, `y`).
// The circle's radius is determined by the `radius` parameter, scaled by the cursor's `scale` attribute.
// The function respects the cursor's `color` attribute to define the appearance of the filled area.
//
// Parameters:
// - SDL_Renderer* renderer: The SDL renderer used to draw the filled circle.
// - Cursor* cursor: A pointer to the Cursor object that provides position, color,
//   and scaling factor for the filled circle.
// - int radius: The radius of the filled circle before scaling.
//
// Implementation Details:
// - The filled circle is drawn by iterating over all points within the bounding box of the circle.
// - For each point, the distance from the circle's center is calculated. If the distance
//   is less than or equal to the circle's radius, the point is drawn.
// - The `color` is set using `SDL_SetRenderDrawColor`.
//
// Notes:
// - Ensure the `cursor->thickness` is positive, as it affects the extent of the filled area.
// - Rotation (via `cursor->angle`) is supported by rotating each pixel around the circle's center.
//
// Example Usage:
// Cursor cursor = createCursor(300, 300, {255, 0, 0, 255}, 0, 1);
// drawFilledCircle(renderer, &cursor, 50); // Draws a red filled circle with a 50-pixel radius.
void drawFilledCircle(SDL_Renderer* renderer, Cursor* cursor, int radius) {
    if(cursor->visible){
        int scaled_radius = (int)(radius * cursor->scale); // Adjust radius based on the cursor's scale.
        float rad_angle = cursor->angle * M_PI / 180.0;    // Convert the angle to radians.

        // Set the color for the filled circle.
        SDL_SetRenderDrawColor(renderer, cursor->color.r, cursor->color.g, cursor->color.b, cursor->color.a);

        // Iterate through all pixels within the bounding box of the circle.
        for (int y = -scaled_radius; y <= scaled_radius; y++) {
            for (int x = -scaled_radius; x <= scaled_radius; x++) {
                // Check if the point is within the circle's radius.
                if (x * x + y * y <= scaled_radius * scaled_radius) {
                    // Apply rotation to the point.
                    int rotated_x = (int)(x * cos(rad_angle) - y * sin(rad_angle));
                    int rotated_y = (int)(x * sin(rad_angle) + y * cos(rad_angle));

                    // Draw the point on the renderer.
                    SDL_RenderDrawPoint(renderer, cursor->x + rotated_x, cursor->y + rotated_y);
                }
            }
        }
    }
}


// Function to draw an arc using a Cursor object.
//
// This function draws a portion of a circle (arc) centered at the cursor's current position (`x`, `y`).
// The arc's radius is determined by the `radius` parameter, scaled by the cursor's `scale` attribute.
// The arc starts and ends at the specified angles (`startAngle` and `endAngle`) in degrees.
// It respects the cursor's `color`, `thickness`, and `angle` attributes for appearance and orientation.
//
// Parameters:
// - SDL_Renderer* renderer: The SDL renderer used to draw the arc.
// - Cursor* cursor: A pointer to the Cursor object that provides position, color,
//   thickness, scale, and rotation for the arc.
// - int radius: The radius of the arc before scaling.
// - int startAngle: The starting angle of the arc in degrees (measured counterclockwise from the x-axis).
// - int endAngle: The ending angle of the arc in degrees (measured counterclockwise from the x-axis).
//
// Implementation Details:
// - The arc's points are calculated using the parametric equations of a circle:
//     x = r * cos(angle)
//     y = r * sin(angle)
// - The angles are iterated between `startAngle` and `endAngle` to draw the arc segment.
// - Rotation is applied using the cursor's `angle`, and thickness is simulated by drawing
//   multiple concentric arcs.
//
// Notes:
// - Ensure the `startAngle` is less than or equal to `endAngle` for correct rendering.
// - The `cursor->thickness` determines the width of the arc.
//
// Example Usage:
// Cursor cursor = createCursor(300, 300, {0, 255, 255, 255}, 5, 1);
// drawArc(renderer, &cursor, 100, 0, 180); // Draws a semi-circle arc with a 100-pixel radius.
void drawArc(SDL_Renderer* renderer, Cursor* cursor, int radius, int startAngle, int endAngle) {
    int scaled_radius = (int)(radius * cursor->scale); // Adjust radius based on the cursor's scale.
    float rad_angle = cursor->angle * M_PI / 180.0;    // Convert the cursor's angle to radians.

    // Set the color for the arc.
    SDL_SetRenderDrawColor(renderer, cursor->color.r, cursor->color.g, cursor->color.b, cursor->color.a);

    // Draw concentric arcs to simulate thickness.
    for (int offset = 0; offset < cursor->thickness; offset++) {
        // Iterate through the angles between startAngle and endAngle.
        for (float angle = startAngle; angle <= endAngle; angle += 0.1) {
            // Calculate the point on the arc using the parametric equations.
            int x = (scaled_radius + offset) * cos(angle * M_PI / 180.0);
            int y = (scaled_radius + offset) * sin(angle * M_PI / 180.0);

            // Apply rotation to the point.
            int rotated_x = (int)(x * cos(rad_angle) - y * sin(rad_angle));
            int rotated_y = (int)(x * sin(rad_angle) + y * cos(rad_angle));

            // Draw the rotated point on the renderer.
            SDL_RenderDrawPoint(renderer, cursor->x + rotated_x, cursor->y + rotated_y);
        }
    }
}