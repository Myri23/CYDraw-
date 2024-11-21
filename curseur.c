// gcc -Wall -Wextra -g3 /home/cytech/Desktop/CYDraw-/test.c -o /home/cytech/Desktop/CYDraw-/test $(sdl2-config --cflags --libs) -lm

#include <stdio.h>
#include <SDL2/SDL.h>
#include <stdlib.h>
#include <math.h>

#define SCREEN_WIDTH 800
#define SCREEN_HEIGHT 600

#ifndef M_PI
#define M_PI 3.14159265358979323846
#endif

typedef struct {
    int x, y;
    int angle;         // Angle en degrés
    SDL_Color color;   // Couleur du curseur
    int thickness;     // Épaisseur de la ligne
    int visible;       // 1 si le curseur est visible, 0 sinon
} Cursor;

// Fonction pour créer un curseur
Cursor createCursor(int x, int y, SDL_Color color, int thickness, int visible) {
    Cursor cursor;
    cursor.x = x;
    cursor.y = y;
    cursor.angle = 0;
    cursor.color = color;
    cursor.thickness = thickness;
    cursor.visible = visible;
    return cursor;
}

void setThickness(Cursor* cursor, int newThickness) {
    cursor->thickness = newThickness;
}

void draw_cursor(SDL_Renderer* renderer, Cursor* cursor) {
    if (cursor->visible) {
        SDL_SetRenderDrawColor(renderer, cursor->color.r, cursor->color.g, cursor->color.b, cursor->color.a);

        for (int w = 0; w < cursor->thickness; w++) {
            for (int h = 0; h < cursor->thickness; h++) {
                int dx = w - cursor->thickness / 2;
                int dy = h - cursor->thickness / 2;
                if ((dx * dx + dy * dy) <= (cursor->thickness / 2) * (cursor->thickness / 2)) {
                    SDL_RenderDrawPoint(renderer, cursor->x + dx, cursor->y + dy);
                }
            }
        }
    }
}



void draw_cross_cursor(SDL_Renderer* renderer, Cursor* cursor){
    if (cursor->visible) {
        SDL_SetRenderDrawColor(renderer, 0, 0, 255, 255);
        
        // Dessiner une croix en fonction de l'épaisseur
        for (int offset = -cursor->thickness / 2; offset <= cursor->thickness / 2; offset++) {
            SDL_RenderDrawLine(renderer, cursor->x - cursor->thickness, cursor->y + offset, cursor->x + cursor->thickness, cursor->y + offset);
            SDL_RenderDrawLine(renderer, cursor->x + offset, cursor->y - cursor->thickness, cursor->x + offset, cursor->y + cursor->thickness);
        }
    }
}


void draw_square_cursor(SDL_Renderer* renderer, Cursor* cursor) {
    if (cursor->visible) {
        SDL_SetRenderDrawColor(renderer, cursor->color.r, cursor->color.g, cursor->color.b, cursor->color.a);

        // Dessiner un carré avec une épaisseur
        for (int offset = 0; offset < cursor->thickness; offset++) {
            SDL_Rect rect = {
                cursor->x - offset,
                cursor->y - offset,
                cursor->thickness + (2 * offset),
                cursor->thickness + (2 * offset)
            };
            SDL_RenderDrawRect(renderer, &rect);
        }
    }
}

// Dessiner un segment (ligne) avec un curseur
void drawLine(SDL_Renderer* renderer, Cursor* cursor, int length) {
    int x_end = cursor->x + length * cos(cursor->angle * M_PI / 180.0);
    int y_end = cursor->y + length * sin(cursor->angle * M_PI / 180.0);

    SDL_SetRenderDrawColor(renderer, cursor->color.r, cursor->color.g, cursor->color.b, cursor->color.a);
    SDL_RenderDrawLine(renderer, cursor->x, cursor->y, x_end, y_end);

    // Mettre à jour la position du curseur
    cursor->x = x_end;
    cursor->y = y_end;

    // Dessiner le curseur si visible
    if (cursor->visible) {
        draw_cursor(renderer, cursor);
    }
}


// Changer la couleur et l'épaisseur du curseur
// ne sert à rien
void setCursorAppearance(Cursor* cursor, SDL_Color color, int thickness) {
    cursor->color = color;
    cursor->thickness = thickness;
}

// Déplacer le curseur d'une distance en pixels dans la direction actuelle
void moveCursor(Cursor* cursor, int distance) {
    cursor->x += distance * cos(cursor->angle * M_PI / 180.0);
    cursor->y += distance * sin(cursor->angle * M_PI / 180.0);
}

