import pygame
from constants import *
from player import Player
from world import *
import csv
from os import system
from weapons import *
from enemies import *
from pygame import mixer

system("cls")

pygame.init()
mixer.init()

mixer.music.load("assets/sound/music.ogg")
mixer.music.set_volume(0.5)
mixer.music.play(-1)

explosion_sound = mixer.Sound("assets/sound/bomb.mp3")
mixer.Sound.set_volume(explosion_sound, 0.5)

enemy_hit_sound = mixer.Sound("assets/sound/enemy_hurt.mp3")
mixer.Sound.set_volume(enemy_hit_sound, 0.5)

def draw_volume_slider(x, y, width, height, volume):
    # Dibuja la barra de fondo
    pygame.draw.rect(screen, (100, 100, 100), (x, y, width, height))
    # Dibuja la barra de volumen actual
    pygame.draw.rect(screen, (70, 130, 180), (x, y, int(width * volume), height))
    # Dibuja el "handle"
    handle_x = x + int(width * volume)
    pygame.draw.circle(screen, (255, 255, 255), (handle_x, y + height // 2), height // 2 + 2)

def handle_volume_slider(x, y, width, height, event):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if click[0] and x <= mouse[0] <= x + width and y <= mouse[1] <= y + height:
        # Calcula el nuevo volumen
        new_volume = (mouse[0] - x) / width
        new_volume = max(0, min(1, new_volume))
        mixer.music.set_volume(new_volume)
        return new_volume
    return None

interactables_group = pygame.sprite.Group()

score_guardado = False

player_name = ""


def pedir_nombre():
    global player_name
    font = pygame.font.Font(FONT_PATH, 40)
    input_box = pygame.Rect(250, 300, 300, 50)
    color_inactive = (150, 150, 150)
    color_active = (200, 200, 255)
    color = color_inactive
    active = False
    text = ""
    done = False

    while not done:
        screen.fill((40, 25, 25))
        mensaje = font.render("Ingresa tu nombre:", True, (255, 255, 255))
        screen.blit(mensaje, (SCREEN_WIDTH // 2 - mensaje.get_width() // 2, 200))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = True
                else:
                    active = False
                color = color_active if active else color_inactive
            elif event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        player_name = text if text.strip() != "" else "Anonimo"
                        done = True
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        if len(text) < 12:
                            text += event.unicode

        txt_surface = font.render(text, True, (255, 255, 255))
        width = max(300, txt_surface.get_width() + 10)
        input_box.w = width
        pygame.draw.rect(screen, color, input_box, 2)
        screen.blit(txt_surface, (input_box.x + 5, input_box.y + 10))

        pygame.display.flip()
        clock.tick(30)

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

bloquear_disparo = False

#botones del menu 
def ventana_jugar():
    global ESTADO
    ESTADO = "seleccion_PJ"
    
def ventana_salir():
    pygame.quit()
    exit()
    pygame.display.update()
    clock.tick(60)

def ventana_configuracion():
    global ESTADO
    ESTADO = "configuracion"

def reiniciar_juego():
    global player, personaje_activo, world, level, pociones, interactables_group, world_data, explosions_group, trown_group

    level = 0
    pociones = []
    trown_group.empty()
    explosions_group.empty()

    # Reiniciar datos del mundo
    world_data = [[-1 for _ in range(WORLD_COLS)] for _ in range(WORLD_ROWS)]
    with open(f"levels/level{level}.csv", newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for y, row in enumerate(reader):
            for x, tile in enumerate(row):
                world_data[y][x] = int(tile)

    world = World()
    interactables = world.load_map(world_data, tile_list, mage_animations, ENEMY_TYPES, spike_trap_images)
    interactables_group = pygame.sprite.Group(interactables)
    player = world.player
    personaje_activo = None

    # Reiniciar vida y mana si el jugador ya existe
    if player is not None:
        player.health = 100
        player.mana = 100
        player.key = False
        player.speed_boost = 0

def regresar():
    global ESTADO
    ESTADO = "menu"
    reiniciar_juego()

def cambiar_estado(nuevo_estado):
    global ESTADO, bloquear_disparo, score_guardado
    ESTADO = nuevo_estado
    if nuevo_estado == "menu":
        reiniciar_juego()
        score_guardado = False
    ESTADO = nuevo_estado
    if nuevo_estado == "menu":
        reiniciar_juego()
        score_guardado = False
    if nuevo_estado == "juego":
        bloquear_disparo = True
        if player is not None:
            player.health = 100
            player.mana = 100

def mostrar_info():
    screen.fill((40, 25, 25))
    font_titulo = pygame.font.Font(FONT_PATH, 50)
    font_texto = pygame.font.Font(FONT_PATH, 30)

    # Título
    titulo = font_titulo.render("Ayuda y Controles", True, (255, 255, 255))
    screen.blit(titulo, (SCREEN_WIDTH//2 - titulo.get_width()//2, 40))

    # Controles
    controles = [
        "Moverse: W, A, S, D o Flechas",
        "Pausa: ESC",
        "Lanzar bomba/disparo: Click izquierdo",
        "Usar pociones: Teclas 1-9",
    ]
    for i, texto in enumerate(controles):
        t = font_texto.render(texto, True, (200, 200, 200))
        screen.blit(t, (80, 120 + i*40))

    # Objetivo
    objetivo = font_texto.render("Objetivo: Llega a la salida y derrota a los enemigos mientras bajas de nivel.", True, (255, 220, 100))
    screen.blit(objetivo, (80, 300))

    # Imágenes alineadas con su texto
    y_iconos = 370
    espacio = 60

    # Vida
    screen.blit(full_hearth, (80, y_iconos))
    leyenda_vida = font_texto.render("Vida", True, (200, 200, 200))
    screen.blit(leyenda_vida, (80 + full_hearth.get_width() + 15, y_iconos + full_hearth.get_height()//2 - leyenda_vida.get_height()//2))

    # Mana
    screen.blit(mana[0], (300, y_iconos))
    leyenda_mana = font_texto.render("Mana", True, (200, 200, 200))
    screen.blit(leyenda_mana, (300 + mana[0].get_width() + 15, y_iconos + mana[0].get_height()//2 - leyenda_mana.get_height()//2))

    # Llave
    screen.blit(level_key, (520, y_iconos))
    leyenda_llave = font_texto.render("Llave", True, (200, 200, 200))
    screen.blit(leyenda_llave, (520 + level_key.get_width() + 15, y_iconos + level_key.get_height()//2 - leyenda_llave.get_height()//2))

    # Botón para volver al menú
    draw_button("Volver al menu", 500, 500, 200, 60, (70, 130, 180), (100, 180, 250), regresar)

    draw_button("Volver", 200, 500, 200, 60, (70, 130, 180), (100, 180, 250), lambda: cambiar_estado("pausa"))

def informacion():
    screen.fill((40, 25, 25))
    font_titulo = pygame.font.Font(FONT_PATH, 50)
    font_texto = pygame.font.Font(FONT_PATH, 30)

    # Título
    titulo = font_titulo.render("Informacion", True, (255, 255, 255))
    screen.blit(titulo, (SCREEN_WIDTH//2 - titulo.get_width()//2, 40))

    # Controles
    info = [
        "Creadores:",
        "Brandon Alvarez y Bradly Morgan",
        "Profes:",
        "Jeff Schmidt Peralta y Diego Mora Rojas"
    ]
    
    for i, texto in enumerate(info):
        t = font_texto.render(texto, True, (200, 200, 200))
        screen.blit(t, (80, 120 + i*40))

    # Objetivo
    objetivo = font_texto.render("Carrera: IC,  Asignatura: Introduccion a la programacion,  Ano: 2025 ", True, (255, 230, 100))
    screen.blit(objetivo, (80, 450))

    # Cargar y mostrar las fotos debajo de los profesores
    foto1 = pygame.image.load("assets/perfil/brad.png").convert_alpha()
    foto2 = pygame.image.load("assets/perfil/brandon.jpg").convert_alpha()
    foto1 = pygame.transform.scale(foto1, (120, 120))
    foto2 = pygame.transform.scale(foto2, (120, 120))
    # Calcula la posición Y justo debajo de la última línea de texto (profesores)
    y_fotos = 120 + len(info)*40 + 20  # 20 píxeles de espacio extra
    screen.blit(foto1, (80, y_fotos))
    screen.blit(foto2, (220, y_fotos))

def guardar_score():
    global player_name, score
    if not player_name:
        player_name = "Anonimo"
    with open("scores.txt", "a", encoding="utf-8") as file:
        file.write(f"{player_name},{score}\n")

def mostrar_leaderboard(offset_y=50):
    try:
        with open("scores.txt", "r", encoding="utf-8") as file:
            lineas = file.readlines()
    except FileNotFoundError:
        lineas = []

    puntajes = []
    for linea in lineas:
        try:
            nombre, puntaje = linea.strip().split(",")
            puntajes.append((nombre, int(puntaje)))
        except:
            continue

    puntajes.sort(key=lambda x: x[1], reverse=True)
    top5 = puntajes[:5]

    font_titulo = pygame.font.Font(FONT_PATH, 50)
    font = pygame.font.Font(FONT_PATH, 30)
    titulo = font_titulo.render("Leaderboard", True, (255, 255, 255))
    screen.blit(titulo, (SCREEN_WIDTH // 2 - titulo.get_width() // 2, offset_y))

    for i, (nombre, puntos) in enumerate(top5):
        texto = font.render(f"{i+1}. {nombre} - {puntos}", True, (255, 255, 255))
        screen.blit(texto, (SCREEN_WIDTH // 2 - texto.get_width() // 2, offset_y + 60 + i * 35))



escape_pressed = False # Boton de pausa

# Variables del juego
level = 1  # Establecer el nivel a cargar
screen_scroll = [0, 0]  # Inicializar la posición de desplazamiento de la pantalla
interactables = None  # Inicializar la lista de objetos interactivos
score = 0
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

faded_key = pygame.image.load("assets/images/items/faded_key.png").convert_alpha()
faded_key = scale_image_by_height(faded_key, ITEM_SIZE)
level_key = pygame.image.load("assets/images/items/key.png").convert_alpha()
level_key = scale_image_by_height(level_key, ITEM_SIZE)

# Animaciones de las clases
def seleccionar_mago():
    pedir_nombre()
    global ESTADO, player, world, personaje_activo, interactables_group
    interactables = world.load_map(world_data, tile_list, mage_animations, ENEMY_TYPES, spike_trap_images)
    interactables_group = pygame.sprite.Group(interactables)
    player = world.player
    personaje_activo = RedMage(red_mage_weapons, world.tile_categories, explosion_images)
    ESTADO = "juego"

def seleccionar_arquero():
    pedir_nombre()
    global ESTADO, player, world, personaje_activo
    world.load_map(world_data, tile_list, archer_animations, ENEMY_TYPES)
    player = world.player
    personaje_activo = Archer(archer_weapons, world.obstacles)
    ESTADO = "juego"

def seleccionar_guerrero():
    pedir_nombre()
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

    for i in range(HEARTHS_PJ + player.extra_hearts):
        if (i + 1) * 20 <= player.health:
            screen.blit(full_hearth, (10 + i * (ITEM_SIZE + 5), 10))
        elif (i + 1) * 20 <= player.health + 10:
            screen.blit(half_hearth, (10 + i * (ITEM_SIZE + 5), 10))
        else:
            screen.blit(empty_hearth, (10 + i * (ITEM_SIZE + 5), 10))

    for i in range(11):
        if (i * 10) <= player.mana < ((i * 10) + 10):
            screen.blit(mana[10-i], (SCREEN_WIDTH - (ITEM_SIZE * 4), -15))
            continue

    score_label = pygame.font.Font(FONT_PATH, 40).render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_label, (SCREEN_WIDTH - score_label.get_width() - 275, 10))
    
    if not player.key:
        screen.blit(faded_key, (SCREEN_WIDTH - ITEM_SIZE - 10, 10))
    else:
        screen.blit(level_key, (SCREEN_WIDTH - ITEM_SIZE - 10, 10))

    if pociones is not None:
        for i, pocion in enumerate(pociones):
            screen.blit(tile_list[pocion], (SCREEN_WIDTH - ITEM_SIZE - 10, 10 + (i + 1) * (ITEM_SIZE + 5)))

       
def tile_here(center):
    pos_rect = Rect(center[0], center[1], 1, 1)
    for tile in world.map_tiles:
        if tile[1].colliderect(pos_rect):
            return tile
    return None

def explosion(epi):
        global score

        explosion_sound.play()
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

        for explosion in explosiones:
            if explosion[4]:
                score += 10
                
        for tile in explosiones:
            world.explotar(tile, tile_list)

        explosiones = [tile for tile in explosiones if tile not in world.walls]

        for explosion in explosiones:
            if explosion[1].colliderect(player.collide_rect):
                player.health -= 50
                player_hurt_sound.play()

                break
        
        

        explosiones = [Explosion(explosion_images, tile[1].center) for tile in explosiones]

        # Daño a enemigos por explosión
        for explosion_obj in explosiones:
            for enemy in world.enemies:
                if explosion_obj.rect.colliderect(enemy.collide_rect):
                    enemy_hit_sound.play()
                    score += 50
                    enemy.take_damage(200 + player.strenght) 
        return explosiones

def next_level():
    global level, world, ESTADO, player, personaje_activo, interactables_group, pociones
    pociones = []
    level += 1
    
    if level > 4:
        global ESTADO
        ESTADO = "gane"
        """pygame.quit()
        exit()"""
    else:

        world_data = [[-1 for _ in range(WORLD_COLS)] for _ in range(WORLD_ROWS)]

        # Cargar datos del mundo desde un archivo CSV
        with open(f"levels/level{level}.csv", newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for y, row in enumerate(reader):
                for x, tile in enumerate(row):
                    world_data[y][x] = int(tile)

        world = World()
        interactables = world.load_map(world_data, tile_list, mage_animations, ENEMY_TYPES, spike_trap_images)
        interactables_group = pygame.sprite.Group(interactables)
        player = world.player
        personaje_activo = RedMage(red_mage_weapons, world.tile_categories, explosion_images)
        ESTADO = "juego"

def manage_inventory(index):
    global pociones

    try:
        pocion = pociones[index]
        pociones.pop(index)
    except:
        return
    
    if pocion == 14:
        player.mana += 20
        if player.mana > 100:
            player.mana = 100
        
    elif pocion == 15:
        player.health += 20
        if player.health > 100:
            player.health = 100

    elif pocion == 19:
        personaje_activo.explosion_range += 1
    
    elif pocion == 20:
        player.speed_boost += 3
        player.last_speed_boost = pygame.time.get_ticks()

    elif pocion == 25:
        player.health += 40
        player.extra_hearts += 1

        if player.health > (100 + (player.extra_hearts * 20)):
            player.health = 100 + (player.extra_hearts * 20)

    elif pocion == 26:
        player.strenght += 50


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
    img = scale_image_by_height(img, SLIME_HEIGHT)
    slime_idle_images.append(img)

snail_idle_images = []
for i in range(4):  # Snail
    img = pygame.image.load(f"assets/images/enemies/snail/idle_mov/{i}.png").convert_alpha()
    img = scale_image_by_height(img, SNAIL_HEIGHT)
    snail_idle_images.append(img)

goblin_idle_images = []
for i in range(4):  # Goblin
    img = pygame.image.load(f"assets/images/enemies/goblin/idle_mov/{i}.png").convert_alpha()
    img = scale_image_by_height(img, GOBLIN_HEIGHT)
    goblin_idle_images.append(img)

demon_idle_images = []
for i in range(6):  # Demon
    img = pygame.image.load(f"assets/images/enemies/demon/idle_mov/{i}.png").convert_alpha()
    img = scale_image_by_height(img, DEMON_HEIGHT)
    demon_idle_images.append(img)

skeleton_idle_images = []
for i in range(5):  # Skeleton
    img = pygame.image.load(f"assets/images/enemies/skeleton/idle_mov/{i}.png").convert_alpha()
    img = scale_image_by_height(img, SKELETON_HEIGHT)
    skeleton_idle_images.append(img)

boss_idle_images = []
for i in range(4):  # Boss
    img = pygame.image.load(f"assets/images/enemies/boss/idle_mov/{i}.png").convert_alpha()
    img = scale_image_by_height(img, BOSS_HEIGHT)
    boss_idle_images.append(img)


ENEMY_TYPES = {
    11: (Slime, slime_idle_images), 
    
    21: (Snail, snail_idle_images),

    22: (Demon, demon_idle_images),

    23: (Goblin, goblin_idle_images),

    24: (Skeleton, skeleton_idle_images),

    27: (Boss, boss_idle_images)
}

world.enemies = [enemy for enemy in world.enemies if enemy.health > 0]

# Bucle principal del juego 
run = True
explosions = None
pociones = []
NUMBER_KEYS = (pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9)
while run:

    # Controlar la tasa de fotogramas
    clock.tick(FPS)

    # Manejo de eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if ESTADO == "juego":
            if event.type == pygame.KEYDOWN:
                    if event.key in [pygame.K_a, pygame.K_LEFT]:
                        moving_left = True
                    if event.key in [pygame.K_d, pygame.K_RIGHT]:
                        moving_right = True
                    if event.key in [pygame.K_w, pygame.K_UP]:
                        moving_up = True
                    if event.key in [pygame.K_s, pygame.K_DOWN]:
                        moving_down = True
                    if event.key in NUMBER_KEYS:
                        index = NUMBER_KEYS.index(event.key)
                        manage_inventory(index)
                    if event.key == pygame.K_ESCAPE and not escape_pressed:
                        ESTADO = "pausa"
                        escape_pressed = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    escape_pressed = False
                if event.key in [pygame.K_a, pygame.K_LEFT]:
                    moving_left = False
                if event.key in [pygame.K_d, pygame.K_RIGHT]:
                    moving_right = False
                if event.key in [pygame.K_w, pygame.K_UP]:
                    moving_up = False
                if event.key in [pygame.K_s, pygame.K_DOWN]:
                    moving_down = False

            elif ESTADO == "pausa":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE and not escape_pressed:
                        ESTADO = "juego"
                        escape_pressed = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_ESCAPE:
                escape_pressed = False
                
    
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
            dx = PLAYER_SPEED + player.speed_boost
        if moving_left: 
            dx = -PLAYER_SPEED - player.speed_boost
        if moving_up:
            dy = -PLAYER_SPEED - player.speed_boost
        if moving_down:
            dy = PLAYER_SPEED + player.speed_boost
         
        # Mover jugador
        screen_scroll = player.move(dx, dy, world.get_obstacle_rects())

        # Dibujar el mundo
        world.draw(screen)
        for trap in world.traps:
            trap.draw(screen)
        
        # Actualizar objetos en el mundo
        player.update()
        world.update(screen_scroll, tile_list, player)
        for trap in world.traps:
            trap.update(screen_scroll, player)
        
        world.enemies = [enemy for enemy in world.enemies if enemy.health > 0]

        if bloquear_disparo:
            if not pygame.mouse.get_pressed()[0]:
                bloquear_disparo = False
        else:
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

                if not isinstance(object, FireBomb):
                    for enemy in world.enemies:
                        if object.rect.colliderect(enemy.collide_rect):
                            enemy_hit_sound.play()
                            score += 50
                            enemy.take_damage(object.damage + player.strenght)
                            object.kill()

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
        for i, enemy in enumerate(world.enemies):
            enemy.update(world.get_obstacle_rects(), screen_scroll, player, RANGO_VISION)
            # Evita superposición con otros enemigos
            for j, other in enumerate(world.enemies):
                if i != j and enemy.rect.colliderect(other.rect):
                    # Retrocede el movimiento o ajusta la posición
                    if hasattr(enemy, "last_dx") and hasattr(enemy, "last_dy"):
                        enemy.collide_rect.x -= int(enemy.last_dx)
                        enemy.collide_rect.y -= int(enemy.last_dy)
                        enemy.rect.center = enemy.collide_rect.center
            enemy.draw(screen, screen_scroll)
        
            if enemy.collide_rect.colliderect(player.collide_rect):
                if pygame.time.get_ticks() - player.last_hit > 2000:
                    player.health -= enemy.damage
                    player_hurt_sound.play()
                    player.last_hit = pygame.time.get_ticks()
                    break

            if player.health <= 0:
                ESTADO = "game_over"


        for interactable in interactables_group:
            pocim = interactable.update(screen_scroll, player, personaje_activo)
            interactable.draw(screen)

            if pocim != None:
                pociones.append(pocim)

        #print(pociones)

        exit_rect = Rect(0, 0, 5, 5)
        exit_rect.center = world.exit_tile[1].center
    

        if exit_rect.colliderect(player.collide_rect) and world.exit_open:
            next_level()

        # Dibuja la pantalla según el estado
    elif ESTADO == "menu":
        font = pygame.font.Font(FONT_PATH, 60)
        bg_img = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        bg_img.fill((40, 25, 25))

        screen.blit(bg_img, (0, 0))
        title = font.render("Dungeonfall", True, (255, 255, 255))
        screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 100))

        # Botón Jugar
        draw_button("Jugar", 300, 200, 200, 60, (70, 130, 180), (100, 180, 250), ventana_jugar)

        draw_button("configuracion", 300, 300, 200, 60, (70, 130, 180), (100, 180, 250), ventana_configuracion)

        draw_button("Informacion", 300, 400, 200, 60, (70, 130, 180), (100, 180, 250), lambda: cambiar_estado("info"))

        draw_button("Salir", 300, 500, 200, 60, (70, 130, 180), (100, 180, 250), ventana_salir)

        # Dibuja el menú y botones
    elif ESTADO == "seleccion_PJ":
    
        # Dibuja la selección de personaje
        screen.fill((40, 25, 25))
        font = pygame.font.Font(FONT_PATH, 50)
        texto = font.render("Selecciona tu personaje", True, (255, 255, 255))
        screen.blit(texto, (SCREEN_WIDTH//2 - texto.get_width()//2, 50))
        
        screen.blit(img_mago, (100 + 75 - img_mago.get_width() // 2, 350 - img_mago.get_height() - 40))

        screen.blit(img_arquero, (300 + 75 - img_arquero.get_width() // 2, 350 - img_arquero.get_height() - 40))
        
        screen.blit(img_guerrero, (500 + 75 - img_guerrero.get_width() // 2, 350 - img_guerrero.get_height() - 40))

        draw_button("Mago", 100, 350, 150, 45, (70, 130, 180), (100, 180, 250), seleccionar_mago)

        draw_button("Arquero", 300, 350, 150, 45, (70, 130, 180), (100, 180, 250), seleccionar_arquero)

        draw_button("Guerrero", 500, 350, 150, 45, (70, 130, 180), (100, 180, 250), seleccionar_guerrero)
    
    elif ESTADO == "configuracion":
        screen.fill((40, 25, 25))
        font = pygame.font.Font(FONT_PATH, 40)
        texto = font.render("Volumen de la musica", True, (255, 255, 255))
        screen.blit(texto, (SCREEN_WIDTH//2 - texto.get_width()//2, 100))
        draw_volume_slider(200, 200, 400, 20, mixer.music.get_volume())
        for event in pygame.event.get():
            new_vol = handle_volume_slider(200, 200, 400, 20, event)
            if new_vol is not None:
                pass

        draw_button("regresar al menu", 300, 350, 200, 60, (70, 130, 180), (100, 180, 250), regresar)

    elif ESTADO == "pausa":
        screen.fill((40, 25, 25))
        font = pygame.font.Font(FONT_PATH, 60)
        texto = font.render("PAUSA", True, (255, 255, 255))
        screen.blit(texto, (SCREEN_WIDTH//2 - texto.get_width()//2, 150))

        draw_button("Reanudar", 300, 300, 200, 60, (70, 130, 180), (100, 180, 250), lambda: cambiar_estado("juego"))

        draw_button("Menu principal", 300, 400, 200, 60, (70, 130, 180), (100, 180, 250), lambda: cambiar_estado("menu"))

        draw_button("ayuda y controles", 300, 500, 200, 60, (70, 130, 180), (100, 180, 250), lambda: cambiar_estado("ayuda"))

    elif ESTADO == "ayuda":
        mostrar_info()

    elif ESTADO == "info":
        informacion()

    elif ESTADO == "game_over":

        if not score_guardado:
            guardar_score()
            score_guardado = True
        screen.fill((40, 25, 25))

        # Título GAME OVER
        font_gigante = pygame.font.Font(FONT_PATH, 80)
        texto = font_gigante.render("GAME OVER", True, (255, 50, 50))
        screen.blit(texto, (SCREEN_WIDTH // 2 - texto.get_width() // 2, 40))

        # Leaderboard
        mostrar_leaderboard(offset_y=150)

        # Texto inferior
        font_medio = pygame.font.Font(FONT_PATH, 30)
        texto2 = font_medio.render("Pulsa para volver al menu", True, (255, 255, 255))
        screen.blit(texto2, (SCREEN_WIDTH // 2 - texto2.get_width() // 2, 400))

        # Botón para volver
        draw_button("Menu principal", 300, 450, 200, 60, (70, 130, 180), (100, 180, 250), lambda: cambiar_estado("menu"))

    elif ESTADO == "gane":

        if not score_guardado:
            guardar_score()
            score_guardado = True

        screen.fill((40, 25, 25))

        # Título de victoria
        font_gigante = pygame.font.Font(FONT_PATH, 60)
        texto = font_gigante.render("¡FELICIDADES, GANASTE EL JUEGO!", True, (255, 255, 255))
        screen.blit(texto, (SCREEN_WIDTH // 2 - texto.get_width() // 2, 40))

        # Leaderboard
        mostrar_leaderboard(offset_y=150)

        # Texto de instrucciones
        font_medio = pygame.font.Font(FONT_PATH, 30)
        texto2 = font_medio.render("Pulsa para volver al menu", True, (255, 255, 255))
        screen.blit(texto2, (SCREEN_WIDTH // 2 - texto2.get_width() // 2, 400))

        # Botón para regresar
        draw_button("Menu principal", 300, 450, 200, 60,
                    (70, 130, 180), (100, 180, 250), lambda: cambiar_estado("menu"))

    # Actualizar pantalla
    pygame.display.update()

    if not pygame.mouse.get_pressed()[0]:
        draw_button.clicked = False

pygame.quit()