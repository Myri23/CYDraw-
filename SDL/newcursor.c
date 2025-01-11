#include "newcursor.h"
#include "config.h"
#include <math.h>
#include <SDL2/SDL.h>


// Function to create and initialize a Cursor object.
// This function sets the initial properties of a Cursor, such as position, color, thickness, visibility, and scale.
//
// Parameters:
// - int x: The initial x-coordinate of the cursor (position on the horizontal axis).
// - int y: The initial y-coordinate of the cursor (position on the vertical axis).
// - SDL_Color color: The RGBA color of the cursor or the shapes it draws.
// - int thickness: The initial thickness of the cursor's lines or borders.
// - int visible: Visibility flag (1 = visible, 0 = hidden).
//
// Returns:
// - Cursor: A newly created Cursor object with the specified properties.
Cursor createCursor(int x, int y, SDL_Color color, int thickness, int visible) {
    Cursor cursor;                 // Declare a Cursor structure.
    cursor.x = x;                  // Set the initial x-coordinate.
    cursor.y = y;                  // Set the initial y-coordinate.
    cursor.angle = 0;              // Initialize the rotation angle to 0 degrees.
    cursor.color = color;          // Assign the specified RGBA color.
    cursor.thickness = thickness;  // Set the line or border thickness.
    cursor.visible = visible;      // Set the visibility status (visible or hidden).
    cursor.scale = 1.0;            // Set the scale to its default value (1.0 = normal size).
    return cursor;                 // Return the initialized Cursor.
}



// Function to update the thickness of a Cursor's lines or borders.
//
// This function modifies the thickness attribute of a Cursor object, which
// affects the width of the lines or borders drawn by the cursor.
//
// Parameters:
// - Cursor* cursor: A pointer to the Cursor object whose thickness will be updated.
// - int newThickness: The new thickness value to set for the cursor.
//
// Notes:
// - The thickness value must be positive for the drawing to render correctly.
// - This function does not directly redraw shapes; it only updates the property.
//
// Example Usage:
// Cursor cursor = createCursor(200, 200, {255, 0, 0, 255}, 5, 1);
// setThickness(&cursor, 10); // Change the thickness of the cursor to 10 pixels.
void setThickness(Cursor* cursor, int newThickness) {
    cursor->thickness = newThickness; // Update the cursor's thickness property.
}


// Function to move a Cursor object in the direction of its current angle.
//
// This function updates the position (`x`, `y`) of the cursor based on its
// current angle and a specified distance. The movement is calculated using
// trigonometric functions to determine the x and y components of the displacement.
//
// Parameters:
// - Cursor* cursor: A pointer to the Cursor object to be moved.
// - int distance: The distance (in pixels) to move the cursor.
//
// Implementation Details:
//   The cursor's `angle` is specified in degrees, but trigonometric functions in C
//   (`cos` and `sin`) use radians. To convert degrees to radians, the angle is multiplied
//   by `M_PI / 180` (where `M_PI` is the mathematical constant π).
// - The `distance` determines the magnitude of movement, while the angle sets the direction.
// - The x-component of movement is calculated as `distance * cos(angle_in_radians)`.
// - The y-component of movement is calculated as `distance * sin(angle_in_radians)`.
//
// Notes:
// - The angle must be in degrees (0 to 360 degrees), and it is converted to radians for calculations.
//
// Example Usage:
// Cursor cursor = createCursor(200, 200, {255, 255, 255, 255}, 5, 1);
// moveCursor(&cursor, 50); // Moves the cursor 50 pixels in the direction of its angle.
void moveCursor(Cursor* cursor, int distance) {
    // Calculate the x and y displacement based on the cursor's angle and distance.
    cursor->x += distance * cos(cursor->angle * M_PI / 180.0); // Update x-coordinate.
    cursor->y += distance * sin(cursor->angle * M_PI / 180.0); // Update y-coordinate.
}


// Function to rotate a Cursor object by a specified angle.
//
// This function updates the `angle` attribute of a Cursor object, adding the
// specified rotation angle to its current orientation. The angle is normalized
// to remain within the range [0, 360) degrees.
//
// Parameters:
// - Cursor* cursor: A pointer to the Cursor object to be rotated.
// - int angle: The angle (in degrees) to rotate the cursor by. Positive values
//   rotate clockwise, and negative values rotate counterclockwise.
//
// Implementation Details:
// - The new angle is calculated by adding the given `angle` to the current angle of the cursor.
// - To ensure the angle remains within the standard range of [0, 360] degrees,
//   the modulo operator (`% 360`) is used to normalize the result.
// - If the resulting angle is negative, 360 is added to bring it back into the positive range.
//
// Notes:
// - This function only updates the cursor's angle and does not modify its position or appearance.
// - Ensure the `angle` parameter is in degrees, as the function does not perform conversions.
//
// Example Usage:
// Cursor cursor = createCursor(200, 200, {255, 255, 255, 255}, 5, 1);
// rotateCursor(&cursor, 90);  // Rotates the cursor 90 degrees clockwise.
// rotateCursor(&cursor, -45); // Rotates the cursor 45 degrees counterclockwise.
void rotateCursor(Cursor* cursor, int angle) {
    cursor->angle = (cursor->angle + angle) % 360; // Update the angle and normalize it to [0, 360].
    if (cursor->angle < 0) {
        cursor->angle += 360; // Ensure the angle is positive if it becomes negative.
    }
}


// Function to update the rotation angle of a Cursor object without altering its position.
//
// This function adds a specified angle (in degrees) to the cursor's current
// angle of rotation. Unlike `rotateCursor`, this function is designed for
// scenarios where the cursor rotates around its own center without affecting
// its x or y position. => Use in the function animateRotation2.
//
// Parameters:
// - Cursor* cursor: A pointer to the Cursor object to be rotated.
// - double angle: The angle (in degrees) to add to the cursor's current rotation.
//
// Implementation Details:
// - The cursor's new angle is calculated by adding the given `angle` to its current angle.
// - If the resulting angle exceeds 360 degrees, the function subtracts 360 to keep it within
//   the valid range of [0, 360). This ensures the angle stays normalized.
// - This function does not modify the cursor's position or other attributes.
//
// Notes:
// - This function is primarily used in animations or cases where the cursor's
//   orientation changes while its position remains fixed.
// - Ensure the input angle is in degrees.
//
// Example Usage:
// Cursor cursor = createCursor(300, 300, {255, 255, 255, 255}, 5, 1);
// rotateCursor2(&cursor, 45.0);  // Rotates the cursor by 45 degrees clockwise.
void rotateCursor2(Cursor* cursor, double angle) {
    cursor->angle += angle;      // Add the given angle to the current angle.
    if (cursor->angle >= 360.0) {
        cursor->angle -= 360.0;  // Normalize to stay within the range [0, 360).
    } else if (cursor->angle < 0.0) {
        cursor->angle += 360.0;  // Normalize negative angles to positive equivalents.
    }
}
