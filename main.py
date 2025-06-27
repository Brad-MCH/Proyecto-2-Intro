import pygame
from constants import *
from player import Player
from world import *
import csv
from os import system
from weapons import *
from enemies import *

system("cls")

pygame.init()

interactables_group = pygame.sprite.Group()
# el jugador no se ha creado
player = None
seleccionando_personaje = False

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
        if click[0] == 1 and action is not None and not draw_button.clicked:
            action()
            draw_button.clicked = True
    else:
        pygame.draw.rect(screen, color, button_rect)
    font_btn = pygame.font.Font(FONT_PATH, 40)
    text_surf = font_btn.render(text, True, (255, 255, 255))
    text_rect = text_surf.get_rect(center=button_rect.center)
    screen.blit(text_surf, text_rect)

draw_button.clicked = False

def ventana_jugar():
    global ESTADO
    ESTADO = "seleccion_PJ"
    
def ventana_salir():
    pygame.quit()
    exit()
    pygame.display.update()
    clock.tick(60)

# Variables del juego
level = 0  # Establecer el nivel a cargar
screen_scroll = [0, 0]  # Inicializar la posición de desplazamiento de la pantalla
interactables = None  # Inicializar la lista de objetos interactivos

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

mage_animations = []      
archer_animations = []    
warrior_animations = []

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
    # Mago
    temp_animation_list = []
    num_frames = 8 if animation_type == "idle" else 4
    for i in range(num_frames):
        img = pygame.image.load(f"assets/images/Mage-Red/{animation_type}/{i}.png").convert_alpha()
        img = scale_image_by_height(img, PLAYER_HEIGHT)
        temp_animation_list.append(img)
    mage_animations.append(temp_animation_list)
     # Arquero
    temp_animation_list = []
    for i in range(num_frames):
        img = pygame.image.load(f"assets/images/Archer/{animation_type}/{i}.png").convert_alpha()
        img = scale_image_by_height(img, PLAYER_HEIGHT)
        temp_animation_list.append(img)
    archer_animations.append(temp_animation_list)
    # Guerrero
    temp_animation_list = []
    for i in range(num_frames):
        img = pygame.image.load(f"assets/images/Warrior/{animation_type}/{i}.png").convert_alpha()
        img = scale_image_by_height(img, PLAYER_HEIGHT)
        temp_animation_list.append(img)
    warrior_animations.append(temp_animation_list)

# cargar imagenes de explosion
explosion_images = []
for i in range(6):
    img = pygame.image.load(f"assets/images/explosion/{i}.png").convert_alpha()
    img = scale_image_by_height(img, TILE_SIZE)
    explosion_images.append(img)

# Imagenes de trampa de pinchos
spike_trap_images = []
for i in range(4):
    img = pygame.image.load(f"assets/images/spikes/{i}.png").convert_alpha()
    img = scale_image_by_height(img, TILE_SIZE)
    spike_trap_images.append(img)

# Animaciones de las clases
def seleccionar_mago():
    global ESTADO, player, world, personaje_activo, interactables_group
    interactables = world.load_map(world_data, tile_list, mage_animations, ENEMY_TYPES, spike_trap_images)
    interactables_group = pygame.sprite.Group(interactables)
    player = world.player
    personaje_activo = RedMage(red_mage_weapons, world.tile_categories, explosion_images)
    ESTADO = "juego"

def seleccionar_arquero():
    global ESTADO, player, world, personaje_activo
    world.load_map(world_data, tile_list, archer_animations, ENEMY_TYPES)
    player = world.player
    personaje_activo = Archer(archer_weapons, world.obstacles)
    ESTADO = "juego"

def seleccionar_guerrero():
    global ESTADO, player, world, personaje_activo
    world.load_map(world_data, tile_list, warrior_animations, ENEMY_TYPES)
    player = world.player
    personaje_activo = Warrior(warrior_weapons, world.obstacles)
    ESTADO = "juego"

def selecionar_skin(armas, clase):
    global ESTADO, player, world, personaje_activo
    interactables = world.load_map(world_data, tile_list, mage_animations, ENEMY_TYPES, spike_trap_images)
    player = world.player
    personaje_activo = clase(armas, world.tile_categories, explosion_images)
    ESTADO = "juego"

