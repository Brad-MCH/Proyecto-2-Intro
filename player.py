import pygame
import math
from constants import *


class Player:
    def __init__(self, x, y, animation_list):
        self.last_mov = 0
        self.frame_index = 0
        self.action = 0 # 0:idle, 1:corriendo_arriba, 2:corriendo_abajo, 3:corriendo_izquierda, 4:corriendo_derecha, 5:corriendo_arriba_izquierda, 6:corriendo_arriba_derecha, 7:corriendo_abajo_izquierda, 8:corriendo_abajo_derecha
        self.animation_list = animation_list
        self.update_time = pygame.time.get_ticks()
        self.image = animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        self.collide_rect = pygame.Rect(0, 0, 40, 40)
        self.collide_rect.center = self.rect.center

    def move(self, dx, dy, obstacles):

        screen_scroll = [0, 0]  # Inicializar la posición de desplazamiento de la pantalla

        if dx < 0 and dy < 0:
            self.last_mov = 1
            self.update_action(5)  # corriendo_arriba_izquierda
        elif dx > 0 and dy < 0:
            self.last_mov = 1
            self.update_action(6)  # corriendo_arriba_derecha
        elif dx < 0 and dy > 0:
            self.last_mov = 0
            self.update_action(7)  # corriendo_abajo_izquierda
        elif dx > 0 and dy > 0:
            self.last_mov = 0
            self.update_action(8)  # corriendo_abajo_derecha
        elif dx == 0 and dy == 0:
            self.update_idle()
        elif dx < 0:
            self.last_mov = 2
            self.update_action(3)
        elif dx > 0:
            self.last_mov = 3
            self.update_action(4)    
        elif dy < 0:
            self.last_mov = 1
            self.update_action(1)
        elif dy > 0:
            self.last_mov = 0
            self.update_action(2)
        
        

        # Manejar movimiento diagonal
        if dx != 0 and dy != 0:
            dx = dx * (math.sqrt(2) / 2)
            dy = dy * (math.sqrt(2) / 2)


        
        self.collide_rect.x += dx
        for obstacle in obstacles:
            if self.collide_rect.colliderect(obstacle[1]):
                if dx > 0:
                    self.collide_rect.right = obstacle[1].left
                if dx < 0:
                    self.collide_rect.left = obstacle[1].right

            
        self.collide_rect.y += dy
        for obstacle in obstacles:
            if self.collide_rect.colliderect(obstacle[1]):
                if dy > 0:
                    self.collide_rect.bottom = obstacle[1].top
                if dy < 0:
                    self.collide_rect.top = obstacle[1].bottom

        
        self.rect.center = (self.collide_rect.centerx, self.collide_rect.centery)

        # TODO: Hacer esto solo aplicable al jugador cuando se implementen los mobs
        # Mantener al jugador dentro de los límites de la pantalla
        # Mover la cámara izquierda/derecha
        if self.collide_rect.right > (SCREEN_WIDTH - SCROLL_THRESH):
            screen_scroll[0] = SCREEN_WIDTH - SCROLL_THRESH - self.collide_rect.right
            self.collide_rect.right = SCREEN_WIDTH - SCROLL_THRESH
        if self.collide_rect.left < SCROLL_THRESH:
            screen_scroll[0] = SCROLL_THRESH - self.collide_rect.left
            self.collide_rect.left = SCROLL_THRESH

        # Mover la cámara arriba/abajo
        if self.collide_rect.bottom > (SCREEN_HEIGHT - SCROLL_THRESH):
            screen_scroll[1] = SCREEN_HEIGHT - SCROLL_THRESH - self.collide_rect.bottom
            self.collide_rect.bottom = SCREEN_HEIGHT - SCROLL_THRESH
        if self.collide_rect.top < SCROLL_THRESH:
            screen_scroll[1] = SCROLL_THRESH - self.collide_rect.top
            self.collide_rect.top = SCROLL_THRESH

        return screen_scroll

    def update(self):
        if self.action == 0:
            self.update_idle()
        elif self.action == 1:
            self.update_action(1)
        elif self.action == 2:
            self.update_action(2)
        elif self.action == 3:
            self.update_action(3)
        elif self.action == 4:
            self.update_action(4)
        elif self.action == 5:
            self.update_action(5)  # corriendo_arriba_izquierda
        elif self.action == 6:
            self.update_action(6)  # corriendo_arriba_derecha
        elif self.action == 7:
            self.update_action(7)  # corriendo_abajo_izquierda
        elif self.action == 8:
            self.update_action(8)  # corriendo_abajo_derecha

        animation_cooldown = 70
        # Manejar animación
        if self.action != 0: # si no está idle
            #Actualizar imagen
            self.image = self.animation_list[self.action][self.frame_index]
            # Verificar si ha pasado suficiente tiempo para actualizar el cuadro
            if pygame.time.get_ticks() - self.update_time > animation_cooldown:
                self.frame_index += 1
                self.update_time = pygame.time.get_ticks()
            # Verificar si el índice del cuadro excede la longitud de la lista de animación
            if self.frame_index >= len(self.animation_list[self.action]):
                self.frame_index = 0

    # Actualizar la acción basada en la acción actual
    # Esto se llama cuando el jugador cambia de dirección o acción
    def update_action(self, action):
        # Actualizar la acción si ha cambiado
        if self.action != action:
            self.action = action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()
            self.image = self.animation_list[self.action][self.frame_index]

    # Cuando está idle, hace que el jugador mire hacia la dirección del mouse
    def update_idle(self):
        self.action = 0
        mouse_x, mouse_y = pygame.mouse.get_pos()
        p_pos_x, p_pos_y = self.rect.center
        x_diff = abs(mouse_x - p_pos_x)
        y_diff = abs(mouse_y - p_pos_y)
        xy_diff = abs(x_diff - y_diff)
        DIAGONAL = 100
        
        if mouse_y < p_pos_y and y_diff > x_diff:
            if xy_diff > DIAGONAL:
                self.image = self.animation_list[0][1]
            elif mouse_x < p_pos_x:
                self.image = self.animation_list[0][4]
            elif mouse_x > p_pos_x:
                self.image = self.animation_list[0][5]

        elif mouse_y > p_pos_y and y_diff > x_diff:
            if xy_diff > DIAGONAL:
                self.image = self.animation_list[0][0]
            elif mouse_x < p_pos_x:
                self.image = self.animation_list[0][7]
            elif mouse_x > p_pos_x:
                self.image = self.animation_list[0][6]
            
        elif mouse_x < p_pos_x and x_diff > y_diff:

            if xy_diff > DIAGONAL:
                self.image = self.animation_list[0][2]
            elif mouse_y > p_pos_y:
                self.image = self.animation_list[0][7]
            elif mouse_y < p_pos_y:
                self.image = self.animation_list[0][4]

            
        elif mouse_x > p_pos_x and x_diff > y_diff:
            
            if xy_diff > DIAGONAL:
                self.image = self.animation_list[0][3]
            elif mouse_y > p_pos_y:
                self.image = self.animation_list[0][6]
            elif mouse_y < p_pos_y:
                self.image = self.animation_list[0][5]
        

        

    # Dibujar al jugador en la pantalla      
    def draw(self, screen):
        screen.blit(self.image, self.rect)
        #pygame.draw.rect(screen, RED, self.rect, 1)
        #pygame.draw.rect(screen, RED, self.collide_rect, 1)