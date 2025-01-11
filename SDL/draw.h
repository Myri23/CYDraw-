#ifndef DRAW_H
#define DRAW_H

#include "newcursor.h"

void drawLine(SDL_Renderer* renderer, Cursor* cursor, int length);
void drawSquare(SDL_Renderer* renderer, Cursor* cursor, int size);
void drawFilledSquare(SDL_Renderer* renderer, Cursor* cursor, int size);
void drawCircle(SDL_Renderer* renderer, Cursor* cursor, int radius);
void drawFilledCircle(SDL_Renderer* renderer, Cursor* cursor, int radius);
void drawArc(SDL_Renderer* renderer, Cursor* cursor, int radius, int startAngle, int endAngle);

#endif
