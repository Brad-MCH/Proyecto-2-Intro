import pygame
from constants import *
from player import Player
from world import World
import csv
from os import system

system("cls")

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("BomberCraft")

# Create clock for controlling frame rate
clock = pygame.time.Clock()

# Game variables
level = 1  # Set the level to load
screen_scroll = [0, 0]  # Initialize screen scroll position

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
    
animation_list = []
animation_types = ["idle", "running_up", "running_down", "running_left", "running_right"]

for animation_type in animation_types:
    temp_animation_list = []

    for i in range(4):
        img = pygame.image.load(f"assets/images/steve/{animation_type}/{i}.png").convert_alpha()
        img = scale_image_by_height(img, PLAYER_HEIGHT)
        temp_animation_list.append(img)

    animation_list.append(temp_animation_list)

# Create player
player = Player(400, 300, animation_list)


#load map tiles
tile_list = []
for i in range(TILE_TYPES):
    img = pygame.image.load(f"assets/images/tiles/{i}.png").convert_alpha()
    img = scale_image_by_height(img, TILE_SIZE)
    tile_list.append(img)

# Create empty world data
world_data = [[-1 for _ in range(WORLD_COLS)] for _ in range(WORLD_ROWS)]

# Load world data from CSV file
with open(f"levels/level{level}.csv", newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for y, row in enumerate(reader):
        for x, tile in enumerate(row):
            world_data[y][x] = int(tile)

world = World()
world.load_map(world_data, tile_list)


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
     
    # Draw the world
    world.draw(screen)

    # Move player
    screen_scroll = player.move(dx, dy)
    

    # Update objets in the world
    player.update()
    world.update(screen_scroll)

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