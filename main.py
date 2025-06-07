import pygame
from constants import *
from player import Player
from os import system

system("cls")

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("BomberCraft")

# Create clock for controlling frame rate
clock = pygame.time.Clock()

# Define player movement variables
moving_left = False
moving_right = False
moving_up = False
moving_down = False

# Aux funtion to scale images
def scale_image_by_height(image, height):
    aspect_ratio = image.get_width() / image.get_height()
    new_width = int(height * aspect_ratio)
    return pygame.transform.scale(image, (new_width, height))
    

player_image = pygame.image.load("assets/images/steve/idle/0.png").convert_alpha()
player_image = scale_image_by_height(player_image, PLAYER_HEIGHT)


# Create player
player = Player(100, 100, player_image)

# Main game loop
run = True
while run:

    # Control frame rate
    clock.tick(FPS)

    screen.fill(BG)

    # Calculate player movement
    dx = 0
    dy = 0

    if moving_right:
        dx = PLAYER_SPEED
    if moving_left:
        dx = -PLAYER_SPEED
    if moving_up:
        dy = -PLAYER_SPEED
    if moving_down:
        dy = PLAYER_SPEED

    # Move player
    player.move(dx, dy)

    # Draw player
    player.draw(screen)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        # Handle key presses
        if event.type == pygame.KEYDOWN:
            if event.key in [pygame.K_a, pygame.K_LEFT]:
                moving_left = True
            if event.key and event.key in [pygame.K_d, pygame.K_RIGHT]:
                moving_right = True
            if event.key in [pygame.K_w, pygame.K_UP]:
                moving_up = True
            if event.key in [pygame.K_s, pygame.K_DOWN]:
                moving_down = True

        # Handle key releases
        if event.type == pygame.KEYUP:
            if event.key in [pygame.K_a, pygame.K_LEFT]:
                moving_left = False
            if event.key in [pygame.K_d, pygame.K_RIGHT]:
                moving_right = False
            if event.key in [pygame.K_w, pygame.K_UP]:
                moving_up = False
            if event.key in [pygame.K_s, pygame.K_DOWN]:
                moving_down = False
    

    # Update display
    pygame.display.update()

pygame.quit()