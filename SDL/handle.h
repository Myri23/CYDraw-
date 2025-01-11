#ifndef HANDLE_H
#define HANDLE_H

#include "newcursor.h"

extern Cursor* selected_cursor;  // Declare the global variable as extern.

void handleSelection(int x, int y, Cursor** cursors, int num_cursors);
void handleMovement(int x, int y);
void handleZoom(int zoomIn);
void handleDeletion();
void applyRotationToCursor(Cursor* cursor, int angle);
void debugSelectionArea(SDL_Renderer* renderer, Cursor* cursor);

#endif
