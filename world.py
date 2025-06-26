from player import Player
from constants import *

class World:
    def __init__(self):
        self.map_tiles = []
        self.obstacles = []
        self.destroyable_blocks = []
        self.walls = []
        self.tile_categories = {
            "obstacles": self.obstacles,
            "destroyable_blocks": self.destroyable_blocks,
            "walls": self.walls,
            "map_tiles": self.map_tiles
        }
        self.player = None

    def load_map(self, map_data, tile_list, animation_list):

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

                if tile >= 0:
                    self.map_tiles.append(tile_data) # Esta lista contiene todos los tiles del mapa

    def explotar(self, explosion_tile, tile_list):
        for tile in self.map_tiles:
            if tile == explosion_tile:
                if tile in self.obstacles:
                    self.obstacles.remove(tile)
                tile[0] = tile_list[0]

    def update(self, screen_scroll, tile_list):
        for tile in self.map_tiles:

            if tile[4]: # Hubo una explosión en el tile
                tile[4] = False
                print(tile[5])
                    

            tile[2] += screen_scroll[0]
            tile[3] += screen_scroll[1]
            tile[1].center = (tile[2], tile[3])

    def draw(self, screen):
        for tile in self.map_tiles:
            screen.blit(tile[0], tile[1])
    
    def get_obstacle_rects(self): # Para los enemigos
        return [tile[1] for tile in self.obstacles]
            