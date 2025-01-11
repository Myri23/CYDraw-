#include "handle.h"
#include "config.h"
#include <math.h>
#include <SDL2/SDL.h>


// ======================================================
// SELECT, MOVE, ZOOM, DELETE AND ROTATION FUNCTIONS
// ======================================================

// This section contains functions that handle user interactions with the cursors,
// including selecting, moving, zooming, deleting, and rotating.
// These functions form the core of the application's interactivity,
// enabling users to dynamically manipulate the cursors.
//
// Functions in this section:
// - handleSelection: Identifies which cursor was clicked by the user.
// - handleMovement: Updates the position of the selected cursor during mouse drag.
// - handleZoom: Adjusts the size of the selected cursor based on zooming input.
// - handleDeletion: Deletes the currently selected cursor.
// - applyRotationToCursor: Rotates the selected cursor by a specified angle.


// Global variable to track the currently selected cursor:
Cursor* selected_cursor = NULL;  // The currently selected cursor.


// Function to select a drawing:
// This function checks if the coordinates of a mouse click correspond to a cursor.
//
// Parameters:
// - int x: The x-coordinate of the mouse click.
// - int y: The y-coordinate of the mouse click.
// - Cursor** cursors: An array of pointers to Cursor objects representing the drawings.
// - int num_cursors: The total number of Cursor objects in the array.
//
// Logic:
// - The function iterates through all cursors.
// - For each cursor, it calculates the selection area based on the cursor's position, scale, and thickness.
// - If the mouse click falls within this area, the cursor is selected, and the loop terminates.
//
// Notes:
// - If no cursor is selected, the global `selected_cursor` remains NULL.
//
// Example:
// - A mouse click at coordinates (300, 300) selects a cursor located at (300, 300),
//   assuming the click is within the cursor's scaled selection area.
void handleSelection(int x, int y, Cursor** cursors, int num_cursors) {
    selected_cursor = NULL;  // Reset the selection.

    for (int i = 0; i < num_cursors; i++) {
        Cursor* cursor = cursors[i];
        
        // Calculate the effective size of the drawing, scaled by the cursor's scale.
        int scaled_size = (int)(50 * cursor->scale);  // Example: base size of 50 units.
        int half_size = scaled_size / 2;

        // Compute the selection area's boundaries.
        int left = cursor->x - half_size - cursor->thickness;  // Left edge.
        int right = cursor->x + half_size + cursor->thickness; // Right edge.
        int top = cursor->y - half_size - cursor->thickness;   // Top edge.
        int bottom = cursor->y + half_size + cursor->thickness;// Bottom edge.

        // Check if the click falls within the selection area's boundaries.
        if (x >= left && x <= right && y >= top && y <= bottom) {
            selected_cursor = cursor;  // Select the cursor.
            return;  // Exit once a cursor is selected.
        }
    }
}


// Function to move the selected cursor to a new position.
//
// This function updates the position (`x`, `y`) of the currently selected cursor
// based on the new mouse coordinates. It ensures that only the selected cursor
// is moved.
//
// Parameters:
// - int x: The new x-coordinate where the selected cursor should be moved.
// - int y: The new y-coordinate where the selected cursor should be moved.
//
// Logic:
// - The function checks if a cursor is currently selected (`selected_cursor` is not NULL).
// - If a cursor is selected, its `x` and `y` attributes are updated with the provided coordinates.
//
// Notes:
// - This function does nothing if no cursor is selected.
// - Ensure that `handleMovement` is called only during a mouse motion event
//   while the left mouse button is held down.
//
// Example:
// - If the selected cursor's current position is (200, 200) and the mouse is moved to (300, 300),
//   the function updates the cursor's position to (300, 300).
void handleMovement(int x, int y) {
    // Check if a cursor is currently selected.
    if (selected_cursor != NULL) {
        // Update the selected cursor's position.
        selected_cursor->x = x;
        selected_cursor->y = y;
    }
}


// Function to zoom in or out on the selected cursor, adjusting its position to match the new scale.
//
// This function modifies the scaling factor (`scale`) of the currently selected cursor,
// making it appear larger (zoom in) or smaller (zoom out). Additionally, it adjusts the
// cursor's position (`x`, `y`) proportionally to ensure consistency in rendering.
//
// Parameters:
// - int zoomIn: A flag indicating the direction of zoom.
//   - If `zoomIn` is non-zero (true), the cursor is zoomed in (scale increases).
//   - If `zoomIn` is zero (false), the cursor is zoomed out (scale decreases).
//
// Logic:
// - The function first checks if a cursor is currently selected (`selected_cursor` is not NULL).
// - If a cursor is selected:
//   - Its `scale` is adjusted based on the `zoomIn` flag.
//   - A minimum scale limit is enforced (e.g., 0.1).
//   - The cursor's position (`x`, `y`) is updated proportionally to the scaling factor.
//
// Notes:
// - This function has no effect if no cursor is selected.
// - Ensure that `handleZoom` is only called when a mouse wheel event occurs.
//
// Example:
// - If the selected cursor has a scale of 1.0 and `zoomIn` is true, the scale becomes 1.1,
//   and its position is adjusted accordingly.
void handleZoom(int zoomIn) {
    // Check if a cursor is currently selected.
    if (selected_cursor != NULL) {
        float old_scale = selected_cursor->scale; // Store the old scale.

        // Adjust the scale based on the zoom direction.
        if (zoomIn) {
            selected_cursor->scale += 0.1f; // Increase the scale for zoom in.
        } else {
            selected_cursor->scale -= 0.1f; // Decrease the scale for zoom out.
            // Enforce a minimum scale limit.
            if (selected_cursor->scale < 0.1f) {
                selected_cursor->scale = 0.1f;
            }
        }

        // Calculate the scale factor and adjust the cursor's position proportionally.
        float scale_factor = selected_cursor->scale / old_scale;
        selected_cursor->x = (int)(selected_cursor->x * scale_factor);
        selected_cursor->y = (int)(selected_cursor->y * scale_factor);
    }
}