def display_info():

    for i in range(5):
        if (i + 1) * 20 <= player.health:
            screen.blit(full_hearth, (10 + i * (ITEM_SIZE + 5), 10))
        elif (i + 1) * 20 <= player.health + 10:
            screen.blit(half_hearth, (10 + i * (ITEM_SIZE + 5), 10))
        else:
            screen.blit(empty_hearth, (10 + i * (ITEM_SIZE + 5), 10))

    for i in range(11):
        if (i * 10) <= player.mana < ((i * 10) + 10):
            screen.blit(mana[10-i], (10*30, -15))
            continue
       
def tile_here(center):
    pos_rect = Rect(center[0], center[1], 1, 1)
    for tile in world.map_tiles:
        if tile[1].colliderect(pos_rect):
            return tile
    return None

def explosion(epi):
    
        epicenter = tile_here(epi)
        
        if not epicenter:
            return None
        
        explosiones = [epicenter]
        arriba_libre = True
        abajo_libre = True
        derecha_libre = True
        izquierda_libre = True
        for i in range(personaje_activo.explosion_range):

            # Explosión hacia arriba
            tile = tile_here((epicenter[2], epicenter[3] - (i + 1) * TILE_SIZE))
            if tile and arriba_libre and tile not in world.walls:
                explosiones.append(tile)
            else:
                arriba_libre = False

            # Explosión hacia abajo
            tile = tile_here((epicenter[2], epicenter[3] + (i + 1) * TILE_SIZE))

            if tile and abajo_libre and tile not in world.walls:
                explosiones.append(tile)
            else:
                abajo_libre = False
          
            # Explosión hacia la izquierda
            tile = tile_here((epicenter[2] - (i + 1) * TILE_SIZE, epicenter[3]))
            if tile and izquierda_libre and tile not in world.walls:
                explosiones.append(tile)
            else:
                izquierda_libre = False
            
            # Explosión hacia la derecha
            tile = tile_here((epicenter[2] + (i + 1) * TILE_SIZE, epicenter[3]))
            if tile and derecha_libre and tile not in world.walls:
                explosiones.append(tile)
            else:
                derecha_libre = False
            
        
        explosiones = [tile for tile in explosiones if tile is not None]
        
        for tile in explosiones:
            world.explotar(tile, tile_list)

        explosiones = [tile for tile in explosiones if tile not in world.walls]

        for explosion in explosiones:
            if explosion[1].colliderect(player.collide_rect):
                player.health -= 50
                break



        explosiones = [Explosion(explosion_images, tile[1].center) for tile in explosiones]

        


        return explosiones


                


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


# Cargar imagenes de items
full_hearth = scale_image_by_height(pygame.image.load("assets/images/items/hearth0.png").convert_alpha(), ITEM_SIZE)
empty_hearth = scale_image_by_height(pygame.image.load("assets/images/items/hearth1.png").convert_alpha(), ITEM_SIZE)
half_hearth = scale_image_by_height(pygame.image.load("assets/images/items/hearth2.png").convert_alpha(), ITEM_SIZE)

mana = []
for i in range(11):
    img = pygame.image.load(f"assets/images/items/mana/{i}.png").convert_alpha()
    img = scale_image_by_height(img, 100)
    mana.append(img)



# Cargar imágenes de armas
red_fireball = scale_image_by_height(pygame.image.load("assets/images/weapons/fireball.png").convert_alpha(), TROWABLE_SIZE)
firebomb = scale_image_by_height(pygame.image.load("assets/images/weapons/firebomb.png").convert_alpha(), 50)
firebomb = pygame.transform.rotate(firebomb, 90)
dagger = scale_image_by_height(pygame.image.load("assets/images/weapons/dagger.png").convert_alpha(), 50)
arrow = scale_image_by_height(pygame.image.load("assets/images/weapons/arrow.png").convert_alpha(), 50)

red_mage_weapons = [red_fireball, firebomb]
archer_weapons = [arrow, firebomb]
warrior_weapons = [dagger, firebomb]

img_mago = mage_animations[0][0]
img_arquero = archer_animations[0][0]
img_guerrero = warrior_animations[0][0]

