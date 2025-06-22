import pygame
from constants import *
from player import Player
from world import *
import csv
from os import system
from weapons import *

system("cls")

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Dungeonfall")

# Crear reloj para controlar la tasa de fotogramas
clock = pygame.time.Clock()

def draw_button(text, x, y, width, height, color, hover_color, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    button_rect = pygame.Rect(x, y, width, height)
    if button_rect.collidepoint(mouse):
        pygame.draw.rect(screen, hover_color, button_rect)
        if click[0] == 1 and action is not None:
            action()
    else:
        pygame.draw.rect(screen, color, button_rect)
    font_btn = pygame.font.Font(FONT_PATH, 40)
    text_surf = font_btn.render(text, True, (255, 255, 255))
    text_rect = text_surf.get_rect(center=button_rect.center)
    screen.blit(text_surf, text_rect)

def ventana_jugar():
    global ESTADO
    ESTADO = "seleccion_PJ"
    
    

def ventana_salir():
    pygame.quit()
    exit()
    pygame.display.update()
    clock.tick(60)

def main_menu():
    global menu
    menu = True
    font = pygame.font.Font(FONT_PATH, 60)
    bg_img = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    bg_img.fill((40, 25, 25))
    while menu:
        screen.blit(bg_img, (0, 0))
        title = font.render("Dungeonfall", True, (255, 255, 255))
        screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 100))
        # Botón Jugar
        draw_button("Jugar", 300, 250, 200, 60, (70, 130, 180), (100, 180, 250), ventana_jugar)
        # Botón Créditos
        draw_button("Salir", 300, 350, 200, 60, (70, 130, 180), (100, 180, 250), ventana_salir)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        pygame.display.update()
        clock.tick(60)
        while menu:
            if ESTADO == "menu":
                main_menu()
            if ESTADO == "seleccion_PJ":
                screen.fill(BLACK)
                font = pygame.font.Font(FONT_PATH, 50)
            texto = font.render("Selecciona tu personaje", True, (255, 255, 255))
            screen.blit(texto, (SCREEN_WIDTH//2 - texto.get_width()//2, 200))
            pygame.display.update()
            # Aquí puedes agregar botones para elegir personaje, etc.
            if ESTADO == "juego":
                pass

main_menu()

# Variables del juego
level = 1  # Establecer el nivel a cargar
screen_scroll = [0, 0]  # Inicializar la posición de desplazamiento de la pantalla

# Definir variables de movimiento del jugador
moving_left = False
moving_right = False
moving_up = False
moving_down = False


# Función auxiliar para escalar imágenes
def scale_image_by_height(image, height):
    aspect_ratio = image.get_width() / image.get_height()
    new_width = int(height * aspect_ratio)
    return pygame.transform.scale(image, (new_width, height))

def load_animation_images(info_list):
    animation_list = []
    folder_name, number_frames = info_list
    for i in range(number_frames):
        img = pygame.image.load(f"assets/images/{folder_name}/{i}.png").convert_alpha()
        img = scale_image_by_height(img, PLAYER_HEIGHT)
        animation_list.append(img)

animation_list = []
animation_types = [
    "idle",
    "running_up",
    "running_down",
    "running_left",
    "running_right",
    "running_up_left",
    "running_up_right",
    "running_down_left",
    "running_down_right"]

for animation_type in animation_types:
    temp_animation_list = []
    num_frames = 8 if animation_type == "idle" else 4
    for i in range(num_frames):
        img = pygame.image.load(f"assets/images/Mage-Red/{animation_type}/{i}.png").convert_alpha()
        img = scale_image_by_height(img, PLAYER_HEIGHT)
        temp_animation_list.append(img)
    animation_list.append(temp_animation_list)

# Cargar tiles del mapa
tile_list = []
for i in range(TILE_TYPES):
    img = pygame.image.load(f"assets/images/tiles/{i}.png").convert_alpha()
    img = scale_image_by_height(img, TILE_SIZE)
    tile_list.append(img)

# Crear datos de mundo vacíos
world_data = [[-1 for _ in range(WORLD_COLS)] for _ in range(WORLD_ROWS)]

# Cargar datos del mundo desde un archivo CSV
with open(f"levels/level{level}.csv", newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for y, row in enumerate(reader):
        for x, tile in enumerate(row):
            world_data[y][x] = int(tile)

world = World()
world.load_map(world_data, tile_list, animation_list)

player = world.player

# Cargar imágenes de armas
RedFireball = scale_image_by_height(pygame.image.load("assets/images/weapons/fireball.png").convert_alpha(), TROWABLE_SIZE)
firebomb = scale_image_by_height(pygame.image.load("assets/images/weapons/firebomb.png").convert_alpha(), 50)
firebomb = pygame.transform.rotate(firebomb, 90)
red_mage_weapons = [RedFireball, firebomb]

mage = RedMage(red_mage_weapons, world.obstacles)

trown_group = pygame.sprite.Group()

# Bucle principal del juego
run = True
while run:

    # Controlar la tasa de fotogramas
    clock.tick(FPS)

    screen.fill(BG)

    # Calcular movimiento del jugador
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
     
    # Dibujar el mundo
    world.draw(screen)

    # Mover jugador
    screen_scroll = player.move(dx, dy, world.obstacles)
    
    # Actualizar objetos en el mundo
    player.update()
    world.update(screen_scroll)

    object_fired = mage.update(player)
    if object_fired:
        trown_group.add(object_fired)
        print(object_fired.angle)
    for object in trown_group:
        object.update(screen_scroll)
        object.draw(screen)

    # Dibujar jugador
    player.draw(screen)

    # Manejo de eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        # Manejar teclas presionadas
        if event.type == pygame.KEYDOWN:
            if event.key in [pygame.K_a, pygame.K_LEFT]:
                moving_left = True
            if event.key and event.key in [pygame.K_d, pygame.K_RIGHT]:
                moving_right = True
            if event.key in [pygame.K_w, pygame.K_UP]:
                moving_up = True
            if event.key in [pygame.K_s, pygame.K_DOWN]:
                moving_down = True

        # Manejar teclas soltadas
        if event.type == pygame.KEYUP:
            if event.key in [pygame.K_a, pygame.K_LEFT]:
                moving_left = False
            if event.key in [pygame.K_d, pygame.K_RIGHT]:
                moving_right = False
            if event.key in [pygame.K_w, pygame.K_UP]:
                moving_up = False
            if event.key in [pygame.K_s, pygame.K_DOWN]:
                moving_down = False
    

    # Actualizar pantalla
    pygame.display.update()

pygame.quit()
