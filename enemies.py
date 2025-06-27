import pygame
from constants import *
import random



class Move_enemy:
    def __init__(self, x, y, animation_list_enemy):
        self.x = x
        self.y = y
        self.width = TILE_SIZE 
        self.height = TILE_SIZE
        self.real_x = x
        self.real_y = y 
        self.animation_list_enemy = animation_list_enemy
        self.direction = random.choice(['up', 'down', 'left', 'right'])
        self.move_timer = pygame.time.get_ticks()
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.animation_cooldown = 120
        self.rect = animation_list_enemy[0].get_rect()
        self.rect.center = (x, y)
        self.collide_rect = pygame.Rect(0, 0, 40, 40)
        self.collide_rect.center = self.rect.center

    def update(self, obstacles, screen_scroll):

        self.collide_rect.x += screen_scroll[0]
        self.collide_rect.y += screen_scroll[1]

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
        self.collide_rect.x += dx
        for obstacle in obstacles:
            if self.collide_rect.colliderect(obstacle):
                if dx > 0:
                    self.collide_rect.right = obstacle.left
                if dx < 0:
                    self.collide_rect.left = obstacle.right

        self.collide_rect.y += dy
        for obstacle in obstacles:
            if self.collide_rect.colliderect(obstacle):
                if dy > 0:
                    self.collide_rect.bottom = obstacle.top
                if dy < 0:
                    self.collide_rect.top = obstacle.bottom

        self.rect.center = (self.collide_rect.centerx, self.collide_rect.centery)

        # Animación
        now = pygame.time.get_ticks()
        if now - self.last_update > self.animation_cooldown:
            self.frame = (self.frame + 1) % len(self.animation_list_enemy)
            self.last_update = now

    def draw(self, surface, screen_scroll):
        surface.blit(self.animation_list_enemy[self.frame], (self.rect.x, self.rect.y))


class Slime(Move_enemy):
    def __init__(self, x, y, animation_list_enemy):
        super().__init__(x, y, animation_list_enemy)
        self.frame = 0