// Function to delete the currently selected cursor.
//
// This function removes the selected cursor by marking it as invisible (`visible = 0`).
// Once a cursor is deleted, it is no longer rendered or interacts with user input.
// The `selected_cursor` is reset to `NULL` to ensure no operations can be performed
// on the deleted cursor.
//
// Parameters:
// - None.
//
// Logic:
// - The function first checks if a cursor is currently selected (`selected_cursor` is not NULL).
// - If a cursor is selected, its `visible` attribute is set to `0`, effectively removing it
//   from the rendering loop and user interactions.
// - The `selected_cursor` is reset to `NULL` to indicate that no cursor is currently selected.
//
// Notes:
// - This function only marks the cursor as invisible; the actual object is not deleted from memory.
// - Ensure that other parts of the code respect the `visible` attribute and skip over invisible cursors.
//
// Example:
// - If the selected cursor has `visible = 1` and its position is (300, 300),
//   calling `handleDeletion` will set `visible = 0` and reset `selected_cursor`.
void handleDeletion() {
    // Check if a cursor is currently selected.
    if (selected_cursor != NULL) {
        // Mark the selected cursor as invisible.
        selected_cursor->visible = 0;

        // Reset the selected cursor to NULL.
        selected_cursor = NULL;
    } 
}


// Function to apply a rotation to a Cursor object.
//
// This function adjusts the rotation angle (`angle`) of the given cursor by adding
// a specified value. The angle is normalized to ensure it remains within the range [0, 360) degrees.
//
// Parameters:
// - Cursor* cursor: A pointer to the cursor whose rotation angle will be updated.
// - int angle: The angle (in degrees) to add to the cursor's current rotation.
//   - Positive values rotate clockwise.
//   - Negative values rotate counterclockwise.
//
// Logic:
// - The function first checks if the `cursor` is valid (not NULL).
// - The rotation angle is added to the cursor's current angle.
// - The resulting angle is normalized using the modulo operator (`% 360`) to ensure it
//   stays within the range [0, 360).
//
// Notes:
// - If the `cursor` parameter is `NULL`, the function does nothing.
// - This function only modifies the `angle` attribute of the cursor; it does not affect
//   the cursor's position or other attributes.
//
// Example:
// - If a cursor's current angle is 45° and `applyRotationToCursor(cursor, 90)` is called,
//   the cursor's new angle will be 135°.
// - If `applyRotationToCursor(cursor, -60)` is called, the angle will become 75°.
void applyRotationToCursor(Cursor* cursor, int angle) {
    if (cursor != NULL) {
        // Add the specified angle to the cursor's current angle and normalize it to [0, 360).
        cursor->angle = (cursor->angle + angle) % 360;

        // Handle negative angles by adding 360 to bring them into the valid range.
        if (cursor->angle < 0) {
            cursor->angle += 360;
        }
    }
}



// Function to visually debug the selection area of a cursor.
//
// This function draws a green outline around the selection area of the specified cursor,
// allowing developers to visually debug the boundaries of the selectable area for the cursor.
//
// Parameters:
// - SDL_Renderer* renderer: The SDL renderer used to draw the debug indicator.
// - Cursor* cursor: A pointer to the cursor whose selection area is being visualized.
//
// Logic:
// - The function calculates the size of the selection area based on the cursor's scale and thickness.
// - It then draws a green rectangle around the cursor to represent its selectable region.
//
// Notes:
// - This function is intended for debugging purposes only and should not be included in production builds.
// - The color and transparency of the rectangle can be customized for better visualization.
//
// Example Usage:
// If a cursor is located at (300, 300) with a scale of 1.0 and a thickness of 5,
// calling this function will draw a green rectangle around its selection area.
void debugSelectionArea(SDL_Renderer* renderer, Cursor* cursor) {
    if (renderer == NULL || cursor == NULL) {
        printf("Invalid renderer or cursor for debugging selection area.\n");
        return;
    }

    // Set the debug color to semi-transparent green.
    SDL_SetRenderDrawColor(renderer, 0, 255, 0, 128);

    // Calculate the selection area's size and boundaries.
    int scaled_size = (int)(50 * cursor->scale); // Base size of 50 units, scaled by the cursor's scale.
    int half_size = scaled_size / 2;

    SDL_Rect rect = {
        cursor->x - half_size - cursor->thickness,  // Left boundary
        cursor->y - half_size - cursor->thickness,  // Top boundary
        scaled_size + 2 * cursor->thickness,        // Width (including thickness)
        scaled_size + 2 * cursor->thickness         // Height (including thickness)
    };

    // Draw the debug rectangle.
    SDL_RenderDrawRect(renderer, &rect);
}