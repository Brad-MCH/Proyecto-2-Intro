from player import Player
from constants import *

class World:
    def __init__(self):
        self.map_tiles = []
        self.obstacles = []
        self.destroyable_blocks = []
        self.player = None

    def load_map(self, map_data, tile_list, animation_list):

        for y, row in enumerate(map_data):
            for x, tile in enumerate(row):
                img = tile_list[tile]
                img_rect = img.get_rect()   
                img_rect.x = x * TILE_SIZE
                img_rect.y = y * TILE_SIZE
                img_rect.center = (img_rect.x, img_rect.y)
                tile_data = [img, img_rect, img_rect.x, img_rect.y]

                # Dividir los tiles en diferentes listas según su tipo

                if tile in (7, 9): # Paredes
                    self.obstacles.append(tile_data)

                if tile == 9:
                    self.destroyable_blocks.append(tile_data) # Bloques destructibles

                if tile == 10:
                    player = Player(img_rect.x, img_rect.y, animation_list)
                    self.player = player # Guardar el jugador
                    
                    tile_data[0] = tile_list[0] # Cambiar el tile del jugador a un tile vacío

                if tile >= 0:
                    self.map_tiles.append(tile_data) # Esta lista contiene todos los tiles del mapa

    def update(self, screen_scroll):
        for tile in self.map_tiles:
            tile[2] += screen_scroll[0]
            tile[3] += screen_scroll[1]
            tile[1].center = (tile[2], tile[3])

    def draw(self, screen):
        for tile in self.map_tiles:
            screen.blit(tile[0], tile[1])
    
    def get_obstacle_rects(self): # Para los enemigos
        return [tile[1] for tile in self.obstacles]
            