trown_group = pygame.sprite.Group()
explosions_group = pygame.sprite.Group()

# Cargar animaciones de los enemigos
slime_idle_images = []
for i in range(6):  # Slime
    img = pygame.image.load(f"assets/images/enemies/slime/idle_mov/{i}.png").convert_alpha()
    img = scale_image_by_height(img, PLAYER_HEIGHT)  
    slime_idle_images.append(img)

ENEMY_TYPES = {
    11: (Slime, slime_idle_images),  # 11 es el tile del slime
}

# Bucle principal del juego 
run = True
explosions = None
while run:

    # Controlar la tasa de fotogramas
    clock.tick(FPS)

    # Manejo de eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if ESTADO == "juego":
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
        
        # Manejo de eventos para cada estado
        
    if ESTADO == "juego" and player is not None and personaje_activo is not None:
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
         
        # Mover jugador
        screen_scroll = player.move(dx, dy, world.get_obstacle_rects())

        # Dibujar el mundo
        world.draw(screen)
        for trap in world.traps:
            trap.draw(screen)
        
        # Actualizar objetos en el mundo
        player.update()
        world.update(screen_scroll, tile_list)
        for trap in world.traps:
            trap.update(screen_scroll, player)
        

        object_fired = personaje_activo.update(player)

        if object_fired:
            trown_group.add(object_fired)
        for object in trown_group:
            bomb = object.update(screen_scroll)
            if bomb:
                explosions = explosion(bomb)
                object.kill() 
            else:
                explosions = None

            object.draw(screen)
        
        
        if explosions:
            for epicentro in explosions:
                explosions_group.add(epicentro)
        for object in explosions_group:
            if not object.update(screen_scroll):
                object.draw(screen)

        # Dibujar jugador
        player.draw(screen)
      
        # Actualizar menú suprerior
        display_info()

        # Dibuja a los enemigos
        for enemy in world.enemies:
            enemy.update(world.get_obstacle_rects(), screen_scroll)
            enemy.draw(screen, screen_scroll)

        for interactable in interactables_group:
            interactable.update(screen_scroll, player)
            interactable.draw(screen)

        # Dibuja la pantalla según el estado
    elif ESTADO == "menu":
        font = pygame.font.Font(FONT_PATH, 60)
        bg_img = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        bg_img.fill((40, 25, 25))

        screen.blit(bg_img, (0, 0))
        title = font.render("Dungeonfall", True, (255, 255, 255))
        screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 100))

        # Botón Jugar
        draw_button("Jugar", 300, 250, 200, 60, (70, 130, 180), (100, 180, 250), ventana_jugar)

        # Botón Créditos
        draw_button("Salir", 300, 350, 200, 60, (70, 130, 180), (100, 180, 250), ventana_salir)

        # Dibuja el menú y botones
    elif ESTADO == "seleccion_PJ":
    
        # Dibuja la selección de personaje
        screen.fill(BLACK)
        font = pygame.font.Font(FONT_PATH, 50)
        texto = font.render("Selecciona tu personaje", True, (255, 255, 255))
        screen.blit(texto, (SCREEN_WIDTH//2 - texto.get_width()//2, 50))
        
        screen.blit(img_mago, (100 + 75 - img_mago.get_width() // 2, 350 - img_mago.get_height() - 40))

        screen.blit(img_arquero, (300 + 75 - img_arquero.get_width() // 2, 350 - img_arquero.get_height() - 40))
        
        screen.blit(img_guerrero, (500 + 75 - img_guerrero.get_width() // 2, 350 - img_guerrero.get_height() - 40))

        draw_button("Mago", 100, 350, 150, 45, (70, 130, 180), (100, 180, 250), seleccionar_mago)

        draw_button("Arquero", 300, 350, 150, 45, (70, 130, 180), (100, 180, 250), seleccionar_arquero)

        draw_button("Guerrero", 500, 350, 150, 45, (70, 130, 180), (100, 180, 250), seleccionar_guerrero)
    

    # Actualizar pantalla
    pygame.display.update()

    if not pygame.mouse.get_pressed()[0]:
        draw_button.clicked = False

pygame.quit()
