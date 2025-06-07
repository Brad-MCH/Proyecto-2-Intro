import pygame
import math
from constants import *

class Player:
    def __init__(self, x, y, animation_list):
        self.frame_index = 0
        self.animation_list = animation_list
        self.update_time = pygame.time.get_ticks()
        self.image = animation_list[self.frame_index]
        self.rect = pygame.Rect(0, 0, PLAYER_WIDTH, PLAYER_HEIGHT)
        self.rect.center = (x, y) 

    def move(self, dx, dy):
        # Handle diagonal movement
        if dx != 0 and dy != 0:
            dx = dx * (math.sqrt(2) / 2)
            dy = dy * (math.sqrt(2) / 2)



        self.rect.x += dx
        self.rect.y += dy

    def update(self):
        animation_cooldown = 70
        # Handle animation
        #Update image
        self.image = self.animation_list[self.frame_index]
        # Check if enough time has passed to update the frame
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()
        # Check if the frame index exceeds the length of the animation list
        if self.frame_index >= len(self.animation_list):
            self.frame_index = 0
            
            
    def draw(self, screen):
        screen.blit(self.image, self.rect)
        pygame.draw.rect(screen, RED, self.rect, 1)