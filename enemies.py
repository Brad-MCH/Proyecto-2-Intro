import pygame
from constants import *
import random



class Move_enemy:
    def __init__(self, x, y, animation_list_enemy):
        self.x = x
        self.y = y
        self.width = TILE_SIZE # Ajusta al tamaño de tu sprite
        self.height = TILE_SIZE
        self.real_x = x
        self.real_y = y 
        self.animation_list_enemy = animation_list_enemy
        self.direction = random.choice(['up', 'down', 'left', 'right'])
        self.move_timer = pygame.time.get_ticks()
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.animation_cooldown = 120
        self.rect = pygame.Rect(x, y, self.width, self.height)

    def update(self, obstacles):
        # Movimiento aleatorio
        if pygame.time.get_ticks() - self.move_timer > 1000:
            self.direction = random.choice(['up', 'down', 'left', 'right'])
            self.move_timer = pygame.time.get_ticks()

        dx, dy = 0, 0
        if self.direction == 'up':
            dy = -2
        elif self.direction == 'down':
            dy = 2
        elif self.direction == 'left':
            dx = -2
        elif self.direction == 'right':
            dx = 2

        # --- COLISIONES ---
        future_rect = self.rect.move(dx, dy)
        collision = False
        for obstacle in obstacles:
            if future_rect.colliderect(obstacle):
                collision = True
                break

        # Solo se mueve si NO hay colisión
        if not collision:
            self.real_y += dy
            self.real_x += dx
        # Actualiza el rect para colisiones
        self.rect.x = self.real_x
        self.rect.y = self.real_y

        # Animación
        now = pygame.time.get_ticks()
        if now - self.last_update > self.animation_cooldown:
            self.frame = (self.frame + 1) % len(self.animation_list_enemy)
            self.last_update = now

    def draw(self, surface, screen_scroll):
        screen_x = self.rect.x + screen_scroll[0]
        screen_y = self.rect.y + screen_scroll[1]
        if (-TILE_SIZE < screen_x < SCREEN_WIDTH and -TILE_SIZE < screen_y < SCREEN_HEIGHT):
            surface.blit(self.animation_list_enemy[self.frame], (screen_x, screen_y))


class Slime(Move_enemy):
    def __init__(self, x, y, animation_list_enemy):
        super().__init__(x, y, animation_list_enemy)
        self.frame = 0

