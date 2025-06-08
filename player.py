import pygame
import math
from constants import *

class Player:
    def __init__(self, x, y, animation_list):
        self.last_mov = 0
        self.frame_index = 0
        self.action = 0 # 0:iddle, 1:running_up, 2:running_down, 3:running_left, 4:running_right
        self.animation_list = animation_list
        self.update_time = pygame.time.get_ticks()
        self.image = animation_list[self.action][self.frame_index]
        self.rect = pygame.Rect(0, 0, PLAYER_WIDTH, PLAYER_HEIGHT)
        self.rect.center = (x, y) 

    def move(self, dx, dy):

        screen_scroll = [0, 0]  # Initialize screen scroll position

        if dx == 0 and dy == 0:
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
        

        # Handle diagonal movement
        if dx != 0 and dy != 0:
            dx = dx * (math.sqrt(2) / 2)
            dy = dy * (math.sqrt(2) / 2)

        self.rect.x += dx
        self.rect.y += dy

        # TODO: Make this only applicable to player when mobs are implemented
        # Keep player within screen bounds
        # Move camera left/right
        if self.rect.right > (SCREEN_WIDTH - SCROLL_THRESH):
            screen_scroll[0] = SCREEN_WIDTH - SCROLL_THRESH - self.rect.right
            self.rect.right = SCREEN_WIDTH - SCROLL_THRESH
        if self.rect.left < SCROLL_THRESH:
            screen_scroll[0] = SCROLL_THRESH - self.rect.left
            self.rect.left = SCROLL_THRESH

        # Move camera up/down
        if self.rect.bottom > (SCREEN_HEIGHT - SCROLL_THRESH):
            screen_scroll[1] = SCREEN_HEIGHT - SCROLL_THRESH - self.rect.bottom
            self.rect.bottom = SCREEN_HEIGHT - SCROLL_THRESH
        if self.rect.top < SCROLL_THRESH:
            screen_scroll[1] = SCROLL_THRESH - self.rect.top
            self.rect.top = SCROLL_THRESH

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

        animation_cooldown = 70
        # Handle animation
        if self.action != 0: # if not idle
            #Update image
            self.image = self.animation_list[self.action][self.frame_index]
            # Check if enough time has passed to update the frame
            if pygame.time.get_ticks() - self.update_time > animation_cooldown:
                self.frame_index += 1
                self.update_time = pygame.time.get_ticks()
            # Check if the frame index exceeds the length of the animation list
            if self.frame_index >= len(self.animation_list[self.action]):
                self.frame_index = 0

    # Update the action based on the current action
    # This is called when the player changes direction or action
    def update_action(self, action):
        # Update the action if it has changed
        if self.action != action:
            self.action = action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()
            self.image = self.animation_list[self.action][self.frame_index]

    # Update idle according to the last movement direction
    # This is called when the player is not moving
    def update_idle(self):
        self.action = 0
        self.image = self.animation_list[0][self.last_mov]

    # Draw the player on the screen      
    def draw(self, screen):
        screen.blit(self.image, self.rect)
        #pygame.draw.rect(screen, BG, self.rect, 1)