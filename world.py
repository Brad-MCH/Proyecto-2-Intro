from player import Player
from constants import *
from enemies import *
from pygame import *


class World:
    def __init__(self):
        self.map_tiles = []
        self.obstacles = []
        self.destroyable_blocks = []
        self.walls = []
        self.enemies = []
        self.tile_categories = {
            "obstacles": self.obstacles,
            "destroyable_blocks": self.destroyable_blocks,
            "walls": self.walls,
            "map_tiles": self.map_tiles
        }
        self.player = None
        self.traps = []

    def load_map(self, map_data, tile_list, animation_list, enemy_types, spike_trap_animations):

        for y, row in enumerate(map_data):
            for x, tile in enumerate(row):
                img = tile_list[tile]
                img_rect = img.get_rect()   
                img_rect.x = x * TILE_SIZE
                img_rect.y = y * TILE_SIZE
                img_rect.center = (img_rect.x, img_rect.y)
                tile_data = [img, img_rect, img_rect.x, img_rect.y, False, "Random"]  # Lista que contiene la imagen, el rectángulo y las coordenadas del tile

                # Dividir los tiles en diferentes listas según su tipo

                if tile in (7, 9): # Paredes
                    if tile == 7:
                        self.walls.append(tile_data)
                    self.obstacles.append(tile_data)

                if tile == 9:
                    self.destroyable_blocks.append(tile_data) # Bloques destructibles
                    tile_data[4] = True
                    
                        

                if tile == 10:
                    player = Player(img_rect.x, img_rect.y, animation_list)
                    self.player = player # Guardar el jugador
        
                    
                    tile_data[0] = tile_list[0] # Cambiar el tile del jugador a un tile vacío

                if tile == 12: # Trampa de pinchos
                    trap = Spike_trap(tile_data, spike_trap_animations)
                    self.traps.append(trap)

                if tile in enemy_types:
                    enemy_class, enemy_animations = enemy_types[tile]
                    enemy = enemy_class(x * TILE_SIZE, y * TILE_SIZE, enemy_animations)
                    self.enemies.append(enemy)
                    tile_data[0] = tile_list[0]

                if tile >= 0:
                    self.map_tiles.append(tile_data) # Esta lista contiene todos los tiles del mapa

    def explotar(self, explosion_tile, tile_list):
        for tile in self.map_tiles:
            if tile == explosion_tile:
                if tile in self.destroyable_blocks:
                    self.obstacles.remove(tile)
                    self.destroyable_blocks.remove(tile)
                    tile[0] = tile_list[0]
                    

    def update(self, screen_scroll, tile_list):
        for tile in self.map_tiles:
            tile[2] += screen_scroll[0]
            tile[3] += screen_scroll[1]
            tile[1].center = (tile[2], tile[3])

    def draw(self, screen):
        for tile in self.map_tiles:
            screen.blit(tile[0], tile[1])
    
    def get_obstacle_rects(self): # Para los enemigos
        return [tile[1] for tile in self.obstacles]
    
class Spike_trap:
    def __init__(self, tile, animation_list):
        self.rect = animation_list[0].get_rect()
        self.rect.centerx = tile[1].x
        self.rect.centery = tile[1].y
        self.animation_list = animation_list
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.animation_cooldown = 75
        self.last_spike = pygame.time.get_ticks()
        self.pierce_cooldown = 2000
        self.pierce = False
        self.last_hit = 0

    def update(self, screen_scroll, player):
        self.rect.x += screen_scroll[0]
        self.rect.y += screen_scroll[1]



        now = pygame.time.get_ticks()

        if now - self.last_spike > self.pierce_cooldown:
            self.pierce = True
            self.last_spike = now

        if now - self.last_update > self.animation_cooldown and self.pierce:
            self.frame = (self.frame + 1) if self.frame < 3 else 0
            self.last_update = now
            self.pierce = False if self.frame == 0 else True

        
        if self.pierce:
            if self.rect.colliderect(player.collide_rect) and now - self.last_hit > 1000:  
                player.health -= 20
                self.last_hit = now
                


    def draw(self, surface):
        surface.blit(self.animation_list[self.frame], (self.rect.x, self.rect.y))
            