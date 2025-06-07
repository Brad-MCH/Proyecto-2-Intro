import pygame
import math
from constants import *

class Player:
    def __init__(self, x, y, image):
        self.image = image
        self.rect = pygame.Rect(0, 0, PLAYER_WIDTH, PLAYER_HEIGHT)
        self.rect.center = (x, y) 

    def move(self, dx, dy):
        # Handle diagonal movement
        if dx != 0 and dy != 0:
            dx = dx * (math.sqrt(2) / 2)
            dy = dy * (math.sqrt(2) / 2)



        self.rect.x += dx
        self.rect.y += dy

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        pygame.draw.rect(screen, RED, self.rect, 1)