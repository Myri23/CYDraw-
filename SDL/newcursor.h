#ifndef NEWCURSOR_H
#define NEWCURSOR_H

#include <math.h>
#include <SDL2/SDL.h>

typedef struct {
    int x, y;             // The current position of the cursor on the screen (center of the shape).
    int angle;            // The rotation angle of the cursor in degrees, used for shape orientation.
    SDL_Color color;      // The color of the cursor or the shapes it draws (RGBA format).
    int thickness;        // The thickness of lines or borders drawn by the cursor.
    int visible;          // Visibility flag: 1 means the cursor is visible, 0 means it is hidden.
    float scale;          // Scaling factor for the size of shapes (1.0 = default size, <1.0 = smaller, >1.0 = larger).
} Cursor;

Cursor createCursor(int x, int y, SDL_Color color, int thickness, int visible);
void setThickness(Cursor* cursor, int newThickness);
void moveCursor(Cursor* cursor, int distance);
void rotateCursor(Cursor* cursor, int angle);
void rotateCursor2(Cursor* cursor, double angle);

#endif