// Faire pivoter le curseur d'un angle en degrés
void rotateCursor(Cursor* cursor, int angle) {
    cursor->angle = (cursor->angle + angle) % 360;
}

// Dessiner un point
//ne sert à rien
void drawPoint(SDL_Renderer* renderer, Cursor* cursor) {
    SDL_SetRenderDrawColor(renderer, cursor->color.r, cursor->color.g, cursor->color.b, cursor->color.a);
    SDL_RenderDrawPoint(renderer, cursor->x, cursor->y);
}




// Dessiner un carré avec un curseur
void drawSquare(SDL_Renderer* renderer, Cursor* cursor, int size) {
    for (int i = 0; i < 4; i++) {
        drawLine(renderer, cursor, size);   // Dessiner un côté du carré
        rotateCursor(cursor, 90);           // Tourner le curseur de 90 degrés

        // Dessiner le curseur après chaque rotation si visible
        if (cursor->visible) {
            draw_cursor(renderer, cursor);
        }
    }
}


// Dessiner un cercle avec un curseur
void drawCircle(SDL_Renderer* renderer, Cursor* cursor, int radius) {
    int x_center = cursor->x;
    int y_center = cursor->y;

    SDL_SetRenderDrawColor(renderer, cursor->color.r, cursor->color.g, cursor->color.b, cursor->color.a);
    for (int angle = 0; angle < 360; angle++) {
        int x = x_center + radius * cos(angle * M_PI / 180.0);
        int y = y_center + radius * sin(angle * M_PI / 180.0);
        SDL_RenderDrawPoint(renderer, x, y);

        /*
        // Dessiner le curseur si visible et faire une boucle pr avoir le choix entre les deux
        if (cursor->visible) {
            cursor->x = x;
            cursor->y = y;
            draw_cross_cursor(renderer, cursor); // pour plusieurs curseurs sur le cercle
        }
        */
        
    }

    // Dessiner le curseur si visible
    if (cursor->visible) {
        draw_square_cursor(renderer, cursor); // un curseur au centre
    }

    // Remettre le curseur au centre du cercle après le dessin
    cursor->x = x_center;
    cursor->y = y_center;
}


// Animer un dessin avec plusieurs curseurs
void animateDrawing(SDL_Renderer* renderer) {
    Cursor cursor1 = createCursor(200, 200, (SDL_Color){255, 255, 0, 255}, 7, 1); // Jaune
    Cursor cursor2 = createCursor(400, 300, (SDL_Color){0, 255, 255, 255}, 3, 1);
    Cursor cursor3 = createCursor(350, 100, (SDL_Color){255, 255, 0, 255}, 7, 0); 

    int running = 1;
    SDL_Event event;
    while (running) {
        while (SDL_PollEvent(&event)) {
            if (event.type == SDL_QUIT) {
                running = 0;
            }
        }

        // Effacer l'écran
        SDL_SetRenderDrawColor(renderer, 0, 0, 0, 255);
        SDL_RenderClear(renderer);

        
        // Dessiner le carré et le curseur
        drawSquare(renderer, &cursor1, 50);
        //rotateCursor(&cursor1, 10);

        // Dessiner le cercle et le curseur
        drawCircle(renderer, &cursor2, 30);
        moveCursor(&cursor2, 5);

        drawSquare(renderer, &cursor3, 25);

        SDL_RenderPresent(renderer); // Mettre à jour l'affichage
        SDL_Delay(100);
    }
}



int main(){

  // Initialiser SDL
    if (SDL_Init(SDL_INIT_VIDEO) != 0) {
        printf("Erreur d'initialisation de SDL: %s\n", SDL_GetError());
        return 1;
    }

    SDL_Window* window = SDL_CreateWindow("SDL Cursor Drawing", SDL_WINDOWPOS_CENTERED, SDL_WINDOWPOS_CENTERED, SCREEN_WIDTH, SCREEN_HEIGHT, SDL_WINDOW_SHOWN);
    if (!window) {
        printf("Erreur de création de la fenêtre: %s\n", SDL_GetError());
        SDL_Quit();
        return 1;
    }

    SDL_Renderer* renderer = SDL_CreateRenderer(window, -1, SDL_RENDERER_ACCELERATED);
    if (!renderer) {
        SDL_DestroyWindow(window);
        printf("Erreur de création du renderer: %s\n", SDL_GetError());
        SDL_Quit();
        return 1;
    }

    // Lancer l'animation de dessin
    animateDrawing(renderer);

    // Nettoyer et quitter
    SDL_DestroyRenderer(renderer);
    SDL_DestroyWindow(window);
    SDL_Quit();


    return 0;
}